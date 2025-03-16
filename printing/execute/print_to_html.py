import base64
import io
from typing import Optional
from typing_extensions import Annotated

from dominate.tags import br, div, hr, img, span
from PIL import Image
from pydantic import AfterValidator, BaseModel, Field


class ConnectionClosedError(Exception):
    pass


def is_one_of_validator_factory(*options):
    def validator(value):
        if value not in options:
            raise ValueError(f"{value} is not one of [{', '.join(options)}]")
        return value

    return validator


def is_num_in_range_validator_factory(min_value, max_value):
    def validator(value):
        if not min_value <= value <= max_value:
            raise ValueError(
                f"{value} is not between {min_value} and {max_value} inclusive"
            )
        return value

    return validator


is_valid_align = is_one_of_validator_factory("center", "left", "right")
is_valid_font = is_one_of_validator_factory("a", "b")
is_valid_underline = is_num_in_range_validator_factory(0, 2)
is_valid_width = is_num_in_range_validator_factory(1, 8)
is_valid_height = is_num_in_range_validator_factory(1, 8)
is_valid_density = is_num_in_range_validator_factory(0, 8)
is_valid_image_impl = is_one_of_validator_factory(
    "bitImageRaster", "graphics", "bitImageColumn"
)


class SetTextProperties(BaseModel):
    align: Optional[Annotated[str, AfterValidator(is_valid_align)]] = Field(
        default=None
    )
    font: Optional[Annotated[str, AfterValidator(is_valid_font)]] = Field(default=None)
    bold: Optional[bool] = Field(default=None)
    underline: Optional[Annotated[int, is_valid_underline]] = Field(default=None)
    normal_textsize: Optional[bool] = Field(default=None)
    double_height: Optional[bool] = Field(default=None)
    double_width: Optional[bool] = Field(default=None)
    custom_size: Optional[bool] = Field(default=None)
    width: Optional[Annotated[int, AfterValidator(is_valid_width)]] = Field(
        default=None
    )
    height: Optional[Annotated[int, AfterValidator(is_valid_height)]] = Field(
        default=None
    )
    density: Optional[Annotated[int, AfterValidator(is_valid_density)]] = Field(
        default=None
    )
    invert: Optional[bool] = Field(default=None)
    smooth: Optional[bool] = Field(default=None)
    flip: Optional[bool] = Field(default=None)


class SetWithDefaultTextProperties(BaseModel):
    align: Optional[Annotated[str, AfterValidator(is_valid_align)]] = Field(
        default="left"
    )
    font: Optional[Annotated[str, AfterValidator(is_valid_font)]] = Field(default="a")
    bold: Optional[bool] = Field(default=False)
    underline: Optional[Annotated[int, is_valid_underline]] = Field(default=0)
    double_height: Optional[bool] = Field(default=False)
    double_width: Optional[bool] = Field(default=False)
    custom_size: Optional[bool] = Field(default=False)
    width: Optional[Annotated[int, AfterValidator(is_valid_width)]] = Field(default=1)
    height: Optional[Annotated[int, AfterValidator(is_valid_height)]] = Field(default=1)
    density: Optional[Annotated[int, AfterValidator(is_valid_density)]] = Field(
        default=8
    )
    invert: Optional[bool] = Field(default=False)
    smooth: Optional[bool] = Field(default=False)
    flip: Optional[bool] = Field(default=False)


class ImageProperties(BaseModel):
    high_density_vertical: Optional[bool] = Field(default=True)
    high_density_horizontal: Optional[bool] = Field(default=True)
    impl: Annotated[str, AfterValidator(is_valid_image_impl)]
    fragment_height: Optional[int] = Field(default=960)
    center: Optional[bool] = Field(default=False)


def style_to_css(styles, *, scale):
    css = "margin-bottom: 0.2rem;"
    parsed_styles = SetWithDefaultTextProperties(**styles)
    text_width = 2 if parsed_styles.double_width else parsed_styles.width
    text_height = 2 if parsed_styles.double_height else parsed_styles.width
    font_size = min(text_width, text_height) * scale
    small_font_size = font_size / (56.0 / 42.0)
    if parsed_styles.font == "a":
        css += f"font-size: {font_size}rem;"
    if parsed_styles.font == "b":
        css += f"font-size: {small_font_size}rem;"
    if text_width > text_height:
        extra_spacing = (text_width - text_height) * scale
        css += f"letter-spacing: {extra_spacing}rem;"
    if text_height > text_width:
        extra_height = (text_height - text_width) * scale / 2
        css += f"padding: {extra_height}rem 0;"
    if parsed_styles.bold:
        css += "font-weight: bold;"
    if parsed_styles.invert:
        spacing = 0.5 * scale
        css += f"color: white; background-color: black; padding: {spacing}rem 0; display: inline-block;"
    # if parsed_styles.align == "center":
    #     css += "align-self:center;"
    # if parsed_styles.align == "right":
    #     css += "align-self:end;"

    return css


class Alignment:
    align = None
    elements = None

    def __init__(self, *elements, align="left"):
        self.align = align
        self.elements = list(elements)

    def add(self, element):
        self.elements.append(element)

    def render(self, scale):
        justify = {"left": "start", "center": "center", "right": "end"}
        container = span(
            style=f"display: flex; flex-wrap: wrap; justify-content: {justify[self.align]};"
        )
        with container:
            for element in self.elements:
                element.render(scale)


class Element:
    style = None

    def __init__(self, style=None):
        self.style = style or {}


class Break(Element):
    _is_first = True

    def not_first(self):
        self._is_first = False
        return self

    def render(self, scale):
        if self._is_first:
            br(style="line-height: 0;")
        else:
            br()


class Span(Element):
    content = None

    def __init__(self, content, *, style):
        self.content = content
        super().__init__(style)

    def render(self, scale):
        css = style_to_css(self.style, scale=scale)
        span(self.content, style=css)


class HorizontalRule(Element):
    def render(self, scale):
        with div(style="width:100%; font-family: noway-icons; display: flex; align-items: center; margin-top: 0.5rem;"):
            with div(style="transform: rotate(90deg); width: fit-content; margin-right: 0.4rem;"):
                span("\u00B0")
            div(style="border: 1px dashed black; flex: 1; height: 0;")


class ImageElement(Element):
    src = None
    width = None
    height = None

    def __init__(self, src, *, width, height, style):
        self.src = src
        self.width = width
        self.height = height
        super().__init__(style)

    def render(self, scale):
        with div(style="width: 100%"):
            img(src=self.src, width="100%", style="object-fit: contain;")


class Profile:
    profile_data = {"media": {"width": {"pixels": 512}}}

    def get_columns(self, font):
        columns = {"a": 42, "b": 56}
        return columns[font]


class HTMLPrinter:
    profile = None
    current_styling = {}
    elements = []
    is_closed = False

    def __init__(self):
        self.profile = Profile()
        self.elements = []
        self.is_closed = False
        self.current_styling = SetWithDefaultTextProperties().model_dump()

    def _add_element(self, element):
        if self.is_closed:
            raise ConnectionClosedError("Printer connection is closed")

        previous_element = self.elements[-1] if self.elements else None
        if isinstance(element, Break) and isinstance(previous_element, Break):
            self.elements.append(element.not_first())
            return

        if isinstance(element, Span):
            if (
                isinstance(previous_element, Alignment)
                and previous_element.align == element.style["align"]
            ):
                previous_element.add(element)
            else:
                self._add_element(Alignment(element, align=element.style["align"]))
            return

        self.elements.append(element)

    def render(self, scale=1.0):
        receipt_container_style = 'font-family: "nudica-mono"; background-color: white; padding: 1rem; white-space: break-spaces; word-break: break-all;'
        container = div(cls="receipt", style=receipt_container_style)
        with container:
            printable_area_style = f"width: {26 * scale + 0.1}rem;"
            with div(cls="printable-area", style=printable_area_style):
                for element in self.elements:
                    element.render(scale=scale)
        return container.render(pretty=False)

    def close(self):
        self.is_closed = True

    def cut(self):
        self._add_element(HorizontalRule())

    def _validate_text_properties(self, properties):
        if properties.get("custom_size"):
            if properties.get("double_width"):
                raise ValueError("double_width cannot be set when using custom size")
            if properties.get("double_height"):
                raise ValueError("double_height cannot be set when using custom size")
            if not properties.get("width"):
                raise ValueError("width must be set when using custom_size")
            if not properties.get("height"):
                raise ValueError("height must be set when using custom_size")

    def set(self, **kwargs):
        properties = SetTextProperties(**kwargs).model_dump()
        if "normal_textsize" in properties:
            properties["double_width"] = False
            properties["double_height"] = False
            properties["custom_size"] = False
            properties["width"] = 1
            properties["height"] = 1
            del properties["normal_textsize"]

        merged_styling = self.current_styling | properties
        self._validate_text_properties(merged_styling)
        self.current_styling = merged_styling

    def set_with_default(self, **kwargs):
        properties = SetWithDefaultTextProperties(**kwargs).model_dump()
        self._validate_text_properties(properties)
        self.current_styling = properties

    def text(self, text):
        if text:
            self._add_element(Span(text, style=self.current_styling))

    def textln(self, text):
        self.text(text)
        self._add_element(Break())

    def image(self, image: Image, **kwargs):
        width, height = image.size
        image_properties = ImageProperties(**kwargs).model_dump()

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        self._add_element(
            ImageElement(
                "data:image/jpeg;base64," + base64_image,
                width=width,
                height=height,
                style=image_properties,
            )
        )

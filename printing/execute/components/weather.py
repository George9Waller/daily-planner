import math
import os

from escpos.printer import Usb
from flask_babel import lazy_gettext as _
from PIL import Image

from printing.data.dataclasses import Weather
from printing.execute.components.utils import divider, transform_rgba_monochrome

# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
DAY_WEATHER_CODE_TO_ICON = {
    # Thunderstorm
    200: "rain-thunderstorm.png",
    201: "rain-thunderstorm.png",
    202: "rain-thunderstorm.png",
    210: "thunderstorm.png",
    211: "thunderstorm.png",
    212: "thunderstorm.png",
    221: "thunderstorm.png",
    230: "rain-thunderstorm.png",
    231: "rain-thunderstorm.png",
    232: "rain-thunderstorm.png",
    # Drizzle
    300: "drizzle.png",
    301: "drizzle.png",
    302: "drizzle.png",
    310: "drizzle.png",
    311: "drizzle.png",
    312: "drizzle.png",
    313: "drizzle.png",
    314: "drizzle.png",
    321: "drizzle.png",
    # Rain
    500: "rain.png",
    501: "rain.png",
    502: "rain-heavy.png",
    503: "rain-heavy.png",
    504: "rain-heavy.png",
    511: "ice.png",
    520: "rain-heavy.png",
    521: "rain-heavy.png",
    522: "rain-heavy.png",
    531: "rain-heavy.png",
    # Snow
    600: "snow.png",
    601: "snow.png",
    602: "snow.png",
    611: "ice.png",
    612: "ice.png",
    613: "ice.png",
    615: "snow.png",
    616: "snow.png",
    620: "snow.png",
    621: "snow.png",
    622: "snow.png",
    # Atmosphere
    701: "fog.png",
    711: "fog.png",
    721: "fog.png",
    731: "fog.png",
    741: "fog-cloud.png",
    751: "fog.png",
    761: "fog.png",
    762: "fog-cloud.png",
    771: "fog-cloud.png",
    781: "fog-cloud.png",
    # Clear
    800: "sun.png",
    # Clouds
    801: "partly-cloudy.png",
    802: "partly-cloudy.png",
    803: "partly-cloudy.png",
    804: "partly-cloudy.png",
}
NIGHT_WEATHER_CODE_TO_ICON = {
    # Thunderstorm
    200: "night-rain-thunderstorm.png",
    201: "night-rain-thunderstorm.png",
    202: "night-rain-thunderstorm.png",
    210: "night-thunderstorm.png",
    211: "night-thunderstorm.png",
    212: "night-thunderstorm.png",
    221: "night-thunderstorm.png",
    230: "night-rain-thunderstorm.png",
    231: "night-rain-thunderstorm.png",
    232: "night-rain-thunderstorm.png",
    # Drizzle
    300: "night-drizzle.png",
    301: "night-drizzle.png",
    302: "night-drizzle.png",
    310: "night-drizzle.png",
    311: "night-drizzle.png",
    312: "night-drizzle.png",
    313: "night-drizzle.png",
    314: "night-drizzle.png",
    321: "night-drizzle.png",
    # Rain
    500: "night-rain.png",
    501: "night-rain.png",
    502: "night-rain-heavy.png",
    503: "night-rain-heavy.png",
    504: "night-rain-heavy.png",
    511: None,
    520: "night-rain-heavy.png",
    521: "night-rain-heavy.png",
    522: "night-rain-heavy.png",
    531: "night-rain-heavy.png",
    # Snow
    600: "night-snow.png",
    601: "night-snow.png",
    602: "night-snow.png",
    611: None,
    612: None,
    613: None,
    615: "night-snow.png",
    616: "night-snow.png",
    620: "night-snow.png",
    621: "night-snow.png",
    622: "night-snow.png",
    # Atmosphere
    701: None,
    711: None,
    721: None,
    731: None,
    741: None,
    751: None,
    761: None,
    762: None,
    771: None,
    781: None,
    # Clear
    800: "night.png",
    # Clouds
    801: "night-partly-cloudy.png",
    802: "night-partly-cloudy.png",
    803: "night-partly-cloudy.png",
    804: "night-partly-cloudy.png",
}


def get_icon(weather_id, is_day):
    day_icon = DAY_WEATHER_CODE_TO_ICON.get(weather_id)
    if is_day:
        return day_icon or "sun.png"
    return NIGHT_WEATHER_CODE_TO_ICON.get(weather_id) or day_icon or "night.png"


def _justify_between(p: Usb, left, right, font="a"):
    columns = p.profile.get_columns(font)
    content_width = len(left) + len(right)
    spacing = " " * max(columns - content_width, 0)
    p.textln(left + spacing + right)


def _row_calc(total_columns):
    columns_per_item = math.floor(total_columns / 6.0)

    def get_pre_post_space(item_length):
        space_to_fill = max(columns_per_item - item_length, 0)
        pre_space = " " * math.floor(space_to_fill / 2.0)
        post_space = " " * math.ceil(space_to_fill / 2.0)
        return pre_space, post_space

    return get_pre_post_space, columns_per_item


def _write_row(p: Usb, items, font="a"):
    p.set(font=font, align="center")
    get_pre_post_space, _ = _row_calc(p.profile.get_columns(font))
    for item in items:
        pre_space, post_space = get_pre_post_space(len(item))
        p.text(pre_space + item + post_space)
    p.textln("")


def _write_row_icons(p: Usb, icons):
    def _greyscale_filter(x):
        return 0 if x > 0 else 255

    image_width = 50
    total_width = p.profile.profile_data["media"]["width"]["pixels"]
    full_image = Image.new("RGBA", (total_width, 50), (0, 0, 0, 0))
    get_pre_post_space, column_width = _row_calc(total_width)
    for index, icon_file_name in enumerate(icons):
        pre_space, _ = get_pre_post_space(image_width)
        offset = (index * column_width) + len(pre_space)
        # TODO: replace with actual icon
        icon = Image.open(
            os.path.join(os.path.dirname(__file__), f"icons/{icon_file_name}")
        )
        monochrome_icon = transform_rgba_monochrome(icon)
        full_image.paste(monochrome_icon, (offset, 0))

    full_image.save("img.png")
    p.image(full_image, impl="graphics", center=True)


def print_weather(p: Usb, print_data: Weather):
    # Title
    p.textln("")
    p.textln("")
    p.set_with_default(
        bold=True,
        double_height=True,
        double_width=True,
        smooth=True,
    )
    p.textln(_("print.Weather"))

    # Day temps
    p.set_with_default(font="b", density=6)
    p.textln("")
    p.textln(f"{print_data.min_temp:.1f}°C · {print_data.max_temp:.1f}°C")
    p.textln(f"{print_data.sunrise} · {print_data.sunset}")

    # Forecast
    forecasts = print_data.forecasts
    p.set_with_default(align="center")

    divider(p)
    _write_row(p, [forecast.time.lower() for forecast in forecasts])
    _write_row(
        p,
        [f"{round(forecast.temp)}°C" for forecast in forecasts],
        font="b",
    )
    _write_row(
        p, [f"{round(forecast.feels_like_temp)}°C" for forecast in forecasts], font="b"
    )
    _write_row_icons(
        p,
        [get_icon(forecast.weather.id, forecast.is_day) for forecast in forecasts],
    )
    _write_row(
        p,
        [
            f"{round(forecast.wind.speed)}·{round(forecast.wind.gust)}m/s"
            for forecast in forecasts
        ],
        font="b",
    )
    _write_row(
        p,
        [f"{round(forecast.rain_percent)}%" for forecast in forecasts],
        font="b",
    )

    p.set_with_default(font="a")
    divider(p)

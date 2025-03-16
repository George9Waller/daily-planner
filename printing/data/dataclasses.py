from typing import List, Optional

from pydantic import BaseModel, Field


class PrintDataContext(BaseModel):
    date: str
    locale: str


class Greeting(BaseModel):
    greeting: str


class Day(BaseModel):
    day: str


class WeatherForecastDay(BaseModel):
    id: int
    label: str
    description: str
    icon: str


class WeatherForecastWind(BaseModel):
    speed: float
    gust: float


class WeatherForecast(BaseModel):
    time: str
    temp: float
    feels_like_temp: float
    weather: WeatherForecastDay
    wind: WeatherForecastWind
    rain_percent: int
    is_day: bool


class Weather(BaseModel):
    min_temp: float
    max_temp: float
    sunrise: str
    sunset: str
    utc_offset_mins: int
    forecasts: List[WeatherForecast]


class HabiticaTask(BaseModel):
    text: str
    notes: Optional[str] = None
    checklist: Optional[List[str]] = Field(default_factory=list)


class HabiticaTasks(BaseModel):
    todos: List[HabiticaTask]
    dailies: List[HabiticaTask]
    habits: List[HabiticaTask]


class Reflection(BaseModel):
    data: str


class PrintData(BaseModel):
    greeting: Greeting
    day: Day
    weather: Optional[Weather]
    todos: Optional[HabiticaTasks]
    habits: Optional[HabiticaTasks]
    dailies: Optional[HabiticaTasks]
    reflection: Optional[Reflection]


class GetPrintDataResponse(BaseModel):
    print_data: PrintData
    errors: dict
    is_fatal: bool

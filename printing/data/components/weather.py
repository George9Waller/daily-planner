import os
from datetime import date, datetime, timedelta
from urllib.parse import urlencode

from flask_babel import format_time

from printing.data.dataclasses import PrintDataContext, Weather
from printing.data.decorators import cached, returns_data_as
from printing.data.utils import make_request


@returns_data_as(Weather)
@cached(timedelta(minutes=30))
def get_weather(*, print_data_context: PrintDataContext, **kwargs):
    weather_response = _get_weather_for_day(
        print_data_context.date, locale=print_data_context.locale
    )
    utc_offset_mins = weather_response["city"]["timezone"] / 60
    forecasts = _parse_forecasts(
        weather_response, day=print_data_context.date, offset=utc_offset_mins
    )
    temperatures = [forecast["temp"] for forecast in forecasts]
    return {
        "min_temp": min(temperatures),
        "max_temp": max(temperatures),
        "sunrise": _parse_time(
            weather_response["city"]["sunrise"], offset=utc_offset_mins
        ),
        "sunset": _parse_time(
            weather_response["city"]["sunset"], offset=utc_offset_mins
        ),
        "utc_offset_mins": utc_offset_mins,
        "forecasts": forecasts,
    }


def _get_weather_for_day(day, *, locale):
    # TODO: store locations in db and add config ui
    response = make_request(
        "https://api.openweathermap.org/data/2.5/forecast?"
        + urlencode(
            {
                # BTN
                "lat": "50.8229",
                "lon": "0.1363",
                # St Vic
                # "lat": "45.8779",
                # "lon": "1.0132",
                "appid": os.environ.get("OPEN_WEATHER_API_KEY"),
                "units": "metric",
                "lang": locale,
            }
        )
    )
    return response.json()


def _parse_forecasts(response, *, day, offset):
    parsed_day = date.fromisoformat(day) + timedelta(minutes=offset)
    forecasts = [
        forecast
        for forecast in response["list"]
        if datetime.fromisoformat(forecast["dt_txt"]).date() >= parsed_day
    ]
    return [
        {
            "time": _parse_date_time(forecast["dt_txt"], offset=offset),
            "temp": forecast["main"]["temp"],
            "feels_like_temp": forecast["main"]["feels_like"],
            "weather": {
                "id": forecast["weather"][0]["id"],
                "label": forecast["weather"][0]["main"],
                "description": forecast["weather"][0]["description"],
                "icon": forecast["weather"][0]["icon"],
            },
            "wind": {
                "speed": forecast["wind"]["speed"],
                "gust": forecast["wind"]["gust"],
            },
            "rain_percent": forecast["pop"] * 100.0,
            "is_day": forecast["sys"]["pod"] == "d",
        }
        for forecast in forecasts
    ][:6]


def _parse_time(timestamp, *, offset):
    parsed_date_time = datetime.utcfromtimestamp(timestamp) + timedelta(minutes=offset)
    return format_time(parsed_date_time, format="short")


def _parse_date_time(timestamp, *, offset):
    parsed_date_time = datetime.fromisoformat(timestamp) + timedelta(minutes=offset)
    return format_time(parsed_date_time, format="ha")

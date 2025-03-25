from flask import redirect, render_template
from flask_babel import get_locale

from actions.printing import (
    create_instant_print_job,
    get_latest_print_jobs,
    get_most_recent_printable_job,
)
from cache.actions import get_printer_is_online
from printing.execute import print_label_as_html
from routes.utils import context


def home():
    extra_context = {
        "recent_print_jobs": get_latest_print_jobs(10),
        "printer_is_online": get_printer_is_online(),
    }
    most_recent_print_job = get_most_recent_printable_job()
    if most_recent_print_job:
        extra_context["recent_receipt"] = print_label_as_html(
            most_recent_print_job.print_data
        )

    return render_template("home.html", **context(extra_context))


def print_now():
    create_instant_print_job(locale=get_locale().language)
    return redirect("/")

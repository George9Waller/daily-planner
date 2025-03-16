import json
from datetime import date

from printing.data import get_print_data
from printing.data.dataclasses import PrintDataContext
from data import db, models


def create_instant_print_job(*, locale):
    context = PrintDataContext(date=date.today().isoformat(), locale=locale)
    print_data = get_print_data(context)
    db.session.add(
        models.PrintJob(
            print_data=print_data.print_data.model_dump(),
            errors=print_data.errors,
            is_printable=not print_data.is_fatal,
        )
    )
    db.session.commit()
    return print_data.print_data.model_dump()


def get_most_recent_printable_job():
    return db.session.execute(
        db.select(
            models.PrintJob.created, models.PrintJob.errors, models.PrintJob.print_data
        )
        .filter_by(is_printable=True)
        .order_by(models.PrintJob.created.desc())
        .limit(1)
    ).one_or_none()


def get_latest_print_jobs(count=10):
    def get_status(job):
        if not job.is_printable:
            return "FAILED"
        if any(job.errors.values()):
            return "WARNING"
        return "SUCCESS"

    jobs = db.session.execute(
        db.select(
            models.PrintJob.created,
            models.PrintJob.is_printable,
            models.PrintJob.errors,
        )
        .order_by(models.PrintJob.created.desc())
        .limit(count)
    ).all()
    return [
        {
            **job._mapping,
            "status": get_status(job),
            "errors": json.dumps(job.errors, indent=2),
        }
        for job in jobs
    ]

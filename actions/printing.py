import json
import os
from datetime import date, datetime, timedelta, timezone

from data import db, models
from printing.data import get_print_data
from printing.data.dataclasses import PrintDataContext


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
            models.PrintJob.created,
            models.PrintJob.errors,
            models.PrintJob.print_data,
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

    def get_state(job):
        threshold_minutes = int(os.environ.get("PRINT_THRESHOLD_MINUTES") or 5)
        created_since_threshold = datetime.now(timezone.utc) - timedelta(
            minutes=threshold_minutes
        )
        if job.state == "PENDING":
            if not job.is_printable:
                return "FAILED"
            if job.created < created_since_threshold:
                return "STALE"
            return "PENDING"
        if job.state == "SENT":
            return "SENT"
        return "UNKNOWN"

    jobs = db.session.execute(
        db.select(
            models.PrintJob.id,
            models.PrintJob.created,
            models.PrintJob.is_printable,
            models.PrintJob.errors,
            models.PrintJob.state,
        )
        .order_by(models.PrintJob.created.desc())
        .limit(count)
    ).all()
    return [
        {
            **job._mapping,
            "status": get_status(job),
            "state": get_state(job),
            "errors": json.dumps(job.errors, indent=2),
        }
        for job in jobs
    ]

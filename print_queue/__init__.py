import logging
import os
import time
from datetime import datetime, timedelta, timezone

from data import db, models
from printing.execute import print_label

logger = logging.getLogger(__name__)


def _get_print_job_or_none():
    threshold_minutes = int(os.environ.get("PRINT_THRESHOLD_MINUTES") or 5)
    age_threshold = timedelta(minutes=threshold_minutes)
    created_since_threshold = datetime.now(timezone.utc) - age_threshold

    print_job = db.session.execute(
        db.select(
            models.PrintJob.id,
            models.PrintJob.print_data,
        )
        .filter_by(is_printable=True, state="PENDING")
        .filter(models.PrintJob.created > created_since_threshold)
        .order_by(models.PrintJob.created.asc())
        .limit(1)
    ).one_or_none()
    db.session.close()
    return print_job


def _process_queue():
    print_job = _get_print_job_or_none()
    printed = False
    if print_job:
        logger.info(f"Processing print job {print_job.id}")
        try:
            printed = print_label(print_job.print_data)
        except Exception as e:
            logger.error(f"Error printing job {print_job.id}: {e}")
            return
        else:
            if printed:
                db.session.execute(
                    db.update(models.PrintJob)
                    .where(models.PrintJob.id == print_job.id)
                    .values(state="SENT")
                )
                db.session.commit()
                logger.info(f"Print job {print_job.id} complete")


def run():
    while True:
        _process_queue()
        time.sleep(1)

import json
from datetime import datetime

from pydantic import BaseModel

from data import db, models


def serialize_args_kwargs(args, kwargs):
    def maybe_serialize_model(value):
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value

    return {
        "args": json.loads(json.dumps([maybe_serialize_model(arg) for arg in args])),
        "kwargs": json.loads(
            json.dumps(
                {key: maybe_serialize_model(value) for key, value in kwargs.items()},
                sort_keys=True,
            )
        ),
    }


def get_cached_result(*, function, args, kwargs, max_age):
    hit_created_since = datetime.now() - max_age
    serialized_args_kwargs = serialize_args_kwargs(args, kwargs)
    cached_record = db.session.execute(
        db.select(models.CachedCall.result)
        .filter_by(function=function.__name__)
        .filter(models.CachedCall.created > hit_created_since)
        .filter_by(call_args_kwargs=serialized_args_kwargs)
        .order_by(models.CachedCall.created.desc())
        .limit(1)
    ).one_or_none()
    if cached_record:
        return cached_record.result


def store_cached_result(*, function, args, kwargs, result):
    db.session.add(
        models.CachedCall(
            function=function.__name__,
            call_args_kwargs=serialize_args_kwargs(args, kwargs),
            result=json.loads(json.dumps(result)),
        )
    )
    db.session.commit()

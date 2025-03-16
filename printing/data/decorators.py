from pydantic import BaseModel

from actions.cached_call import get_cached_result, store_cached_result


def returns_data_as(data_model: BaseModel):
    def decorator(function):
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            data_model.validate(value)
            return value

        return wrapper

    return decorator


def cached(max_age):
    def decorator(function):
        def wrapper(*args, **kwargs):
            cached_result = get_cached_result(
                function=function, args=args, kwargs=kwargs, max_age=max_age
            )
            if cached_result:
                return cached_result

            result = function(*args, **kwargs)
            store_cached_result(
                function=function, args=args, kwargs=kwargs, result=result
            )
            return result

        return wrapper

    return decorator

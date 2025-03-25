import requests
from requests.exceptions import HTTPError, Timeout
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

RETRY_ON_STATUS_CODES = [429, 408, 500, 502, 503, 504]


class RetryStatusCodeError(Exception):
    pass


def make_request(url, *, method="get"):
    session = requests.session()

    @retry(
        retry=(
            retry_if_exception(ConnectionError)
            | retry_if_exception(Timeout)
            | retry_if_exception(RetryStatusCodeError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential_jitter(initial=0.5),
    )
    def _make_reuqest(url, *, method="get"):
        method = getattr(session, method)
        response = method(url)
        if response.status_code in RETRY_ON_STATUS_CODES:
            raise RetryStatusCodeError()
        response.raise_for_status()
        return response

    return _make_reuqest(url, method=method)

import json
import logging
from typing import Callable, Dict, Optional

from anonymizeip import anonymize_ip
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app import settings

LOGURU_ELASTICSEARCH = "{time:YYYY-MM-DD\tHH:mm:ss}\t{message}"
LOGURU_MONITORING = "{time:YYYY-MM-DD HH:mm:ss zz} {message}"
MONITORING_MESSAGE = "{masked_ip} {client} {special} {method} {url} {headers}"


class LoguruInterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


logging.getLogger(None).addHandler(LoguruInterceptHandler())


class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        request_info = extract_request(request)
        monitoring_info = format_monitoring_info(request_info)
        # logging
        logger.info(request_info)
        logger.bind(monitoring=True).info(monitoring_info)
        # finish
        response = await call_next(request)
        return response


def log_args(**kwargs) -> None:
    """Log keyword args passed to this function."""
    logger.bind(elasticsearch=True).info(kwargs)
    return None


def elasticsearch_predicate(record) -> bool:
    """Check if record is valid to go to elasticsearch monitoring."""
    valid = False
    if "elasticsearch" in record["extra"]:
        valid = True
    return valid


def monitoring_predicate(record) -> bool:
    if "monitoring" in record["extra"] and record["extra"]["monitoring"]:
        return True
    return False


def extract_request(request: Request):
    # Process headers and remove cookie field
    headers = dict(request.headers)
    info = {
        "method": request.method,
        "url": {
            "url": str(request.url),
            "path": request.url.path,
            "port": request.url.port,
            "scheme": request.url.scheme,
        },
        "params": {
            "query_params": dict(request.query_params),
            "path_params": dict(request.path_params),
        },
        "client": {"host": request.client.host},
        "headers": headers,
    }
    return info


def special_headers(headers) -> str:
    """Mark incoming request for whether it is for special usage:
    unit tests, client package building, etc

    If True, returns "special", otherwise returns "normal".
    """
    if "client-type" in headers.keys():
        if headers["client-type"] == "pytest":
            return "special"
    if "ci" in headers.keys() and json.loads(headers["ci"].lower()):
        return "special"
    return "normal"


def get_masked_ip(headers: Dict) -> Optional[str]:
    if "x-forwarded-for" in headers.keys():
        field = "x-forwarded-for"
    elif "X-Forwarded-For" in headers.keys():
        field = "X-Forwarded-For"
    else:
        return None
    x_forwarded_for = headers[field]
    masked_ip = None
    try:
        # "1.2.3.4, 1.2.3.4" -> "1.2.3.4" the last field
        if "," in x_forwarded_for:
            ip = x_forwarded_for.split(",")[-1].strip()
        else:
            ip = x_forwarded_for
        # "1.2.3.4" -> "1.2.3.0"
        masked_ip = anonymize_ip(ip)
    except:
        return None
    return masked_ip


def filter_headers(headers: Dict) -> Dict:
    filtered_headers = headers
    filtered_headers.pop("cookie", None)
    filtered_headers.pop("x-forwarded-for", None)
    filtered_headers.pop("X-Forwarded-For", None)
    return filtered_headers


def format_monitoring_info(info):
    headers = info["headers"]
    special = special_headers(headers)
    masked_ip = get_masked_ip(headers)
    filtered_headers = filter_headers(headers)
    client = "others"
    if "client-type" in headers:
        client = headers["client-type"]
    message = MONITORING_MESSAGE.format(
        masked_ip=masked_ip,
        client=client,
        special=special,
        method=info["method"],
        url=info["url"],
        headers=filtered_headers,
    )
    return message


# daily logs, verbose
logger.add(
    settings.log_dir / "api.log",
    enqueue=False,
    rotation="7 days",
    retention="7 days",
    compression="tar.gz",
)
# elasticsearch monitor
logger.add(
    settings.log_dir / "elasticsearch.log",
    format=LOGURU_ELASTICSEARCH,
    filter=elasticsearch_predicate,
    enqueue=False,
    rotation="7 days",
    retention="7 days",
    compression="tar.gz",
    backtrace=False,
    catch=False,
    serialize=True,
)
# a new attempt at monitoring
logger.add(
    settings.log_dir / "monitoring.log",
    format=LOGURU_MONITORING,
    enqueue=False,
    filter=monitoring_predicate,
    rotation="7 days",
    retention="7 days",
    compression="tar.gz",
)

import logging

from loguru import logger

from app import settings


class LoguruInterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


logging.getLogger(None).addHandler(LoguruInterceptHandler())


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


# daily logs, verbose
logger.add(
    settings.log_dir / "api.log",
    enqueue=True,
    rotation="7 days",
    retention="7 days",
    compression="tar.gz",
)
# elasticsearch monitor
logger.add(
    settings.log_dir / "elasticsearch.log",
    format="{time:YYYY-MM-DD\tHH:mm:ss}\t{message}",
    filter=elasticsearch_predicate,
    enqueue=True,
    rotation="7 days",
    retention="7 days",
    compression="tar.gz",
    backtrace=False,
    catch=False,
    serialize=True,
)

# Listing 12.2 Logging and a reusable retry decorator
import functools
import logging
import sys
import time

logger = logging.getLogger("ruckzone.pipeline")  #A


def configure_logging(level=logging.INFO):  #B
    """Send pipeline logs to stdout with timestamps."""
    logger.setLevel(level)
    if not logger.handlers:  #C
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s | %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
    return logger


def with_retries(max_attempts=3, base_delay=1.0,
                 exceptions=(Exception,)):  #D
    """Retry a function with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)  #E
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)  #F
                except exceptions as exc:
                    if attempt >= max_attempts:  #G
                        logger.warning(
                            "%s failed after %d attempts: %s",
                            func.__name__, attempt, exc,
                        )
                        raise
                    delay = base_delay * (2 ** (attempt - 1))  #H
                    logger.info(
                        "%s attempt %d failed (%s); retry in %.1fs",
                        func.__name__, attempt, exc, delay,
                    )
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

#A One named logger shared by every agent in the pipeline
#B Call once at the start of a run to turn logging on
#C Guard against adding duplicate handlers if the cell re-runs
#D A decorator any agent can wear to become resilient
#E Preserve the wrapped function's name so logs stay readable
#F The happy path: succeed and return immediately
#G Out of attempts, log the failure and re-raise for the caller
#H Wait longer after each failure (1s, 2s, 4s, ...)

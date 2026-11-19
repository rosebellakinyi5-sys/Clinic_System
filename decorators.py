import time
from datetime import datetime
from functools import wraps

LOG_FILE = "clinic_log.txt"


def _write_log(line):
    with open(LOG_FILE, "a") as file:
        file.write(line + "\n")


def log_action(func):
    """Record every scheduling action, whether it worked or was blocked."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = func(*args, **kwargs)
        except ValueError as error:
            _write_log(f"{stamp} | {func.__name__} | BLOCKED | {error}")
            raise                      # pass the error on so the menu can show it
        _write_log(f"{stamp} | {func.__name__} | OK | {args[1:]}")
        return result
    return wrapper


def time_it(func):
    """Show how long a report took to generate."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - started
        print(f"(report generated in {elapsed:.4f} seconds)")
        return result
    return wrapper
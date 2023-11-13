import os

# Logging
BASE_LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(BASE_LOG_DIR, "logs.log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"},
        "simple": {"format": "%(levelname)s\t%(asctime)s\t%(filename)s\t%(lineno)d\t%(message)s"},
    },
    "root": {"level": "ERROR", "handlers": ["console"]},
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_FILE_PATH,
            "when": "D",
            "encoding": "utf-8",
            "formatter": "simple",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "default"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

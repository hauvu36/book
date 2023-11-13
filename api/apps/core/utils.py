import logging
from datetime import datetime
from logging import Logger
from typing import Optional
from mimetypes import MimeTypes

import pytz
from dateutil.parser import parse
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_logger(name: Optional[str] = "django") -> Logger:
    return logging.getLogger(name)


def get_now() -> datetime:
    return datetime.now(tz=pytz.utc)


def get_utc_now() -> datetime:
    """
    Get current UTC time
    :return:
    """
    return get_now().replace(tzinfo=pytz.utc)


def parse_datetime(date_str: str, tz=timezone.utc) -> Optional[datetime]:
    try:
        return parse(date_str).replace(tzinfo=tz)
    except Exception as ex:
        logger.exception(ex)
        return None


def get_mime_type(file_name: str) -> str:
    mime = MimeTypes()
    return mime.guess_type(file_name)[0]


def default_create_token(token_model, user, serializer):
    return None

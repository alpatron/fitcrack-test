from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class WebadminSnackbarNotificationType(Enum):
    SUCCESS = 'success'
    ERROR   = 'error'


@dataclass(frozen=True)
class WebadminSnackbarNotification:
    type : WebadminSnackbarNotificationType
    message : str

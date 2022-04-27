from typing import Optional
from enum import Enum
from pydantic import BaseModel


class NotificationLevel(Enum):
    panic = 1
    abnormal = 2
    normal = 3


class Notification(BaseModel):
    message: Optional[str]
    at: Optional[str]
    level: Optional[NotificationLevel]

    class Config:
        orm_mode = True


class PatientNotifications(BaseModel):
    oid: str
    name: str
    at: Optional[str]
    notifications: Optional[list[Notification]]
    level: Optional[NotificationLevel]

    class Config:
        orm_mode = True

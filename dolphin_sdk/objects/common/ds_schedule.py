"""
海豚调度的定时配置
"""

import dataclasses
import datetime

from dolphin_sdk.objects.base import ObjectBase

__all__ = [
    "DSSchedule",
]


@dataclasses.dataclass(slots=True)
class DSSchedule(ObjectBase):
    """海豚调度的定时配置"""

    start_time: datetime.datetime = dataclasses.field(kw_only=True)
    end_time: datetime.datetime = dataclasses.field(kw_only=True)
    crontab: str = dataclasses.field(kw_only=True)
    timezone_id: str = dataclasses.field(kw_only=True)

    def to_json(self) -> dict:
        return {
            "startTime": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "endTime": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "crontab": self.crontab,
            "timezoneId": self.timezone_id,
        }

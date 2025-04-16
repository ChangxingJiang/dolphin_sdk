"""
海豚调度任务定时任务
"""

import dataclasses
import datetime
from typing import Any, Dict, Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.enum import DSReleaseState

__all__ = [
    "DSScheduleRecord"
]


@dataclasses.dataclass(slots=True)
class DSScheduleRecord(ObjectBase):
    """海豚调度任务定时任务

    除 process_code 外，该类的属性与 t_ds_schedules 表中的字段一一对应：

    - process_code：对应 t_ds_schedules 表的 process_definition_code 字段
    """

    # key（在构造时不需要）
    id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # process definition code
    process_code: int = dataclasses.field(kw_only=True, default=None)

    # start time
    start_time: datetime.datetime = dataclasses.field(kw_only=True, default=None)

    # end time
    end_time: datetime.datetime = dataclasses.field(kw_only=True, default=None)

    # schedule timezone id
    timezone_id: Optional[str] = dataclasses.field(kw_only=True, default=None)

    # crontab description
    crontab: str = dataclasses.field(kw_only=True, default=None)

    # failure strategy. 0:end,1:continue
    failure_strategy: int = dataclasses.field(kw_only=True, default=None)

    # user id
    user_id: int = dataclasses.field(kw_only=True, default=None)

    # release state. 0:offline,1:online
    release_state: DSReleaseState = dataclasses.field(kw_only=True, default=None)

    # Alarm type: 0 is not sent, 1 process is sent successfully, 2 process is sent failed, 3 process is sent successfully and all failures are sent
    warning_type: int = dataclasses.field(kw_only=True)

    # alert group id
    warning_group_id: int = dataclasses.field(kw_only=True)

    # process instance priority：0 Highest,1 High,2 Medium,3 Low,4 Lowest
    process_instance_priority: int = dataclasses.field(kw_only=True)

    # worker group id
    worker_group: Optional[str] = dataclasses.field(kw_only=True, default="")

    # environment code
    environment_code: int = dataclasses.field(kw_only=True, default=-1)

    # create time（在构造时不需要）
    create_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    # update time（在构造时不需要）
    update_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    @staticmethod
    def from_t_ds_schedules_record(record: Dict[str, Any]) -> "DSScheduleRecord":
        return DSScheduleRecord(
            id=record["id"],
            process_code=record["process_definition_code"],
            start_time=record["start_time"],
            end_time=record["end_time"],
            timezone_id=record["timezone_id"],
            crontab=record["crontab"],
            failure_strategy=record["failure_strategy"],
            user_id=record["user_id"],
            release_state=DSReleaseState.from_db_value(record["release_state"]),
            warning_type=record["warning_type"],
            warning_group_id=record["warning_group_id"],
            process_instance_priority=record["process_instance_priority"],
            worker_group=record["worker_group"],
            environment_code=record["environment_code"],
            create_time=record["create_time"],
            update_time=record["update_time"],
        )

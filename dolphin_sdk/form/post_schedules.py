"""
创建海豚工作流的定时任务
"""

import dataclasses
import datetime
import json
from typing import Dict, Optional

from dolphin_sdk.objects import DSFailureStrategy
from dolphin_sdk.objects import DSPriority
from dolphin_sdk.objects import DSSchedule
from dolphin_sdk.objects import DSWarningType

__all__ = [
    "DSPostSchedulesForm"
]


@dataclasses.dataclass(slots=True)
class DSPostSchedulesForm:
    """创建海豚工作流的定时任务"""

    process_code: int = dataclasses.field(kw_only=True)
    schedule: DSSchedule = dataclasses.field(kw_only=True)
    failure_strategy: DSFailureStrategy = dataclasses.field(kw_only=True, default=DSFailureStrategy.CONTINUE)
    warning_type: DSWarningType = dataclasses.field(kw_only=True, default=DSWarningType.NONE)
    process_instance_priority: DSPriority = dataclasses.field(kw_only=True, default=DSPriority.MEDIUM)
    warning_group_id: Optional[int] = dataclasses.field(kw_only=True, default=None)
    worker_group: str = dataclasses.field(kw_only=True)
    environment_code: Optional[int] = dataclasses.field(kw_only=True, default=None)
    deadline: Optional[int] = dataclasses.field(kw_only=True, default=0)

    @staticmethod
    def create_by_crontab(process_code: int, crontab: str, worker_group: str,
                          deadline: Optional[int],
                          warning_type: DSWarningType = DSWarningType.NONE,
                          warning_group_id: Optional[int] = None) -> "DSPostSchedulesForm":
        """根据默认值创建"""
        start_time = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        end_time = start_time + datetime.timedelta(days=100 * 365)
        schedule = DSSchedule(
            start_time=start_time,
            end_time=end_time,
            crontab=crontab,
            timezone_id="Asia/Shanghai"
        )
        return DSPostSchedulesForm(
            process_code=process_code,
            schedule=schedule,
            worker_group=worker_group,
            deadline=deadline,
            warning_type=warning_type,
            warning_group_id=warning_group_id
        )

    def to_dict(self) -> Dict[str, str]:
        result = {
            "schedule": json.dumps(self.schedule.to_json(), ensure_ascii=False),
            "failureStrategy": self.failure_strategy.web_value,
            "warningType": self.warning_type.web_value,
            "processInstancePriority": self.process_instance_priority.web_value,
            "warningGroupId": str(self.warning_group_id) if self.warning_group_id is not None else "",
            "workerGroup": self.worker_group,
            "environmentCode": str(self.environment_code) if self.environment_code is not None else "",
            "processDefinitionCode": str(self.process_code)
        }
        if self.deadline is not None:
            result["deadline"] = str(self.deadline)
        return result

"""
海豚调度优先级枚举值
"""

import enum
from typing import Tuple

__all__ = [
    "DSPriority"
]


class DSPriority(enum.Enum):
    """海豚调度优先级枚举值

    适用字段：
    t_ds_command.workflow_instance_priority
    t_ds_error_command.workflow_instance_priority
    t_ds_task_definition.task_priority
    t_ds_task_definition_log.task_priority
    t_ds_workflow_instance.workflow_instance_priority
    t_ds_schedules.workflow_instance_priority
    t_ds_task_instance.task_instance_priority

    Notes
    -----
    需要注意的是，task_group 的优先级似乎不适用于这个枚举值。
    """

    HIGHEST = (0, "HIGHEST")  # Highest
    HIGH = (1, "HIGH")  # High
    MEDIUM = (2, "MEDIUM")  # Medium
    LOW = (3, "LOW")  # Low
    LOWEST = (4, "LOWEST")  # Lowest

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSPriority":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

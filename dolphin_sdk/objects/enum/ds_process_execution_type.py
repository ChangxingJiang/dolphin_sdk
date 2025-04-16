"""
海豚调度任务定义表 execution_type 的枚举值
"""

import enum

__all__ = [
    "DSProcessExecutionType"
]


class DSProcessExecutionType(enum.Enum):
    """海豚调度工作流定义表任务执行类型的枚举值

    适用字段：
    t_ds_process_definition.execution_type
    """

    PARALLEL = (0, 0)  # parallel
    SERIAL_WAIT = (1, 1)  # serial wait
    SERIAL_DISCARD = (2, 2)  # serial discard
    SERIAL_PRIORITY = (3, 3)  # serial priority

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSProcessExecutionType":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

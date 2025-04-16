"""
海豚调度依赖关系的枚举值
"""

import enum

__all__ = [
    "DSConditionType"
]


class DSConditionType(enum.Enum):
    """海豚调度任务定义表 flag 字段的枚举值

    适用字段：
    t_ds_process_task_relation.condition_type
    """

    NONE = (0, "NONE")
    JUDGE = (1, "JUDGE")
    DELAY = (1, "DELAY")

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSConditionType":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

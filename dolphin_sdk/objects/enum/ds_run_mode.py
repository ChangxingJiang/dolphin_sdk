"""
海豚调度补数的执行方式
"""

import enum

__all__ = [
    "DSRunMode"
]


class DSRunMode(enum.Enum):
    """海豚调度补数的执行方式

    适用表单：
    /projects/{project_code}/executors/start-process-instance 接口表单的 runMode 字段
    """

    RUN_MODE_SERIAL = (None, "RUN_MODE_SERIAL")  # 串行执行
    RUN_MODE_PARALLEL = (None, "RUN_MODE_PARALLEL")  # 并行执行

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSRunMode":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

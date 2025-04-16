"""
海豚工作流是的失败策略
"""

import enum

__all__ = [
    "DSFailureStrategy"
]


class DSFailureStrategy(enum.Enum):
    """海豚工作流是的失败策略

    适用表单：
    /projects/{project_code}/executors/start-process-instance 接口表单的 failureStrategy 字段
    """

    CONTINUE = (None, "CONTINUE")  # 继续
    END = (None, "END")  # 结束

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSFailureStrategy":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

"""
海豚工作流的通知策略
"""

import enum

__all__ = [
    "DSWarningType"
]


class DSWarningType(enum.Enum):
    """海豚工作流的通知策略

    适用表单：
    /projects/{project_code}/executors/start-process-instance 接口表单的 warningType 字段
    """

    NONE = (None, "NONE")  # 都不发
    SUCCESS = (None, "SUCCESS")  # 成功发
    FAILURE = (None, "FAILURE")  # 失败发
    ALL = (None, "ALL")  # 成功和失败都发

    def __new__(cls, db_value: int, web_value: str):
        member = object.__new__(cls)
        member.db_value = db_value  # 数据库中存储的值
        member.web_value = web_value  # Web API 中的值
        return member

    @classmethod
    def from_db_value(cls, db_value: int) -> "DSWarningType":
        for member in cls:
            if member.db_value == db_value:
                return member
        raise KeyError(f"{db_value} 不是 {cls.__name__} 的有效枚举值")

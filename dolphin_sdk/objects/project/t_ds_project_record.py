"""
海豚调度项目级对象
"""

import dataclasses
import datetime
from typing import Any, Dict, Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.enum import DSAvailableFlag

__all__ = [
    "DSProjectRecord"
]


@dataclasses.dataclass(slots=True)
class DSProjectRecord(ObjectBase):
    """海豚元数据中 t_ds_project 表的记录"""

    # key（在构造时不需要）
    id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # t_ds_project.name: project name
    project_name: Optional[str] = dataclasses.field(kw_only=True, default=None)

    # t_ds_project.code: encoding
    project_code: int = dataclasses.field(kw_only=True)

    # t_ds_project.description
    description: Optional[str] = dataclasses.field(kw_only=True, default=None)

    # t_ds_project.user_id: creator id
    user_id: int = dataclasses.field(kw_only=True)

    # t_ds_project.flag: 0 not available, 1 available
    flag: DSAvailableFlag = dataclasses.field(kw_only=True, default=DSAvailableFlag.AVAILABLE)

    # create time（在构造时不需要）
    create_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    # update time（在构造时不需要）
    update_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    @staticmethod
    def from_record_dict(record_dict: Dict[str, Any]) -> "DSProjectRecord":
        """根据 t_ds_project 表记录的字典格式构造 DSScheduleRecord 对象"""
        return DSProjectRecord(
            id=record_dict["id"],
            project_name=record_dict["name"],
            project_code=record_dict["code"],
            description=record_dict["description"],
            user_id=record_dict["user_id"],
            flag=DSAvailableFlag.from_db_value(record_dict["flag"]),
            create_time=record_dict["create_time"],
            update_time=record_dict["update_time"],
        )

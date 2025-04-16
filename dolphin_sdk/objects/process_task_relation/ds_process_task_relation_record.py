"""
海豚调度工作流、任务关系对象
"""

import dataclasses
import datetime
import json
from typing import Any, Dict
from typing import Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.enum import DSConditionType


@dataclasses.dataclass(slots=True)
class DSProcessTaskRelationRecord(ObjectBase):
    """海豚调度工作流、任务关系对象

    该类的属性与 t_ds_process_task_relation 表中的字段一一对应
    """

    # relation name
    id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # relation name
    name: str = dataclasses.field(kw_only=True, default="")

    # project code
    project_code: int = dataclasses.field(kw_only=True)

    # process code
    process_code: int = dataclasses.field(kw_only=True)

    # process version
    process_version: int = dataclasses.field(kw_only=True)

    # pre task code
    pre_task_code: int = dataclasses.field(kw_only=True)

    # pre task version
    pre_task_version: int = dataclasses.field(kw_only=True)

    # post task code
    post_task_code: int = dataclasses.field(kw_only=True)

    # post task version
    post_task_version: int = dataclasses.field(kw_only=True)

    # condition type : 0 none, 1 judge 2 delay
    condition_type: DSConditionType = dataclasses.field(kw_only=True)

    # condition params(json)
    condition_params: list = dataclasses.field(kw_only=True)

    # create time（在构造时不需要）
    create_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    # update time（在构造时不需要）
    update_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    @staticmethod
    def from_t_ds_process_task_relation_record(record: Dict[str, Any]) -> "DSProcessTaskRelationRecord":
        return DSProcessTaskRelationRecord(
            id=record["id"],
            name=record["name"],
            project_code=record["project_code"],
            process_code=record["process_definition_code"],
            process_version=record["process_definition_version"],
            pre_task_code=record["pre_task_code"],
            pre_task_version=record["pre_task_version"],
            post_task_code=record["post_task_code"],
            post_task_version=record["post_task_version"],
            condition_type=DSConditionType.from_db_value(record["condition_type"]),
            condition_params=json.loads(record["condition_params"]),
            create_time=record["create_time"],
            update_time=record["update_time"],
        )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "preTaskCode": self.pre_task_code,
            "preTaskVersion": self.pre_task_version,
            "postTaskCode": self.post_task_code,
            "postTaskVersion": self.post_task_version,
            "conditionType": self.condition_type,
            "conditionParams": self.condition_params,
        }

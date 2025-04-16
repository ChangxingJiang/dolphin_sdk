"""
海豚调度工作流定义详情节点
"""

import dataclasses
import datetime
from typing import Any, Dict, List, Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.common import DSLocation
from dolphin_sdk.objects.common import create_ds_location_list_from_db_value
from dolphin_sdk.objects.enum import DSProcessExecutionType
from dolphin_sdk.objects.enum import DSReleaseState
from dolphin_sdk.objects.process.ds_process_definition import DSProcessDefinition

__all__ = [
    "DSProcessDefinitionRecord"
]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSProcessDefinitionRecord(DSProcessDefinition):
    """海豚调度工作流定义详情节点

    除 process_code 外，该类的属性与 t_ds_process_definition 表中的字段一一对应：

    - process_code 属性对应 t_ds_process_definition 表中的 code 字段
    """

    # self-increasing id（在构造时不需要）
    id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # process definition name
    name: str = dataclasses.field(kw_only=True)

    # process definition version
    version: int = dataclasses.field(kw_only=True, default=0)

    # description
    description: str = dataclasses.field(kw_only=True)

    # process definition release state：0:offline,1:online
    release_state: DSReleaseState = dataclasses.field(kw_only=True)

    # process definition creator id
    user_id: int = dataclasses.field(kw_only=True)

    # global parameters
    global_params: str = dataclasses.field(kw_only=True)

    # 0 not available, 1 available
    flag: int = dataclasses.field(kw_only=True)

    # Node location information
    locations: List[DSLocation] = dataclasses.field(kw_only=True)

    # alert group id
    warning_group_id: int = dataclasses.field(kw_only=True)

    # time out, unit: minute
    timeout: int = dataclasses.field(kw_only=True)

    # tenant id
    tenant_id: int = dataclasses.field(kw_only=True)

    # execution_type 0:parallel,1:serial wait,2:serial discard,3:serial priority
    execution_type: DSProcessExecutionType = dataclasses.field(kw_only=True)

    # create time（在构造时不需要）
    create_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    # update time（在构造时不需要）
    update_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    @staticmethod
    def from_t_ds_process_definition_record(record: Dict[str, Any]) -> "DSProcessDefinitionRecord":
        return DSProcessDefinitionRecord(
            id=record["id"],
            process_code=record["code"],
            name=record["name"],
            version=record["version"],
            description=record["description"],
            project_code=record["project_code"],
            release_state=DSReleaseState.from_db_value(record["release_state"]),
            user_id=record["user_id"],
            global_params=record["global_params"],
            flag=record["flag"],
            locations=create_ds_location_list_from_db_value(record["locations"]),
            warning_group_id=record["warning_group_id"],
            timeout=record["timeout"],
            tenant_id=record["tenant_id"],
            execution_type=DSProcessExecutionType.from_db_value(record["execution_type"]),
            create_time=record["create_time"],
            update_time=record["update_time"],
        )

"""
任务定义中的任务参数
"""

import abc
import dataclasses
import json

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.enum import DSTaskRelation

__all__ = [
    "DSTaskDefinitionParams",
    "DSTaskDefinitionConditionsParams",
    "DSTaskDefinitionShellParams",
]


@dataclasses.dataclass(slots=True)
class DSTaskDependence:
    """海豚任务定义的 task_params 字段中 dependence 属性的类型"""

    relation: DSTaskRelation = dataclasses.field(kw_only=True)

    def to_json(self) -> dict:
        return {
            "relation": self.relation.web_value,
            "dependTaskList": self.resource_list,
        }


# "dependTaskList":[{"relation":"AND","dependItemList":[{"projectCode":9653786894208,"definitionCode":16838989777920,"depTaskCode":0,"cycle":"day","dateValue":"today","state":null}]}]


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParams(ObjectBase, abc.ABC):
    """任务定义参数的抽象基类"""

    @staticmethod
    @abc.abstractmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParams":
        """根据 t_ds_task_definition 表记录的 task_params 字段值构造"""


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionConditionsParams(DSTaskDefinitionParams):
    """海豚 CONDITIONS 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)
    dependence: dict = dataclasses.field(kw_only=True, default_factory=lambda: {})

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionConditionsParams":
        data = json.loads(string)
        return DSTaskDefinitionConditionsParams(
            local_params=data["localParams"],
            resource_list=data["resourceList"],
            script_version=data["scriptVersion"],
            dependence=data["dependence"],
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "dependence": self.dependence
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionDependentParams(DSTaskDefinitionParams):
    """海豚 DEPENDENT 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)
    condition_result: str = dataclasses.field(kw_only=True)  # TODO 待替换为枚举值

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionConditionsParams":
        data = json.loads(string)
        return DSTaskDefinitionConditionsParams(
            local_params=data["localParams"],
            resource_list=data["resourceList"],
            script_version=data["scriptVersion"],
            dependence=data["dependence"],
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "customConfig": self.custom_config
        }

        # "dependence":{"relation":"AND","dependTaskList":[{"relation":"AND","dependItemList":[{"projectCode":9653786894208,"definitionCode":16838989777920,"depTaskCode":0,"cycle":"day","dateValue":"today","state":null}]}]}


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionShellParams(DSTaskDefinitionParams):
    """海豚 SHELL 类型任务的任务定义的参数"""

    raw_script: str = dataclasses.field(kw_only=True)
    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionShellParams":
        data = json.loads(string)
        return DSTaskDefinitionShellParams(
            raw_script=data["rawScript"],
            local_params=data["localParams"],
            resource_list=data["resourceList"],
            script_version=data["scriptVersion"],
        )

    def to_json(self) -> dict:
        return {
            "rawScript": self.raw_script,
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
        }

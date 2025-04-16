"""
创建工作流
"""

import dataclasses
import json
from typing import Dict, List

from dolphin_sdk.common import meta_list_to_json
from dolphin_sdk.form.process_task_relation_form import DSProcessTaskRelationForm
from dolphin_sdk.objects import DSLocation, DSTaskDefinitionRecord


@dataclasses.dataclass(slots=True)
class PostProcessDefinitionForm:
    task_definition_json: List[DSTaskDefinitionRecord] = dataclasses.field(kw_only=True)
    task_relation_json: List[DSProcessTaskRelationForm] = dataclasses.field(kw_only=True)
    locations: List[DSLocation] = dataclasses.field(kw_only=True)
    name: str = dataclasses.field(kw_only=True)

    tenant_code: str = dataclasses.field(kw_only=True, default="default")
    execution_type: str = dataclasses.field(kw_only=True, default="PARALLEL")
    description: str = dataclasses.field(kw_only=True, default="")
    globalParams: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    timeout: int = dataclasses.field(kw_only=True, default=0)

    def to_dict(self) -> Dict[str, str]:
        return {
            "taskDefinitionJson": meta_list_to_json(self.task_definition_json),
            "taskRelationJson": meta_list_to_json(self.task_relation_json),
            "locations": meta_list_to_json(self.locations),
            "name": self.name,
            "tenantCode": self.tenant_code,
            "executionType": self.execution_type,
            "description": self.description,
            "globalParams": json.dumps(self.globalParams, ensure_ascii=False),
            "timeout": str(self.timeout)
        }

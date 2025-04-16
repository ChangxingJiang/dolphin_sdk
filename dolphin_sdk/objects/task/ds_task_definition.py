"""
海豚调度任务定义节点
"""

import dataclasses
from typing import Optional

__all__ = [
    "DSTaskDefinition"
]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSTaskDefinition:
    """海豚调度任务定义节点"""

    # 项目编号
    project_code: int = dataclasses.field(kw_only=True)

    # 工作流编号（如果基于 t_ds_task_definition 则为空）
    process_code: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # 任务编号
    task_code: int = dataclasses.field(kw_only=True)

    def get_process_url(self, domain: str):
        """获取工作流定义的 Url"""
        return f"{domain}/dolphinscheduler/ui/projects/{self.project_code}/workflow/definitions/{self.process_code}"

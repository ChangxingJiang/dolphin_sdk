"""
海豚调度工作流定义节点
"""

import dataclasses

__all__ = [
    "DSProcessDefinition"
]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class DSProcessDefinition:
    """海豚调度工作流定义节点"""

    # 项目编号
    project_code: int = dataclasses.field(kw_only=True)

    # 工作流编号
    process_code: int = dataclasses.field(kw_only=True)

    def get_process_url(self, domain: str):
        """获取工作流定义的 Url"""
        return f"{domain}/dolphinscheduler/ui/projects/{self.project_code}/workflow/definitions/{self.process_code}"

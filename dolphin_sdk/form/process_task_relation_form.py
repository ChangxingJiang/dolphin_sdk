"""
海豚调度工作流、任务关系的表单
"""

import dataclasses

__all__ = [
    "DSProcessTaskRelationForm"
]


@dataclasses.dataclass(slots=True)
class DSProcessTaskRelationForm:
    """海豚调度工作流、任务关系的表单"""

    # relation name
    name: str = dataclasses.field(kw_only=True, default="")

    # pre task code
    pre_task_code: int = dataclasses.field(kw_only=True, default=0)

    # pre task version
    pre_task_version: int = dataclasses.field(kw_only=True, default=0)

    # post task code
    post_task_code: int = dataclasses.field(kw_only=True)

    # post task version
    post_task_version: int = dataclasses.field(kw_only=True, default=0)

    # condition type : 0 none, 1 judge 2 delay
    condition_type: str = dataclasses.field(kw_only=True, default="NONE")

    # condition params(json)
    condition_params: str = dataclasses.field(kw_only=True, default_factory=lambda: [])

    @staticmethod
    def create_single(task_code: int) -> "DSProcessTaskRelationForm":
        """根据 task_code 构造（没有前置任务关系，仅注册单个任务与工作流的关系）"""
        return DSProcessTaskRelationForm(
            post_task_code=task_code
        )

    @staticmethod
    def create_relation(pre_task_code: int, post_task_code: int) -> "DSProcessTaskRelationForm":
        """构造前置任务 pre_task_code 和任务 post_task_code 的关系"""
        return DSProcessTaskRelationForm(
            pre_task_code=pre_task_code,
            post_task_code=post_task_code
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

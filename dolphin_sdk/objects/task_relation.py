import dataclasses

from dolphin_sdk.objects.base import ObjectBase


@dataclasses.dataclass(slots=True)
class TaskRelation(ObjectBase):
    name: str = dataclasses.field(kw_only=True, default="")
    preTaskCode: int = dataclasses.field(kw_only=True, default=0)
    preTaskVersion: int = dataclasses.field(kw_only=True, default=0)
    postTaskCode: int = dataclasses.field(kw_only=True)
    postTaskVersion: int = dataclasses.field(kw_only=True, default=0)
    conditionType: str = dataclasses.field(kw_only=True, default="NONE")
    conditionParams: str = dataclasses.field(kw_only=True, default_factory=lambda: [])

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "preTaskCode": self.preTaskCode,
            "preTaskVersion": self.preTaskVersion,
            "postTaskCode": self.postTaskCode,
            "postTaskVersion": self.postTaskVersion,
            "conditionType": self.conditionType,
            "conditionParams": self.conditionParams,
        }

import abc

__all__ = [
    "ObjectBase"
]


class ObjectBase(abc.ABC):
    def to_json(self) -> dict:
        """"""

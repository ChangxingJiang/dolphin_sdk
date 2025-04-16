import json
from typing import List

from dolphin_sdk.objects.base import ObjectBase

__all__ = [
    "meta_list_to_json"
]


def meta_list_to_json(meta_list: List[ObjectBase]) -> str:
    return json.dumps([meta.to_json() for meta in meta_list], ensure_ascii=False)

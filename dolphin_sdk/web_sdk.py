"""
基于海豚调度 Web API 的 SDK
"""

from typing import List

import requests

from dolphin_sdk.form import PostProcessDefinitionForm
from dolphin_sdk.objects import DSReleaseState

__all__ = [
    "DolphinWebSdk",
    "DolphinApiError"
]


class DolphinApiError(Exception):
    """海豚 API 请求异常"""
    pass


class DolphinWebSdk:
    """基于海豚调度 Web API 的 SDK"""

    def __init__(self, base_url: str, token: str):
        self._base_url = base_url
        self._token = token

    # ------------------------------ SDK 属性 ------------------------------

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def token(self) -> str:
        return self._token

    # ------------------------------ 通用请求方法 ------------------------------

    def _do_get(self, url, params):
        """执行海豚调度的 GET 请求"""
        actual_url = f"{self._base_url}{url}"
        headers = {
            "Accept": "application/json",
            "token": self.token
        }
        return requests.get(actual_url, params=params, headers=headers).json()

    def _do_post(self, url, data):
        """执行海豚调度的 POST 请求"""
        actual_url = f"{self._base_url}{url}"
        headers = {
            "Accept": "application/json",
            "token": self.token
        }
        return requests.post(actual_url, data=data, headers=headers).json()

    def _do_put(self, url, data):
        """执行海豚调度的 PUT 请求"""
        actual_url = f"{self._base_url}{url}"
        headers = {
            "Accept": "application/json",
            "token": self.token
        }
        print(actual_url)
        print(data)
        response = requests.put(actual_url, data=data, headers=headers)
        if response.status_code != 200:
            raise DolphinApiError(f"status_code={response.status_code}, text={response.text}")
        return response.json()

    # ------------------------------ SDK 方法 ------------------------------

    def get_process_definition_verify_name(self, project_code: int, name: str) -> bool:
        """【get】验证工作流名称是否可用

        Parameters
        ----------
        project_code : int
            项目ID
        name : name
            工作流名称
        """
        url = f"/dolphinscheduler/projects/{project_code}/process-definition/verify-name"
        params = {"name": name}
        response = self._do_get(url, params)
        return response["code"] == 0

    def get_process_definition(self, project_code: int, process_code: int):
        """获取工作流定义

        Parameters
        ----------
        project_code : int
            项目ID
        process_code : int
            工作流ID
        """
        url = f"/dolphinscheduler/projects/{project_code}/process-definition/{process_code}"
        params = {}
        response = self._do_get(url, params)
        if response["code"] != 0:
            response_code = response["code"]
            raise DolphinApiError(f"url={url} params={params} code={response_code}")
        return response["data"]

    def get_task_definition_gen_task_codes(self, project_code: int, gen_num: int) -> List[int]:
        """生成新建 task 的 task_code

        Parameters
        ----------
        project_code : int
            项目ID
        gen_num : int
            生成数量
        """
        url = f"/dolphinscheduler/projects/{project_code}/task-definition/gen-task-codes"
        params = {"genNum": gen_num}
        response = self._do_get(url, params)
        if response["code"] != 0:
            response_code = response["code"]
            raise DolphinApiError(f"url={url} params={params} code={response_code}")
        return response["data"]

    def post_process_definition(self, project_code: int, data: PostProcessDefinitionForm) -> dict:
        """提交一个新的工作流"""
        url = f"/dolphinscheduler/projects/{project_code}/process-definition"
        data_dict = data.to_dict()
        response = self._do_post(url, data_dict)
        return response

    def put_process_definition(self, project_code: int, process_code: int, data: PostProcessDefinitionForm) -> dict:
        """更新一个工作流"""
        url = f"/dolphinscheduler/projects/{project_code}/process-definition/{process_code}"
        response = self._do_put(url, data.to_dict())
        return response

    def post_process_definition_release(self, project_code: int,
                                        process_code: int,
                                        process_name: str,
                                        release_state: DSReleaseState) -> bool:
        """上线 / 下线工作流"""
        url = f"/dolphinscheduler/projects/{project_code}/process-definition/{process_code}/release"
        response = self._do_post(url, {
            "name": process_name,
            "releaseState": release_state.web_value
        })
        return response["code"] == 0

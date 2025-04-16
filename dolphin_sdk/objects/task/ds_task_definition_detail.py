"""
海豚调度任务定义详情节点
"""

import dataclasses
import datetime
from typing import Any, Dict, Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.enum import DSPriority
from dolphin_sdk.objects.enum import DSTaskExecuteType
from dolphin_sdk.objects.enum import DSAvailableFlag
from dolphin_sdk.objects.enum import DSTimeoutFlag
from dolphin_sdk.objects.task_params import DSTaskDefinitionConditionsParams
from dolphin_sdk.objects.task_params import DSTaskDefinitionParams
from dolphin_sdk.objects.task_params import DSTaskDefinitionShellParams

__all__ = [
    "DSTaskDefinitionDetail"
]


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionDetail(ObjectBase):
    """海豚调度任务定义详情节点

    除 task_code 和 process_code 外，该类的属性与 t_ds_task_definition 表中的字段一一对应：

    - task_code 属性对应 t_ds_task_definition 表中的 code 字段
    - process_code 属性在 t_ds_task_definition 表中没有对应字段

    用途：
    1. 作为海豚调度任务定义表查询结果的返回值
    2. 用于构造海豚调度任务定义表的插入逻辑
    """

    # self-increasing id（在构造时不需要）
    id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # encoding
    task_code: int = dataclasses.field(kw_only=True)

    # 工作流编号（如果基于 t_ds_task_definition 构造则为空）
    process_code: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # task definition name
    name: str = dataclasses.field(kw_only=True)

    # task definition version（在构造时不需要）
    version: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # description
    description: str = dataclasses.field(kw_only=True, default="")

    # project code（在构造时不需要）
    project_code: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # task definition creator id（在构造时不需要）
    user_id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # task type
    task_type: str = dataclasses.field(kw_only=True)

    # task execute type: 0-batch, 1-stream（在构造时使用字符串）
    task_execute_type: DSTaskExecuteType = dataclasses.field(kw_only=True, default=DSTaskExecuteType.BATCH)

    # job custom parameters
    task_params: DSTaskDefinitionParams = dataclasses.field(kw_only=True)

    # 0 not available 1 available（在构造时使用字符串）
    flag: DSAvailableFlag = dataclasses.field(kw_only=True, default=DSAvailableFlag.AVAILABLE)

    # job priority（在构造时使用字符串）
    task_priority: DSPriority = dataclasses.field(kw_only=True, default=DSPriority.MEDIUM)

    # worker grouping
    worker_group: str = dataclasses.field(kw_only=True)

    # environment code
    environment_code: int = dataclasses.field(kw_only=True)

    # number of failed retries
    fail_retry_times: int = dataclasses.field(kw_only=True, default=0)

    # failed retry interval
    fail_retry_interval: int = dataclasses.field(kw_only=True, default=1)

    # timeout flag: 0-close, 1-open（在构造时使用字符串） TODO 需要增加映射表
    timeout_flag: DSTimeoutFlag = dataclasses.field(kw_only=True, default=DSTimeoutFlag.CLOSE)

    # timeout notification policy: 0-warning, 1-fail
    timeout_notify_strategy: Optional[str] = dataclasses.field(kw_only=True, default=None)

    # timeout length, unit: minute
    timeout: int = dataclasses.field(kw_only=True, default=0)

    # delay execution time, unit: minute
    delay_time: int = dataclasses.field(kw_only=True, default=0)

    # resource id, separated by comma（在构造时不需要）
    resource_ids: Optional[str] = dataclasses.field(kw_only=True, default=None)

    # task group id（在构造时不需要）
    task_group_id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # task group priority（在构造时不需要）
    task_group_priority: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # cpuQuota(%): -1 = infinity
    cpu_quota: int = dataclasses.field(kw_only=True, default=-1)

    # memory max(MB): -1 = infinity
    memory_max: int = dataclasses.field(kw_only=True, default=-1)

    # create time（在构造时不需要）
    create_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    # update time（在构造时不需要）
    update_time: Optional[datetime.datetime] = dataclasses.field(kw_only=True, default=None)

    def to_json(self) -> dict:
        return {
            "code": self.task_code,
            "name": self.name,
            "taskType": self.task_type,
            "environmentCode": self.environment_code,
            "taskParams": self.task_params.to_json(),
            "delayTime": str(self.delay_time),
            "description": self.description,
            "failRetryInterval": str(self.fail_retry_interval),
            "failRetryTimes": str(self.fail_retry_times),
            "flag": self.flag.web_value,
            "timeout": self.timeout,
            "taskPriority": self.task_priority.web_value,
            "timeoutFlag": self.timeout_flag.web_value,
            "timeoutNotifyStrategy": self.timeout_notify_strategy,
            "workerGroup": self.worker_group,
            "cpuQuota": self.cpu_quota,
            "memoryMax": self.memory_max,
            "taskExecuteType": self.task_execute_type.web_value,
        }

    @staticmethod
    def from_t_ds_task_definition_record(record: Dict[str, Any]) -> "DSTaskDefinitionDetail":
        task_type = record["task_type"]
        if task_type == "CONDITIONS":
            task_params = DSTaskDefinitionShellParams.from_t_ds_task_definition_record(record["task_params"])
        elif task_type == "SHELL":
            task_params = DSTaskDefinitionConditionsParams.from_t_ds_task_definition_record(record["task_params"])
        else:
            print(f"暂未定义的海豚任务类型: {task_type}")
            task_params = None

        return DSTaskDefinitionDetail(
            id=record["id"],
            task_code=record["code"],
            name=record["name"],
            version=record["version"],
            description=record["description"],
            project_code=record["project_code"],
            user_id=record["user_id"],
            task_type=task_type,
            task_execute_type=DSTaskExecuteType.from_db_value(record["task_execute_type"]),
            task_params=task_params,
            flag=DSAvailableFlag.from_db_value(record["flag"]),
            task_priority=DSPriority.from_db_value(record["task_priority"]),
            worker_group=record["worker_group"],
            environment_code=record["environment_code"],
            fail_retry_times=record["fail_retry_times"],
            fail_retry_interval=record["fail_retry_interval"],
            timeout_flag=DSTimeoutFlag.from_db_value(record["timeout_flag"]),
            timeout_notify_strategy=record["timeout_notify_strategy"],
            timeout=record["timeout"],
            delay_time=record["delay_time"],
            resource_ids=record["resource_ids"],
            task_group_id=record["task_group_id"],
            task_group_priority=record["task_group_priority"],
            cpu_quota=record["cpu_quota"],
            memory_max=record["memory_max"],
            create_time=record["create_time"],
            update_time=record["update_time"],
        )

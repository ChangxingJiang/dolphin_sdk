"""
启动海豚工作流实例
"""

import dataclasses
import json
from typing import Dict, Optional

from dolphin_sdk.objects import DSComplementDependentMode
from dolphin_sdk.objects import DSComplementTimeRange
from dolphin_sdk.objects import DSFailureStrategy
from dolphin_sdk.objects import DSPriority
from dolphin_sdk.objects import DSRunMode
from dolphin_sdk.objects import DSWarningType

__all__ = [
    "DSStartProcessInstanceForm"
]


@dataclasses.dataclass(slots=True)
class DSStartProcessInstanceForm:
    """启动海豚工作流实例的接口表单"""

    process_code: int = dataclasses.field(kw_only=True)

    # 失败策略
    failure_strategy: DSFailureStrategy = dataclasses.field(kw_only=True, default=DSFailureStrategy.CONTINUE)

    # 通知策略
    warning_type: DSWarningType = dataclasses.field(kw_only=True, default=DSWarningType.NONE)

    # 告警组
    warning_group_id: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # 补数的依赖模式：关闭（默认） & 打开
    complement_dependent_mode: DSComplementDependentMode = dataclasses.field(kw_only=True,
                                                                             default=DSComplementDependentMode.OFF_MODE)

    # 补数的执行方式：串行执行（默认） & 并行执行
    run_mode: DSRunMode = dataclasses.field(kw_only=True, default=DSRunMode.RUN_MODE_SERIAL)

    # 流程优先级
    process_instance_priority: DSPriority = dataclasses.field(kw_only=True, default=DSPriority.MEDIUM)

    # Worker 分组
    worker_group: str = dataclasses.field(kw_only=True)

    # 环境名称
    environment_code: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # 启动参数
    start_params: Optional[Dict[str, str]] = dataclasses.field(kw_only=True, default=None)

    # 使用并行执行方式补数时的并发度
    expected_parallelism_number: Optional[int] = dataclasses.field(kw_only=True, default=None)

    # 是否空跑
    dry_run: bool = dataclasses.field(kw_only=True, default=False)

    # 补跑调度时间
    schedule_time: DSComplementTimeRange = dataclasses.field(kw_only=True)

    @staticmethod
    def create_as_default(process_code: int, worker_group: str) -> "DSStartProcessInstanceForm":
        """根据默认值创建"""
        return DSStartProcessInstanceForm(
            process_code=process_code,
            worker_group=worker_group,
            schedule_time=DSComplementTimeRange.create_as_default()
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "processDefinitionCode": str(self.process_code),
            "failureStrategy": self.failure_strategy.web_value,
            "warningType": self.warning_type.web_value,
            "warningGroupId": str(self.warning_group_id) if self.warning_group_id is not None else "",
            "execType": "START_PROCESS",
            "startNodeList": "",
            "taskDependType": "TASK_POST",
            "complementDependentMode": self.complement_dependent_mode.web_value,
            "runMode": self.run_mode.web_value,
            "processInstancePriority": self.process_instance_priority.web_value,
            "workerGroup": self.worker_group,
            "environmentCode": str(self.environment_code) if self.environment_code is not None else "",
            "startParams": json.dumps(self.start_params, ensure_ascii=False) if self.start_params is not None else "",
            "expectedParallelismNumber": (str(self.expected_parallelism_number)
                                          if self.expected_parallelism_number is not None else ""),
            "dryRun": "1" if self.dry_run is True else "0",
            "scheduleTime": json.dumps(self.schedule_time.to_json(), ensure_ascii=False),
        }

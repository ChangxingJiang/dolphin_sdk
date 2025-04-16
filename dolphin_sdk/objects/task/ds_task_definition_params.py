"""
任务定义中的任务参数
"""

import abc
import dataclasses
import json
from typing import Any, List, Optional

from dolphin_sdk.objects.base import ObjectBase
from dolphin_sdk.objects.common import DSDependence

__all__ = [
    "DSTaskDefinitionParams",
    "DSTaskDefinitionParamsConditions",
    "DSTaskDefinitionParamsShell",
    "DSTaskDefinitionParamsDependent",
    "DSTaskDefinitionParamsSpark",
    "DSTaskDefinitionParamsSql",
    "DSTaskDefinitionParamsFlink",
]


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParams(ObjectBase, abc.ABC):
    """任务定义参数的抽象基类"""

    @staticmethod
    @abc.abstractmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParams":
        """根据 t_ds_task_definition 表记录的 task_params 字段值构造"""


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsConditions(DSTaskDefinitionParams):
    """海豚 CONDITIONS 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)
    dependence: dict = dataclasses.field(kw_only=True, default_factory=lambda: {})

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsConditions":
        data = json.loads(string)
        return DSTaskDefinitionParamsConditions(
            local_params=data["localParams"],
            resource_list=data["resourceList"],
            script_version=data["scriptVersion"],
            dependence=data["dependence"],
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "dependence": self.dependence
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsDependent(DSTaskDefinitionParams):
    """海豚 DEPENDENT 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)
    dependence: DSDependence = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by_one_daily_dependent(project_code: int, process_code: int):
        """构造单工作流单日依赖"""
        return DSTaskDefinitionParamsDependent(
            local_params=[],
            resource_list=[],
            script_version=0,
            dependence=DSDependence.create_by_one_daily_dependent(project_code, process_code),
        )

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsDependent":
        data = json.loads(string)
        return DSTaskDefinitionParamsDependent(
            local_params=data.get("localParams"),
            resource_list=data.get("resourceList"),
            script_version=data.get("scriptVersion"),
            dependence=DSDependence.from_db_json(data["dependence"]),
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "dependence": self.dependence.to_json()
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsShell(DSTaskDefinitionParams):
    """海豚 SHELL 类型任务的任务定义的参数"""

    raw_script: str = dataclasses.field(kw_only=True)
    local_params: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    resource_list: list = dataclasses.field(kw_only=True, default_factory=lambda: [])
    script_version: int = dataclasses.field(kw_only=True, default=0)

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsShell":
        data = json.loads(string)
        return DSTaskDefinitionParamsShell(
            raw_script=data["rawScript"],
            local_params=data["localParams"],
            resource_list=data["resourceList"],
            script_version=data.get("scriptVersion"),
        )

    def to_json(self) -> dict:
        return {
            "rawScript": self.raw_script,
            "localParams": self.local_params,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsSpark(DSTaskDefinitionParams):
    """海豚 SPARK 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True)
    raw_script: str = dataclasses.field(kw_only=True)
    resource_list: list = dataclasses.field(kw_only=True)
    script_version: int = dataclasses.field(kw_only=True)
    program_type: str = dataclasses.field(kw_only=True)
    main_class: str = dataclasses.field(kw_only=True)
    deploy_mode: str = dataclasses.field(kw_only=True)
    app_name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    main_args: Optional[str] = dataclasses.field(kw_only=True, default=None)
    others: Optional[Any] = dataclasses.field(kw_only=True, default=None)  # TODO 待补充
    spark_version: str = dataclasses.field(kw_only=True)
    driver_cores: int = dataclasses.field(kw_only=True)
    driver_memory: str = dataclasses.field(kw_only=True)
    num_executors: int = dataclasses.field(kw_only=True)
    executor_memory: str = dataclasses.field(kw_only=True)
    executor_cores: int = dataclasses.field(kw_only=True)
    var_pool: Optional[Any] = dataclasses.field(kw_only=True, default=None)  # TODO 待补充
    main_jar: Optional[dict] = dataclasses.field(kw_only=True, default=None)

    @staticmethod
    def create_as_script(raw_script: str,
                         local_params: Optional[list] = None,
                         resource_list: Optional[list] = None,
                         deploy_mode: str = "local",
                         spark_version: str = "SPARK2"):
        """创建程序类型为 SCRIPT 类型新的 Spark 任务的参数对象"""
        if local_params is None:
            local_params = []
        if resource_list is None:
            resource_list = []
        return DSTaskDefinitionParamsSpark(
            local_params=[],
            raw_script=raw_script,
            resource_list=resource_list,
            script_version=0,
            program_type="SCRIPT",
            main_class="",
            deploy_mode=deploy_mode,
            spark_version=spark_version,
            driver_cores=1,  # 不生效
            driver_memory="512M",  # 不生效
            num_executors=2,  # 不生效
            executor_memory="2G",  # 不生效
            executor_cores=2,  # 不生效
        )

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsSpark":
        data = json.loads(string)
        return DSTaskDefinitionParamsSpark(
            local_params=data["localParams"],
            raw_script=data["rawScript"],
            resource_list=data["resourceList"],
            script_version=data.get("scriptVersion"),
            program_type=data.get("programType"),
            main_class=data.get("mainClass"),
            deploy_mode=data.get("deployMode"),
            app_name=data.get("appName"),
            main_args=data.get("mainArgs"),
            others=data.get("others"),
            spark_version=data.get("sparkVersion"),
            driver_cores=data.get("driverCores"),
            driver_memory=data.get("driverMemory"),
            num_executors=data.get("numExecutors"),
            executor_memory=data.get("executorMemory"),
            executor_cores=data.get("executorCores"),
            var_pool=data.get("varPool"),
            main_jar=data.get("mainJar"),
        )

    def to_json(self) -> dict:
        """生成 web 的 Json 格式"""
        if self.program_type == "SCRIPT":
            return {
                "localParams": self.local_params,
                "rawScript": self.raw_script,
                "resourceList": self.resource_list,
                "scriptVersion": self.script_version,
                "programType": self.program_type,
                "mainClass": self.main_class,
                "deployMode": self.deploy_mode,
                "sparkVersion": self.spark_version,
                "driverCores": self.driver_cores,
                "driverMemory": self.driver_memory,
                "numExecutors": self.num_executors,
                "executorMemory": self.executor_memory,
                "executorCores": self.executor_cores,
            }
        return {
            "localParams": self.local_params,
            "rawScript": self.raw_script,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "programType": self.program_type,
            "mainClass": self.main_class,
            "deployMode": self.deploy_mode,
            "appName": self.app_name,
            "mainArgs": self.main_args,
            "others": self.others,
            "sparkVersion": self.spark_version,
            "driverCores": self.driver_cores,
            "driverMemory": self.driver_memory,
            "numExecutors": self.num_executors,
            "executorMemory": self.executor_memory,
            "executorCores": self.executor_cores,
            "varPool": self.var_pool,
            "mainJar": self.main_jar,
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsSql(DSTaskDefinitionParams):
    """海豚 SQL 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True)
    var_pool: Optional[Any] = dataclasses.field(kw_only=True)  # TODO 待补充
    type: str = dataclasses.field(kw_only=True)
    data_source: str = dataclasses.field(kw_only=True)
    sql: str = dataclasses.field(kw_only=True)
    sql_type: int = dataclasses.field(kw_only=True)
    send_email: Optional[Any] = dataclasses.field(kw_only=True)  # TODO 待补充
    display_rows: int = dataclasses.field(kw_only=True)
    udfs: str = dataclasses.field(kw_only=True)
    show_type: Optional[Any] = dataclasses.field(kw_only=True)  # TODO 待补充
    conn_params: Optional[Any] = dataclasses.field(kw_only=True)  # TODO 待补充
    pre_statements: List[str] = dataclasses.field(kw_only=True)
    post_statements: List[str] = dataclasses.field(kw_only=True)
    group_id: int = dataclasses.field(kw_only=True)
    title: Optional[str] = dataclasses.field(kw_only=True)
    limit: int = dataclasses.field(kw_only=True)
    segment_separator: str = dataclasses.field(kw_only=True)
    script_version: int = dataclasses.field(kw_only=True)

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsSql":
        data = json.loads(string)
        return DSTaskDefinitionParamsSql(
            local_params=data["localParams"],
            var_pool=data.get("varPool"),
            type=data["type"],
            data_source=data["datasource"],
            sql=data["sql"],
            sql_type=data["sqlType"],
            send_email=data.get("sendEmail"),
            display_rows=data.get("displayRows"),
            udfs=data.get("udfs"),
            show_type=data.get("showType"),
            conn_params=data.get("connParams"),
            pre_statements=data.get("preStatements"),
            post_statements=data.get("postStatements"),
            group_id=data.get("groupId"),
            title=data.get("title"),
            limit=data.get("limit"),
            segment_separator=data.get("segmentSeparator"),
            script_version=data.get("scriptVersion")
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "varPool": self.var_pool,
            "type": self.type,
            "datasource": self.data_source,
            "sql": self.sql,
            "sqlType": self.sql_type,
            "sendEmail": self.send_email,
            "displayRows": self.display_rows,
            "udfs": self.udfs,
            "showType": self.show_type,
            "connParams": self.conn_params,
            "preStatements": self.pre_statements,
            "postStatements": self.post_statements,
            "groupId": self.group_id,
            "title": self.title,
            "limit": self.limit,
            "segmentSeparator": self.segment_separator,
            "scriptVersion": self.script_version
        }


@dataclasses.dataclass(slots=True)
class DSTaskDefinitionParamsFlink(DSTaskDefinitionParams):
    """海豚 FLINK 类型任务的任务定义的参数"""

    local_params: list = dataclasses.field(kw_only=True)
    init_script: str = dataclasses.field(kw_only=True)
    raw_script: str = dataclasses.field(kw_only=True)
    resource_list: list = dataclasses.field(kw_only=True)
    script_version: int = dataclasses.field(kw_only=True)
    program_type: str = dataclasses.field(kw_only=True)
    main_class: str = dataclasses.field(kw_only=True)
    main_jar: Optional[dict] = dataclasses.field(kw_only=True)
    deploy_mode: str = dataclasses.field(kw_only=True)
    app_name: str = dataclasses.field(kw_only=True)
    main_args: Optional[str] = dataclasses.field(kw_only=True)
    others: str = dataclasses.field(kw_only=True)
    flink_version: str = dataclasses.field(kw_only=True)
    job_manager_memory: str = dataclasses.field(kw_only=True)
    task_manager_memory: str = dataclasses.field(kw_only=True)
    slot: int = dataclasses.field(kw_only=True)
    task_manager: int = dataclasses.field(kw_only=True)
    parallelism: int = dataclasses.field(kw_only=True)

    @staticmethod
    def from_t_ds_task_definition_record(string: str) -> "DSTaskDefinitionParamsFlink":
        data = json.loads(string)
        return DSTaskDefinitionParamsFlink(
            local_params=data.get("localParams"),
            init_script=data.get("initScript"),
            raw_script=data.get("rawScript"),
            resource_list=data.get("resourceList"),
            script_version=data.get("scriptVersion"),
            program_type=data.get("programType"),
            main_class=data.get("mainClass"),
            main_jar=data.get("mainJar"),
            deploy_mode=data.get("deployMode"),
            app_name=data.get("appName"),
            main_args=data.get("mainArgs"),
            others=data.get("others"),
            flink_version=data.get("flinkVersion"),
            job_manager_memory=data.get("jobManagerMemory"),
            task_manager_memory=data.get("taskManagerMemory"),
            slot=data.get("slot"),
            task_manager=data.get("taskManager"),
            parallelism=data.get("parallelism")
        )

    def to_json(self) -> dict:
        return {
            "localParams": self.local_params,
            "initScript": self.init_script,
            "rawScript": self.raw_script,
            "resourceList": self.resource_list,
            "scriptVersion": self.script_version,
            "programType": self.program_type,
            "mainClass": self.main_class,
            "mainJar": self.main_jar,
            "deployMode": self.deploy_mode,
            "appName": self.app_name,
            "mainArgs": self.main_args,
            "others": self.others,
            "flinkVersion": self.flink_version,
            "jobManagerMemory": self.job_manager_memory,
            "taskManagerMemory": self.task_manager_memory,
            "slot": self.slot,
            "taskManager": self.task_manager,
            "parallelism": self.parallelism
        }

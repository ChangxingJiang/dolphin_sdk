"""
基于海豚调度元数据的 SDK
"""

import collections
from typing import Dict, Generator, List

import metasequoia_connector as ms_conn
from dolphin_sdk.objects import DSProcessDefinition
from dolphin_sdk.objects import DSProcessDefinitionRecord
from dolphin_sdk.objects import DSProcessTaskRelationRecord
from dolphin_sdk.objects import DSProjectRecord
from dolphin_sdk.objects import DSScheduleRecord
from dolphin_sdk.objects import DSTaskDefinition
from dolphin_sdk.objects import DSTaskDefinitionRecord
from dolphin_sdk.objects import DSTaskDefinitionRecordDependent

__all__ = [
    "DolphinMetaSdk"
]


class DolphinMetaSdk:
    """基于海豚调度元数据的 SDK"""

    def __init__(self, manager: ms_conn.ConnectManager, mysql_name: str, db_name: str):
        """

        Parameters
        ----------
        manager : ms_conn.ConnectManager
            连接海豚调度元数据的连接管理器
        mysql_name : str
            海豚调度元数据所在的 MySQL 实例名称
        db_name : str
            海豚调度元数据所在的数据库名称
        """
        self._manager = manager
        self._mysql_name = mysql_name
        self._db_name = db_name

    # ----------------------------------------------------------------------
    # ------------------------------ 项目级方法 ------------------------------
    # ----------------------------------------------------------------------

    def get_all_project_list(self) -> List[DSProjectRecord]:
        """返回海豚调度中所有项目的 DSProjectRecord 对象的列表"""
        project_list = []
        for query_row in self._select_all_as_dict("SELECT * FROM t_ds_project"):
            project_list.append(DSProjectRecord.from_record_dict(query_row))
        return project_list

    # ----------------------------------------------------------------------
    # ----------------------------- 工作流级方法 -----------------------------
    # ----------------------------------------------------------------------

    def get_process_definition_by_id(self, row_id: int) -> DSProcessDefinition:
        """根据 t_ds_process_definition 表主键 row_id 构造工作流定义对象"""
        sql = f"SELECT project_code, code FROM t_ds_process_definition WHERE id = '{row_id}'"
        query_row = self._select_one_as_dict(sql)
        return DSProcessDefinition(project_code=query_row["project_code"], process_code=query_row["code"])

    def get_depend_process_definition_list_by_process_definition_list(
            self,
            process_definition_list: List[DSProcessDefinition],
            include: bool = True
    ) -> List[DSProcessDefinition]:
        """根据工作流定义的列表，获取其依赖的上游工作流定义的列表

        Parameters
        ----------
        process_definition_list : List[DSProcessDefinition]
            工作流定义的列表
        include : bool, default = True
            返回列表中是否包含当前工作流定义
        """
        visited = set(process_definition_list)
        queue = list(process_definition_list)
        while queue:
            new_queue = []

            # 按项目分析工作流
            for project_code, grouped_process_definition_list in self._grouped_process_by_project(queue).items():

                # 获取工作流定义的列表，获取其中包含的任务定义的列表（任务定义中包含工作流编号）
                task_definition_list = self.get_task_definition_list_by_process_definition_list(
                    process_definition_list=grouped_process_definition_list
                )

                # 根据任务定义的列表，获取任务定义的详细信息的列表
                task_definition_detail_list = self.get_task_definition_detail_list_by_task_definition_list(
                    task_definition_list=task_definition_list
                )

                # 遍历所有 task_params 字段，并将其中依赖的上游任务添加到新队列中
                for task_definition in task_definition_detail_list:
                    if not isinstance(task_definition, DSTaskDefinitionRecordDependent):
                        continue
                    for depend_task in task_definition.task_params.dependence.depend_task_list:
                        for depend_item in depend_task.depend_item_list:
                            dependence_process = DSProcessDefinition(
                                project_code=depend_item.project_code,
                                process_code=depend_item.definition_code
                            )
                            if dependence_process not in visited:
                                visited.add(dependence_process)
                                new_queue.append(dependence_process)
            queue = new_queue

        if include is False:
            visited -= set(process_definition_list)

        return list(visited)

    def get_process_definition_detail_list_by_project_code(
            self,
            project_code: int
    ) -> List[DSProcessDefinitionRecord]:
        """根据工作流定义的列表，获取工作流定义的详细信息的列表"""
        result = []
        for query_row in self._select_iter_as_dict(
                f"SELECT * FROM t_ds_process_definition WHERE project_code = '{project_code}'",
                primary_key="id"
        ):
            result.append(DSProcessDefinitionRecord.from_t_ds_process_definition_record(query_row))
        return result

    def get_process_definition_detail_list_by_process_definition_list(
            self,
            process_definition_list: List[DSProcessDefinition],
            batch_size: int = 100
    ) -> List[DSProcessDefinitionRecord]:
        """根据工作流定义的列表，获取工作流定义的详细信息的列表"""
        result = []
        for i in range(0, len(process_definition_list), batch_size):
            end_i = min(i + batch_size, len(process_definition_list))
            sub_task_definition_code_list = ms_conn.sql_format.to_quote_str_list_none_as_ignore([
                task.process_code for task in process_definition_list[i: end_i]
            ])
            for query_row in self._select_all_as_dict(
                    f"SELECT * "
                    f"FROM t_ds_process_definition "
                    f"WHERE `code` IN {sub_task_definition_code_list}"
            ):
                process_definition_detail = DSProcessDefinitionRecord.from_t_ds_process_definition_record(query_row)
                result.append(process_definition_detail)
        return result

    def get_task_definition_list_by_process_definition_list(
            self,
            process_definition_list: List[DSProcessDefinition],
            batch_size: int = 100
    ) -> List[DSTaskDefinition]:
        """获取工作流定义的列表，获取其中包含的任务定义的列表（任务定义中包含工作流编号）"""
        result = []
        for i in range(0, len(process_definition_list), batch_size):
            sub_process_definition_code_list = ms_conn.sql_format.to_quote_str_list_none_as_ignore([
                process.process_code
                for process in process_definition_list[i:min(i + batch_size, len(process_definition_list))]
            ])
            for query_row in self._select_all_as_dict(
                    f"SELECT `project_code`, `process_definition_code`, `post_task_code` "
                    f"FROM t_ds_process_task_relation "
                    f"WHERE `process_definition_code` IN {sub_process_definition_code_list}"
            ):
                result.append(DSTaskDefinition(
                    project_code=query_row["project_code"],
                    task_code=query_row["post_task_code"],
                    process_code=query_row["process_definition_code"]
                ))
        return list(set(result))  # 当同一个任务包含多个上游任务时，会出现重复的任务定义，因此需要去重

    def get_task_definition_detail_list_by_task_definition_list(
            self,
            task_definition_list: List[DSTaskDefinition],
            batch_size: int = 100
    ) -> List[DSTaskDefinitionRecord]:
        """根据任务定义的列表，获取任务定义的详细信息的列表"""
        task_code_to_process_code_hash = {task.task_code: task.process_code for task in task_definition_list}
        result = []
        for i in range(0, len(task_definition_list), batch_size):
            sub_task_definition_code_list = ms_conn.sql_format.to_quote_str_list_none_as_ignore([
                task.task_code for task in task_definition_list[i: min(i + batch_size, len(task_definition_list))]
            ])
            for query_row in self._select_all_as_dict(
                    f"SELECT * "
                    f"FROM t_ds_task_definition "
                    f"WHERE `code` IN {sub_task_definition_code_list}"
            ):
                task_definition_detail = DSTaskDefinitionRecord.from_t_ds_task_definition_record(
                    query_row,
                    process_code=task_code_to_process_code_hash[query_row["code"]]
                )
                result.append(task_definition_detail)
        return result

    def get_all_task_definition_detail_list(
            self,
    ) -> Generator[DSTaskDefinitionRecord, None, None]:
        """读取 t_ds_process_task_relation 表中所有记录"""
        for query_row in self._select_iter_as_dict("SELECT * FROM t_ds_task_definition", primary_key="id"):
            yield DSTaskDefinitionRecord.from_t_ds_task_definition_record(query_row)

    def get_schedule_record_list_by_process_definition_list(
            self,
            process_definition_list: List[DSProcessDefinition],
            batch_size: int = 100
    ) -> List[DSScheduleRecord]:
        """获取当前工作流集合的定时上线状态"""
        result = []
        for i in range(0, len(process_definition_list), batch_size):
            sub_process_code_list = ms_conn.sql_format.to_quote_str_list_none_as_ignore([
                process_definition.process_code
                for process_definition in process_definition_list[i: min(i + batch_size, len(process_definition_list))]
            ])
            for query_row in self._select_all_as_dict(
                    f"SELECT * "
                    f"FROM `t_ds_schedules` "
                    f"WHERE `process_definition_code` IN {sub_process_code_list}"
            ):
                task_definition_detail = DSScheduleRecord.from_t_ds_schedules_record(query_row)
                result.append(task_definition_detail)
        return result

    def get_all_process_task_relation_list(
            self,
    ) -> Generator[DSProcessTaskRelationRecord, None, None]:
        """读取 t_ds_process_task_relation 表中所有记录"""
        for query_row in self._select_iter_as_dict("SELECT * FROM t_ds_process_task_relation", primary_key="id"):
            yield DSProcessTaskRelationRecord.from_t_ds_process_task_relation_record(query_row)

    @staticmethod
    def _grouped_process_by_project(process_list: List[DSProcessDefinition]) -> Dict[int, List[DSProcessDefinition]]:
        """按所属项目对工作流定义进行分组"""
        grouped_process_dict = collections.defaultdict(list)
        for process in process_list:
            grouped_process_dict[process.project_code].append(process)
        return grouped_process_dict

    def _select_one_as_dict(self, sql: str):
        return ms_conn.mysql.select_one_as_dict(
            manager=self._manager, mysql_name=self._mysql_name, db_name=self._db_name,
            sql=sql
        )

    def _select_all_as_dict(self, sql: str):
        return ms_conn.mysql.select_all_as_dict(
            manager=self._manager, mysql_name=self._mysql_name, db_name=self._db_name,
            sql=sql
        )

    def _select_iter_as_dict(self, sql: str, primary_key: str):
        yield from ms_conn.mysql.select_iter_as_dict(
            manager=self._manager, mysql_name=self._mysql_name, db_name=self._db_name,
            sql=sql, primary_key=primary_key
        )

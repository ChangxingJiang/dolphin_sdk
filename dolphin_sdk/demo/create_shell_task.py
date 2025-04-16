from dolphin_sdk.form import DSProcessTaskRelationForm
from dolphin_sdk.form import PostProcessDefinitionForm
from dolphin_sdk.objects import DSLocation, DSTaskDefinitionParamsShell, DSTaskDefinitionRecordShell
from dolphin_sdk.web_sdk import DolphinWebSdk


def create_process_with_one_shell_task(sdk: DolphinWebSdk,
                                       project_code: int,
                                       task_name: str,
                                       process_name: str,
                                       worker_group: str,
                                       environment_code: int,
                                       shell_script: str,
                                       process_description: str = ""):
    """创建仅包含一个 Shell 任务的工作流，返回创建的工作流 ID"""

    # 获取任务 ID
    task_code_list = sdk.get_task_definition_gen_task_codes(project_code=project_code, gen_num=1)
    task_code = task_code_list[0]

    # 构造任务定义
    task_definition = DSTaskDefinitionRecordShell(
        project_code=project_code,
        task_code=task_code,
        name=task_name,
        environment_code=environment_code,
        task_params=DSTaskDefinitionParamsShell(
            raw_script=shell_script
        ),
        worker_group=worker_group,
        fail_retry_times=3,
        fail_retry_interval=10
    )

    # 构造任务关联定义
    task_relation = DSProcessTaskRelationForm(
        post_task_code=task_code
    )

    # 构造任务位置
    location = DSLocation(
        task_code=task_code,
        x=100.0,
        y=100.0
    )

    form_data = PostProcessDefinitionForm(
        task_definition_json=[task_definition],
        task_relation_json=[task_relation],
        locations=[location],
        name=process_name,
        description=process_description
    )

    if sdk.get_process_definition_verify_name(project_code, process_name) is False:
        raise KeyError("工作流名称不合法")

    response_json = sdk.post_process_definition(
        project_code=project_code,
        data=form_data
    )

    print(response_json)
    return response_json["data"]["code"]

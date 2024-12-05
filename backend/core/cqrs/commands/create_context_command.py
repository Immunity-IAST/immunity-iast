"""
Команда для обработки контекста выполнения запроса, присылаемого агентом.
"""

import base64
from datetime import datetime
from django.db import transaction
from celery import shared_task
from core.models import Application, Context, Event, Request, Response
from core.result import Result


class CreateContextCommand:
    """
    Команда для обработки контекста выполнения запроса, присылаемого агентом.
    """

    def __init__(
        self, project_id, request_base_64, control_flow_base_64, response_base_64
    ):
        """
        Конструктор команды.
        :param project_id: id анализируемого приложения.
        :param context_base_64: контекст выполнения запроса в формате base64.
        """
        self.project_id = project_id
        self.request_base_64 = request_base_64
        self.control_flow_base_64 = control_flow_base_64
        self.response_base_64 = response_base_64

    def _handle_request(self, context, json_request):
        """
        Создание объекта запроса в базе данных.
        :param context: объект контекста выполнения запроса.
        :param json_request: данные о запросе в формате json.
        :return: None.
        """
        Request.objects.create(
            context=context,
            method=json_request["method"],
            path=json_request["path"],
            body=json_request["body"],
            headers=json_request["headers"],
            user=json_request["user"],
            get_params=json_request["GET"],
            post_params=json_request["POST"],
            cookies=json_request["COOKIES"],
            files=json_request["FILES"],
            meta=json_request["META"],
        )

    def _handle_control_flow(self, context, json_control_flow):
        """
        Обработка потока управления.
        Создание объектов событий в базе данных.
        :param context: объект контекста выполнения запроса.
        :param json_control_flow: данные о контексте выполнения запроса в формате json.
        :return: None.
        """

        for node in json_control_flow:
            if node["event"] == "external_call" or node["event"] == "internal_call":
                Event.objects.create(
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    external_call=(True if node["event"] == "external_call" else False),
                    name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    args=node["args"],
                )
            elif node["event"] == "code_line":
                Event.objects.create(
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    func_name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    args=node["args"],
                    code=node["code"],
                )
            elif node["event"] == "return":
                Event.objects.create(
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    func_name=node["name"],
                    module=node["module"],
                    filename=node["filename"],
                    line=node["line"],
                    final_state=node["final_state"],
                    returned_value=node["returned_value"],
                )
            elif node["event"] == "error":
                Event.objects.create(
                    context=context,
                    timestamp=datetime.strptime(node["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    source_function=node["source"][0]["function"],
                    source_module=node["source"][0]["module"],
                    source_filename=node["source"][0]["filename"],
                    source_line=node["source"][0]["line"],
                    exception_type=node["details"]["exception_type"],
                    exception_message=node["details"]["message"],
                )

    def _handle_response(self, context, json_response):
        """
        Создание объекта ответа в базе данных.
        :param context: объект контекста выполнения запроса.
        :param json_response: данные о контексте выполнения запроса в формате json.
        :return: None.
        """

        Response.objects.create(
            context=context,
            status_code=json_response["status"],
            headers=json_response["headers"],
            body=json_response["body"],
            content_type=json_response["content_type"],
            content_length=(
                json_response["content_length"]
                if json_response["content_length"]
                else ""
            ),
            charset=json_response["charset"] if json_response["charset"] else "",
            version=json_response["version"] if json_response["version"] else "",
            reason_phrase=json_response["reason_phrase"],
            cookies=json_response["cookies"],
            streaming=json_response["streaming"],
        )

    @shared_task
    def handle(self, project_id, json_request, json_control_flow, json_response):
        """
        Асинхронный таск для отправки загруженного файла на
        анализ и вызова формирования отчёта.
        """

        with transaction.atomic():
            app = Application.objects.get(name=project_id)

            context = Context.objects.create(
                application=app,
            )

            _handle_request(context, json_request)
            _handle_control_flow(context, json_control_flow)
            _handle_response(context, json_response)

    def execute(self):
        """
        Выполнение команды.
        """

        json_request = base64.b64decode(self.request_base_64).decode("utf-8")
        json_control_flow = base64.b64decode(self.control_flow_base_64).decode("utf-8")
        json_response = base64.b64decode(self.response_base_64).decode("utf-8")

        task = self.handle.delay(
            project_id, json_request, json_control_flow, json_response
        )

        return Result.success(data={"task_id": task.id})

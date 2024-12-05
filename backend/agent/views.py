"""
Модуль для реализации API, предназначенного для взаимодействия
с агентами интерактивного анализа.

Этот модуль предоставляет следующие возможности:
- Отправка контекста выполнения запроса.
"""

from core.cqrs.commands.create_context_command import CreateContextCommand
from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from core.result import Result


class ContextSerializer(serializers.Serializer):
    """Сериализатор для приема контекста выполнения запроса.

    Атрибуты:
        project (CharField): ID проекта.
        request (TextField): Запрос.
        control_flow (TextField): Поток управления.
        response (TextField): Ответ.
    """
    project = serializers.CharField(max_length=255)
    request = serializers.CharField(max_length=None)
    control_flow = serializers.CharField(max_length=None)
    response = serializers.CharField(max_length=None)


class ContextAPIViewset(viewsets.ViewSet):
    """
    APIView для приема контекста выполнения запроса.

    Методы:
    - POST: Добавить контекст выполнения запроса.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=ContextSerializer,
        responses={
            200: OpenApiResponse(
                description="Успешный ответ.",
                response=Result.success().to_dict(),
                examples=[
                    OpenApiExample(
                        "Успешный ответ",
                        value=Result.success().to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Сообщение о пользовательской ошибке.",
                response=Result.failure(errors="Сообщение об ошибке.").to_dict(),
                examples=[
                    OpenApiExample(
                        "Некорректный запрос",
                        value=Result.failure(errors="Сообщение об ошибке.").to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="Сообщение о внутренней ошибке.",
                response=Result.failure(errors="Сообщение о внутренней ошибке.").to_dict(),
                examples=[
                    OpenApiExample(
                        "Внутренняя ошибка сервера",
                        value=Result.failure(errors="Сообщение об ошибке.", meta={
                            "exception_type": "Класс исключения",
                        }).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                    OpenApiExample(
                        "Внутренняя ошибка сервера (режим отладки)",
                        value=Result.failure(errors="Сообщение об ошибке.", meta={
                            "exception_type": "Класс исключения",
                            "traceback": ["Трассировка ошибки"]
                        }).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
        },
        description="Принимает три строки в base64, расшифровывает их и передает в асинхронную Celery задачу.",
        tags=['agent'],
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Добавить контекст выполнения запроса.

        Параметры:
            request (Request): Объект HTTP-запроса с JSON-данными контекста.

        Возвращает:
            Response: JSON-объект с подтверждением или сообщением об ошибке.
        """
        serializer = ContextSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = serializer.validated_data

                command = CreateContextCommand(
                    data["project"],
                    data["request"],
                    data["control_flow"],
                    data["response"],
                )
                result = command.execute()

                return Response(result.to_dict(), status=200)
            except Exception as e:
                return Response(Result(e).to_dict(), status=500)
        else:
            return Response(Result.failure(serializer.errors).to_dict(), status=400)

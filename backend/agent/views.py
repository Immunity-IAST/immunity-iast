"""
Модуль для реализации API, предназначенного для взаимодействия
с агентами интерактивного анализа.

Этот модуль предоставляет следующие возможности:
- Отправка контекста выполнения запроса.
"""

import base64
import json
import logging

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Project
from core.result import Result
from engine.context import handle_context

logger = logging.getLogger(__name__)


class ContextSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """Сериализатор для приема контекста выполнения запроса.

    Атрибуты:
        project (CharField): Название приложения.
        request (TextField): Запрос.
        control_flow (TextField): Поток управления.
        response (TextField): Ответ.
    """

    def validate_project(self, value):
        """
        Валидатор для параметра project (анализируемый проект).
        :param value: Входное значение параметра.
        """
        if not value:
            raise ValidationError("Параметр project не может быть пустым.")
        try:
            Project.objects.get(name=value)
        except Project.DoesNotExist as exc:
            raise ValidationError(
                f"Приложение с названием {value} не найдено."
            ) from exc
        return value

    def validate_request(self, value):
        """
        Валидатор для параметра request (перехваченный запрос).
        :param value: Входное значение параметра.
        """
        try:
            base64.b64decode(value).decode("utf-8")
        except Exception as exc:
            raise ValidationError(
                "Параметр request должен быть закодирован в Base64."
            ) from exc
        return value

    def validate_control_flow(self, value):
        """
        Валидатор для параметра control_flow (поток управления).
        :param value: Входное значение параметра.
        """
        try:
            base64.b64decode(value).decode("utf-8")
        except Exception as exc:
            raise ValidationError(
                "Параметр control_flow должен быть закодирован в Base64."
            ) from exc
        return value

    def validate_response(self, value):
        """
        Валидатор для параметра response (ответ).
        :param value: Входное значение параметра.
        """
        try:
            base64.b64decode(value).decode("utf-8")
        except Exception as exc:
            raise ValidationError(
                "Параметр response должен быть закодирован в Base64."
            ) from exc
        return value

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
                        value=Result.failure(
                            errors={
                                "Параметр": "Сообщение об ошибке.",
                            }
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
            500: OpenApiResponse(
                description="Сообщение о внутренней ошибке.",
                response=Result.failure(
                    errors="Сообщение о внутренней ошибке."
                ).to_dict(),
                examples=[
                    OpenApiExample(
                        "Внутренняя ошибка сервера",
                        value=Result.failure(
                            errors="Сообщение об ошибке.",
                            meta={
                                "exception_type": "Класс исключения",
                            },
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                    OpenApiExample(
                        "Внутренняя ошибка сервера (режим отладки)",
                        value=Result.failure(
                            errors="Сообщение об ошибке.",
                            meta={
                                "exception_type": "Класс исключения",
                                "traceback": ["Трассировка ошибки"],
                            },
                        ).to_dict(),
                        request_only=False,
                        response_only=True,
                    ),
                ],
            ),
        },
        summary="Добавить контекст выполнения запроса.",
        description="Принимает три строки в base64"
        + ", расшифровывает их и передает в асинхронную Celery задачу.",
        tags=["agent"],
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Добавить контекст выполнения запроса.
        """
        serializer = ContextSerializer(data=request.data)

        if serializer.is_valid():
            try:
                data = serializer.validated_data

                task = handle_context.delay(
                    data["project"],
                    json.loads(base64.b64decode(data["request"]).decode("utf-8")),
                    json.loads(base64.b64decode(data["control_flow"]).decode("utf-8")),
                    json.loads(base64.b64decode(data["response"]).decode("utf-8")),
                )

                return Response(
                    Result.success(data={"task_id": task.id}).to_dict(), status=200
                )
            except Exception as e:
                return Response(Result(e).to_dict(), status=500)
        else:
            return Response(Result.failure(serializer.errors).to_dict(), status=400)

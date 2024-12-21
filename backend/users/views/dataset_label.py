"""
API эндпоинты для проектов.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.command import Command
from core.models import DatasetLabel
from core.query import Query
from core.result import Result
import logging

logger = logging.getLogger(__name__)

class DatasetSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=10)
    file = serializers.CharField(max_length=None)
    line = serializers.CharField(max_length=255)

class DatasetAPIView(viewsets.ViewSet):
    """
    API для работы с уязвимостями.
    """

    # permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Страница пагинации",
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Количество объектов на странице пагинации",
            ),
        ],
        tags=["dataset"],
    )
    def filter(self, request):
        """Фильтрация объектов."""
        try:

            filters = {
                "page": request.GET.get("page"),
                "page_size": request.GET.get("page_size"),
            }

            query = Query(model=DatasetLabel)
            result = query.filter(
                filters={},
                pagination={
                    "page": int(filters["page"]) if filters["page"] is not None else 1,
                    "page_size": (
                        int(filters["page_size"])
                        if filters["page_size"] is not None
                        else 10
                    ),
                },
            )

            if result.is_success:
                return Response(result.to_dict(), status=200)
            else:
                return Response(result.to_dict(), status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

    @extend_schema(
        request=MarkupSerializer,
        responses={
            201: OpenApiResponse(description="Уязвимые контексты размечены"),
            400: OpenApiResponse(description="Ошибка валидации данных"),
        },
        methods=["POST"],
        tags=["dataset"],
    )
    def post(self, request):
        """
        Разметка датасета.
        На вход подаются данные из отчетов стат анализа,
        :param request: На входе - результаты статического анализа,
        где находятся уязвимые участки кода.
        :return: На выходе - что было размечено.
        """

        try:
            serializer = DatasetSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data

                # ... логичная логика

                if result.is_success:
                    return Response(result.to_dict(), status=201)
                else:
                    return Response(result.to_dict(), status=400)
            return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(e)
            return Response(Result(e).to_dict(), status=500)

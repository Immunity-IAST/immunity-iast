"""
Команда для создания проекта.
"""

import logging

from core.models import Project
from core.result import Result

logger = logging.getLogger(__name__)


class CreateProjectCommand:
    """
    Команда для создания проекта.
    """

    def __init__(self, project_name):
        """
        Инициализация команды.
        """
        self.project_name = project_name

    def execute(self):
        """
        Выполнение команды.
        """

        exists = Project.objects.filter(name=self.project_name).exists()

        if exists:
            return Result.failure(f"Project {self.project_name} already exists")
        else:
            return Result.success(
                Project.objects.create(data={"name": self.project_name})
            )

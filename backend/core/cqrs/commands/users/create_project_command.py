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
        if Project.objects.filter(name=self.project_name).exists():
            return Result(False, "Проект с таким именем уже существует.")

        project = Project.objects.create(name=self.project_name)
        return Result(True, "Проект успешно создан.", project)

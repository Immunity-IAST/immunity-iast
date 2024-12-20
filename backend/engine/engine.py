"""
Модуль движка интерактивного анализа.

Входными данными является контекст обработки запроса анализируемого приложения.
На выходе создаются объекты уязвимостей в базе данных.
Функциональность движка реализуется через плагины.
"""

import importlib
import os
from typing import List, Dict
from .models import Vulnerability


class AnalysisEngine:
    """
    Движок для выполнения анализа с использованием плагинов.
    """

    def __init__(self):
        self.plugins = self.load_plugins()

    def load_plugins(self) -> List:
        """
        Загружает все плагины из каталога plugins.
        """
        plugins = []
        plugin_dir = os.path.dirname(__file__) + "/plugins"

        for filename in os.listdir(plugin_dir):
            if filename.endswith("_plugin.py") and filename != "base.py":
                module_name = f"analysis_engine.plugins.{filename[:-3]}"
                module = importlib.import_module(module_name)

                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, BasePlugin) and cls != BasePlugin:
                        plugins.append(cls())
        return plugins

    def run_analysis(self, context_id: int, data: Dict[str, Any]):
        """
        Запускает анализ с использованием всех плагинов.
        """
        vulnerabilities = []
        for plugin in self.plugins:
            vulnerabilities.extend(plugin.run(context_id, data))

        # Сохраняем уязвимости в БД
        for vuln in vulnerabilities:
            Vulnerability.objects.create(
                context_id=vuln["context_id"],
                type=vuln["type"],
                description=vuln["description"],
                evidence=vuln["evidence"],
            )
        return vulnerabilities

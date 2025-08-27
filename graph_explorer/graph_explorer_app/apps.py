from typing import List

from django.apps import AppConfig

from core.application import Application
from core.model.command_processor import CommandProcessor
from core.model.workspace import Workspace


class GraphExplorerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'graph_explorer_app'

    def ready(self):
        self.app_core = Application()

    @property
    def workspaces(self) -> List[Workspace]:
        return self.app_core.workspaces
    @property
    def command_processor(self) -> CommandProcessor:
        return self.app_core.command_processor

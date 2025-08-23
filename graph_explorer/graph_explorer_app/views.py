import random
from typing import List

from api.model import Graph, Node, Edge
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from simple_visualizer.implementation import SimpleVisualizer
from block_visualizer.block_visualizer import BlockVisualizer

from core.model.command_processor import Command
from django.apps import apps

from core.application import Application
from api.services.visualizer import Visualizer


def index(request):
    app_core = apps.get_app_config("graph_explorer_app").app_core

    context = {}

    # Current workspace (if any)
    if getattr(app_core, "current_workspace_id", None):

        current_ws = next(
            filter(lambda ws: ws.id == app_core.current_workspace_id, app_core.workspaces),
            None
        )
        print("DEBUG -> Current WS:", current_ws.id, current_ws.name, current_ws.visualizer_id)
        if current_ws.visualizer_id:
            visualizers : List[Visualizer] = app_core.service_plugin.get_plugins("graph_explorer.visualizers")
            visualizer = next((v for v in visualizers if v.identifier() == current_ws.visualizer_id), None)

            if visualizer:
                context["graph_html"] = visualizer.display_graph(current_ws.graph)

        context["current_workspace"] = current_ws

    # Pass all workspaces
    context["workspaces"] = app_core.workspaces

    # Pass plugin options
    context["visualizer_plugins"] = [
        {"id": p.__class__.__name__, "name": getattr(p, "name", p.__class__.__name__)}
        for p in app_core.service_plugin.get_plugins("graph_explorer.visualizers")
    ]

    context["data_plugins"] = [
        {"id": p.__class__.__name__, "name": getattr(p, "name", p.__class__.__name__)}
        for p in app_core.service_plugin.get_plugins("sok.plugins.datasource")
    ]

    return render(request, "index.html", context)

    return render(request, "index.html", context)
@csrf_exempt
def save_workspace(request):
    app_config = apps.get_app_config("graph_explorer_app")
    app_core = app_config.app_core
    if request.method == "POST":
        app_core.command_processor.execute(Command.CREATE_WORKSPACE,
                                           workspace=request.POST.get("workspace"),
                                           data_plugin=request.POST.get("data_plugin"),
                                           visualizer=request.POST.get("visualizer"))
        return redirect("index")

    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def select_workspace(request):
    app_core = apps.get_app_config("graph_explorer_app").app_core
    if request.method == "POST":
        ws_id = request.POST.get("workspace_id")
        if ws_id:
            ws_id = str(ws_id)
            found = next((ws for ws in app_core.workspaces if ws.id == ws_id), None)
            if found:
                app_core.current_workspace_id = ws_id
                app_core.command_processor.execute(Command.SELECT_WORKSPACE,id=ws_id)
        return redirect("index")
    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def select_visualizer(request):
    app_core = apps.get_app_config("graph_explorer_app").app_core

    if request.method == "POST":
        visualizer_id = request.POST.get("visualizer_id")

        print(visualizer_id)

        if app_core.current_workspace_id and visualizer_id:
            app_core.command_processor.execute(
                Command.SELECT_VISUALIZER,
                visualizer=visualizer_id
            )

        return redirect("index")

    return JsonResponse({"error": "Only POST allowed"}, status=405)

import random
from typing import List
import json

from api.model import Graph, Node, Edge
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from simple_visualizer.implementation import SimpleVisualizer
from block_visualizer.block_visualizer import BlockVisualizer

from core.model.command_processor import Command
from core.model.filter import Filter
from core.model.search import Search
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
        if current_ws.visualizer_id:
            visualizers : List[Visualizer] = app_core.service_plugin.get_plugins("graph_explorer.visualizers")
            visualizer = next((v for v in visualizers if v.identifier() == current_ws.visualizer_id), None)

            if visualizer:
                context["graph_html"] = visualizer.display_graph(current_ws.graph)
        data = {
            "nodes": [{"id": str(n.id), "data": n.data} for n in current_ws.graph.nodes],
            "edges": [{"from": str(e.origin.id), "to": str(e.target.id)} for e in current_ws.graph.edges],
        }
        context["graph_json"] = json.dumps(data)
        context["current_workspace"] = current_ws
        context["current_filters"] = list(current_ws.filters) if current_ws else []

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


@csrf_exempt
def apply_filter(request):
    """Apply a filter to the current workspace using filter string"""
    app_core = apps.get_app_config("graph_explorer_app").app_core

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            filter_query = data.get("query")

            if not filter_query:
                return JsonResponse({"error": "Missing filter query"}, status=400)

            # Create and apply filter using the new string format
            if app_core.current_workspace_id:
                current_ws = next(
                    (ws for ws in app_core.workspaces if ws.id == app_core.current_workspace_id),
                    None
                )

                if current_ws:
                    try:
                        # Use the new decorator functionality - pass filter string directly
                        current_ws.add_filter(filter_query)

                        return JsonResponse({
                            "success": True,
                            "message": f"Filter applied: {filter_query}",
                            "filter_query": filter_query
                        })
                    except (ValueError, TypeError) as e:
                        return JsonResponse({"error": str(e)}, status=400)
                else:
                    return JsonResponse({"error": "No current workspace found"}, status=400)
            else:
                return JsonResponse({"error": "No workspace selected"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def remove_filter(request):
    """Remove a filter from the current workspace using filter string"""
    app_core = apps.get_app_config("graph_explorer_app").app_core

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            filter_query = data.get("query")

            if not filter_query:
                return JsonResponse({"error": "Missing filter query"}, status=400)

            if app_core.current_workspace_id:
                current_ws = next(
                    (ws for ws in app_core.workspaces if ws.id == app_core.current_workspace_id),
                    None
                )

                if current_ws:
                    try:
                        # Use the new decorator functionality - pass filter string directly
                        current_ws.remove_filter(filter_query)

                        return JsonResponse({
                            "success": True,
                            "message": f"Filter removed: {filter_query}"
                        })
                    except ValueError as e:
                        return JsonResponse({"error": str(e)}, status=400)
                else:
                    return JsonResponse({"error": "No current workspace found"}, status=400)
            else:
                return JsonResponse({"error": "No workspace selected"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def apply_search(request):
    """Apply a search filter to the current workspace"""
    app_core = apps.get_app_config("graph_explorer_app").app_core

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            search_value = data.get("value")

            if not search_value:
                return JsonResponse({"error": "Missing search value"}, status=400)

            # Convert value to appropriate type (same logic as filter)
            try:
                # Try to convert to int first
                if search_value.isdigit() or (search_value.startswith('-') and search_value[1:].isdigit()):
                    search_value = int(search_value)
                # Try to convert to float
                elif '.' in search_value:
                    try:
                        search_value = float(search_value)
                    except ValueError:
                        pass  # Keep as string
                # Check for boolean values
                elif search_value.lower() in ['true', 'false']:
                    search_value = search_value.lower() == 'true'
            except (ValueError, AttributeError):
                pass  # Keep as string

            # Create and apply search
            if app_core.current_workspace_id:
                current_ws = next(
                    (ws for ws in app_core.workspaces if ws.id == app_core.current_workspace_id),
                    None
                )

                if current_ws:
                    try:
                        search_obj = Search(value=search_value)
                        current_ws.add_filter(search_obj)

                        return JsonResponse({
                            "success": True,
                            "message": f"Search applied: {search_value}",
                            "search_id": f"search_{search_value}"
                        })
                    except (ValueError, TypeError) as e:
                        return JsonResponse({"error": str(e)}, status=400)
                else:
                    return JsonResponse({"error": "No current workspace found"}, status=400)
            else:
                return JsonResponse({"error": "No workspace selected"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def remove_search(request):
    """Remove a search filter from the current workspace"""
    app_core = apps.get_app_config("graph_explorer_app").app_core

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            search_value = data.get("value")

            if not search_value:
                return JsonResponse({"error": "Missing search value"}, status=400)

            # Convert value to appropriate type (same logic as apply_search)
            try:
                if search_value.isdigit() or (search_value.startswith('-') and search_value[1:].isdigit()):
                    search_value = int(search_value)
                elif '.' in str(search_value):
                    try:
                        search_value = float(search_value)
                    except ValueError:
                        pass
                elif str(search_value).lower() in ['true', 'false']:
                    search_value = str(search_value).lower() == 'true'
            except (ValueError, AttributeError):
                pass

            if app_core.current_workspace_id:
                current_ws = next(
                    (ws for ws in app_core.workspaces if ws.id == app_core.current_workspace_id),
                    None
                )

                if current_ws:
                    try:
                        search_obj = Search(value=search_value)
                        current_ws.remove_filter(search_obj)

                        return JsonResponse({
                            "success": True,
                            "message": f"Search removed: {search_value}"
                        })
                    except ValueError as e:
                        return JsonResponse({"error": str(e)}, status=400)
                else:
                    return JsonResponse({"error": "No current workspace found"}, status=400)
            else:
                return JsonResponse({"error": "No workspace selected"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def execute_cli_command(request):
    """Execute a CLI command in the backend and return the output"""
    if request.method != "POST":
        return JsonResponse({"output": "Invalid request", "refresh_graph": False})

    try:
        data = json.loads(request.body)
        command_str = data.get("command", "").strip()
        app_core = apps.get_app_config("graph_explorer_app").app_core

        if not command_str:
            return JsonResponse({"output": "No command provided", "refresh_graph": False})

        def convert_value(value):
            try:
                if str(value).isdigit() or (str(value).startswith('-') and str(value)[1:].isdigit()):
                    return int(value)
                elif '.' in str(value):
                    try:
                        return float(value)
                    except ValueError:
                        pass
                elif str(value).lower() in ['true', 'false']:
                    return str(value).lower() == 'true'
            except (ValueError, AttributeError):
                pass
            return value

        def get_current_workspace():
            ws = next((ws for ws in app_core.workspaces if ws.id == app_core.current_workspace_id), None)
            if not ws:
                raise ValueError("No current workspace found")
            return ws

        tokens = command_str.split()
        if not tokens:
            return JsonResponse({"output": "Empty command", "refresh_graph": False})

        cmd = tokens[0].lower()

        if cmd == "search":
            if len(tokens) < 2:
                return JsonResponse({"output": "Missing search value", "refresh_graph": False})
            value = convert_value(" ".join(tokens[1:]))
            ws = get_current_workspace()
            search_obj = Search(value=value)
            ws.add_filter(search_obj)
            return JsonResponse({
                "output": f"Search applied: {value}",
                "refresh_graph": True,
                "search_id": f"search_{value}"
            })

        elif cmd == "filter":
            if len(tokens) < 4:
                return JsonResponse({"output": "Missing field/operator/value for filter", "refresh_graph": False})
            # Join all tokens after "filter" to create the filter string
            filter_query = " ".join(tokens[1:])
            ws = get_current_workspace()
            # Use the new decorator functionality - pass filter string directly
            ws.add_filter(filter_query)
            return JsonResponse({
                "output": f"Filter applied: {filter_query}",
                "refresh_graph": True,
                "filter_query": filter_query
            })

        else:
            output = app_core.command_processor.parse_and_execute(command_str)
            refresh_graph = any(op in command_str for op in [
                "create_node", "delete_node",
                "create_edge", "delete_edge",
                "edit_node", "edit_edge", "clear_graph"
            ])
            return JsonResponse({
                "output": output,
                "refresh_graph": refresh_graph
            })

    except Exception as e:
        return JsonResponse({"output": str(e), "refresh_graph": False})
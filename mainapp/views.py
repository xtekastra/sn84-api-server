import hashlib
import json

from channels.db import database_sync_to_async
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import History
from .solver import solve
from django.core.paginator import Paginator
from django.shortcuts import render
import csv
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "index.html", {})

@database_sync_to_async
def get_history(request_id):
    return list(History.objects.filter(request_id=request_id))

@database_sync_to_async
def create_new_history(request_id, task_type, image, predictions):
    History.objects.create(request_id = request_id, task_type = task_type, image = image, predictions = predictions)

@database_sync_to_async
def update_history(request_id, predictions):
    h = History.objects.get(request_id = request_id)
    h.predictions = predictions
    h.save()

@database_sync_to_async
def get_all_data():
    return list(History.objects.all())


@csrf_exempt
async def predict(request):
    if request.method == "POST":
        try:
            request_id = None
            task_type = None
            image = None
            predictions = []
            if request.POST:
                if "image" in request.POST:
                    image = request.POST["image"]
                if "request_id" in request.POST:
                    request_id = request.POST["request_id"]
                if "task_type" in request.POST:
                    task_type = request.POST["task_type"]
            else:
                data = json.loads(request.body)
                if "image" in data:
                    image = data["image"]
                if "request_id" in data:
                    request_id = data["request_id"]
                if "task_type" in data:
                    task_type = data["task_type"]
            status = "Unknown"
            if image:
                try:
                    predictions = await solve(image = image, request_id = request_id, task_type = task_type)
                    hs = await get_history(request_id)
                    if hs:
                        h = hs[0]
                        await update_history(h.request_id, predictions)
                    else:
                        await create_new_history(image = image, request_id = request_id, task_type = task_type, predictions =  predictions)
                    status = "Solved"
                except Exception as e:
                    status = "Error: {}".format(e)
            predictions = json.loads(predictions)
            print(predictions)

            return JsonResponse({"status": status,"predictions": predictions})
        except json.JSONDecodeError:
            return JsonResponse({"status": "Error: Invalid JSON","predictions": []}, status=400)
    return JsonResponse({"status": "Error: Unknown","predictions": []}, 505)


def item_list(request):
    items = History.objects.all().order_by('-created')
    paginator = Paginator(items, 10)  # 10 items per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "list.html", {"page_obj": page_obj})


def history_detail(request, pk):
    history = get_object_or_404(History, pk=pk)
    return render(request, 'detail.html', {'history': history})

@csrf_exempt
async def rerun(request):
    request_id = request.POST['request_id']
    history = await get_history(request_id)
    if history:
        h = history[0]
    predictions = await solve(image = h.image, request_id = h.request_id, task_type = h.task_type)
    await update_history(request_id, predictions)
    return JsonResponse({'status': 'ok'})


import json
from datetime import datetime as dt
from django.core.exceptions import BadRequest
# from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from foobar.models import Log, Notify
from foobar.forms import LogForm, NotifyForm

JSON_HEADER = {"content_type": "application/json"}


def index(request):
    result = json.dumps({
        "/ts/": {
            "GET": {
                "returns": "Current date and current ts"
            }
        },
        "/log/": {
            "POST": {
                "args": {
                    "level": "One of [DBG, INF, WRN, ERR]",
                    "message": "Text of log-message"
                },
                "returns": "Log-entry"
            }
        },
        "/notify/": {
            "POST": {
                "args": {
                    "ts": "After that timestamp notify will be triggered",
                    "message": "Text of notification"
                },
                "returns": '{"success": true or false, "error": error message if there is an error} whether notification were successfully activated'
            },
            "GET": {
                "args": {
                    "ts": "current timestamp",
                },
                "returns": "If there is notification that should be activate for that timestamp, then return message(s)"
            }
        }
    })
    return HttpResponse(result, **JSON_HEADER)


def notify(request):
    if request.method == "POST":
        status = {"success": True}
        form = NotifyForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            status["success"] = False
            status["status"] = form.errors
        return HttpResponse(json.dumps(status), **JSON_HEADER)
    elif request.method == "GET":
        result = []
        try:
            ts = int(request.GET["ts"])
        except (KeyError, ValueError):
            raise BadRequest("ts argument should be a valid timestamp")
        d = dt.fromtimestamp(ts)
        if Notify.objects.filter(ts__gte=d).exists():
            # from django.core.serializers import serialize
            result = [
                {"ts": obj["ts"].strftime("%Y-%m-%d+%Z %T"), "message": obj["message"]}
                for obj in Notify.objects.filter(ts__gte=d).values()
            ]
        return HttpResponse(json.dumps(result), **JSON_HEADER)
    else:
        return HttpResponseNotAllowed([request.method])

def log(request):
    if request.method == "POST":
        form = LogForm(request.POST or None)
        if form.is_valid():
            log_obj = form.save()
            return HttpResponse(str(log_obj))
        else:
            raise BadRequest(form.errors)
    else:
        return HttpResponseNotAllowed([request.method])

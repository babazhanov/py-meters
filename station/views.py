from django.shortcuts import render
from datetime import datetime, timedelta

from .models import Cell, Profile
from .mailutils import MailBox
from ensfera.models import Preference


def index(request):
    cell_id = "-1"
    cell = "unknown"
    date = "-1"

    try:
        
        cell_id = request.GET.get("cell", Cell.objects.all().first().pk)
        cell_id = int(cell_id)
        cell = Cell.objects.get(pk=cell_id)
        
        date = request.GET.get("date")
        try:
            date = datetime.strptime(date, "%d.%m.%Y")
        except:
            date = datetime.now() - timedelta(days=1)

        profile = Profile.objects.filter(cell__pk=cell_id, date=date, value_type=1).order_by("time")

        return render(request, "index.html", {
            "cells": Cell.objects.all(),
            "cell_id": cell_id,
            "cell_name": str(cell),
            "date": date.strftime("%d.%m.%Y"),
            "profile": profile,
            "info": str(cell_id) + '\n' + str(date)
        })

    except Exception as e:
        return render(request, "index.html", {
            "cells": Cell.objects.all(),
            "cell_id": cell_id,
            "cell_name": str(cell),
            "date": (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y"),
            "profile": [],
            "info": "Ошибка " + str(e) + " " + str(cell_id) + '\n' + str(date)
        })


def mail(request):
    M = MailBox()
    
    return render("mail.html", {
        "objects": M.get_headers_lastn(5)
        })


def ws(request):
    com_port = Preference.objects.get_or_create(
        name="com-port",
        defaults={'value': 'COM2'}
    )[0].value
    
    return render(request, "ws.html", {"com_port": com_port})


def celery(request):
    #celery_task.delay()
    return render(request, "celery.html")

import os
import time
import random
import socket
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

APP_TO_MONGO_VMS_IP = {
	"billing": ["172.16.2.121"],
	"accounting": ["172.16.3.121", "172.16.3.122"]
}
MONGO_PORT= 27017

def nc(ip, port):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect((ip, port))
	time.sleep(3)

# Create your views here.

def index(request):
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    nc(random.choice(APP_TO_MONGO_VMS_IP[os.getenv("OPENSHIFT_BUILD_NAMESPACE")]), MONGO_PORT)
    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    return HttpResponse(PageView.objects.count())

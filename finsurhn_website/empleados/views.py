from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from empleados.models import *
from empleados.forms import *

from django.db import transaction
from htmlmin.decorators import minified_response

import os, json

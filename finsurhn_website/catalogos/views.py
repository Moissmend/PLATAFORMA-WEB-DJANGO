from lib2to3.pytree import Base
from logging import exception
from django.db.models.expressions import ExpressionWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from catalogos.models import *
from django.db import transaction
from htmlmin.decorators import minified_response

# Para poder mandar el correo con archivos
from django.core.mail import send_mail, EmailMessage
from django.core.cache import cache

import os, json
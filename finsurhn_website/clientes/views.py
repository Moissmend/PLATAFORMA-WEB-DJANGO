#IMPORTACIONES
from django.shortcuts import render
from django.db import DatabaseError, transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from htmlmin.decorators import minified_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils import timezone
import os
from django.conf import settings 
from django.core.mail import send_mail
from .utils import *
import json
import base64
from django.core.files.base import ContentFile
from google.cloud import storage
from django.core.files.storage import default_storage
from importlib import reload
reload(sys)
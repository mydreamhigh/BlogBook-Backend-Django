from django.contrib.auth.models import Group
from django.contrib import admin
from . import models

admin.site.register(models.Writer)
admin.site.unregister(Group)

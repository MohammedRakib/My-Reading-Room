from django.contrib import admin
from .models import *


class ReadingMaterialAdmin(admin.ModelAdmin):
    # readonly_fields = ('id',)
    readonly_fields = ('id',)


admin.site.register(ClassRoom)
admin.site.register(ReadingMaterial, ReadingMaterialAdmin )
admin.site.register(ReadingInfo)

from django.contrib import admin
from .models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Repository._meta.get_fields()]
    list_filter = [field.name for field in Repository._meta.get_fields()]


# Register your models here.
admin.site.register(Repository, RepositoryAdmin)

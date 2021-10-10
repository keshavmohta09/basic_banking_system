from django.contrib import admin
from .models import *
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','account_no','ifsc_code','balance')
    search_fields = ('id','name','email','account_no')


admin.site.register(User,UsersAdmin)
admin.site.register(Transaction)

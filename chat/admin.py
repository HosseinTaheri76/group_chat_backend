from django.contrib import admin
from chat.models import Member, Message, ChatGroup
# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(Member)
admin.site.register(Message)

from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tag, Question, Answer

admin.site.register(CustomUser)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
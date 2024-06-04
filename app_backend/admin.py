from django.contrib import admin
from app_backend.models import *

class ProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)



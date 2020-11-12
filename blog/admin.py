from django.contrib import admin
from blog.models import Post, BlogComment

admin.site.register((Post, BlogComment))

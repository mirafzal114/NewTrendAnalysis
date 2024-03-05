from django.contrib import admin

from news.models import News,Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','content')
    search_fields = ('post',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish','status')
    search_fields = ('title', 'body')
    list_filter = ('status', 'publish', 'created_at', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    raw_id_fields = ('author',)
    ordering = ('status','-publish',)
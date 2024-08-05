from django.contrib import admin
from .models import Notice, Category, Reply, Subscription


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted', 'category', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    search_fields = ('category_name',)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'commentator', 'notice', 'date', 'reply_content')
    list_display_links = ('id', 'reply_content')
    search_fields = ('notice', 'reply_content')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category')
    list_display_links = ('id', 'user', 'category')
    search_fields = ('user', 'category',)


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Subscription, SubscriptionAdmin)


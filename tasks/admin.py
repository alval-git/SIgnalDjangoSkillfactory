from django.contrib import admin

from tasks.models import TodoItem, Category, Priority


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('slug', 'priority_name')


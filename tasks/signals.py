from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter

# Счетчики увеличения/уменьшения задач в категориях
@receiver(m2m_changed, sender=TodoItem.category.through)  
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add": 
        return
    print(action)
    for cat in instance.category.all(): 
        slug = cat.slug
        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()

        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through) 
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove": 
        return

    print(action)

    for cat in Category.objects.all():
        slug = cat.slug
        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()
        Category.objects.filter(slug=slug).update(todos_count=new_count)

@receiver(post_delete, sender=TodoItem)  
def task_category_removed(instance, **kwargs):
    for cat in Category.objects.all():
        slug = cat.slug
        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()
        Category.objects.filter(slug=slug).update(todos_count=new_count)




# Счетчики увеличения/уменьшения задач в  приоритетах
@receiver(post_save, sender=TodoItem)  
def task_priority_added( instance, **kwargs):
    # priority = instance.priority
    # priority.priority_count = 
    # priority.save()
    for priority in Priority.objects.all():
        slug = priority.slug
        new_count = 0
        for task in TodoItem.objects.all():
            if task.priority.slug == slug:
                new_count += 1
        Priority.objects.filter(slug=slug).update(priority_count=new_count)

@receiver(post_delete, sender=TodoItem)  
def task_priority_removed(instance, **kwargs):
    priority = instance.priority
    priority.priority_count -= 1
    priority.save()

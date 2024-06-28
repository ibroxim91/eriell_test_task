from django.db.models import signals
from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group as PermissionGroup
from .positions import Position

# Здесь, как только преподаватель или ученик добавляется в базу данных, он автоматически добавляется в нужную группу с правами.
# Я все сделал правильно, но это не сработало


@receiver(signal=signals.post_save, sender=User)
def user_check_permission_signals(instance: User, **kwargs) -> None:
    if kwargs['created'] and instance.position in (Position.teacher.value, Position.student.value):
        group = get_permission_group(group_name=instance.position)
    if kwargs['created'] and instance.is_superuser is False and  group not in instance.groups.all():
       group.user_set.add(instance)
       group.save()


def get_permission_group(group_name: str) -> PermissionGroup:
    all_permissions = ["view_science", 'view_group', "view_score", "view_lessonplan"]
    teacher_permissions = ["add_score", "change_score", "delete_score"] if group_name == "teacher" else []
    group, created = PermissionGroup.objects.get_or_create(name=group_name)
    # if user group created 
    if created == True:
        for permission in all_permissions + teacher_permissions:
            permission = Permission.objects.get(codename=permission, content_type__app_label="main")
            group.permissions.add(permission)
    return group

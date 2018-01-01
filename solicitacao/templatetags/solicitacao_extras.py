from django import template
from django.contrib.auth.models import Group

register = template.Library()


# Checar se existe um usuário X em um grupo
@register.filter
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

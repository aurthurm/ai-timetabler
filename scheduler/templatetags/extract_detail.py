from django import template
from scheduler.models import *

register = template.Library()

@register.simple_tag
def extract_created(*args, **kwargs): 
    table = kwargs['table']
    for k, v in table.items():
        if k == 'created':
            created = v
    return created
from cron_descriptor import get_description
from datetime import datetime
from django import template
register = template.Library()

@register.filter
def convert_cron_to_readable_fromat(cron_value):
    return get_description(cron_value)


@register.filter(expects_localtime=True)
def convert_date(date_string):  
  return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")


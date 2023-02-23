from django import template

register = template.Library()

@register.filter(name='short_name')
def cut(value):
    return str(value).split(" ")[0] + " " + str(value).split(" ")[1]

@register.filter(name='surname')
def GetSurname(value):
    return str(value).split(" ")[0]

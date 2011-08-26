from django.template import Library

register = Library()

def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

register.filter('sub', sub)

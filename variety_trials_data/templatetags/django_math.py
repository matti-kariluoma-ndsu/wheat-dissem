from django.template import Library

register = Library()

def sub(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

def divide(value, arg):
		"Divides the arg by the value, as ints"
		return int(value) / int(arg)

register.filter('sub', sub)
register.filter('divide', divide)

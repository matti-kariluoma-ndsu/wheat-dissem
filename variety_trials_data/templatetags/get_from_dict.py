from django.template import Library
from django.utils.http import urlencode

register = Library()

def get_from_dict(value, arg):
	"""
	Returns value[arg] or None.
	"""
	try:
		result = value[arg]
	except:
		result = None
	return result


register.filter('get_from_dict', get_from_dict)

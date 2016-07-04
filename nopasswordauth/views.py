#!/usr/bin/env python
# coding: ascii

"""
:copyright: 2016 Matti Kariluoma <matti.kariluoma@gmail.com>
:license: CC BY-NC-ND 3.0 @see LICENSE
"""
from django.http import HttpResponse
from django.conf import settings
from nopassword import views as nopassviews
from .models import NoPasswordUser

def login(request):
	if request.method == 'POST':
		try:
			username = request.POST['username']
		except:
			username = ''
		try:
			user = NoPasswordUser.objects.get(email=username)
		except:
			user = None
		if user is None:
			next = request.GET.get('next')
			here = settings.LOGIN_URL
			if next is not None:
				here += '?next=' + next
			html = '''<html>
<head><title>No Account</title></head>
<body>
<p>The email address "{username}" is not a valid account on this system.</p>
<p>Please contact the system administrator in order to register a new account.</p>
<p>If you've reached this page in error, please <a href="{here}">reload the page</a> to try again.</p>
</body>
</html>
'''
			return HttpResponse(html.format(username=username, here=here))
	return nopassviews.login(request)

def page_not_found(request):
	html = '''<html>
<head><title>404 - Page Not Found</title></head>
<body>
<h3>The page or resource you requested was not found.</h3>
<h4>If you were trying to visit a page on this site:</h4>
<p>You may have entered the url incorrectly, or the page no longer exists.
Please visit the previous page and try again, or start your query over
from our <a href="{base_url}">home page</a>.</p>
<h4>If you were trying to login:</h4>
<p>This can happen if you are trying to login using an old link, or if your
login request is otherwise invalid. Please try to <a href="{login_url}">login 
again</a>.</p>

<h3>If this problem persists, please contact the site administrator.</h3>
</body>
</html>
'''
	response = HttpResponse(html.format(
			base_url=settings.BASE_URL,
			login_url=settings.LOGIN_URL)
		)
	response.status_code = 404
	return response

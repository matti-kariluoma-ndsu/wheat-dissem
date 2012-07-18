from django.contrib.redirects.models import Redirect
from django import http
from django.conf import settings
from django.shortcuts import redirect

class RedirectFallbackMiddleware(object):

	def process_request(self, request):
		if request.GET.__contains__('zipcode'):
			if request.GET.get('zipcode',None) =='56763':
				return redirect('view/2011/bushels_acre/?zipcode=56560')
		# print request.GET.__getitem__('zipcode')
		# if True: #request.GET.get('zipcode').contains('56763'):
			# print 'success'
			# new_request=copy.deepcopy(request)
			# new_request.GET.update({'zipcode':['56560']})
			# return new_response
		# return response

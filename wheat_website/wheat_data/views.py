from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from wheat_data.models import VarietyForm

# Create your views here.
def add_variety(request):
    if request.method == 'POST': # If the form has been submitted...
        form = VarietyForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/variety/') # Redirect after POST
    else:
        form = VarietyForm() # An unbound form

    return render_to_response('add.html', {
        'form': form,
    })

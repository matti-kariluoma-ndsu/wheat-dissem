from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from wheat_data import models

# Create your views here.
def index(request):
  return render_to_response('base.html')

def add_variety(request):
  DiseaseFormset = inlineformset_factory(models.Variety, models.Disease_Entry)
  
  if request.method == 'POST': # If the form has been submitted...
    form = models.VarietyForm(request.POST)
    if form.is_valid():
      new_variety = form.save()
      formset = DiseaseFormset(request.POST, instance=new_variety)
      if formset.is_valid():
        formset.save()
      return HttpResponseRedirect('/variety/')
    else:
      formset = DiseaseFormset(request.POST)
      
  else:
    form = models.VarietyForm()
    formset = DiseaseFormset()

  return render_to_response('add.html', 
    {'form': form, 'formset': formset},
      context_instance=RequestContext(request)
  )

def add_trial_entry(request):
  if request.method == 'POST': # If the form has been submitted...
    form = models.Trial_EntryForm(request.POST)
    if form.is_valid():
      new_variety = form.save()
      return HttpResponseRedirect('/admin/')
  else:
    form = models.Trial_EntryForm()

  return render_to_response('add.html', 
    {'form': form },
      context_instance=RequestContext(request)
  )

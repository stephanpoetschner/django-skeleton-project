# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
    ctx = {}
    return render_to_response('core/homepage.html', ctx,
                              context_instance=RequestContext(request))
def error_500(request):
    raise StandardError(u'Testing 500 error page')

def error_404(request):
    raise Http404(u'Testing 404 error page')

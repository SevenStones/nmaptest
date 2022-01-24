from django.shortcuts import render
from .forms import ScanForm
from django.core import serializers
from .tasks import do_scan, task_io
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
def scan_config(request):
    context = {}
    scanout = {}
    print("in views.scan_config - request.method is {0}".format(request.method))
    if request.is_ajax():
        print("request is ajax")

    if request.is_ajax() and request.method == 'POST':
        print("ajaxy submit received")
        form = ScanForm(request.POST)
        if form.is_valid():
            print("form found to be valid")
            ipaddress = form.cleaned_data.get("target")
            print(type(ipaddress))
            scanout['scanout'] = scan_run(ipaddress)
            return HttpResponse(
                json.dumps(scanout),
                content_type="application/json"
            )
        else:
            print("form has problems: {0}".format(form.errors))
            context = {'form': form.errors}
            return JsonResponse(context, status=500)

    context = {'form': ScanForm}
    return render(request, 'scan.html', context)

def scan_run(target):

    scanout = {}

    result = do_scan.apply_async((target, ), )
    tree = result.get()
    print("tree is {0}".format(tree))
    scanout['scanout'] = tree

    return scanout

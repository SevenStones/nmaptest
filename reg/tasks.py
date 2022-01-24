from __future__ import print_function
from celery import shared_task
from nmaptest.celery import app
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser



@shared_task
def task_io(ipaddress):

    scanout = {}
    result = do_scan.apply_async(args=[ipaddress], kwargs={}, countdown=1)

    scanout = result.get()

    return scanout

@app.task
def do_scan(ipaddress):

    nm = NmapProcess(ipaddress, "-sT")

    nm.run()

    nmap_stdout_parsed = NmapParser.parse(nm.stdout)

    return nmap_stdout_parsed



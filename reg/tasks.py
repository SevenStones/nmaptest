from __future__ import print_function
from celery import shared_task
from nmaptest.celery import app
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException



@shared_task
def task_io(ipaddress):

    print("in task_io")

    scanout = {}
    result = do_scan.apply_async(args=[ipaddress], kwargs={}, countdown=1)
    print("just ignored aply_aysnc")
    scanout = result.get()

    return scanout

@app.task
def do_scan(ipaddress):

    print("cock is {0} of type {1}".format(ipaddress, type(ipaddress)))

    nm = NmapProcess(ipaddress, "-sT")

    nm.run()

    nmap_stdout_parsed = NmapParser.parse(nm.stdout)
    print("nmap_stdout_parsed is {0} of type {1}".format(nmap_stdout_parsed, type(nmap_stdout_parsed)))
    return nmap_stdout_parsed



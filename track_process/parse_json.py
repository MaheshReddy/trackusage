#!/bin/python 
import json
import csv
from models import SampleRun,Process_Record,Run_Record
from django.utils import timezone
import sys
def parse(file):
    fd = open(file,'r');
    lines = fd.readlines()
    fd.close()
    #creating SampleRun instane from the file name
    sample_run = SampleRun(name=file.split('/')[-1],tags='none',date=timezone.now())
    sample_run.save()
    for line in lines:
	    line_dict = json.loads(line)
	    #creating run_record instance for this sample run using Django's foreign key infra
	    run_record_sample = sample_run.run_record_set.create(run_time=line_dict['id'], 
			    total_mem=line_dict['total_mem'],
			    total_vmem=line_dict['total_vmem'],
			    total_cpu=line_dict['total_cpu'])
	    process_list = line_dict['processes']
	    for process in process_list:
		    run_record_sample.process_record_set.create(
				    create_time=process['create_time'],
				    cpu_percent=process['cpu_percent'],
				    name = process['name'],
				    cmd_line = process['cmdline'],
				    mem_info = str(process['memory_info'][0])+","+str(process['memory_info'][1]))
#
#    #cpu_data = [['Time(sec)', 'process']]
#    cpu_data = []
#    #memory_data = [['Time(sec)',  'memory']]
#    memory_data = []
#    for line in lines:
#        process = json.loads(line)
#	cpu_data.append({'x':str(process['id']), 'y':process['total_cpu']})
#	#cpu_data.append([str(process['id']), process['total_cpu']])
#	memory_data.append({'x':str(process['id']), 'y':process['total_mem']/(1024*1024)})
#        #memory_data.append([str(process['id']), (process['total_mem']/(1024*1024))])
#    return (cpu_data,memory_data)

def convert_to_csv(file):
   print "hi"
   fd = open(file,'r'); 
   lines = fd.readlines()
   fd.close()
   csvfd = open('file'+'.csv','w')
   fieldnames = ["create_time","get_cpu_percent","get_io_counters", "get_memory_info","name"]
   writer = csv.DictWriter(csvfd,fieldnames=fieldnames,extrasaction='ignore')
   writer.writeheader()
   for line in lines:
       process = json.loads(line)
       print process
       print 'hi'
       writer.writerow (process)
   csvfd.close()


if  __name__ == "__main__":
	parse(sys.argv[1])

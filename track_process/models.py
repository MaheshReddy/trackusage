from django.db import models
import numpy as np

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class SampleRun_manager(models.Manager):
    def to_json(self):
        run_display_keys = ['name', 'tags', 'select']
	form_str='<div class="checkbox"> <label> <input type="checkbox" name="runid" value="replace"></label> </div>'
	data = [dict({str(xs):str(x[xs]) for xs in x.keys() if xs in run_display_keys}.items() + {'select':form_str.replace("replace",str(x['id']))}.items()) \
			for x in self.values()]
	return {'columns':run_display_keys, \
	        'data': data}
    def charts_data(self,ids):
        chart_data = {}
        cpu_data = [] 
	mem_data = []
        y_labels = []
	y_keys = []
	for id_count in xrange(0,len(ids)):
	    (cpu,mem) = Run_Record.objects.charts_data(ids[id_count])
	    y_labels.append(str(self.filter(id=ids[id_count]).values('name')[0]['name']))
	    y_keys.append(('y'+str(id_count)))
	    for count in xrange(0,len(cpu)):
                try:
	            cpu_data[count] = dict(cpu_data[count].items() + {('y'+str(id_count)):cpu[count]}.items() + {'x':count}.items())
		    mem_data[count] = dict(mem_data[count].items() + {('y'+str(id_count)):mem[count]}.items() + {'x':count}.items())
		except:
		    cpu_data.append((dict({'y0':cpu[count]}.items() + {'x':count}.items())))
		    mem_data.append((dict({'y0':mem[count]}.items() + {'x':count}.items())))
        chart_data['cpu_data']=cpu_data
        chart_data['mem_data']=mem_data
	chart_data['y_labels']=y_labels
	chart_data['y_keys']=y_keys
	print y_labels,y_keys
	return chart_data



class SampleRun(models.Model):
    name = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    date = models.DateField()
    objects = SampleRun_manager()
    def __str__(self):
        return self.name



class Run_Record_manager(models.Manager):
    def charts_data(self,run_id):
       cpu_data= [] 
       memory_data = []
       rsts = self.filter(sample_run_id=run_id).values('total_cpu',
		       'total_mem','run_time')
       for  rst in rsts:
           #cpu_data.append({'x':str(rst['run_time']), 'y':rst['total_cpu']})
	   #memory_data.append({'x':str(rst['run_time']), 'y':rst['total_mem']/(1024*1024)})
           cpu_data.append(rst['total_cpu'])
	   memory_data.append(rst['total_mem']/(1024*1024))
       compress_cpu_data = [ (np.mean(x)) for x in np.array_split(np.array(cpu_data), 
	                     len(cpu_data)/6)]
       compress_mem_data = [ np.mean(x) for x in np.array_split(np.array(memory_data), 
	                     len(memory_data)/6)]

       return (compress_cpu_data,compress_mem_data)

class Run_Record(models.Model):
	run_time = models.IntegerField()
	total_mem= models.IntegerField()
	total_cpu= models.IntegerField()
	total_vmem=models.IntegerField()
	sample_run = models.ForeignKey('SampleRun')
	objects = Run_Record_manager()
	def __str__(self):
		return "Nothing here"

class Process_Record(models.Model):
	create_time = models.FloatField()
	cpu_percent = models.FloatField()
	name = models.CharField(max_length=200)
	cmd_line = models.CharField(max_length=500)
	mem_info = models.CommaSeparatedIntegerField(max_length=50)
	run_record = models.ForeignKey('Run_Record')
	def _str__(self):
		return self.name

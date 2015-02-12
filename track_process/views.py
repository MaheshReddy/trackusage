from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse

from track_process.models import Question,SampleRun

from track_process.parse_json import *


run_display_keys = ['name', 'tags', 'time_unit', 'date', 'path', u'id']

# Create your views here.

def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    chart_data = SampleRun.objects.charts_data([1])
    context = { 'cpu_data': chart_data['cpu_data'], 
		'mem_data':chart_data['mem_data'],
		'y_labels':chart_data['y_labels'],
		'y_keys':chart_data['y_keys'],
		'run_data':SampleRun.objects.to_json()}
    #print data;
    #print sample_run_data
    #print SampleRun.objects.to_json()
    return render(request,'track_process/index.html',context)

def details(request,question_id):
   question = get_object_or_404(Question, pk=question_id)
   return render(request,'track_process/details.html',{'question':question});

def charts(request):
    runids = request.GET.getlist('runid')
    print runids
    chart_data = SampleRun.objects.charts_data(runids)
    context = { 'cpu_data': chart_data['cpu_data'], 
		'mem_data':chart_data['mem_data'],
		'y_labels':chart_data['y_labels'],
		'y_keys':chart_data['y_keys'],
		'run_data':SampleRun.objects.to_json()}
    return render(request,'track_process/index.html',context)

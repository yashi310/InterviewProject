from django.shortcuts import render,redirect
from . models import *
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy,reverse
from . forms import *
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

# Create your views here.

class ParticipantRegister(CreateView):
	model=Member
	fields= ['name','resume','email']
	template_name='SchedulerApp/index.html'
	success_url=reverse_lazy('interview-create')

	def form_valid(self,form):
		form.instance.user= self.request.user
		return super(ParticipantRegister,self).form_valid(form)

class InterviewCreate(CreateView,ListView):
	model= Interview
	form_class = CreateForm
	context_object_name = 'interviews'
	template_name= 'SchedulerApp/index.html'
	success_url=reverse_lazy('interview-create')

	def form_valid(self,form):
		form.instance.user= self.request.user
		start=form.cleaned_data['start']
		end=form.cleaned_data['end']
		members = form.cleaned_data['members']
		if (len(members)>=2):
			lis=[]
			for i in members:
				c=Interview.objects.filter(start__range=(start,end),end__range=(start,end),members=i)
				d=Interview.objects.filter(start__lte=start,end__range=(start,end),members=i)
				e=Interview.objects.filter(start__range=(start,end),end__gte=end,members=i)
				f=Interview.objects.filter(start__lte=start,end__gte=end,members=i)
				if(c or d or e or f):
					lis.append(i)
			if lis:
				for participant in lis:
					messages.info(self.request,"Participant " + str(participant) + " is already busy in another interview schedule! ")
				return redirect('interview-create')	
			else:
				for p in members:
					subject = "Interview Schedule" 
					body = {
					    'Interview message': "Your inteview has been scheduled for this respective time.We request you to be present on time. ",
						'Interview start time': str(form.cleaned_data['start']), 
						'Interview End time': str(form.cleaned_data['end']), 
					}
					message = "\n".join(body.values())
					try:
						send_mail(subject, message, 'shrey.agarwal343@gmail.com', [p.email]) 
					except BadHeaderError:
						return HttpResponse('Invalid header found.')		
				return super(InterviewCreate,self).form_valid(form)
		messages.info(self.request,'Atleast 2 participants')
		return redirect('interview-create')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		queryset = super().get_queryset().values_list(flat=True)	
		context['interviews']=context['interviews']
		context['count'] = context['interviews'].count()
		return context

class DeleteView(DeleteView):
	model = Interview
	context_object_name='interview'
	success_url=reverse_lazy('interview-create')

class Update(UpdateView):
	model = Interview
	fields = ['start','end','members']
	template_name = 'SchedulerApp/index.html'
	success_url= reverse_lazy('interview-create')




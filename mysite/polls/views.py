from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Question, Choice

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template_url = 'polls/index.html'
	# template = loader.get_template(template_url)
	context = {'latest_question_list': latest_question_list,}

	# output = ', '.join([q.question_text for q in latest_question_list])
	# return HttpResponse(template.render(context, request))

	return render(request, template_url, context)

def detail(request, question_id):
	try:
		# question = Question.objects.get(pk=question_id)
		question = get_object_or_404(Question, pk=question_id) ## shortcut
	except Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question= get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice']) # 뷰에서 전송한 choice number
	except(KeyError, Choice.DoesNotExists):
		# Choice Key가 DB에 존재하는 데이터가 아닐 경우
		return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
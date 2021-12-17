from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

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
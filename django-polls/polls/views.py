from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from polls.models import Choice, Poll

class IndexView(generic.ListView):
	template_name = 'polls/index.jade'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		"""Return the last five published polls."""
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.jade'

	def get_queryset(self):
		return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.jade'


def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.jade', {
			'poll': p,
			'error_message': "You didn't select a choice"
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse(
			'polls:results',
			args=(p.id,)
		))


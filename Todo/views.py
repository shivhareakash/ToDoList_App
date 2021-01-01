from django.shortcuts import render, redirect
from django.utils import timezone
# Create your views here.
from django.http import HttpResponseRedirect
from .models import TodoDB
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404


def homepage(request):
    return render(request, 'todo/homepage.html')



class list(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name ='context'

    def get_queryset(self):
        all_item = TodoDB.objects.filter(owner=self.request.user).order_by('-date_added')
        return all_item

@login_required
def add_item(request):
    item_name=TodoDB.objects.create(item_text=request.POST['item'], date_added=timezone.now(), owner=request.user)
    item_name.save()
    print("Message from the view function- created item with item id: "+ str(item_name.id))
    return redirect('todo:list')

@login_required
def delete_item(request, item_id):
    if TodoDB.objects.get(id=item_id).owner==request.user:
        TodoDB.objects.get(id=item_id).delete()
    else:
        raise Http404
    return redirect('todo:list')
#if redirect to a view needed some arguments, they could be passed like this
# return redirect(viewArticles, year = "2045", month = "02")


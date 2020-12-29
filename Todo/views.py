from django.shortcuts import render, redirect
from django.utils import timezone
# Create your views here.
from django.http import HttpResponseRedirect
from .models import TodoDB
from django.views import generic


# def home(request):
#     all_item = TodoDB.objects.all().order_by('-date_added')
#     return render(request, 'todo/index.html', {'context': all_item})

class home(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name ='context'

    def get_queryset(self):
        all_item = TodoDB.objects.all().order_by('-date_added')
        return all_item


def add_item(request):

    item_name=TodoDB.objects.create(item_text=request.POST['item'], date_added=timezone.now())
    item_name.save()
    print(item_name.id)
    return redirect('todo:home')


def delete_item(request, item_id):
    TodoDB.objects.get(id=item_id).delete()

    return redirect('todo:home')

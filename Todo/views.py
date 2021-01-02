from django.shortcuts import render, redirect
from django.utils import timezone
# Create your views here.
from django.http import HttpResponseRedirect
from .models import TodoDB
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

def homepage(request):
    return render(request, 'todo/homepage.html')



# @login_required ---We can't use the login_required decorator on a class like that. We need to use method_decorator or pass LoginRequiredMixin
# When using class-based views, you can achieve the same behavior as with login_required by using the LoginRequiredMixin. This mixin should be at the leftmost position in the inheritance list.

# @method_decorator(login_required, name='dispatch')
class list(LoginRequiredMixin, generic.ListView):

    template_name = 'todo/index.html'
    context_object_name ='context'

    def get_queryset(self):
        all_item = TodoDB.objects.filter(owner=self.request.user).order_by('-date_added')
        return all_item


@login_required
# //login_required(redirect_field_name='next', login_url=None)
#login_required redirects the non-logged in user to the page passed in its login_url argument or whatever we have defined in settings.py >>LOGIN_URL
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


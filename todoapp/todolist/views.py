from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import TodoList, TodoItem


class OverviewView(generic.ListView):
    template_name = 'todolist/overview.html'
    context_object_name = 'all_todo_list'

    def get_queryset(self):
        return TodoList.objects.order_by('title')


class DetailView(generic.DetailView):
    model = TodoList
    template_name = 'todolist/detail.html'


class NoticeView(generic.DetailView):
    model = TodoList
    template_name = 'todolist/notice.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        print(context)
        return context


def todo_complete(request, todolist_id):
    todo_list = get_object_or_404(TodoList, pk=todolist_id)
    task_count = len(todo_list.todoitem_set.filter(is_completed=False))
    completed_list = (request.POST.getlist('todo'))
    x = 0
    for i in completed_list:
        # Update item is_completed attribute
        try:
            selected_item = todo_list.todoitem_set.get(pk=int(i))

        except (KeyError, TodoItem.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'todolist/detail.html', {
                'todo_list': todo_list,
                'error_message': "You didn't select an item.",
            })
        else:

            if selected_item.is_completed == False:
                x += 1

            selected_item.is_completed = True
            selected_item.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    # Update # of completed items inside the db at TodoLists completed attribute
    todo_list.completed += x
    todo_list.save()
    if len(completed_list) == task_count:
        message = "Congratulations, you completed all items in the list!"
    else:
        message = f"You completed {len(completed_list)} out of {task_count} items in the list."
    reversed_url = reverse('todolist:notice', args=(todolist_id,))
    return redirect(reversed_url, {'message': message})
    # return HttpResponseRedirect(reverse('todolist:notice', args=(todolist_id,)), {'message': message})


def clear_all(request):
    # todo_list = get_object_or_404(TodoList, pk=todolist_id)
    my_items = TodoItem.objects.all()

    for i in my_items:
        i.is_completed = False
        i.save()

    my_lists = TodoList.objects.all()

    for l in my_lists:
        l.completed = 0
        l.save()
    print("All items have been cleared")
    return HttpResponseRedirect(reverse('todolist:overview'))

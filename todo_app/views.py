from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import ToDoItem, ToDoList


def is_admin(user):
    return user.is_superuser


class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"


class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context


class ListCreate(UserPassesTestMixin, CreateView):
    model = ToDoList
    fields = ["title"]
    template_name = "todo_app/todo_list_form.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить новый список"
        return context


class ItemCreate(UserPassesTestMixin, CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]
    template_name = "todo_app/todo_item_form.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Создать новую запись"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ItemUpdate(UserPassesTestMixin, UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]
    template_name = "todo_app/todo_item_form.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        context["title"] = "Редактировать запись"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(UserPassesTestMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")
    template_name = "todo_app/todo_list_confirm_delete.html"

    def test_func(self):
        return is_admin(self.request.user)


class ItemDelete(UserPassesTestMixin, DeleteView):
    model = ToDoItem
    template_name = "todo_app/todo_item_confirm_delete.html"

    def test_func(self):
        return is_admin(self.request.user)

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context

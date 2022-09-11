from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from LMS.models import Book
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

# Create your views here.

# Login view was customised just a little bit and inbuilt django login form was used.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('books')

# Inbuilt Register Form was used.
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

class BooksView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['books'] = context['books'].filter(name__icontains=search_input).values()
        context['search_input'] = search_input
        return context


class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'isbn', 'authors','publisher']
    template_name = 'addbook.html'
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddBookView, self).form_valid(form)


# View that executes in Edit Tab.
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'updatebook.html'
    fields = ['name', 'isbn', 'authors','publisher']
    success_url = reverse_lazy('books')

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    context_object_name = 'book'
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('books')

    
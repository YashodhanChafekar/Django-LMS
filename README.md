# Django-LMS
## This is Library Management System Based on Django.

* This Project uses Django, MySQL, Django-ORM and HTML,CSS,JAVASCRIPT.
* Project can be used for two types of users,1) Admin : Able to perform CRUD operations on Books. 2) Student: Able to view books and search by title.
* To perform CRUD operations admin can login or Register using email and password. (Created by Custom User Implementation.)
### Login Page
![LoginPage](https://user-images.githubusercontent.com/108964197/189505894-21dd77b2-0b0d-4430-982b-ef1df9cde32c.png)
### Register Page
![RegisterPage](https://user-images.githubusercontent.com/108964197/189505904-4fff05b2-a305-4cc1-a578-d26a5500d73e.png)
### Landing Page by Admin
![Landing Page](https://user-images.githubusercontent.com/108964197/189505918-dce29c53-a15c-4ad7-a65b-7dff658d3611.png)
### Student View (No Login Required)
![StudentView](https://user-images.githubusercontent.com/108964197/189505930-b777f123-d68d-487e-b952-5310296d40e4.png)
### Search By Title
![SearchByTitle](https://user-images.githubusercontent.com/108964197/189505936-a1a590e6-5ca4-4108-aec5-b4fe10302bea.png)
### Add Book form.
![AddBook](https://user-images.githubusercontent.com/108964197/189505954-c62f9c05-5f5a-49cb-a192-48f7af810348.png)
### Update Book
![UpdateBook](https://user-images.githubusercontent.com/108964197/189505963-cebbd648-7214-409d-a7be-c6d1a6be192a.png)
### Delete Book 
![DeleteBook](https://user-images.githubusercontent.com/108964197/189505972-be0c5966-7e45-4fae-8b4b-8ccf6937fa95.png)
### MySQL Tables
![MySQLAdmin](https://user-images.githubusercontent.com/108964197/189506012-35d59010-f7df-425d-b639-277c947d17b7.png)
![MySQLBooks](https://user-images.githubusercontent.com/108964197/189506016-e9c198b9-d1e3-414d-baf5-62f4172cb63c.png)

---
# Backend Code Documentation.
### Important Concepts.
* Creating Custom User by inheriting base functionality.
* Creating Search By Result.
* Usage of Inbuilt CRUD Class Based Views.

## Creating Custom User.
``` Python
class Admin(AbstractBaseUser, PermissionsMixin):
    username = None  
    email = models.EmailField(_('email_address'), unique=True, max_length = 200)  
    date_joined = models.DateTimeField(auto_now_add=True)  
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True) 


    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []


    objects = CustomAdminManager()
 ```
 * This is Custom class used in this project. 
 * It inherits from AbstractBaseUser. For unabling user to login through email we are creating our custom class. There is also Book model which has usual implementation of a model and its fields.
 * USERNAME_FIELD = 'email' --> Now will be unique for every user. REQUIRED_FIELDS --> Fields that are must not be kept blank for superuser creation.
 * is_staff --> If true, then perticular user can login to admin panel.
 
 ### Creating Custom Manager file.
 ```Python 
 class CustomAdminManager(BaseUserManager):  

    def create_user(self, email, password, **extra_fields):  
        if not email:  
            raise ValueError(_('The Email must be set'))  
        email = self.normalize_email(email)  
        user = self.model(email=email, **extra_fields)  
        user.set_password(password)  
        user.save()  
        return user  
  
    def create_superuser(self, email, password, **extra_fields):  
        extra_fields.setdefault('is_staff', True)  
        extra_fields.setdefault('is_superuser', True)  
        extra_fields.setdefault('is_active', True)  
  
        if extra_fields.get('is_staff') is not True:  
            raise ValueError(_('Superuser must have is_staff=True.'))  
        if extra_fields.get('is_superuser') is not True:  
            raise ValueError(_('Superuser must have is_superuser=True.'))  
        return self.create_user(email, password, **extra_fields)  
 ```
 * For creating user and superuser. 
 * The methods create_user and create_superuser have to be customised as well to accept newly formed email and password fields.
 This is actual operation making django admin panel use our customised way of user creation.
 After This step we can craete a superuser with email and passsword.
 * As shown above is_staff ad is_active will be true for superuser.
 * Superuser can then edit other user's is_staff to allow him log in to admin panel.
 * Here we can initialize our superuser with "python manage.py createsuperuser" with email and password fields.
  ### Creating Custom forms for Admin using inbuilt functionality.
 ```Python
 class CustomUserCreationForm(UserCreationForm):  
  
    password1 = forms.CharField(widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)  

  
    class Meta:  
        model = Admin  
        fields = ('email', )  
      
    def clean_email(self):  
        email = self.cleaned_data.get('email')  
        qs = User.objects.filter(email=email)  
        if qs.exists():  
            raise forms.ValidationError("Email is taken")  
        return email  
  
    def clean(self):  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")  
        password2 = cleaned_data.get("password2")  
          
        if password1 is not None and password1 != password2:  
            self.add_error("password2", "Your passwords must match")  
        return cleaned_data  
  
    def save(self, commit=True):  
        # Save the provided password in hashed format  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])  
        if commit:  
            user.save()  
        return user          
      
  
class CustomUserChangeForm(UserChangeForm):  
    class Meta:  
        model = Admin  
        fields = ('email',)  
  
    def clean_password(self):  
        # Regardless of what the user provides, return the initial value.  
        # This is done here, rather than on the field, because the  
        # field does not have access to the initial value  
        return self.initial["password1"] 
 ```
* The Admin is custom class which can login with email making it essential to create forms and associated fields according to our custom class. 
 New forms will mak sure that the email and password fields are used everywhere along with Admin functionality.
### Updating admin.py file to get changes done.
```Python
class CustomUserAdmin(UserAdmin):  
    add_form = CustomUserCreationForm  
    form = CustomUserChangeForm  
    model = Admin  
  
    list_display = ('email', 'is_staff', 'is_active',)  
    list_filter = ('email', 'is_staff', 'is_active',)  
    fieldsets = (  
        (None, {'fields': ('email', 'password')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()  
```
* Here mainly, we will have to add the custom user creation form. Now we will be able to filter with our customised parameters.
Also while creating new user through admin panel and while creating superuser we will user email and password fields now.
---
# CRUD Operations thorugh inbuilt Views.
### Listing all books from Database.(ListView) 
```Python
class BooksView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books.html'
```
* This is simple builtin list view. 
* model is database table we want to list.
* Context_object_name gives us ability to name all queries in model stated together. (Book is model of books. So now in HTML file we can call for loop on books to list all. )
* template_name is html template we are going to use for this list of books.
#### Searching in ListView.
```Python
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['books'] = context['books'].filter(name__icontains=search_input).values()
        context['search_input'] = search_input
        return context
```
* This is method under ListView above.
* On HTML template search form is used. "self.request.GET.get('search-area')" gets data from that HTML form on books page.
### CreateView
```Python
class AddBookView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'isbn', 'authors','publisher']
    template_name = 'addbook.html'
    success_url = reverse_lazy('books')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddBookView, self).form_valid(form)
```
* LoginRequiredMixin allows user to access perticular function only if he is logged in.
* CreateView let us create form directly without having to code one.
* we can add fields we want and also a success url. 
* form_valid is method to perform form validation.
* This view is so helpful that is manages fields, field labels, errors etc.
* UpdateView works same way.
* Django automatically allocates ids to form fields.
* For styling these forms, individual ids of form fields can be accessed using Chrome Dev Tools. In project the forms are styled by aceessing ids.

### Update, Delete Views.
```Python 
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
```
* Used to update and delete.
### Register and Login Views
```Python
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('books')
        
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
```
* These work in similar ways to create view. Here Login and Register forms are autogenerated and are managed for errors and field names.
---
### Urls 
```Python
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page = 'books'), name='logout'),
    path('', BooksView.as_view(), name='books' ),
    path('add-book', AddBookView.as_view(), name='add-book'),
    path('update-book/<int:pk>/', BookUpdateView.as_view(), name='update-book'),
    path('delete-book/<int:pk>/', BookDeleteView.as_view(), name='delete-book'),
```
* These are paths used for urls.py. Every path can be named and accessed in HTML using DTL which makes routing fun.


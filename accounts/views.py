from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from accounts.forms import SiteUserCreationForm

# Create your views here.
class SignupView(SuccessMessageMixin, CreateView):
    """Create a new user"""
    model = get_user_model()
    form_class = SiteUserCreationForm
    template_name = 'registration/signup.html'

    success_url = reverse_lazy('login')
    success_message = 'Your profile was created successfully'

    extra_context = {'page_title': 'Sign Up'}

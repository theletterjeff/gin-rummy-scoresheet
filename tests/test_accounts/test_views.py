import urllib.parse

from django.urls import reverse

from accounts.views import SignupView
from accounts.models import Player

def test_signup_view_get(rf):
    """Submitting a GET request to the signup view returns a response with 
    status code 200 and uses the correct template.
    """
    url = reverse('accounts:signup')
    view = SignupView.as_view()

    request = rf.get(url)
    response = view(request)

    assert response.status_code == 200
    assert response.template_name == ['registration/signup.html']

def test_signup_view_post(client, transactional_db):
    """Submitting a POST request to the signup view with username and password 
    returns status code 201.
    """
    url = reverse('accounts:signup')
    data = urllib.parse.urlencode({
        'username': 'player0',
        'password1': 'test_password',
        'password2': 'test_password',
        'email': 'player0@gmail.com',
    })
    content_type = 'application/x-www-form-urlencoded'
    response = client.post(url, data, content_type=content_type)

    assert response.status_code == 302
    assert response.url == '/accounts/login/'
    assert Player.objects.get(username='player0')

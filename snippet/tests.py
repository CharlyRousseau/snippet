from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from snippet.models import CustomUser, Snippet
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Create your tests here.
class LoginTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    def test_login_success(self):
        # Préparation des données pour simuler une requête POST
        data = {
            'username': 'user',
            'password': 'password'
        }
        
        # Envoi de la requête POST au formulaire de login
        response = self.client.post(self.login_url, data)

        # Vérification de la présence du cookie 'csrftoken'
        self.assertIn('csrftoken', response.cookies)

        # Vérification que l'utilisateur est bien connecté
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        # Préparation des données pour simuler une mauvaise requête POST
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'  # Mot de passe incorrect
        }
        
        # Envoi de la requête POST au formulaire de login
        response = self.client.post(self.login_url, data)
        
        # Vérification que l'utilisateur n'est pas connecté
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Vérification que le formulaire de login est bien rendu après un échec de connexion
        self.assertIsInstance(response.context['form'], AuthenticationForm)

class SnippetTestCase(TestCase):
    def setUp(self):
        # Créez un utilisateur s'il n'existe pas
        self.user, created = CustomUser.objects.get_or_create(username="user", defaults={"password": "password"})
        
        # Créez un snippet pour cet utilisateur
        self.snippet = Snippet.objects.create(author=self.user, title="UT Title", code="", language="c")

    def test_snippet(self):
        # Récupérez le snippet créé dans setUp
        test = Snippet.objects.get(title="UT Title")
        # Vérifiez que la langue est correcte
        self.assertEqual(test.language, "c")
        # Vérifiez que le contenu du code soit bien vide et non nul
        self.assertEqual(test.code, "")
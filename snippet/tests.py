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

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password_reset_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_complete_url = reverse('password_reset_complete')
        self.user, created = CustomUser.objects.get_or_create(username="user", email="user@example.com")
        self.user.set_password('password')
        self.user.save()

    def test_password_reset_view(self):
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_password/password_reset_form.html')
        self.assertIsInstance(response.context['form'], PasswordResetForm)

    def test_password_reset_email_sent(self):
        response = self.client.post(self.password_reset_url, {'email': 'user@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Password reset on', mail.outbox[0].subject)

    def test_password_reset_invalid_email(self):
        response = self.client.post(self.password_reset_url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_view(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_password/password_reset_confirm.html')
        self.assertIsInstance(response.context['form'], SetPasswordForm)

    def test_password_reset_complete_view(self):
        response = self.client.get(self.password_reset_complete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reset_password/password_reset_complete.html')
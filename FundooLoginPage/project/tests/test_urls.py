from django.test import SimpleTestCase
from django.urls import reverse, resolve
from snippets.views import Login, Registrations, ForgotPassword
from note.views import NoteList,LabelList

class TestUrls(SimpleTestCase):
    def test_login(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, Login)

    def test_registration(self):
        url = reverse('registration')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, Registrations)

    def test_forgotPassword(self):
        url = reverse('forgotPassword')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ForgotPassword)

    def test_note(self):
        url = reverse('note')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, NoteList)
    

    def test_label(self):
        url = reverse('label')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, LabelList)

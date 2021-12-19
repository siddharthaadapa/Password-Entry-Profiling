import datetime
import unittest

from flask_login import current_user

from project import db
from project.models import User
from project.util import BaseTestCase
from project.user.forms import RegisterForm, \
    LoginForm, ChangePasswordForm, ForgotForm
from project.token import generate_confirmation_token, confirm_token


class TestUserForms(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure correct data validates.
        form = RegisterForm(
            email='new@test.test',
            password='example', confirm='example')
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure incorrect data does not validate.
        form = RegisterForm(
            email='new@test.test',
            password='example', confirm='')
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = RegisterForm(
            email='test@user.com',
            password='just_a_test_user',
            confirm='just_a_test_user'
        )
        self.assertFalse(form.validate())

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='test@user.com', password='just_a_test_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())



class TestUserViews(BaseTestCase):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="test@user.com", password="just_a_test_user"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertTrue(current_user.email == "test@user.com")
            self.assertTrue(current_user.is_active())
            self.assertTrue(current_user.is_authenticated())
            self.assertTemplateUsed('main/index.html')

    def test_incorrect_login(self):
        # Ensure login behaves correctly with incorrect credentials.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="not@correct.com", password="incorrect"),
                follow_redirects=True
            )
            self.assertTrue(response.status_code == 200)
            self.assertIn(b'Invalid email and/or password.', response.data)
            self.assertFalse(current_user.is_active())
            self.assertFalse(current_user.is_authenticated())
            self.assertTemplateUsed('user/login.html')

    def test_profile_route_requires_login(self):
        # Ensure profile route requires logged in user.
        self.client.get('/profile', follow_redirects=True)
        self.assertTemplateUsed('user/login.html')




if __name__ == '__main__':
    unittest.main()
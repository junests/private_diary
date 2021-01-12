from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ..models import Diary


class LoggedInTestCase(TestCase):


    def setUp(self):
        # preset before test method execution
        self.password = '<ログインパスワード>'
        self.test_user = get_user_model().objects.create_user(
            username = 'django',
            email = 'django@test.com',
            password = self.password,
        )
        self.client.login(email=self.test_user.email, password=self.password)


class TestDiaryCreateView(LoggedInTestCase):
    # for DiaryCreateView

    def test_create_diary_success(self):
        # Verify that the diary creation process succeeds
        params = {'title': 'テストタイトル',
                  'content': '本文',
                  'photo1': '',
                  'photo2': '',
                  'photo3': ''}

        response = self.client.post(reverse_lazy('diary:diary_create'), params)
        self.assertRedirects(response, reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(title='テストタイトル').count(), 1)

    def test_create_diary_failure(self):
        # Verify that the diary creation process failure
        response = self.client.post(reverse_lazy('diary:diary_create'))
        self.assertFormError(response, 'form', 'title', 'このフィールドは必須です。')


class TestDiaryUpdateView(LoggedInTestCase):
    # for DiaryUpdateView

    def test_update_diary_success(self):
        # Verify that the diary editing process succeeds
        diary = Diary.objects.create(user=self.test_user, title='タイトル編集前')
        params = {'title': 'タイトル編集後'}

        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': diary.pk}), params)
        self.assertRedirects(response, reverse_lazy('diary:diary_detail', kwargs={'pk': diary.pk}))
        self.assertEqual(Diary.objects.get(pk=diary.pk).title, 'タイトル編集後')

    def test_update_diary_failure(self):
        # Verify that the diary editing process failure
        response = self.client.post(reverse_lazy('diary:diary_update', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class TestDiaryDeleteView(LoggedInTestCase):
    # for DiaryDeleteView

    def test_delete_diary_success(self):
        # Verify that the diary deleting process succeeds
        diary = Diary.objects.create(user=self.test_user, title='タイトル')
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': diary.pk}))

        self.assertRedirects(response, reverse_lazy('diary:diary_list'))
        self.assertEqual(Diary.objects.filter(pk=diary.pk).count(), 0)

    def test_delete_diary_failure(self):
        # Verify that the diary deleting process failure
        response = self.client.post(reverse_lazy('diary:diary_delete', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

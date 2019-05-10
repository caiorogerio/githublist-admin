from unittest.mock import patch

from django.test import TestCase
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AnonymousUser

from .models import Language, Repository, User, ImportedModel, remote_values
from .signals import get_github_data
from .services import get_repositories
from .auto_auth import AnonymousSuperUser, Middleware


class MockGithubRequest(TestCase):
    def setUp(self):
        patcher = patch('github.services.requests.get')
        self.addCleanup(patcher.stop)
        self.mock_requests_get = patcher.start()

        _parent = self

        class MockRequests:
            def json(self):
                language = _parent.mock_requests_get.call_args[1]['params']['q'].split(':')[1]

                return {
                    'items': _parent._get_return_value(language)
                }

        self.mock_requests_get.return_value = MockRequests()

    @staticmethod
    def _get_return_value(language):
        user_laravel = {
            'id': 1,
            'login': 'laravel',
            'avatar_url': 'https://avatars3.githubusercontent.com/u/958072?v=4',
        }

        mocked_responses = {
            'php': [
                {
                    'id': 1,
                    'name': 'laravel',
                    'language': 'php',
                    'owner': user_laravel,
                },
                {
                    'id': 2,
                    'name': 'framework',
                    'language': 'php',
                    'owner': user_laravel,
                }
            ],
            'python': [
                {
                    'id': 3,
                    'name': 'django',
                    'language': 'python',
                    'owner': {
                        'id': 2,
                        'login': 'django',
                        'avatar_url': 'https://avatars2.githubusercontent.com/u/27804?v=4',
                    }
                }
            ]
        }

        return mocked_responses[language]


# Tests for mocking requests
class MockingServiceTestCase(MockGithubRequest):
    def test_request_case_insensitive(self):
        self.assertListEqual(get_repositories('php'), get_repositories('PHP'))

    def test_request_language_php(self):
        repos = get_repositories('php')
        self.assertEqual(len(repos), 2)

    def test_request_language_python(self):
        repos = get_repositories('python')
        self.assertEqual(len(repos), 1)


# Tests for models
class ModelManipulatingLanguagesTestCase(MockGithubRequest):
    def test_create_language(self):
        Language.objects.create(name='PHP')
        Language.objects.create(name='Python')

        self.assertEqual(Language.objects.count(), 2)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Repository.objects.count(), 3)

        self.assertEqual(User.objects.get(name='laravel').repositories.count(), 2)
        self.assertEqual(User.objects.get(name='django').repositories.count(), 1)

        self.assertEqual(Language.objects.get(name='PHP').repositories.count(), 2)
        self.assertEqual(Language.objects.get(name='Python').repositories.count(), 1)

    def test_update_language(self):
        language = Language.objects.create(name='PHP')

        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.get().name, 'PHP')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'laravel')
        self.assertEqual(Repository.objects.count(), 2)

        language.name = 'Python'
        language.save()

        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.get().name, 'Python')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'django')
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, 'django')

    def test_delete_language(self):
        language = Language.objects.create(name='PHP')

        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(Language.objects.get().name, 'PHP')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'laravel')
        self.assertEqual(Repository.objects.count(), 2)

        language.delete()

        self.assertEqual(Language.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Repository.objects.count(), 0)


class ModelTranslatingTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        @remote_values({
            'name': 'login',
            'avatar': 'avatar_url',
        })
        class TestImportedModel(ImportedModel):
            pass

        cls.TestImportedModel = TestImportedModel

    @classmethod
    def tearDownClass(cls):
        pass

    def test_translation_from_datasource_without_id(self):
        self.assertDictEqual(self.TestImportedModel.translate({
            'login': 'django',
            'avatar_url': 'https://avatars2.githubusercontent.com/u/27804?v=4',
        }), {
            'name': 'django',
            'avatar': 'https://avatars2.githubusercontent.com/u/27804?v=4',
        }, 'Testing origin data without id')

    def test_translation_from_datasource_with_id(self):
        self.assertDictEqual(self.TestImportedModel.translate({
            'id': 1,
            'login': 'django',
            'avatar_url': 'https://avatars2.githubusercontent.com/u/27804?v=4',
        }), {
            'id': 1,
            'name': 'django',
            'avatar': 'https://avatars2.githubusercontent.com/u/27804?v=4',
        }, 'Testing origin data with id')


# Tests for signals
class SignalsTestCase(MockGithubRequest):
    @staticmethod
    def create_language(**kwargs):
        post_save.disconnect(get_github_data, sender=Language)
        language = Language.objects.create(**kwargs)
        post_save.connect(get_github_data, sender=Language)

        return language

    @staticmethod
    def exec_without_signals(func):
        post_save.disconnect(get_github_data, sender=Language)
        ret = func()
        post_save.connect(get_github_data, sender=Language)

        return ret


    def test_language_creation(self):
        language = self.exec_without_signals(lambda: Language.objects.create(name='PHP'))
        post_save.send(Language, instance=language, created=True)

        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Repository.objects.count(), 2)

        self.assertEqual(User.objects.get(name='laravel').repositories.count(), 2)

        self.assertEqual(Language.objects.get(name='PHP').repositories.count(), 2)

    def test_language_update(self):
        language = self.exec_without_signals(lambda: Language.objects.create(name='PHP'))
        language.name = 'Python'
        self.exec_without_signals(lambda: language.save())

        post_save.send(Language, instance=language, created=False)

        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Repository.objects.count(), 1)

        self.assertEqual(User.objects.get(name='django').repositories.count(), 1)

        self.assertEqual(Language.objects.get(name='Python').repositories.count(), 1)

    def test_language_delete(self):
        language = self.exec_without_signals(lambda: Language.objects.create(name='PHP'))
        post_save.send(Language, instance=language, created=True)
        self.exec_without_signals(lambda: language.delete())

        self.assertEqual(Language.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Repository.objects.count(), 0)


# Admin tests
class AdminTestCase(TestCase):
    def test_anonymous_superuser_authorization(self):
        user = AnonymousSuperUser()

        self.assertTrue(user.has_module_perms('github'))
        self.assertFalse(user.has_module_perms('other'))

        self.assertTrue(user.has_perm('github.view_language'))
        self.assertTrue(user.has_perm('github.view_repository'))
        self.assertFalse(user.has_perm('github.view_user'))

        self.assertFalse(user.has_perm('github.create_language'))
        self.assertFalse(user.has_perm('github.create_repository'))
        self.assertFalse(user.has_perm('github.create_user'))

        self.assertTrue(user.has_perms(['github.view_language', 'github.view_repository']))
        self.assertFalse(user.has_perms(['github.view_language', 'github.view_user']))
        self.assertFalse(user.has_perms(['github.create_language', 'github.create_repository']))

    def test_middleware_in_login_page(self):
        middleware = Middleware()
        anonymous = AnonymousUser()
        super_anonymous = AnonymousSuperUser()
        known = User()

        class MockRequest:
            path = None
            user = None
            _cached_user = None

        request = MockRequest()

        # Tests for login page
        request.path = '/login/'

        # Responds normal anonymous for show login page, except logged
        request._cached_user = anonymous
        middleware.process_request(request)
        self.assertEquals(request.user, anonymous)

        request._cached_user = super_anonymous
        middleware.process_request(request)
        self.assertEquals(request.user, anonymous)

        request._cached_user = known
        middleware.process_request(request)
        self.assertEquals(request.user, known)

        # Tests for login page
        request.path = '/github/language/'

        # Responds super anonymous for all other pages, except logged
        request._cached_user = anonymous
        middleware.process_request(request)
        self.assertEquals(request.user, super_anonymous)

        request._cached_user = super_anonymous
        middleware.process_request(request)
        self.assertEquals(request.user, super_anonymous)

        request._cached_user = known
        middleware.process_request(request)
        self.assertEquals(request.user, known)
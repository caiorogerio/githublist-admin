from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve


class AnonymousSuperUser(AnonymousUser):
    is_superuser = False
    is_active = True
    is_staff = True
    is_anonymous_superuser = True

    __perms = {
        'github': ('view_language', 'view_repository',)
    }

    def __split_perm(self, perm):
        return tuple(perm.split('.'))

    def has_perm(self, perm, obj=None):
        module, perm = self.__split_perm(perm)
        return perm in self.__perms[module]

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm):
                return False

        return True

    def has_module_perms(self, module):
        return module in self.__perms.keys()


class Middleware(MiddlewareMixin):
    def process_request(self, request):
        user = get_user(request)

        # Changes for custom anonymous user when not accessing login page
        if isinstance(user, AnonymousUser):
            if resolve(request.path).view_name == 'admin:login':
                user = AnonymousUser()
            else:
                user = AnonymousSuperUser()

        request.user = user

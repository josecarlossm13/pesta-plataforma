from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


# decorador para limitar acesso
def user_has_access():
    """
    Permite acesso apenas a utilizadores autenticados que não estão no grupo 'SemAcesso'
    """
    def check(user):
        return user.is_authenticated and not user.groups.filter(name="SemAcesso").exists()
    return user_passes_test(check, login_url="/accounts/account/")


class GroupAccessRequiredMixin(UserPassesTestMixin):
    """
    Permite acesso apenas a utilizadores autenticados e que NÃO estão no grupo 'SemAcesso'
    """
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and not user.groups.filter(name="SemAcesso").exists()

    login_url = "/accounts/account/"

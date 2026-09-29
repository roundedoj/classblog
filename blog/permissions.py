from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def is_author(user):
    """True for the admin (superuser) and anyone in the 'Authors' group."""
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='Authors').exists()
    )


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Anonymous -> login page. Logged in but not an author -> 403 Forbidden."""

    def test_func(self):
        return is_author(self.request.user)


class PostOwnerMixin(AuthorRequiredMixin):
    """Only the post's own author (or the admin) may edit or delete it."""

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return is_author(user) and (post.author_id == user.pk or user.is_superuser)
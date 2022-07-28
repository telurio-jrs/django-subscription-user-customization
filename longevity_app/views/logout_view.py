from django.shortcuts import redirect
from django.views import View


class LogoutView(View):
    def get(self, *args, **kwargs):
        return redirect('longevity_app:index')

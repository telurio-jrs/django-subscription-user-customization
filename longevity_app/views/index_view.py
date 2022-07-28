import calendar
import time

from db.library.utils.auth import auth
from db.models import User
from django.shortcuts import redirect, render
from django.views import View
from longevity_app.forms.index_form import IndexForm


class IndexView(View):
    def get(self, *args, **kwargs):
        context = {}
        if 'success' in self.request.session:
            context['success'] = self.request.session.get('success')
            del self.request.session['success']
        elif 'error' in self.request.session:
            context['error'] = self.request.session.get('error')
            del self.request.session['error']
        return render(
            request=self.request,
            template_name='longevity_app/pages/index.html',
            context=context
        )

    def post(self, *args, **kwargs):
        form = IndexForm(data=self.request.POST)
        if form.is_valid():
            use_login = form.cleaned_data.get('use_login')
            use_password = form.cleaned_data.get('use_password')

            user = User.objects.get_user(use_login, use_password)
            payload = {
                'whoami': user.get('id'),
                'sub': user.get('use_login'),
                'iss': calendar.timegm(time.gmtime()),
                'exp': calendar.timegm(time.gmtime()) + 1800
            }
            self.request.session['auth'] = auth(payload=payload)
            self.request.session['success'] = 'You are logged in.'
            return redirect('longevity_app:dashboard')
        else:
            self.request.session['error'] = 'Invalid email or password.'
            return redirect('longevity_app:index')

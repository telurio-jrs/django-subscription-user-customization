import calendar
import logging
import os
import time

import jwt
from django.shortcuts import redirect

from db.library.utils.auth import auth


class TokenAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        process = self._process_request(request)
        if process:
            return process
        return self.get_response(request)

    def _process_request(self, request):
        tk_free_list = ['/', 'index']
        tk_not_required = [i for i in tk_free_list if i in request.path]
        if not tk_not_required:
            if 'auth' not in request.session:
                request.session['error'] = 'You are not authenticated.'
                return redirect('home:index')
            try:
                # check if credentials are up to date
                payload = jwt.decode(
                    jwt=request.session['auth'],
                    key=os.getenv('JWT_SECRET', 'INSECURE'),
                    algorithms=[os.getenv('JWT_ALGORITHM', 'INSECURE')]
                )
                # renew credentials
                payload['exp'] = calendar.timegm(time.gmtime()) + 1800
                request.session['auth'] = auth(payload=payload)
            except jwt.ExpiredSignatureError as err:
                logging.error(f'{err}')
                del request.session['auth']
                request.session['error'] = 'Your session has expired, please login.'  # noqa: E501
                return redirect('home:index')
            except jwt.InvalidTokenError as err:
                logging.error(f'{err}')
                del request.session['auth']
                request.session['error'] = 'Invalid token.'
                return redirect('home:index')
            except Exception as err:
                logging.error(f'{err}')
                del request.session['auth']
                request.session['error'] = 'Invalid token.'
                return redirect('home:index')
        else:
            if 'auth' in request.session:
                del request.session['auth']

import datetime

import requests


class RHubApiError(Exception):
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        self.problem = kwargs.pop('problem', None)
        super().__init__(*args, **kwargs)

    @classmethod
    def from_requests_response(cls, response):
        try:
            problem = response.json()
            if problem is None:
                problem = {}
        except Exception:
            problem = {}
        return cls(problem.get('detail', 'Unknown error'),
                   response=response, problem=problem)


class RHubAuthError(RHubApiError):
    pass


class RHubApiClient:
    def __init__(self, addr, username, password):
        self.addr = addr.rstrip('/')
        self.username = username
        self.password = password
        self._auth_token = None

    def get_token(self):
        now = datetime.datetime.now()
        if not self._auth_token or self._auth_token['expires'] < now:
            response = requests.post(
                f'{self.addr}/v0/auth/token/create',
                auth=(self.username, self.password),
            )
            if not response.ok:
                raise RHubAuthError.from_requests_response(response)
            self._auth_token = response.json()
            self._auth_token['expires'] = now + datetime.timedelta(
                minutes=self._auth_token['expires_in']
            )
        return self._auth_token['access_token']

    def request(self, method, path, *args, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers']['Authorization'] = 'Bearer ' + self.get_token()
        response = requests.request(method, f'{self.addr}{path}', *args, **kwargs)
        if not response.ok:
            raise RHubApiError.from_requests_response(response)
        return response

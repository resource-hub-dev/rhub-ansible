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


class RHubApiClient:
    def __init__(self, addr, token):
        self.addr = addr.rstrip('/')
        self.token = token

    def request(self, method, path, *args, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['auth'] = ('__token__', self.token)
        response = requests.request(method, f'{self.addr}{path}', *args, **kwargs)
        if not response.ok:
            raise RHubApiError.from_requests_response(response)
        return response

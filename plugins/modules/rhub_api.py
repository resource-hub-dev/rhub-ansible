ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: rhub_api
short_description: Interacts with Resource Hub API.
description:
  - Interacts with Resource Hub API.
options:
  addr:
    description:
      - Resource Hub base address.
      - If not set the environment variable C(RHUB_API_ADDR) will be used.
    required: true
    type: str
  token:
    description:
      - API auth token.
      - If not set the environment variable C(RHUB_API_TOKEN) will be used.
    required: true
    type: str
  method:
    description:
      - HTTP API method.
    required: false
    type: str
    default: GET
    choices: [GET, POST, PATCH, DELETE]
  path:
    description:
      - API endpoint path.
    required: true
    type: str
  body:
    description:
      - Resource Hub base address.
    required: false
    type: raw
"""

EXAMPLES = """
- name: get region info
  rhub.rhub.rhub_api:
    addr: https://rhub.example.com
    token: s3cr3t_t0k3n
    method: GET
    path: /v0/lab/region/1

- name: launch tower template
  rhub.rhub.rhub_api:
    addr: https://rhub.example.com
    token: s3cr3t_t0k3n
    method: POST
    path: /v0/tower/template/123/launch
    body:
      extra_vars:
        cluster_id: 1
"""

RETURN = """
data:
  description:
    - Response data
    - when request succeeded and API returned data (ie. DELETE doesn't return
      any data)
  returned: success
problem:
  description: Problem data (L(RFC 7807, https://tools.ietf.org/html/rfc7807))
  returned: failure
"""


import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback

from ansible_collections.rhub.rhub.plugins.module_utils.rhub_api import (
    RHubApiClient, RHubApiError
)


def main():
    module = AnsibleModule(
        argument_spec={
            'addr': {
                'required': True,
                'type': 'str',
                'fallback': (env_fallback, ['RHUB_API_ADDR'])
            },
            'token': {
                'required': True,
                'type': 'str',
                'no_log': True,
                'fallback': (env_fallback, ['RHUB_API_TOKEN']),
            },
            'path': {
                'required': True,
                'type': 'str',
            },
            'method': {
                'required': False,
                'type': 'str',
                'choices': ['GET', 'POST', 'PATCH', 'DELETE'],
                'default': 'GET'
            },
            'body': {
                'required': False,
                'type': 'raw',
            },
        },
        supports_check_mode=False,
    )

    addr = module.params['addr']
    token = module.params['token']
    path = module.params['path']
    method = module.params['method']
    body = module.params['body']

    if not isinstance(body, str):
        body = json.dumps(body)

    try:
        rhub_api = RHubApiClient(addr, token)
        response = rhub_api.request(method, path, data=body)
        if response.text:
            module.exit_json(data=response.json(), changed=method != 'GET')
        else:
            module.exit_json(changed=method != 'GET')
    except RHubApiError as e:
        module.fail_json(problem=e.problem, msg=str(e))


if __name__ == '__main__':
    main()

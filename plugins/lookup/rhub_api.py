__metaclass__ = type


DOCUMENTATION = """
module: rhub_api
short_description: Interacts with Resource Hub API.
description:
  - Retrieve data from Resource Hub API.
options:
  _terms:
    description:
      - API endpoint path.
    required: true
    type: str
  addr:
    description:
      - Resource Hub base address.
      - If not set the environment variable C(RHUB_API_ADDR) will be used.
    required: false
    type: str
    env:
      - name: RHUB_API_ADDR
  token:
    description:
      - API auth token.
      - If not set the environment variable C(RHUB_API_TOKEN) will be used.
    required: false
    type: str
    env:
      - name: RHUB_API_TOKEN
"""

EXAMPLES = """
- name: get cluster info
  ansible.builtin.debug:
    msg: "{{ lookup('rhub.rhub.rhub_api', '/v0/lab/cluster/1', addr='https://rhub.stage.example.com/') }}"
"""  # noqa: B950

RETURN = """
_list:
  description:
    - Data returned from the API or problem data (L(RFC 7807,
      https://tools.ietf.org/html/rfc7807)).
  type: list
  elements: raw
"""


from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ansible_collections.rhub.rhub.plugins.module_utils.rhub_api import (
    RHubApiClient
)


display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        rhub_api = RHubApiClient(
            self.get_option('addr'),
            self.get_option('token'),
        )

        return [rhub_api.request('GET', term).text for term in terms]

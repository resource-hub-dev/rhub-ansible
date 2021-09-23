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
      required: true
      type: str
      env:
        - name: RHUB_API_ADDR
    username:
      description:
        - API user.
      required: true
      type: str
      env:
        - name: RHUB_API_USER
    password:
      description:
        - Password for API user.
      required: true
      type: str
      env:
        - name: RHUB_API_PASS
"""

EXAMPLES = """
- name: get cluster info
  ansible.builtin.debug:
    msg: "{{ lookup('rhub.rhub.rhub_api', '/v0/lab/cluster/1 addr=https://rhub.stage.example.com/') }}"
"""

RETURN = """
_list:
  description:
    - Data returned from the API.
  type: list
  elements: raw
"""


import os
import datetime

import requests

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

from ansible_collections.rhub.rhub.plugins.module_utils.rhub_api import (
    RHubApiClient, RHubApiError
)


display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        addr = os.getenv('RHUB_API_ADDR') or self.get_option('addr')
        username = os.getenv('RHUB_API_USER') or self.get_option('username')
        password = os.getenv('RHUB_API_PASS') or self.get_option('password')

        rhub_api = RHubApiClient(addr, username, password)
        return [rhub_api.request('GET', term).text for term in terms]

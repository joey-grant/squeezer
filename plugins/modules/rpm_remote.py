#!/usr/bin/python


# copyright (c) 2020, Jacob Floyd
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: rpm_remote
short_description: Manage rpm remotes of a pulp api server instance
description:
  - "This performs CRUD operations on rpm remotes in a pulp api server instance."
options:
  policy:
    description:
      - Whether downloads should be performed immediately, or lazy.
    type: str
    choices:
      - immediate
      - on_demand
      - streamed
  pulp_labels:
    description:
      - Labels consisting of key, value pairs
    type: dict
    required: false
    version_added: "0.0.16"
extends_documentation_fragment:
  - pulp.squeezer.pulp
  - pulp.squeezer.pulp.entity_state
  - pulp.squeezer.pulp.remote
author:
  - Jacob Floyd (@cognifloyd)
"""

EXAMPLES = r"""
- name: Read list of rpm remotes from pulp api server
  pulp.squeezer.rpm_remote:
    pulp_url: https://pulp.example.org
    username: admin
    password: password
  register: remote_status
- name: Report pulp rpm remotes
  debug:
    var: remote_status

- name: Create a rpm remote
  pulp.squeezer.rpm_remote:
    pulp_url: https://pulp.example.org
    username: admin
    password: password
    name: new_rpm_remote
    url: https://example.org/centos/8/BaseOS/x86_64/os/
    state: present

- name: Delete a rpm remote
  pulp.squeezer.rpm_remote:
    pulp_url: https://pulp.example.org
    username: admin
    password: password
    name: new_rpm_remote
    state: absent

- name: Add a label to an rpm remote
  pulp.squeezer.rpm_remote:
    pulp_url: https://pulp.example.org
    username: admin
    password: password
    name: rpm_remote_name
    pulp_labels:
      key1: value1
    state: present
"""

RETURN = r"""
  remotes:
    description: List of rpm remotes
    type: list
    returned: when no name is given
  remote:
    description: Rpm remote details
    type: dict
    returned: when name is given
"""


from ansible_collections.pulp.squeezer.plugins.module_utils.pulp import (
    PulpRemoteAnsibleModule,
    PulpRpmRemote,
)


def main():
    with PulpRemoteAnsibleModule(
        argument_spec={
            "policy": {"choices": ["immediate", "on_demand", "streamed"]},
            "pulp_labels": {"type": "dict"},
        },
        required_if=[("state", "present", ["name"]), ("state", "absent", ["name"])],
    ) as module:
        natural_key = {"name": module.params["name"]}
        desired_attributes = {
            key: module.params[key]
            for key in [
                "url",
                "download_concurrency",
                "policy",
                "tls_validation",
                "pulp_labels",
            ]
            if module.params[key] is not None
        }

        # Nullifiable values
        if module.params["remote_username"] is not None:
            desired_attributes["username"] = module.params["remote_username"] or None
        if module.params["remote_password"] is not None:
            desired_attributes["password"] = module.params["remote_password"] or None
        desired_attributes.update(
            {
                key: module.params[key] or None
                for key in [
                    "proxy_url",
                    "proxy_username",
                    "proxy_password",
                    "ca_cert",
                    "client_cert",
                    "client_key",
                ]
                if module.params[key] is not None
            }
        )

        PulpRpmRemote(module, natural_key, desired_attributes).process()


if __name__ == "__main__":
    main()

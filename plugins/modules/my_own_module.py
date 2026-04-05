#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a text file with specified content
version_added: "1.0.0"
description: This module creates a text file on a remote host at the specified path with the specified content.
options:
    path:
        description: Path to the file to create.
        required: true
        type: str
    content:
        description: Content to write to the file.
        required: true
        type: str
author:
    - SavkinILYA (@SavkinILYA)
'''

EXAMPLES = r'''
- name: Create a text file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello, World!"
'''

RETURN = r'''
path:
    description: Path to the created file.
    type: str
    returned: always
changed:
    description: Whether the file was created or modified.
    type: bool
    returned: always
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    result['path'] = path

    # Проверяем существует ли файл с таким же содержимым
    if os.path.exists(path):
        with open(path, 'r') as f:
            existing_content = f.read()
        if existing_content == content:
            module.exit_json(**result)

    if module.check_mode:
        result['changed'] = True
        module.exit_json(**result)

    # Создаём файл
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
    except Exception as e:
        module.fail_json(msg=f'Failed to create file: {str(e)}', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

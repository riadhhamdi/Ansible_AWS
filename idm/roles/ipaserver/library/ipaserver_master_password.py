#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors:
#   Thomas Woerner <twoerner@redhat.com>
#
# Based on ipa-server-install code
#
# Copyright (C) 2017  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview'],
}

DOCUMENTATION = '''
---
module: master_password
short description: Generate kerberos master password if not given
description:
  Generate kerberos master password if not given
options:
  master_password:
    description: kerberos master password (normally autogenerated)
    required: false
author:
    - Thomas Woerner
'''

EXAMPLES = '''
'''

RETURN = '''
password:
  description: The master password
  returned: always
'''

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ansible_ipa_server import *

def main():
    module = AnsibleModule(
        argument_spec = dict(
            #basic
            dm_password=dict(required=True, no_log=True),
            master_password=dict(required=False, no_log=True),
        ),
        supports_check_mode = True,
    )

    module._ansible_debug = True

    options.dm_password = module.params.get('dm_password')
    options.master_password = module.params.get('master_password')

    fstore = sysrestore.FileStore(paths.SYSRESTORE)
    sstore = sysrestore.StateFile(paths.SYSRESTORE)

    # This will override any settings passed in on the cmdline
    if os.path.isfile(paths.ROOT_IPA_CACHE):
        # dm_password check removed, checked already
        try:
            cache_vars = read_cache(options.dm_password)
            options.__dict__.update(cache_vars)
        except Exception as e:
            module.fail_json(msg="Cannot process the cache file: %s" % str(e))

    if not options.master_password:
        options.master_password = ipa_generate_password()

    module.exit_json(changed=True,
                     password=options.master_password)

if __name__ == '__main__':
    main()

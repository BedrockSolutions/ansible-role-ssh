#!/usr/bin/env python3

try:
    from ansible.errors import AnsibleError, AnsibleActionFail
    from ansible.module_utils._text import to_native
    from ansible.plugins.action import ActionBase
    import socket
    import subprocess
except ImportError as e:
    raise AnsibleError(to_native(e))


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        action_vars = self._task.args

        hosts = [action_vars.pop("host", None)]
        if not hosts or not hosts[0]:
            raise AnsibleError("host parameter missing")

        port = action_vars.pop("port", 22)
        if not port:
            raise AnsibleError("port parameter missing")

        key_type = action_vars.pop("key_type", None)
        if not key_type:
            raise AnsibleError("key_type parameter missing")
        
        allow_no_keys = action_vars.pop("allow_no_keys", False)
        include_ip_address_keys = action_vars.pop("include_ip_address_keys", True)

        if include_ip_address_keys:
            hosts.extend(socket.gethostbyname(hosts[0]).split(" "))

        keyscan_args = ["ssh-keyscan", "-p", str(port)]

        # if key_type:
        #     keyscan_args.extend(["-t ", key_type])

        results = []
        for host in hosts:
            completed_keyscan = subprocess.run(
                args=keyscan_args + [host],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                check=True,
                universal_newlines=True,
            )

            key = completed_keyscan.stdout

            if not allow_no_keys and not key:
                raise AnsibleError("no host key found for " + host)

            results.append({
                host: host,
                key: key,
            })

        print(results)

        return_value = super(ActionModule, self).run(tmp, task_vars)
        return_value["result"] = results

        return return_value

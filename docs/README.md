# bedrock.ssh

Ansible role that contains SSH-related tasks and handers.

A prettier version of this documentation is located at 
https://bedrocksolutions.github.io/ansible-role-ssh
 
* Commands
  * [authorize_keys](#authorize_keys)
  * [harden](#harden)
  * [known_hosts](#known_hosts)
  
* Handlers
  * [ssh_restart](#ssh_restart)

## Installation

To use `bedrock.ssh` in another role, create the file 
`<role_root>/meta/main.yml` with the following structure:

```yaml
dependencies:
  - name: bedrock.ssh
    scm: git
    src: https://github.com/BedrockSolutions/ansible-role-ssh.git
    vars:
      ssh:
        command: dependency
    version: master
```

If you just want to use this role in a playbook or task file, then
add an entry to the `requirements.yml` file:

```yaml
- name: bedrock.ssh
  scm: git
  src: https://github.com/BedrockSolutions/ansible-role-ssh.git
  version: master
```
>__Note:__ In both examples, the `version` field can be a branch, tag, or commit hash.

The role may now be imported or included as `bedrock.ssh`.

## Command Invocation

The role is made up of commands can be invoked using the following 
syntax:

```yaml
- import_role
    name: bedrock.ssh
  vars:
    ssh:
      command: <command_name>
      ...command_vars
```

or

```yaml
- include_role
    name: bedrock.ssh
  vars:
    ssh:
      command: <command_name>
      ...command_vars
```

## Commands

### __authorize_keys__

Adds one or more keys to one or more `<user>/.ssh/authorized_keys` files.

#### Arguments

* __`exclusive`:__ Whether to remove all other non-specified keys from the
keys file.

    * type: boolean
    * default: `false`

* __`authorized_keys`:__ A dict containing public keys to authorize. 
The data structure is a mapping from a username to an array of keys.

    * type: object
    * key: username
    * value: array of public keys

#### Example

Add a key to the keys file of user `foo`, and remove all other keys: 

```yaml
- import_task:
    name: bedrock.ssh
  vars:
    ssh:
      command: authorize_keys
      exclusive: true
      authorized_keys:
        foo:
          - ssh-ed25519 ************************ foo@bar.com
```

### __harden__

Hardens the ssh client and daemon. This command leverages the awesome
[dev-sec/ansible-ssh-hardening](https://github.com/dev-sec/ansible-ssh-hardening)
role to perform the bulk of the hardening operations.

#### Arguments

* __`agent_forwarding_enabled`:__ Toggles the AllowAgentForwarding setting.

    * type: boolean
    * default: `false`

* __`allowed_users`:__ A list of users allowed to connect via SSH.

    * type: list
    * default: `['ubuntu']`
    * min length: 1

* __`tun_device_forwarding_enabled`:__ Toggles the PermitTunnel setting.

    * type: boolean
    * default: `false`

* __`sftp_enabled`:__ Enables or disables SFTP access. If false, use SCP
instead.

    * type: boolean
    * default: `true`

#### Example

Harden the SSH client and daemon of a remote machine:

```yaml
- import_task:
    name: bedrock.ssh
  vars:
    ssh:
      command: harden
      allowed_users:
        - billy
        - bob
```

### __known_hosts__

Adds a given machine's host keys to the `.ssh/known_hosts` file of the
current user.

There are two main scenarios where this is useful:

1) Add the host keys of a newly created machine to the Ansible controller.

2) Add host keys from one machine to another machine, to preconfigure an
SSH connection.

#### Arguments

* __`delegate_to`:__ The machine with the `known_hosts` file to be edited.

    * type: string
    * default: `{{ inventory_hostname }}`
    
* __`host`:__ The machine that will have its host keys added.

    * type: string

* __`key_type`:__ The SSH key type to obtain from the `host`.

    * type: string
    * enum: `['dsa','ecdsa','ed25519','rsa']`

#### Examples

Add the current remote machine's host keys to the ansible controller's
`known_hosts` file:

```yaml
- import_task:
    name: bedrock.ssh
  vars:
    ssh:
      command: known_hosts
      delegate_to: localhost
      host: "{{ inventory_hostname }}"
      key_type: ed25519
```

Add GitHub's host keys to a remote server:

```yaml
- import_task:
    name: bedrock.ssh
  vars:
    ssh:
      command: known_hosts
      host: github.com
      key_type: rsa
```

## Handlers

### __ssh_restart__

Restarts the SSH daemon

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

Adds one or more keys in the `<user>/.ssh/authorized_keys` file.

#### Arguments

* __`exclusive`:__ Whether to remove all other non-specified keys from the
keys file.

    * type: boolean
    * default: `true`

* __`keys`:__ A list containing the public keys to add. At least one key
is required.

    * type: list
    * min length: 1

* __`user`:__ The username whose keys file will be modified.

    * type: string
    * default: `ubuntu`

#### Example

Add a key to the keys file of user `foo`: 

```yaml
- import_task:
    name: bedrock.ssh
  vars:
    ssh:
      command: authorize_keys
      exclusive: false
      keys:
        - ssh-ed25519 ************************ foo@bar.com
      user: foo
```


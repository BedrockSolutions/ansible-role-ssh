# bedrock.ssh

Ansible role that contains SSH-related tasks and handers.

A prettier version of this documentation is located at 
https://bedrocksolutions.github.io/ansible-role-ssh
 
## Installation

To use `bedrock.ssh` in another role, create the file 
`<role_root>/meta/main.yml` with the following structure:

```yaml
dependencies:
  - name: bedrock.ssh
    scm: git
    src: https://github.com/BedrockSolutions/ansible-role-ssh.git
    vars:
      common:
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

### __controller_reset_connection__

Resets the connection between the controller and a target machine.
Subsequent tasks will establish a new SSH login. This is useful when,
for example, the SSH user is added to a new group and a fresh login is
necessary to pick up the new group's privileges.

#### Example

```yaml
- import_task:
    name: bedrock.common
  vars:
    common:
      command: controller_reset_connection
```

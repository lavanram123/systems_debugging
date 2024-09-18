# Plexec

Plexec is a Python module to execute commands on multiple hosts. It supports running commands directly on the hosts or inside Docker containers on those hosts.

## Features

- Execute commands on multiple hosts concurrently.
- Support for running commands inside Docker containers.
- SSH key-based authentication.
- Customizable SSH options.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/lavanram123/plexec.git
    cd plexec
    ```

2. Install the package:
    ```sh
    pip install .
    ```

## Usage

### Command Line Interface

To execute a command on multiple hosts, you can use the `plexec` command-line tool.

#### Basic Usage

```sh
plexec -f hosts.txt -u your_username -p your_password "echo 'Hello World'"
```
```
plexec <cmd> -f <hosts_file> [-u <user>] [-p <password>] [-c] [--dock <container_name>] [--key <private_key_path>]
```

### Arguments

- `<cmd>`: Command to execute on the hosts.
- `-f, --hosts_file <hosts_file>`: File containing host names (one per line).
- `-u <user>`: SSH user (optional).
- `-p <password>`: Login password (optional).
- `-c`: Execute command inside the default container (`object-main`).
- `--dock <container_name>`: Name of the container inside which the command has to be run.
- `--key <private_key_path>`: Path to the private key file for SSH authentication.

### Example

1. Execute a command on multiple hosts:
    ```sh
    plexec "echo 'Hello World'" -f hosts.txt --key ~/.ssh/id_rsa
    ```

2. Execute a command inside a Docker container on multiple hosts:
    ```sh
    plexec "echo 'Hello from container'" -f hosts.txt --dock my_container --key ~/.ssh/id_rsa
    ```

## Hosts File

The hosts file should contain one host per line. Example:

```
host1
host2
host3
```

## License

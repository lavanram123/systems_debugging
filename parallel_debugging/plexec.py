#!/usr/bin/python

"""
Module to execute commands on all the hosts that are given in the input
"""

import os
import sys
import argparse
import ipaddress
from pssh.clients import ParallelSSHClient
from pssh.utils import load_private_key

def read_hosts(filename):
    def is_valid_ipv4(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and is_valid_ipv4(line.strip())]
    except (IOError, FileNotFoundError) as e:
        print(f"Error reading file {filename}: {e}")
        sys.exit(1)

def encapsulate_shell_cmd(cmd):
    """
    1. Replace Single Quotes: --> ('\\''). This is necessary because single quotes can interfere with shell command execution.
    2. Encapsulate with Single Quotes: It then encapsulates the entire command string in single quotes (').
    3. Example:
    cmd  echo 'Hello World', the function will transform it to 'echo '\''Hello World'\'', making it safe to execute in a shell.
    """
	return("'"+cmd.replace("'", "'\\''")+"'")

def execute_command(hosts, user=None, passwd=None, cmd, container_name=None, private_key_path=None):
    ssh_options = {
        'StrictHostKeyChecking': 'no',
        'SendEnv': 'SUDO_USER'
    }
    
    private_key = load_private_key(private_key_path) if private_key_path else None
    client = ParallelSSHClient(hosts, user=user, password=passwd, pkey=private_key, ssh_options=ssh_options)
    
    cmd = encapsulate_shell_cmd(cmd)
    if container_name:
        cmd = f"docker exec {container_name} sh -c '{cmd}'"
    
    output = client.run_command(cmd)
    for host_output in output:
        for line in host_output.stdout:
            print(f"[{host_output.host}] {line}")
        for line in host_output.stderr:
            print(f"[{host_output.host} ERROR] {line}")
        print(f"[{host_output.host}] Exit code: {host_output.exit_code}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Execute commands on multiple hosts.")
    parser.add_argument("cmd", help="Command to execute")
    parser.add_argument("-f", "--hosts_file", dest="filename", help="File containing host names")
    parser.add_argument("-p", dest="passwd", help="Login password")
    parser.add_argument("-u", dest="user", default="root", help="SSH user")
    parser.add_argument("-c", dest="container", action="store_true", help="Execute command inside object container.")
    parser.add_argument("--dock", help="Name of the container inside which the command has to be run")

    args = parser.parse_args()

    if not args.filename:
        print("Hosts file is required")
        parser.print_help()
        sys.exit(1)

    hosts = read_hosts(args.filename)
    if not hosts:
        print("No hosts found in the file")
        sys.exit(1)

    if args.container and args.dock:
        print("Please choose -c or --dock, not both.")
        parser.print_help()
        sys.exit(1)

    container_name = "object-main" if args.container else args.dock

    execute_command(hosts, args.user, args.passwd, args.cmd, container_name)


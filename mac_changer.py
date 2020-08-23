#!/usr/bin/env python3
from argparse import ArgumentParser, Action
from subprocess import run
from sys import exit

from psutil import net_if_addrs


def get_arguments():
    parser = ArgumentParser(
        description='Change the mac address of network interfaces.')

    parser.add_argument('-i', '--interface', dest='interface', required=True,
                        help='name of network interface. (e.g:- wlan0, eth0, etc..)')
    parser.add_argument('-m', '--mac', dest='to_mac', required=True,
                        help='desired mac address. (e.g:- 00:11:22:33:44:55)')
    parser.add_argument('-a', nargs=0,
                        action=ShowInterfacesAction, help='shows all interfaces')
    parser.add_argument('-r', '--reset', nargs=1, default=None, dest='reset_dev', action=ResetInterfaceMac,
                        help='reset the mac address of specified network interface')

    return parser.parse_args()


def is_linux():
    from platform import system
    return system() == 'Linux'


def is_root():
    from os import geteuid
    return geteuid() == 0


def all_interfaces():
    return list(net_if_addrs().keys())


def get_default_mac(interface):
    from json import loads
    from subprocess import run
    cmd_output = run(['ip', '-j', 'link'], capture_output=True).stdout.decode()
    cmd_json_output = loads(cmd_output)
    for item in cmd_json_output:
        if item.get('ifname') == interface:
            permanent_mac = item.get('permaddr')
            if permanent_mac:
                return permanent_mac
            else:
                return None
    else:
        raise Exception('wrong interface given')


def get_vendor(mac):
    from requests import get
    from sys import exit

    url = "https://api.macvendors.com/"

    response = get(url + mac)
    if response.status_code != 200:
        print("[!] Invalid MAC Address!")
        exit(1)
    return response.content.decode()


def get_mac(interface):
    nics = net_if_addrs()[interface]
    for interface in nics:
        if interface.family == 17:
            return interface.address


def check_mac(to_mac, interface):
    if get_mac(interface) == to_mac:
        return True
    return False


def mac_changer(network_interface, to_mac):
    run(['ip', 'link', 'set', network_interface, 'down'])
    run(['ip', 'link', 'set', network_interface, 'address', to_mac])
    run(['ip', 'link', 'set', network_interface, 'up'])


class ShowInterfacesAction(Action):
    def __call__(*args):
        del args
        available_interfaces = all_interfaces()
        print('[+] Available interfaces:')
        for item in available_interfaces:
            current_mac = get_mac(item)
            try:
                vendor = get_vendor(current_mac)
            except:
                vendor = 'unknown'
            print(f"\t> {item}   ---- current_mac ---->   {current_mac}   ---- vendor ---->   {vendor}")
        exit(0)


class ResetInterfaceMac(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        reset_dev = values[0]
        del self, parser, namespace, option_string

        if not is_root():
            print('[!] Run me as root')
            exit(1)

        if reset_dev not in all_interfaces():
            print("[!] Wrong interface selected")
            exit(1)

        permanent_mac = get_default_mac(reset_dev)
        if permanent_mac:
            print(f"[+] changing mac address of {reset_dev} to {permanent_mac}[default]")
            mac_changer(reset_dev, permanent_mac)
            if check_mac(permanent_mac, reset_dev):
                print(
                    f"[+] successfully changed the mac address of {reset_dev}")
                exit(0)
            else:
                print(f'[!] unable to reset {reset_dev}')
                exit(1)
        else:
            print(f"[+] {reset_dev} is already at it's default mac")
            exit(0)


def main():
    options = get_arguments()

    if not is_linux():
        print('[!] I only work in Linux')
        exit(1)

    if not is_root():
        print('[!] Run me as root')
        exit(1)

    network_interface = options.interface
    to_mac = options.to_mac

    if network_interface not in all_interfaces():
        print("[!] Wrong interface selected")
        exit(1)

    if check_mac(to_mac, network_interface):
        print(f"[+] mac address of {network_interface} is already {to_mac}")
        exit(0)

    print(f"[+] changing mac address of {network_interface} to {to_mac}")
    mac_changer(network_interface, to_mac)

    if check_mac(to_mac, network_interface):
        print(
            f"[+] successfully changed the mac address of {network_interface}")
        exit(0)
    else:
        print('[!] unable to change mac')
        print('[!] trying again with different mac might work')
        exit(1)


if __name__ == '__main__':
    main()

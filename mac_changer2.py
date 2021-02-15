#Rodar sempre com python3
#!/usr/bin/env
import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help='Interface to change its MAC address')
    parser.add_option("-m", "--mac", dest="new_mac", help='Choose MAC address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please especify an interface user use --help if you need info')
    elif not options.new_mac:
        parser.error('[-] Please especify a new mac address use --help if you need info')
    else:
      return options


def change_mac(interface, new_mac):
    #print(f'[+] Changing MAC ADDRESS for the interface {interface}  to  {new_mac}.')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    print("[+] MAC ADDRESS CHANGED")

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode("utf-8"))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-]Cannot read MAC address')


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC: ", str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address succesfully changed to ", current_mac)
else:
    print('[-] MAC address did not get changed')


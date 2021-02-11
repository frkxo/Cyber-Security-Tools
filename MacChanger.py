import subprocess
import optparse
import re


def get_user_input():
    parseObject = optparse.OptionParser()
    parseObject.add_option("-i", "--interface", dest="interface", help="interface to change!!!")
    parseObject.add_option("-m", "--mac", dest="macAddress", help="new mac address")
    return parseObject.parse_args()


def change_mac_address(userInterface, userMacAddress):
    subprocess.call(["ifconfig", userInterface, "down"])
    subprocess.call(["ifconfig", userInterface, "hw", "ether", userMacAddress])
    subprocess.call(["ifconfig", userInterface, "up"])


def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    newMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))

    if newMac:
        return newMac.group(0)
    else:
        return None


print("My Mac Changer has started!!!")
(userInput, arguments) = get_user_input()
change_mac_address(userInput.interface, userInput.macAddress)
finalizedMac = control_new_mac(str(userInput.interface))

if finalizedMac == userInput.macAddress:
    print("Success!!!")
else:
    print("ERROR!!!")

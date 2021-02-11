import scapy.all as scapy
import optparse


def get_user_Input():
    parseObject = optparse.OptionParser()
    parseObject.add_option("-i", "--ipaddress", dest="ipAddress", help="Enter Ip Address!!")
    (userInput, arguments) = parseObject.parse_args()

    if not userInput.ipAddress:
        print("Enter An Ip Address!!!")

    return userInput


def scan_my_network(ip):
    arpRequestPacket = scapy.ARP(pdst=ip)

    broadcastPacket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    combinedPacket = broadcastPacket / arpRequestPacket
    (answeredList, unansweredList) = scapy.srp(combinedPacket, timeout=1)
    answeredList.summary()


userIpAddress = get_user_Input()
scan_my_network(userIpAddress.ipAddress)

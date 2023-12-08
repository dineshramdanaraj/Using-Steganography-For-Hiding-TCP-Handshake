from scapy.all import sniff, IP
import struct




def packet_callback(packet):
    
    if packet.haslayer(IP):
        ip_src = 'localhost'
        ip_dst = 'localhost'

        # Extract the protocol number from the IP header
        ip_proto = packet[IP].proto

        if ip_proto == 6:  # TCP protocol number is 6
            tcp_flags = packet['TCP'].flags
            src_port = 9090
            dst_port = 9090
            response_9090 = b'#\x82\x16.\x00\x0009\x00\x00\x00\x00P\x02 \x00&\x14\x00\x00'
            response_9091 = b'#\x82\x16.\x00\x00\x0f_\x00\x00\x00\x00P\x02 \x00F\xee\x00\x00'

# Unpack the source and destination ports from the response
            source_port_9090, dest_port_9090 = struct.unpack('!HH', response_9090[0:4])
            source_port_9091, dest_port_9091 = struct.unpack('!HH', response_9091[0:4])

            # print(f"Source Port 9090: {source_port_9090}, Destination Port 9090: {dest_port_9090}")
            # print(f"Source Port 9091: {source_port_9091}, Destination Port 9091: {dest_port_9091}")
            #print(f"TCP Communication: {ip_src}:{src_port} -> {ip_dst}:{dst_port}, Flags: {tcp_flags}")

        elif ip_proto == 17:  # UDP protocol number is 17
            src_port = packet['UDP'].sport
            dst_port = 9090
            #print(f"UDP Communication: {ip_src}:{src_port} -> {ip_dst}:{dst_port}")

        else:
            # For any other protocol, print the protocol number
            print(ip_proto)
            print(f"TCP Protocol ({ip_proto}): {ip_src} -> {ip_dst}")
            print(packet[IP].payload)
            raw_payload = bytes(packet[IP].payload)
            print("Raw Payload (Hex):")
            print(raw_payload.hex())

# Start sniffing and capture packets
sniff(prn=packet_callback, store=0)

from gnuradio import gr
import numpy as np
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from meshtastic import mesh_pb2, portnums_pb2
from base64 import b64decode

def decrypt(packet, key):
    nonce = packet[8:12] + b'\x00\x00\x00\x00' + packet[4:8] + b'\x00\x00\x00\x00'

    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()

    payload = packet[16:len(packet)]

    decrypted_packet = decryptor.update(payload) + decryptor.finalize()

    data = mesh_pb2.Data()
    data.ParseFromString(decrypted_packet)

    return decrypted_packet

PACKET_FLAGS_HOP_LIMIT_MASK = 0x07
PACKET_FLAGS_WANT_ACK_MASK = 0x08
PACKET_FLAGS_VIA_MQTT_MASK = 0x10
PACKET_FLAGS_HOP_START_MASK = 0xE0
PACKET_FLAGS_HOP_START_SHIFT = 5

def to_simulation_packet(packet, key):
    flags = int.from_bytes(packet[12:13], 'big')

    meshPacket = mesh_pb2.MeshPacket(
        to=int.from_bytes(packet[0:4], 'big'),
        id=int.from_bytes(packet[8:12], 'big'),
        want_ack=not not(flags & PACKET_FLAGS_WANT_ACK_MASK),
        hop_limit=flags & PACKET_FLAGS_HOP_LIMIT_MASK,
        hop_start=(flags & PACKET_FLAGS_HOP_START_MASK) >> PACKET_FLAGS_HOP_START_SHIFT,
        via_mqtt=not not flags & PACKET_FLAGS_VIA_MQTT_MASK,
        decoded=mesh_pb2.Data(
            payload=decrypt(packet, key),
            portnum=portnums_pb2.SIMULATOR_APP
        )
    )

    setattr(meshPacket, "from", int.from_bytes(packet[4:8], 'big'))

    to_radio = mesh_pb2.ToRadio()
    to_radio.packet.CopyFrom(meshPacket)

    return to_radio


class meshtastic(gr.sync_block):
    """Meshtastic Simulator"""

    def __init__(self, key="1PG7OiApB1nwvP+rz05pAQ==", url="https://localhost"):
        gr.sync_block.__init__(
            self,
            name='Meshtastic Simulator',
            in_sig=[np.byte],
            out_sig=[]
        )

        self.key = b64decode(key.encode('ascii'))
        self.url = url

    def work(self, input_items, output_items):
        try:
            requests.put(self.url + '/api/v1/toradio', data=to_simulation_packet(input_items[0].tobytes(), self.key).SerializeToString(), headers={'accept': 'application/x-protobuf'}, verify=False)
        except Exception as exception:
            print(exception)

        self.consume(0, len(input_items[0]))

        return 0

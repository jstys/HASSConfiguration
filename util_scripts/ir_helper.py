#!/srv/homeassistant/bin/python3

import binascii
import struct

def pronto2lirc(pronto):
    codes = [long(binascii.hexlify(pronto[i:i+2]), 16) for i in xrange(0, len(pronto), 2)]

    if codes[0]:
        raise ValueError('Pronto code should start with 0000')
    if len(codes) != 4 + 2 * (codes[2] + codes[3]):
        raise ValueError('Number of pulse widths does not match the preamble')

    frequency = 1 / (codes[1] * 0.241246)
    return [int(round(code / frequency)) for code in codes[4:]]

def lirc2broadlink(pulses):
    array = bytearray()

    for pulse in pulses:
        pulse = pulse * 269 / 8192  # 32.84ms units

        if pulse < 256:
            array += bytearray(struct.pack('>B', pulse))  # big endian (1-byte)
        else:
            array += bytearray([0x00])  # indicate next number is 2-bytes
            array += bytearray(struct.pack('>H', pulse))  # big endian (2-bytes)

    packet = bytearray([0x26, 0x00])  # 0x26 = IR, 0x00 = no repeats
    packet += bytearray(struct.pack('<H', len(array)))  # little endian byte count
    packet += array
    packet += bytearray([0x0d, 0x05])  # IR terminator

    # Add 0s to make ultimate packet size a multiple of 16 for 128-bit AES encryption.
    remainder = (len(packet) + 4) % 16  # rm.send_data() adds 4-byte header (02 00 00 00)
    if remainder:
        packet += bytearray(16 - remainder)

    return packet

if __name__ == '__main__':
    import sys

    code = sys.argv[1]
    code = code.replace(" ", "")
    pronto = bytearray.fromhex(code)
    pulses = pronto2lirc(pronto)
    packet = lirc2broadlink(pulses)

    hexcode = binascii.hexlify(packet)
    base64code = hexcode.decode("hex").encode("base64").strip()

    print("")
    print("lirc - Pulses")
    print(pulses)
    print("Broadlink - HEX")
    print(hexcode)
    print("Broadlink - BASE 64")
    print(base64code)

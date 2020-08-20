import numpy as np
import binascii

memory = np.zeros(4096, dtype=np.byte)
vram = np.zeros(32*64, dtype=np.bool)

# to-do : properly set the font
sprites = {
    '0': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '1': ['0x20', '0x60', '0x20', '0x20', '0x70'],
    '2': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '3': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '4': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '5': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '6': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '7': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '8': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    '9': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'A': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'B': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'C': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'D': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'E': ['0xF0', '0x90',  '0x90', '0x90', '0xF0'],
    'F': ['0xF0', '0x90',  '0x90', '0x90', '0xF0']
}


def load_text_sprites():
    address = 0
    for sprite, data in sprites.items():
        for byte in data:
            memory[address] = (int(byte, 16)).to_bytes(1, byteorder='little')
            address += 1


def load_game(path):
    with open(path, mode='rb') as file:
        address = int('0x200', 16)
        for byte in file.read():
            print(byte)
            memory[address] = byte
            address += 1


load_game('games/PONG')

# load_text_sprites()
# print(memory[0])
# print(memory[1])
# print(memory[2])
# print(memory[3])
import numpy as np
import binascii
# import pygame

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

'''
CHIP-8 has two timers. They both count down at 60 hertz, until they reach 0.
Chip-8 provides 2 timers, a delay timer and a sound timer.
The delay timer is active whenever the delay timer register(DT) is non-zero. This timer does nothing more than 
subtract 1 from the value of DT at a rate of 60Hz. When DT reaches 0, it deactivates.
The sound timer is active whenever the sound timer register(ST) is non-zero. This timer also decrements at a rate of 
60Hz,however, as long as ST's value is greater than zero, the Chip-8 buzzer will sound. When ST reaches zero,
the sound timer deactivates.
The sound produced by the Chip-8 interpreter has only one tone. The frequency of this tone is decided by the author of
the interpreter.
'''


# def timer():
#     wait = int(1/60 * 1000)
#     while True:
#         for i in range(60, 0, -1):
#             pygame.time.wait(wait)
#             return i



class CPU:

    memory = [b'0'] * 4096
    vram = np.zeros(32*64, dtype=np.bool)

    PC = 512
    SP = 0
    I = 0
    v = [b'0']*16

    DT = 60
    ST = 60

    def __init__(self):
        self._load_text_sprites()
        self._load_game('games/PONG')

    def _load_text_sprites(self):
        address = 0
        for sprite, data in sprites.items():
            print(sprite)

    def _load_game(self, path):
        with open(path, mode='rb') as file:
            address = int('0x200', 16)
            for byte in file.read():
                self.memory[address] = byte
                address += 1
    
    def fetch_instruction(self, instruction):

        def ld_vx_byte(self, instruction):
            vx, byte = instruction[0], instruction[1:]
            vx = int(vx, 16)
            self.v[vx] = byte
            print(self.v)
        
        def sys_handler(self, instruction):
            sys_instructions = {
                '0E0': cls,
                '0EE': ret,
            }

            sys_instructions.get(instruction)()
            
            def cls(self):
                pass

            def ret(self):
                pass


        instruction_set={
            '0x0': sys_handler,
            '0x6': ld_vx_byte,
        }

        code = hex(self.memory[512] << 8 | self.memory[513]) 
        instruction_set.get(code[0:3])(self, code[3:])


        
    
    def run(self):
        self.PC = 512
        while True:
            instruction = self.memory[self.PC] << 8| self.memory[self.PC+1]
            self.fetch_instruction(instruction) 
            self.PC += 1

    instruction_set = {
        '0x0':{},
        '0x1':{},
        '0x2':{},
        '0x3':{},
        '0x4':{},
        '0x5':{},
        '0x6':{},
        '0x7':{},
        '0x8':{},
        '0x9':{},
    }

cpu = CPU()
cpu.run()
print(cpu.memory)
# timer()

# load_text_sprites()
# print(memory[512])
# print(memory[1])
# print(memory[2])
# print(memory[3])

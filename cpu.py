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
    stack = [b'0'] * 64

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
    
    def read_vram(self, x, y, offset=0):
        return self.vram[x + y*64 + offset]

    def put_vram(self, x, y, value):
        self.vram[x+y*64] = value

    def fetch_instruction(self, instruction):
        def jmp_addr(self, nnn):
            self.PC = int(nnn, 16)

        def ld_i_addr(self, nnn):
            self.I = int(nnn, 16)

        def ld_vx_byte(self, instruction):
            vx, byte = instruction[0], instruction[1:]
            vx = int(vx, 16)
            self.v[vx] = int(byte, 16)
            print(self.v)
        
        def drw_vx_vy_nibble(self, nnn):
            vx, vy, nibble = nnn[0], nnn[1], nnn[2]
            vx = int(vx, 16)
            vy = int(vy, 16)

            vx = self.v[vx]
            vy = self.v[vy]

            # draw function, save for last

            num_range = int(nibble, 16)
        
        def call_addr(self, nnn):
            self.SP += 1
            self.stack.append(self.PC)

            self.PC = int(nnn, 16)
        
        def sys_handler(self, instruction):
            def cls(self):
                self.vram = np.zeros(32*64, dtype=np.bool)

            def ret(self):
                self.PC = self.SP
                self.SP -= 1

            sys_instructions = {
                '0E0': cls,
                '0E0': ret,
            }

            sys_instructions.get(instruction)()
        
        def sys_manager(self, nnn):
            vx, op = nnn[0], nnn[1:]

            def ld_dt_vx(self, vx):
                vx = int(vx, 16)
                self.dt = self.v[vx]
            
            def ld_b_vx(self, vx):
                vx = int(vx, 16)
                vx = self.v[vx]
                # isso ta feio, mas bls
                self.memory[self.I] = int(str(vx // 100)[-1])
                self.memory[self.I + 1] = int(str(vx // 10)[-1])
                self.memory[self.I + 2] = int(str(vx)[-1])
            
            def ld_vx_I(self, vx):
                vx = int(vx, 16)
                for i in range(vx):
                    self.v[0] = self.memory[self.I + i]
                
                self.I += vx + 1

            sys_handler_instructions = {
                '15': ld_dt_vx,
                '33': ld_b_vx,
                '65': ld_vx_I,
            }
            sys_handler_instructions.get(op)(self, vx)
            

        instruction_set={
            '0': sys_handler,
            '1': jmp_addr,
            '6': ld_vx_byte,
            'a': ld_i_addr,
            'd': drw_vx_vy_nibble,
            '2': call_addr,
            'f': sys_manager,
        }

        code = hex(instruction)[2:]
        instruction_set.get(code[0])(self, code[1:])


        
    
    def run(self):
        self.PC = 512
        while True:
            instruction = self.memory[self.PC] << 8| self.memory[self.PC+1]
            self.fetch_instruction(instruction)
            self.PC += 2

    

cpu = CPU()
cpu.run()
print(cpu.memory)
# timer()

# load_text_sprites()
# print(memory[512])
# print(memory[1])
# print(memory[2])
# print(memory[3])

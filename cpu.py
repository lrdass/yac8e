import numpy as np
import binascii
import random
# import pygame

# to-do : properly set the font


sprites = {
    '0': ['F0', '90',  '90', '90', 'F0'],
    '1': ['20', '60',  '20', '20', '70'],
    '2': ['F0', '90',  '90', '90', 'F0'],
    '3': ['F0', '90',  '90', '90', 'F0'],
    '4': ['F0', '90',  '90', '90', 'F0'],
    '5': ['F0', '90',  '90', '90', 'F0'],
    '6': ['F0', '90',  '90', '90', 'F0'],
    '7': ['F0', '90',  '90', '90', 'F0'],
    '8': ['F0', '90',  '90', '90', 'F0'],
    '9': ['F0', '90',  '90', '90', 'F0'],
    'A': ['F0', '90',  '90', '90', 'F0'],
    'B': ['F0', '90',  '90', '90', 'F0'],
    'C': ['F0', '90',  '90', '90', 'F0'],
    'D': ['F0', '90',  '90', '90', 'F0'],
    'E': ['F0', '90',  '90', '90', 'F0'],
    'F': ['F0', '90',  '90', '90', 'F0']
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

    memory = [b'0000 0000'] * 4096
    vram = np.zeros(32*64, dtype=np.bool)
    stack = [b'0000 0000'] * 64

    PC = 512
    SP = 0
    I = 0
    v = [b'0']*16

    DT = 60
    ST = 60

    k = [1] * 16

    runnig = False

    def __init__(self):
        self._load_text_sprites()
        self._load_game('games/PONG')
        self.runnig = True

    def _load_text_sprites(self):
        address = 0
        for sprite, data in sprites.items():
            for byte in data:
                self.memory[address] = byte
                address +=1

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
        
        def add_vx_byte(self, nnn):
            vx, kk = nnn[0], nnn[1:]
            vx = int(vx, 16)
            kk = int(kk, 16)

            self.v[vx] += kk

        def se_vx_byte(self, xkk):
            vx, kk = xkk[0], xkk[1:]
            vx = int(vx, 16)
            kk = int(kk, 16)

            if self.v[vx] == kk:
                self.PC += 2

        def sne_vx_byte(self, xkk):
            vx, kk = xkk[0], xkk[1:]
            vx = int(vx, 16)
            kk = int(kk, 16)

            if self.v[vx] != kk:
                self.PC += 2
        
        def rnd_vx_byte(self, xkk):
            x, kk = xkk[0], xkk[1:]
            x = int(x, 16)
            kk = int(kk, 16)

            self.v[x] = random.randint(0,255) & kk


        def sys_handler(self, instruction):
            def cls(self):
                self.vram = np.zeros(32*64, dtype=np.bool)

            def ret(self):
                self.PC = self.stack.pop()
                self.SP -= 1
            
            def end(self):
                self.running = False

            sys_instructions = {
                '0e0': cls,
                '0ee': ret,
                '000': end,
            }

            sys_instructions.get(instruction)(self)
        
        def sys_timer(self, nnn):
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
            
            def ld_f_vx(self, vx):
                vx = int(vx, 16)
                self.I = vx*5
            
            def ld_vx_dt(self, vx):
                vx = int(vx, 16)
                self.v[vx] = self.DT
            
            sys_timer_instructions = {
                '15': ld_dt_vx,
                '33': ld_b_vx,
                '65': ld_vx_I,
                '29': ld_f_vx,
                '07': ld_vx_dt,
            }

            sys_timer_instructions.get(op)(self, vx)
        
        def skip_key_instructions(self, xnn):
            x, op = xnn[0], xnn[1:]
            def sknp_vx(self, x):
                x = int(x, 16)
                if self.k[self.v[x]]:
                    self.PC+=2
            
            instruction_set = {
                'a1': sknp_vx,
            }

            instruction_set.get(op)(self, x)
        

        def sys_ula(self, xyn):
            x, y, op = xyn[0], xyn[1], xyn[2]

            def ld_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[y]

            def or_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[x] | self.v[y]

            def and_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[x] & self.v[y]
            
            def xor_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[x] ^ self.v[y]
            
            def add_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[x] + self.v[y] % 255
                self.v[15] = 1 if self.v[x] + self.v[y] > 255 else 0
            
            def sub_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                if self.v[x] < self.v[y]:
                    self.v[15] = 1
                else:
                    self.v[x] = self.v[x] - self.v[y]
            
            def shr_vx_vy(self, x,y):
                x = int(x, 16)
                y = int(y, 16)

                self.v[x] = self.v[x] >> 1


            instruction_set = {
                '0': ld_vx_vy,
                '1': or_vx_vy,
                '2': and_vx_vy,
                '3': xor_vx_vy,
                '4': add_vx_vy,
                '5': sub_vx_vy,
                '6': shr_vx_vy,
            }

            instruction_set.get(op)(self, x,y)


        instruction_set={
            '0': sys_handler,
            '1': jmp_addr,
            '6': ld_vx_byte,
            'a': ld_i_addr,
            'd': drw_vx_vy_nibble,
            '2': call_addr,
            'f': sys_timer,
            '7': add_vx_byte,
            '3': se_vx_byte,
            '4': sne_vx_byte,
            'c': rnd_vx_byte,
            'e': skip_key_instructions,
            '8': sys_ula,
        }

        code = format(instruction, '04x')
        instruction_set.get(code[0])(self, code[1:])


        
    
    def run(self):
        self.PC = 512
        while self.runnig:
            instruction = self.memory[self.PC] << 8| self.memory[self.PC+1]
            self.fetch_instruction(instruction)
            self.PC += 2
            self.DT = 0
        
        print('ended game :)')

    

cpu = CPU()
cpu.run()
print(cpu.memory)
# timer()

# load_text_sprites()
# print(memory[512])
# print(memory[1])
# print(memory[2])
# print(memory[3])

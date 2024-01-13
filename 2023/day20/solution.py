import os
from collections import deque
import math

class Module:
    def __init__(self, key, m_type, subs):
        self.key = key
        self.m_type = m_type
        self.subs = subs
        if m_type == '&':
            self.memory = {}
        else:
            self.memory = False
    
    def hashable(self):
        if self.m_type == '&':
            return ''.join([f'{k}{v}' for k, v in self.memory.items()])
        else:
            return 'T' if self.memory else 'F'
    
    def process_pulse(self, sender, pulse):
        if self.m_type == '&':
            self.memory[sender] = pulse
            return False if all(self.memory.values()) else True
        elif self.m_type == '%':
            if not pulse:
                self.memory = not self.memory
                return self.memory
            return None
        elif self.m_type == 'b':
            return False

class PulseModule:
    def __init__(self, modules):
        self.modules = modules
        self.low_pulses = 0
        self.high_pulses = 0
        self.initialize_connections()
        self.seen = {}

    def initialize_connections(self):
        for k, m in self.modules.items():
            for s in m.subs:
                if s in self.modules and self.modules[s].m_type == '&':
                    self.modules[s].memory[m.key] = False

    def propogate_pulse(self):
        pending = deque([('broadcaster', t, False) 
                         for t in self.modules['broadcaster'].subs])
        while pending:
            sender, target, pulse = pending.popleft()
            pending.extend(self.apply_pulse(sender, target, pulse))
        return False

    def apply_pulse(self, sender: str, recipient: str, pulse=False):
        if not pulse:
            self.low_pulses += 1
        elif pulse:
            self.high_pulses += 1

        curr = self.modules.get(recipient, None)
        if curr is None:
            return []

        output = curr.process_pulse(sender, pulse)
        if output is None:
            return []
        return [(curr.key, sub, output) for sub in curr.subs]
    
    def push_button_1000(self):
        for _ in range(1000):
            self.low_pulses += 1
            self.propogate_pulse()
        return self.low_pulses * self.high_pulses

    def find_target(self, end='rx'):
        # This assumes that the target module has a single source module and
        # that source module and its dependencies are all conjunction modules
        # with a regular cyclical occurence pattern.
        try:
            source, = [k for k, v in self.modules.items() if end in v.subs]
        except ValueError as e:
            print('Invalid input. Target module contains multiple sources.')
            exit(0)
        cycles = {}
        reqs = {k: 0 for k, v in self.modules.items() if source in v.subs}
        c = 0
        while True:
            c += 1
            pending = deque([('broadcaster', t, False) 
                            for t in self.modules['broadcaster'].subs])
            while pending:
                sender, target, pulse = pending.popleft()

                if target == source and pulse:
                    reqs[sender] += 1
                    if sender not in cycles:
                        cycles[sender] = c
                if all(reqs.values()):
                    res = 1
                    for cycle_len in cycles.values():
                        res = math.lcm(res, cycle_len)
                    return res
                
                pending.extend(self.apply_pulse(sender, target, pulse))
                
def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        modules = {}
        for line in file.read().splitlines():
            if line.split()[0] == 'broadcaster':
                prefix = 'b'
                key = 'broadcaster'
                subs = line[15:].split(', ')
            else:
                prefix = line[0]
                key = line[1:3]
                subs = line[7:].split(', ')
            modules[key] = Module(key, prefix, subs)
        return modules

if __name__ == '__main__':
    modules = process_input()
    pm = PulseModule(modules)
    print(pm.push_button_1000())
    
    modules = process_input()
    pm = PulseModule(modules)
    print(pm.find_target())
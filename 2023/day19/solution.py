import os
import re

class WorkflowSorter:
    def __init__(self, workflows, parts):
        self.workflows = self.initialize_wf(workflows)
        self.parts = self.initialize_parts(parts)

    def initialize_wf(self, workflows):
        wfs = {}
        for wf in workflows:
            key, rest = wf.strip('}').split('{')
            conditions = rest.split(',')
    
            wfs[key] = []
            last = conditions.pop()
            for c in conditions:
                pat = r'([a-zA-Z])([<>])(\d+):(\w+)'
                cat, op, comp, out = re.match(pat, c).groups()
                wfs[key].append((cat, 
                                 int.__lt__ if op == '<' else int.__gt__, 
                                 int(comp), 
                                 out))
            wfs[key].append(last)
        return wfs
    
    def initialize_parts(self, parts):
        processed = []
        for part in parts:
            vals = {}
            for category in part[1:-1].split(','):
                ch, val = category.split('=')
                vals[ch] = int(val)
            processed.append(vals)
        return processed
    
    def process_items(self):
        wf = self.workflows
        p = self.parts
        res = 0
        for part in p:
            key = 'lqg' if part['a'] > 2381 else 'kt'
            while True:
                process = wf[key]
                matched = False
                for cat, op, val, dest in process[:-1]:
                    if op(part[cat], val):
                        key = dest
                        matched = True
                        break
                if not matched:
                    key = process[-1]
                if key == 'R':
                    break
                elif key == 'A':
                    res += sum(part.values())
                    break
        return res
    
    def combos(self, limits=None, key='in'):
        if limits is None:
            limits = {'x': (1, 4000),
                      'm': (1, 4000),
                      'a': (1, 4000),
                      's': (1, 4000)
                    }
        if key == 'A':
            c = 1
            for lower, upper in limits.values():
                c *= upper - lower + 1
            return c
        elif key == 'R':
            return 0
        wf = self.workflows[key]
        res = 0
        for cat, op, val, dest in wf[:-1]:
            lower, upper = limits[cat]
            if op is int.__lt__:
                success = (lower, min(upper, val - 1))
                fail = (max(val, lower), upper)
            elif op is int.__gt__:
                success = (max(lower, val + 1), upper)
                fail = (lower, min(upper, val))
            if success[0] <= success[1]:
                limits = limits.copy()
                limits[cat] = success
                res += self.combos(limits, dest)
            if fail[0] <= fail[1]:
                limits = limits.copy()
                limits[cat] = fail
        res += self.combos(limits, wf[-1])
        return res

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        return [x.splitlines() for x in file.read().split('\n\n')]

if __name__ == '__main__':
    workflows, parts = process_input()

    wfs = WorkflowSorter(workflows, parts)
    print(wfs.process_items())
    print(wfs.combos())
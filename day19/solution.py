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
            rule = 0
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
            limits = {'x': [1, 4001], 
                      'm': [1, 4001], 
                      'a': [1, 4001], 
                      's': [1, 4001]
                      }
        wf = self.workflows
        if key == 'A':
            return
        elif key == 'R':
            return 0
        for cat, op, val, dest in wf[key][:-1]:

                        




def main_part_one():
    with open('day19/input.txt', 'r') as file:
        workflows, parts  = [x.splitlines() for x in file.read().split('\n\n')]
    wfs = WorkflowSorter(workflows, parts)
    return wfs.process_items()

def main_part_two():    
    with open('day18/input.txt', 'r') as file:
        pass

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())
import os

class SeedMapper():
    def __init__(self, seeds: list[str], maps: list[str]):
        self.seeds = seeds
        self.maps = self.initialize_map(maps)

    def initialize_map(self, maps: list[str]):
        cleaned_maps = []
        for map in maps:
            map = map.split('\n')
            cleaned_maps.append(map[1:])
        return cleaned_maps
    
    def map_seed_ranges(self) -> int:
        seeds = self.seeds
        seed_ranges = list(zip(seeds[::2], seeds[1::2]))
        seed_min = []
        for pair in seed_ranges:
            start, length = int(pair[0]), int(pair[1]) 
            seed_min.append(self.map_ranges([(start, start + length)]))
        return min(seed_min)

    def map_ranges(self, ranges: list[int, int]) -> int:
        for map_layer in self.maps:
            hit = []
            for map in map_layer:
                new_ranges = []
                dest, src, offset = [int(x) for x in map.split()]
                src_end = int(src) + int(offset)
                while ranges:
                    (seed_start, seed_end) = ranges.pop()
                    map_start = min(seed_end, src)
                    x_start = max(seed_start, src)
                    x_end = min(seed_end, src_end)
                    map_end = max(seed_start, src_end)

                    if map_start > seed_start:
                        new_ranges.append((seed_start, map_start))
                    if x_end > x_start:
                        hit.append((x_start - src + dest, x_end - src + dest))
                    if seed_end > map_end:
                        new_ranges.append((map_end, seed_end))

                ranges = new_ranges
            ranges = hit + ranges
        return min(ranges, key=lambda r: r[0])[0]
    
    def get_min_seed_location(self) -> int:
        min_loc = float('inf')
        for seed in self.seeds:
            min_loc = min(min_loc, self.convert_seed_location(int(seed)))
        return min_loc

    def convert_seed_location(self, seed: int) -> int:
        location = seed
        for map in self.maps:
            location = self.map_seed(location, map)
        return location

    def map_seed(self, seed: int, map: list[str]) -> int:
        for mapping in map:
            m = mapping.split()
            dest, src, offset = int(m[0]), int(m[1]), int(m[2])
            if src <= seed < src + offset:
                return seed - src + dest
        return seed

def process_input():
    cwd = os.path.dirname(__file__)
    filepath = f'{cwd}/input.txt'
    with open(filepath, 'r') as file:
        seeds = file.readline().split(':')[1].split()
        maps = [line for line in file.read().strip().split('\n\n')]
        return seeds, maps

if __name__ == '__main__':
    seeds, maps = process_input()
    sm = SeedMapper(seeds, maps)

    print(sm.get_min_seed_location())
    print(sm.map_seed_ranges())
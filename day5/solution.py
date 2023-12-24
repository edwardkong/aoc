class SeedMapper():
    def __init__(self, seeds: list[str], maps: list[str]):
        self.seeds = seeds
        self.maps = self.initialize_map(maps)
    
    @staticmethod
    def seed_ranges(seeds: list[str]):
        all_seeds = []
        for i in range(0, len(seeds), 2):
            src = int(seeds[i])
            rng = int(seeds[i + 1])
            all_seeds.extend(src + r for r in range(rng))
        return all_seeds
    
    def search_ranges(self):
        for map in self.maps:
            for mapping in map:
                m = mapping.split()
                dest, src, offset = int(m[0]), int(m[1]), int(m[2])
                # calculate min, max of ranges

    
    def initialize_map(self, maps: list[str]):
        cleaned_maps = []
        for map in maps:
            map = map.split('\n')
            cleaned_maps.append(map[1:])
        return cleaned_maps

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

def main_part_one():
    with open('day5/input.txt', 'r') as file:
        seeds = file.readline().split(':')[1].split()
        maps = file.read().strip().split('\n\n')
    sm = SeedMapper(seeds, maps)
    return sm.get_min_seed_location()

def main_part_two():
    with open('day5/input.txt', 'r') as file:
        seeds = file.readline().split(':')[1].split()
        maps = file.read().strip().split('\n\n')
    sm = SeedMapper(SeedMapper.seed_ranges(seeds), maps)
    return sm.get_min_seed_location()

if __name__ == '__main__':
    print(main_part_one())
    print(main_part_two())
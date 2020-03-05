import argparse
from math import log2


class Cachesim:
    total = 0
    miss = 0
    sets = 0

    def __init__(self, ways, cache_size, block_size):
        self.cache_size = cache_size
        self.block_size = block_size
        self.ways = ways
        # fully associative cache
        if self.ways == 0:
            self.ways = cache_size // block_size
        self.sets = self.cache_size // (self.block_size * self.ways)
        self.index = int(log2(self.sets))
        self.offset = int(log2(self.block_size))
        self.tag = 32 - self.index - self.offset
        self.cache_sets = {}

    def update_LRU(self, set):
        for tag in set:
            if set[tag] != self.ways - 1:
                set[tag] = set[tag] + 1

    def access_cache(self, set_index, tag):
        self.total += 1
        if set_index not in self.cache_sets:
            self.miss = self.miss + 1
            self.cache_sets[set_index] = {tag: 0}
        else:
            cur_set = self.cache_sets[set_index]
            if tag not in cur_set:
                self.miss = self.miss + 1
                if len(cur_set) < self.ways:
                    # if the set is not full, load in the empty cache block
                    self.update_LRU(cur_set)
                    cur_set[tag] = 0
                else:
                    # if the set is full, evict the LRU block from cache
                    evict_block = max(
                        cur_set, key=cur_set.get
                    )  # returns the key with max value
                    cur_set.pop(evict_block)
                    self.update_LRU(cur_set)
                    cur_set[tag] = 0
            else:
                # if it is in the cache, update the LRU
                cur_tag = cur_set[tag]
                for key in cur_set:
                    if cur_set[key] < cur_tag:
                        cur_set[key] = cur_set[key] + 1
                cur_set[tag] = 0

    def print_result(self):
        miss_rate = round((self.miss / self.total) * 100, 4)
        print("Total:", self.total)
        print("Hits:", self.total - self.miss)
        print("Misses:", self.miss)
        print("Cache size:", self.cache_size)
        print("Block size:", self.block_size)
        print("Miss rate:", miss_rate, "%")
        print("Hit rate:", 100 - miss_rate, "%")
        print("# of sets:", self.sets)
        print("# of ways:", self.ways)
        print("# of tag bits:", self.tag)
        print("# of index bits:", self.index)
        print("# of offset bits:", self.offset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cache Simulator", allow_abbrev=False)
    parser.add_argument("-c", type=int, help="Cache size", default=524288)
    parser.add_argument("-b", type=int, help="Block size", default=16)
    parser.add_argument("-n", type=int, help="Set Associativity", default=4)
    parser.add_argument("-f", required=True, help="Input file name")
    args = parser.parse_args()

    cache_size = int(args.c)
    block_size = int(args.b)
    ways = int(args.n)
    filename = args.f
    cache = Cachesim(ways, cache_size, block_size)
    try:
        with open(filename, "r") as reader:
            for line in reader.readlines():
                rec = line.strip().split(" ")
                inst = rec[0]
                offset = int(rec[1])
                addr = int(rec[2], 16)
                addr = addr + offset
                bin_addr = bin(addr).replace("0b", "").zfill(32)[-32:]
                tag_bits = bin_addr[0: cache.tag]
                index_bits = bin_addr[cache.tag: cache.tag + cache.index]
                if index_bits == "":
                    index_bits = 0
                else:
                    index_bits = int(index_bits, 2)
                cache.access_cache(index_bits, int(tag_bits, 2))
            cache.print_result()

    except Exception as e:
        print(e)
        print("Error reading ", filename)
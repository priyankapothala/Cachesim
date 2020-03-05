# Cache Simulator

- This simulator implements a simple cache, with support for direct mapped, set-associative, and fully-associative mapping.
- We will utilize two sets of traces collected from a run of gcc. The traces gcc-10K.memtrace, and gcc-1M.memtrace contain ~10 thousand and ~1.5 million entries respectively. A sample of the trace is given below:
    ```code
    L -200 7fffe7ff088
    L 0 7fffe7fefd0
    S 8 12ff228
    S 8 12ff208
    L 0 a295e8
    ```
- Each line in the trace file contains the memory instruction type (L = load, S = store), the
offset in decimal, and the memory address in hexadecimal. This trace was obtained
from an x86 machine, and thus the memory address is 44-bits. For this simulator, only 32-bits are considered and the most significant 12 bits are truncated.

## Executing the script

```sh
$ python3 cachesim.py -f [filename] -c [c] -b [b] -n [n]
```

- *f* input file name
- *c* total cache size in bytes
- *b* cache block size in bytes
- *n* set associativity (# ways)
- n = 1 (for direct mapped cache)
- n = 0 (for fully associative cache)
- Default values for c,b,n are  524288, 16 and 4 respectively

## Example

- 512KB 4-way set associative cache with 16B block size
  
```sh
$ python3 cachesim.py -f gcc-10K.memtrace -c 524288 -b 16 -n 4
```

- 512KB direct mapped cache with 32B block size
  
```sh
$ python3 cachesim.py -f gcc-10K.memtrace -c 524288 -b 32 -n 1
```

- 8KB fully associative cache with 16B block size
  
```sh
$ python3 cachesim.py -f gcc-10K.memtrace -c 8192 -b 16 -n 0
```
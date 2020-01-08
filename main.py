import sys
import math
import copy

def main():
    case_dir = sys.argv[1]
    mode = sys.argv[2]
    cache_size = int(sys.argv[3])
    block_size = int(sys.argv[4])
    way = int(sys.argv[5])
    address = int(sys.argv[6])

    lines = readfile(case_dir)
    offset_size, index_size, tag_size = init_info(cache_size, block_size, way, address)
    
    alg = 'LRU'
    if mode == '1':
        alg = 'MRU'

    run(lines, offset_size, index_size, tag_size, way, alg)

def init_info(cache_size, block_size, way, address):
    offset_size = int(math.log(block_size, 2))
    index_size = int(math.log(cache_size * 1024 / 16 / way, 2))
    tag_size = address - offset_size - index_size
    return offset_size, index_size, tag_size


def hex2bin(HEX):
    DEC = int(HEX, 16)
    return "{0:b}".format(DEC)

def bin2hex(BIN):
    DEC = int(BIN, 2)
    return hex(DEC)[2:]

def readfile(case_dir):
    f = open(case_dir, 'r')
    data = f.read()
    lines = data.splitlines()
    return lines

def init_cache(index_size, way):
    cache = []
    for i in range(2**index_size):
        cell = []
        for j in range(way):
            node = {'tag':'', 'c':-1}
            cell.append(node)
        cache.append(cell)
    return cache

def find_empty_node(cache, index):
    for i, node in enumerate(cache[index]):
        if node['tag'] == '':
            return i
    return -1

def hit(cache, index, tag, cycle):
    for node in cache[index]:
        if node['tag'] == tag:
            node['c'] = cycle
            return True
    return False

def replace(cache, index, tag, alg, cycle):
    least_use_pos = 0
    most_use_pos = 0

    for i, node in enumerate(cache[index]):
        if node['c'] < cache[index][least_use_pos]['c']:
            least_use_pos = i
        if node['c'] > most_use_pos:
            most_use_pos = i

    if alg == 'LRU':
        cache[index][least_use_pos]['tag'] = tag
        cache[index][least_use_pos]['c'] = cycle
    else:
        cache[index][most_use_pos]['tag'] = tag
        cache[index][most_use_pos]['c'] = cycle

def run(lines, offset_size, index_size, tag_size, way, alg):
    logs = {}

    cache = init_cache(index_size, way)
    cycle = 0
    for l in lines:
        cycle += 1

        BIN = hex2bin(l)
        tag = bin2hex(BIN[0:tag_size])
        index = int(BIN[tag_size:tag_size+index_size], 2)
        hex_index = hex(index)[2:]

        h = hit(cache, index, tag, cycle)
        if not h:
            node_pos = find_empty_node(cache, index)
            if node_pos != -1:
                cache[index][node_pos]['tag'] = tag
                cache[index][node_pos]['c'] = cycle
            else:
                replace(cache, index, tag, alg, cycle)

        log = {'cycle':cycle, 'cache':cache, 'tag':tag, 'index':index, 'hit':h}
        if hex_index not in logs.keys():
            logs[hex_index] = [copy.deepcopy(log)]
        else:
            logs[hex_index].append(copy.deepcopy(log))
        print(hex_index, cache[index], h)
    output(logs)

def output(logs):
    fp = open("ans.txt", "w")
    for tag in logs.keys():
        # print(logs[tag][0]['hit'])
        fp.write('\nindex: {tag}\n'.format(tag=tag))
        fp.write('{:^6} | {:^41} | {:^6} | {}\n'.format('Cycle', '', 'tag', 'Hit/Miss'))
        for log in logs[tag]:
            # for i in range(len(log)):
            cycle = log['cycle']
            cache = log['cache']
            index = log['index']
            tag = log['tag']
            hit = log['hit']
            if hit == True:
                hit = 'Hit'
            else:
                hit = 'Miss'

            cell = ''
            for node in cache[index]:
                if node['tag'] != '':
                    n = node['tag'] + '(' + str(node['c']) + ')'
                else:
                    n = ''
                cell += '{n:^8} | '.format(n = n)

            fp.write('{cycle:^6} | {cell} {tag:^5} | {hit}\n'.format(cycle=cycle, cell=cell, tag=tag, hit=hit))
            # cache_info = ""
            # for node in log['cache'][log['index']]:
            #     cache_info += node['tag'] +'('+str(cycle)+') '
            # print(cache_info)
            # print(log['hit'])

main()

from collections import defaultdict
from functools import lru_cache
import struct
import time

LETTERS = b'\0abcdefghijklmnopqrstuvwxyz'

class Trie(object):
    def __init__(self, file_):
        self.file_ = file_

    @lru_cache(102400)
    def find_block(self, key):
        if len(key) == 0:
            return 0

        parent_block = self.find_block(key[:-1])
        char_index = LETTERS.index(key[-1])
        
        self.file_.seek(parent_block + 4 * char_index)

        offset_pos = self.file_.tell()
        offset = struct.unpack('i', self.file_.read(4))[0]
        if offset == -1:
            offset = self._create_block()
            self.file_.seek(offset_pos)
            self.file_.write(struct.pack('i', offset))

        return offset

    def add(self, key, values):
        if not isinstance(key, bytes):
            key = bytes(key, 'ascii')

        pointer = self.find_block(key)

        while True:
            self.file_.seek(pointer)
            next_pointer = struct.unpack('i', self.file_.read(4))[0]

            if next_pointer != -1:
                pointer = next_pointer
            else:
                break

        for value in values:
            if not isinstance(value, bytes):
                value = bytes(value, 'ascii')

            value_offset = self._create_value(value)
            self.file_.seek(pointer)
            self.file_.write(struct.pack('i', value_offset))

            pointer = value_offset

    def _create_block(self):
        pos = self.file_.tell()
        
        self.file_.seek(0, 2)
        block_addr = self.file_.tell()
        
        size_of_block = (len(LETTERS) * 4)
        self.file_.write(b'\xff' * size_of_block)

        return block_addr

    def _create_value(self, value):
        pos = self.file_.tell()
        
        self.file_.seek(0, 2)

        block_addr = self.file_.tell()
        self.file_.write(struct.pack('ii', -1, len(value)))
        self.file_.write(value)

        return block_addr



def generate_variants(word):
#    return [word]

    # Source: https://norvig.com/spell-correct.html
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts + [word])


if __name__ == '__main__':
    trie_file = open("trie.data", 'w+b')
    trie = Trie(trie_file)
    trie._create_block()

    print("Adding words...")
    with open('words2.txt', 'r') as words_file:
        i = 0
        j = 0

        words = defaultdict(set)
        def flush():
            flush_words = len(words)
            print(f'Flushing {flush_words} keys...')
            start_t = time.time()

            for key in sorted(words.keys()):
                trie.add(key, words[key])
            words.clear()
            
            took = time.time() - start_t
            print(f'took {took} seconds. ({1000 * took / flush_words} ms per key.')

            print(f'Total: {j} keys, {i} values')
        for word in words_file:
            word = word.strip()
            
            i += 1
            for variant in generate_variants(word):
                words[variant].add(word)
                j += 1

            if len(words) >= 50000:
                flush()
                
        flush()

from collections import defaultdict, Counter
from functools import lru_cache
import struct
import time

from config import LETTERS

class Trie(object):
    def __init__(self):
        self.buffer = bytearray(256 * 1024 * 1024)
        self.position = 0
        self.length = 0
    
    def seek(self, position, whence=0):
        if whence == 0:
            self.position = position
        elif whence == 1:
            self.position += position
        elif whence == 2:
            self.position = self.length - position
        else:
            raise Error('Invalid whence')
    
    def tell(self):
        return self.position
    
    def read(self, length):
        value = self.buffer[self.position:self.position + length]
        self.position += length
        
        return value

    def write(self, value):
        if self.position + len(value) > self.length:
            self.length = self.position + len(value)
        self.buffer[self.position:self.position + len(value)] = value
        self.position += len(value)

    def serialize(self):
        return self.buffer[:self.length]

    @lru_cache(102400)
    def find_block(self, key):
        if len(key) == 0:
            return 0

        parent_block = self.find_block(key[:-1])
        char_index = LETTERS.index(key[-1])
        
        self.seek(parent_block + 4 * char_index)

        offset_pos = self.tell()
        offset = struct.unpack('i', self.read(4))[0]
        if offset == -1:
            offset = self._create_block()
            self.seek(offset_pos)
            self.write(struct.pack('i', offset))

        return offset

    def add(self, key, value):
        if not isinstance(key, bytes):
            key = bytes(key, 'ascii')

        pointer = self.find_block(key)

        while True:
            self.seek(pointer)
            next_pointer = struct.unpack('i', self.read(4))[0]

            if next_pointer != -1:
                pointer = next_pointer
            else:
                break

        if not isinstance(value, int):
            value = int(value)

        self.seek(pointer)
        self.write(struct.pack('i', value))

    def _create_block(self):
        pos = self.tell()
        
        self.seek(0, 2)
        block_addr = self.tell()
        
        size_of_block = (len(LETTERS) * 4)
        self.write(b'\xff' * size_of_block)

        return block_addr

if __name__ == '__main__':
    trie = Trie()
    trie._create_block()

    print("Adding words...")

    words = open('words.txt').readlines()
    # import nltk
    # words = nltk.corpus.brown.words()
    
    words = [word.strip() for word in words]
    words = [bytes(word.lower(), 'ascii') for word in words]
    valid_words = filter(lambda word: all([w in LETTERS for w in word]), words)
    
    c = Counter(valid_words)
    for word, count in c.items():
        word = word.strip()
        trie.add(word, count)

    print("Write to file...")
    with open("trie.data", 'w+b') as trie_file:
        trie_file.write(trie.serialize())

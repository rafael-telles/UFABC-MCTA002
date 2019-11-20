import struct
import sys
import mmap

from config import LETTERS

class Trie(object):
    def __init__(self, buffer):
        self.buffer = buffer
        pass

    def search_exact(self, key):
        if not isinstance(key, bytes):
            key = bytes(key, 'ascii')
        
        key += b'\0'
        i = 0
        
        offset = 0
        while i < len(key):
            char_index = LETTERS.index(key[i])

            offset += char_index * 4
            offset = struct.unpack('i', self.buffer[offset:offset + 4])[0]
            if offset == -1:
                return None
            
            i += 1

        values = []
        while offset != -1:
            next_offset, value_length = struct.unpack('ii', self.buffer[offset:offset + 8])
            offset += 8
            
            value = self.buffer[offset:offset + value_length]
            values.append(value)

            offset = next_offset
        return values

    def search(self, word):
        if not isinstance(word, bytes):
            word = bytes(word, 'ascii')
        
        results = {}
        _search_edits(self.buffer, 0, b'', word, results, 1)

        items = sorted(results.items(), key=lambda item: item[1], reverse=True)
        items_sum = sum([item[1] for item in items])
        items = [[item[0], item[1] / items_sum] for item in items]
        return items


def _search_edits(buffer, buffer_offset, prefix, word, results, depth):
        letters_offsets = struct.unpack(f'{"i" * len(LETTERS)}', buffer[buffer_offset:buffer_offset + 4 * len(LETTERS)])
        letter_to_offset = dict(filter(lambda pair: pair[1] >= 0, zip(LETTERS, letters_offsets)))

        if len(word) == 0 and depth >= 0 and 0 in letter_to_offset:
            results[prefix] = letter_to_offset[0]

        if depth >= 1:
            # deletion
            _search_edits(buffer, buffer_offset, prefix, word[1:] if len(word) > 0 else b'', results, depth - 1)

            for letter, offset in letter_to_offset.items():
                if letter == 0: continue

                # insertion
                _search_edits(buffer, offset, prefix + bytes([letter]), word, results, depth - 1)

                # substitution
                _search_edits(buffer, offset, prefix + bytes([letter]), word[1:], results, depth - 1)

            # transposition
            _search_edits(buffer, buffer_offset, prefix, word[1:2] + word[0:1] + word[2:], results, depth - 1)


        if len(word) >= 1 and word[0] in letter_to_offset:
            _search_edits(buffer, letter_to_offset[word[0]], prefix + word[0:1], word[1:], results, depth)


if __name__ == '__main__':
    word = sys.argv[1]
    
    with open('trie.data', 'r+') as trie_file:
        buffer = mmap.mmap(trie_file.fileno(), 0)
        trie = Trie(buffer)

        results = trie.search(word)
        print(results)

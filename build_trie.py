from collections import defaultdict
import struct

class Trie(object):
    def __init__(self):
        self.d: defaultdict = defaultdict(Trie)
        self.values: set(bytes) = set()

    def add(self, key, value):
        if not isinstance(key, bytes):
            key = bytes(key, 'ascii')
        if not isinstance(value, bytes):
            value = bytes(value, 'ascii')
        
        first_char = key[0] if len(key) > 0 else 0

        if first_char == 0:
            self.d[first_char].values.add(value)
        else:
            self.d[first_char].add(key[1:], value)

    def serialize(self):
        result = bytearray()
        if self.values:
            result += struct.pack('i', len(self.values))
            for value in self.values:
                result += struct.pack(f'i{"b"*len(value)}', len(value), *value)
        else:
            keys = sorted(self.d.keys())
            sub_tries = [self.d[key] for key in keys]
            
            serialized_sub_tries = [sub_trie.serialize() for sub_trie in sub_tries]
            serialized_sub_tries_offsets = [0 for _ in sub_tries]
            for i in range(1, len(sub_tries)):
                serialized_sub_tries_offsets[i] = serialized_sub_tries_offsets[i - 1] + len(serialized_sub_tries[i - 1])

            result += struct.pack('i', len(keys))
            result += struct.pack(f'{"b"*len(keys)}', *keys)
            result += struct.pack(f'{"i"*len(keys)}', *serialized_sub_tries_offsets)
            for s in serialized_sub_tries:
                result += s
        return result

def generate_variants(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts + [word])


if __name__ == '__main__':
    trie = Trie()

    print("Adding words...")
    with open('words2.txt', 'r') as words_file:
        for word in words_file:
            word = word.strip()
            for variant in generate_variants(word):
                trie.add(variant, word)

    print("Serializing...")
    data = trie.serialize()
    with open('trie.data', 'wb') as f:
        f.write(data)

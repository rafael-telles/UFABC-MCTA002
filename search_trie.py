import struct
import sys
import mmap

LETTERS = b'\0abcdefghijklmnopqrstuvwxyz'

def search(buffer, key):
    if not isinstance(key, bytes):
        key = bytes(key, 'ascii')
    
    key += b'\0'
    i = 0
    
    offset = 0
    while i < len(key):
        char_index = LETTERS.index(key[i])

        offset += char_index * 4
        offset = struct.unpack('i', buffer[offset:offset + 4])[0]
        if offset == -1:
            return None
        
        i += 1

    values = []
    while offset != -1:
        next_offset, value_length = struct.unpack('ii', buffer[offset:offset + 8])
        offset += 8
        
        value = buffer[offset:offset + value_length]
        values.append(value)

        offset = next_offset
    return values


def edits(buffer, buffer_offset, prefix, word, results, depth):
    letters_offsets = struct.unpack(f'{"i" * len(LETTERS)}', buffer[buffer_offset:buffer_offset + 4 * len(LETTERS)])
    letter_to_offset = dict(filter(lambda pair: pair[1] >= 0, zip(LETTERS, letters_offsets)))

    if len(word) == 0 and depth >= 0 and 0 in letter_to_offset:
        results[prefix] = letter_to_offset[0]

    if depth >= 1:
        # deletion
        edits(buffer, buffer_offset, prefix, word[1:] if len(word) > 0 else b'', results, depth - 1)

        for letter, offset in letter_to_offset.items():
            if letter == 0: continue

            # insertion
            edits(buffer, offset, prefix + bytes([letter]), word, results, depth - 1)

            # substitution
            edits(buffer, offset, prefix + bytes([letter]), word[1:], results, depth - 1)

        # transposition
        edits(buffer, buffer_offset, prefix, word[1:2] + word[0:1] + word[2:], results, depth - 1)


    if len(word) >= 1 and word[0] in letter_to_offset:
        edits(buffer, letter_to_offset[word[0]], prefix + word[0:1], word[1:], results, depth)

def search(buffer, word):
    if not isinstance(word, bytes):
        word = bytes(word, 'ascii')
    
    results = {}
    edits(buffer, 0, b'', word, results, 2)

    return results

if __name__ == '__main__':
    word = sys.argv[1]
    
    with open('trie.data', 'r+') as trie_file:
        buffer = mmap.mmap(trie_file.fileno(), 0)

        results = search(buffer, word)
        print(results)

import struct
import sys

LETTERS = b'\0abcdefghijklmnopqrstuvwxyz'

def search(reader, key):
    key += b'\0'
    i = 0
    while i < len(key):
        char_index = LETTERS.index(key[i])
        reader.seek(char_index * 4, 1)

        offset = struct.unpack('i', reader.read(4))[0]
        if offset == -1:
            return None
        
        reader.seek(offset)
        i += 1

    values = []
    while offset != -1:
        reader.seek(offset)
        next_offset, value_length = struct.unpack('ii', reader.read(8))
        value = reader.read(value_length)
        values.append(value)

        offset = next_offset
    return values


if __name__ == '__main__':
    reader = open('trie.data', 'rb')
    word = sys.argv[1]
    key = bytes(word, 'ascii')

    value = search(reader, key)

    print(value)
import struct
import sys

def search(reader, key):
    if len(key) == 0:
        values_quantity = struct.unpack('i', reader.read(4))[0]
        values = []
        for _ in range(values_quantity):
            value_length = struct.unpack('i', reader.read(4))[0]
            value = reader.read(value_length)
            values.append(value)
        return values
    else:
        first_char = key[0]
        quantity_of_keys = struct.unpack('i', reader.read(4))[0]
        keys = [struct.unpack('b', reader.read(1))[0] for _ in range(quantity_of_keys)]
        offsets = [struct.unpack('i', reader.read(4))[0] for _ in range(quantity_of_keys)]

        try:
            index = keys.index(first_char)
            offset = offsets[index]
            reader.seek(offset, 1)
            return search(reader, key[1:])
        except:
            return None


if __name__ == '__main__':
    reader = open('trie.data', 'rb')
    word = sys.argv[1]
    print(search(reader, bytes(word, 'ascii') + b'\0'))
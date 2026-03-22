import argparse
import pathlib
from functools import partial

HASH_BITS = 10
HASH_SIZE = (1 << HASH_BITS)

bytes_to_int = partial(int.from_bytes, byteorder="little")
int_to_bytes = partial(int.to_bytes, length=4, byteorder="little")

def read_wad(path: pathlib.Path):
    with open(path, "rb") as file:
        header = file.read(12)
        if header[:4] != b"DIR\x1A":
            raise IOError("Did not find header signature")
        # length = bytes_to_int(header[4:8])
        toc_offset = bytes_to_int(header[8:12])

        file.seek(toc_offset)
        signature = file.read(4)
        if bytes_to_int(signature) != 0x0000000A:
            raise IOError("Did not find ToC signature")

        hash_table = {}
        for i in range(0, 1024):
            offset = bytes_to_int(file.read(4))
            if offset:
                hash_table[i] = offset

        files = {}
        for entry in hash_table.values():
            next_offset = entry
            while next_offset:
                # Metadata
                file.seek(toc_offset+next_offset)
                next_offset = bytes_to_int(file.read(4))
                file_offset = bytes_to_int(file.read(4))
                file_length = bytes_to_int(file.read(4))
                file_name = file.read(4)
                while 0x00 not in file_name:
                    read = file.read(4)
                    if not read:
                        breakpoint()
                        return
                    file_name += read
                file_name = file_name.split(b"\x00")[0]

                # File
                file.seek(file_offset)
                files[file_name] = file.read(file_length)

    return files

def hash(char_star: bytes):
    sum = 0
    while char_star:
        sum = ((sum << 1) % HASH_SIZE) | (sum >> (HASH_BITS - 1) & 1)
        sum += char_star[0]
        char_star = char_star[1:]
        sum %= HASH_SIZE
    return sum

def pad(char_star: bytes):
    return char_star + (-len(char_star) % 4)*b"\00"

def write_wad(path: pathlib.Path, files: dict[bytes, bytes]):
    length = 0
    hash_offset = 0x1004
    toc_offset = 12

    hash_table = {}
    for fname in files:
        hash_ = hash(fname)
        hash_table[hash_] = hash_table.get(hash_, []) + [fname]

    content = b""
    hash_bytes = b""
    file_list = b""

    for i in range(0, 1024):
        seq = hash_table.get(i, [])
        hash_bytes += int_to_bytes(hash_offset) if seq else int_to_bytes(0)

        for j in range(len(seq)):
            fname_pad = pad(seq[j] + b"\x00")
            content_pad = pad(files[seq[j]] + b"\1a\00")

            file_list += int_to_bytes(hash_offset + 12 + len(fname_pad)) if (j + 1 < len(seq)) else int_to_bytes(0)
            file_list += int_to_bytes(12 + len(content))
            file_list += int_to_bytes(len(files[seq[j]]))
            file_list += fname_pad

            content += content_pad

            hash_offset += 12 + len(fname_pad)
            toc_offset += len(content_pad)

    with open(path, "wb") as file:
        file.write(b"DIR\x1A")
        file.write(int_to_bytes(length))
        file.write(int_to_bytes(toc_offset))

        file.write(content)
        file.write(int_to_bytes(0x0000000A))
        file.write(hash_bytes)
        file.write(file_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser("python wad.py")
    parser.add_argument("wad")

    args = parser.parse_args()

    wad = read_wad(args.wad)
    print(wad)

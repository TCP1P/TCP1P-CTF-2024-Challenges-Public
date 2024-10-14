import argparse
import os
import sys
import lzma

class ForevncryptCompressor:
    def __init__(self, filename, password, action):
        self.filename = filename
        self.password = password
        self.action = action

    def xor(self, data, key):
        try:
            return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        except:
            return b''


    def validate_file(self):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(self.filename)

    def header(self):
        HEADER = 'FOREVNCRYPT'
        return HEADER.encode('utf-8')

    def compress(self):
        target_file = open(self.filename, 'rb').read()
        compressed = lzma.compress(target_file)
        return compressed

    def decompress(self):
        target_file = open(self.filename, 'rb').read()
        header_length = len(self.header())
        check_header = target_file[:header_length]
        if check_header != self.header():
            raise Exception('Not a forevncrypt file')
        name_length = int.from_bytes(target_file[header_length:header_length+4], 'big')
        name = target_file[header_length+4:header_length+4+name_length]
        compressed = target_file[header_length+4+name_length:]
        return {
            'name': name.decode('utf-8'),
            'data': lzma.decompress(compressed)
        }

    def encrypt_compress(self):
        compressed = self.compress()
        keygen = os.urandom(2)
        compressed = self.xor(compressed, keygen)
        result = self.xor(compressed, self.password.encode('utf-8'))
        return result
    
    def archive(self):
        self.validate_file()
        file = self.header()
        if not self.password:
            if not self.action:
                file += len(self.filename).to_bytes(4, 'big')
                file += self.filename.encode('utf-8')
                file += self.compress()
                open(f'{'.'.join(self.filename.split('.')[:-1])}.forevncrypt', 'wb').write(file)
            else:
                file = self.decompress()
                open(file['name'], 'wb').write(file['data'])
        else:
            if not self.action:
                file += len(self.password).to_bytes(4, 'big')
                file += self.filename.encode('utf-8')
                file += self.encrypt_compress()
                os.remove(self.filename)
                open(f'{'.'.join(self.filename.split('.')[:-1])}.forevncrypt', 'wb').write(file)
            else:
                print("Not implemented yet")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="A custom file compressor made just for fun")
    argparser.add_argument("filename", help="file to execute")
    argparser.add_argument("-d", "--decompress", action="store_true", help="Decompress file")
    argparser.add_argument("-p", "--password", help="Password for encryption")
    args = argparser.parse_args()
    try:
        archive = ForevncryptCompressor(args.filename, args.password, args.decompress)
        archive.archive()
    except Exception as e:
        print('Error:', e)
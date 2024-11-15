class LZWCompressor:
    def __init__(self):
        self.dictionary = {}
        self.dictionary_size = 0
        self.MAX_SIZE = pow(2, 15)

    def code(self, w):
        return self.dictionary[w]

    def reset_dictionary(self):
        self.dictionary = {}
        self.dictionary_size = 0

    def fill_dictionary_compression(self):
        for i in range(256):
            i_byte = i.to_bytes(1, byteorder='little')
            self.dictionary[i_byte] = i
        self.dictionary_size = len(self.dictionary)

    def fill_dictionary_decompression(self):
        for i in range(256):
            i_byte = i.to_bytes(1, byteorder='little')
            key_byte = i.to_bytes(2, byteorder='little')
            self.dictionary[key_byte] = i_byte
        self.dictionary_size = len(self.dictionary)

    def decompress_binary_file(self, filename: str):
        self.reset_dictionary()
        self.fill_dictionary_decompression()

        original_filename = filename.split('.lzw')[0]
        with open(filename, 'rb') as input_file, open('original-' + original_filename, 'wb') as output_file:
            string = ''
            next_code = 256
            while True:
                rec = input_file.read(2)
                if len(rec) != 2:
                    break
                if not rec in self.dictionary:
                    value = string + (string[0].to_bytes(1, byteorder='little'))
                    self.dictionary[rec] = value
                output_file.write(self.dictionary[rec])
                if not (len(string) == 0) and next_code < self.MAX_SIZE:
                    # print('the string is', string)
                    # print('next_code is now', next_code)

                    key = next_code.to_bytes(2, byteorder='little')
                    value = string + (self.dictionary[rec][0].to_bytes(1, byteorder='little'))
                    self.dictionary[key] = value
                    next_code += 1
                string = self.dictionary[rec]

    def compress_binary_file(self, filename):
        self.reset_dictionary()
        self.fill_dictionary_compression()

        with open(filename, "rb") as input_file, open(filename + ".lzw", "wb") as output_file:
            w = input_file.read(1)
            while True:
                K = input_file.read(1)
                if not K:
                    value = self.code(w)
                    value_bytes = value.to_bytes(2, byteorder='little')
                    output_file.write(value_bytes)
                    break
                wK = w + K
                if wK in self.dictionary:
                    w = wK
                else:
                    value = self.code(w)
                    value_bytes = value.to_bytes(2, byteorder='little')
                    output_file.write(value_bytes)
                    if len(self.dictionary) < self.MAX_SIZE:
                        self.dictionary[wK] = self.dictionary_size
                        self.dictionary_size += 1
                    w = K
            print('size of dictionary', len(self.dictionary))


def main():
    filename = 'pg100.txt'
    LZWCompressor().compress_binary_file(filename)
    compressed_file = filename + '.lzw'
    LZWCompressor().decompress_binary_file(compressed_file)


if __name__ == "__main__":
    main()

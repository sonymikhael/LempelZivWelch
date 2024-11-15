class LZWCompressor:
    def __init__(self):
        self.dictionary = {}
        self.dictionary_size = 0
        self.MAX_SIZE = pow(2, 15)

    def code(self, w):
        return self.dictionary[w]

    def reset_dictionary(self):
        print('will reset dictionary, size is already: ', len(self.dictionary))
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
        print('====================decompress==================')

        original_filename = filename.split('.lzw')[0]
        with open(filename, 'rb') as input_file, open('original-' + original_filename, 'wb') as output_file:
            string = ''
            next_code = 256
            while True:
                rec = input_file.read(2)
                print('rec', rec)
                if len(rec) != 2:
                    print('EOF encountered')
                    break
                if not rec in self.dictionary:
                    print('rec not in reverse_dict')
                    value = string + (string[0].to_bytes(1, byteorder='little'))
                    print('table[', rec, '] =', value)
                    self.dictionary[rec] = value
                print('will write', self.dictionary[rec], 'to file')
                output_file.write(self.dictionary[rec])
                if not (len(string) == 0) and next_code < self.MAX_SIZE:
                    # print('the string is', string)
                    # print('next_code is now', next_code)

                    key = next_code.to_bytes(2, byteorder='little')
                    value = string + (self.dictionary[rec][0].to_bytes(1, byteorder='little'))
                    print('will add key', key, ' (', next_code, ') with value', value)
                    self.dictionary[key] = value
                    next_code += 1
                print('string is now', self.dictionary[rec])
                string = self.dictionary[rec]
                # print('string is now', string)

    def compress_binary_file(self, filename):
        self.reset_dictionary()
        self.fill_dictionary_compression()

        with open(filename, "rb") as input_file, open(filename + ".lzw", "wb") as output_file:
            w = input_file.read(1)
            print('w', w)
            while True:
                K = input_file.read(1)
                print('K', K)
                if not K:
                    value = self.code(w)
                    value_bytes = value.to_bytes(2, byteorder='little')
                    print('will write', w, 'to the file')
                    output_file.write(value_bytes)
                    break
                wK = w + K
                print('wK', wK)
                if wK in self.dictionary:
                    print('wK is in dictionary, w becomes wK')
                    w = wK
                    print('w', w)
                else:
                    print('wK is not in dictionary')
                    value = self.code(w)
                    print("retrieved code for w", w, 'will write it to compressed file')
                    value_bytes = value.to_bytes(2, byteorder='little')

                    output_file.write(value_bytes)
                    if len(self.dictionary) < self.MAX_SIZE:
                        print('added wK', wK, 'to dictionary with code', self.dictionary_size)
                        self.dictionary[wK] = self.dictionary_size
                        self.dictionary_size += 1
                    print('will assign K', K, 'to w')
                    w = K
                    print('w', w)


def main():
    print("Hello world")
    filename = 'issue2.txt'
    LZWCompressor().compress_binary_file(filename)
    compressed_file = filename + '.lzw'
    LZWCompressor().decompress_binary_file(compressed_file)


if __name__ == "__main__":
    main()

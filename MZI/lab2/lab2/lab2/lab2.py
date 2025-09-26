import random
import binascii


class STB3410131:
    
    # H-table
    H_BOX = [
        0xB1, 0x94, 0xBA, 0xC8, 0x0A, 0x08, 0xF5, 0x3B, 0x36, 0x6D, 0x00, 0x8E, 0x58, 0x4A, 0x5D, 0xE4,
        0x85, 0x04, 0xFA, 0x9D, 0x1B, 0xB6, 0xC7, 0xAC, 0x25, 0x2E, 0x72, 0xC2, 0x02, 0xFD, 0xCE, 0x0D,
        0x5B, 0xE3, 0xD6, 0x12, 0x17, 0xB9, 0x61, 0x81, 0xFE, 0x67, 0x86, 0xAD, 0x71, 0x6B, 0x89, 0x0B,
        0x5C, 0xB0, 0xC0, 0xFF, 0x33, 0xC3, 0x56, 0xB8, 0x35, 0xC4, 0x05, 0xAE, 0xD8, 0xE0, 0x7F, 0x99,
        0xE1, 0x2B, 0xDC, 0x1A, 0xE2, 0x82, 0x57, 0xEC, 0x70, 0x3F, 0xCC, 0xF0, 0x95, 0xEE, 0x8D, 0xF1,
        0xC1, 0xAB, 0x76, 0x38, 0x9F, 0xE6, 0x78, 0xCA, 0xF7, 0xC6, 0xF8, 0x60, 0xD5, 0xBB, 0x9C, 0x4F,
        0xF3, 0x3C, 0x65, 0x7B, 0x63, 0x7C, 0x30, 0x6A, 0xDD, 0x4E, 0xA7, 0x79, 0x9E, 0xB2, 0x3D, 0x31,
        0x3E, 0x98, 0xB5, 0x6E, 0x27, 0xD3, 0xBC, 0xCF, 0x59, 0x1E, 0x18, 0x1F, 0x4C, 0x5A, 0xB7, 0x93,
        0xE9, 0xDE, 0xE7, 0x2C, 0x8F, 0x0C, 0x0F, 0xA6, 0x2D, 0xDB, 0x49, 0xF4, 0x6F, 0x73, 0x96, 0x47,
        0x06, 0x07, 0x53, 0x16, 0xED, 0x24, 0x7A, 0x37, 0x39, 0xCB, 0xA3, 0x83, 0x03, 0xA9, 0x8B, 0xF6,
        0x92, 0xBD, 0x9B, 0x1C, 0xE5, 0xD1, 0x41, 0x01, 0x54, 0x45, 0xFB, 0xC9, 0x5E, 0x4D, 0x0E, 0xF2,
        0x68, 0x20, 0x80, 0xAA, 0x22, 0x7D, 0x64, 0x2F, 0x26, 0x87, 0xF9, 0x34, 0x90, 0x40, 0x55, 0x11,
        0xBE, 0x32, 0x97, 0x13, 0x43, 0xFC, 0x9A, 0x48, 0xA0, 0x2A, 0x88, 0x5F, 0x19, 0x4B, 0x09, 0xA1,
        0x7E, 0xCD, 0xA4, 0xD0, 0x15, 0x44, 0xAF, 0x8C, 0xA5, 0x84, 0x50, 0xBF, 0x66, 0xD2, 0xE8, 0x8A,
        0xA2, 0xD7, 0x46, 0x52, 0x42, 0xA8, 0xDF, 0xB3, 0x69, 0x74, 0xC5, 0x51, 0xEB, 0x23, 0x29, 0x21,
        0xD4, 0xEF, 0xD9, 0xB4, 0x3A, 0x62, 0x28, 0x75, 0x91, 0x14, 0x10, 0xEA, 0x77, 0x6C, 0xDA, 0x1D
    ]
    
    BLOCK_SIZE = 16  # bytes
    WORD_SIZE = 4    # bytes
    ROUNDS = 8
    KEY_SIZE = 32    # bytes

    def __init__(self, key):
        if len(key) != self.KEY_SIZE:
            raise ValueError(f"Key must be {self.KEY_SIZE} bytes long")
            
        # Convert key to words (32-bit numbers)
        key_words = [self.bytes_to_word(key[i:i+4]) for i in range(0, len(key), 4)]
        self.round_keys = [key_words[i % 8] for i in range(56)]

    def rotate_left(self, value, shift):
        bit_length = 32
        shift = shift % bit_length
        return ((value << shift) | (value >> (bit_length - shift))) & 0xFFFFFFFF

    def word_to_bytes(self, word):
        return [(word >> shift) & 0xFF for shift in [24, 16, 8, 0]]

    def bytes_to_word(self, bytes_list):
        return sum(byte << shift for byte, shift in zip(bytes_list, [24, 16, 8, 0]))

    def reverse_word(self, word):
        bytes_list = self.word_to_bytes(word)
        bytes_list.reverse()
        return self.bytes_to_word(bytes_list)

    def modular_subtract(self, x, y):
        return (x - y) & 0xFFFFFFFF

    def modular_add(self, *values):
        result = 0
        for value in values:
            result = (result + self.reverse_word(value)) & 0xFFFFFFFF
        return self.reverse_word(result)

    def h_box_substitution(self, byte):
        return self.H_BOX[byte]

    def g_function(self, x, k):
        # Apply H-box to each byte
        substituted = self.bytes_to_word([self.h_box_substitution(byte) for byte in self.word_to_bytes(x)])
        # Circular shift and return result
        return self.reverse_word(self.rotate_left(self.reverse_word(substituted), k))

    def encrypt_block(self, plaintext):
        if len(plaintext) != self.BLOCK_SIZE:
            raise ValueError(f"Block size must be {self.BLOCK_SIZE} bytes")
            
        a, b, c, d = [self.bytes_to_word(plaintext[i:i+4]) for i in range(0, self.BLOCK_SIZE, 4)]
        
        # 8 rounds
        for round_num in range(self.ROUNDS):
            b ^= self.g_function(self.modular_add(a, self.round_keys[7*round_num + 0]), 5)
            c ^= self.g_function(self.modular_add(d, self.round_keys[7*round_num + 1]), 21)
            
            a = self.reverse_word(self.modular_subtract(self.reverse_word(a),
                                         self.reverse_word(self.g_function(self.modular_add(b, self.round_keys[7*round_num + 2]), 13))))
            
            e = self.g_function(self.modular_add(b, c, self.round_keys[7*round_num + 3]), 21) ^ self.reverse_word(round_num + 1)
            
            b = self.modular_add(b, e)
            c = self.reverse_word(self.modular_subtract(self.reverse_word(c), self.reverse_word(e)))
            d = self.modular_add(d, self.g_function(self.modular_add(c, self.round_keys[7*round_num + 4]), 13))
            
            b ^= self.g_function(self.modular_add(a, self.round_keys[7*round_num + 5]), 21)
            c ^= self.g_function(self.modular_add(d, self.round_keys[7*round_num + 6]), 5)
            
            # Word permutations
            a, b = b, a
            c, d = d, c
            b, c = c, b
        
        # Result
        result = []
        for word in [b, d, a, c]:
            result.extend(self.word_to_bytes(word))
            
        return result

    def decrypt_block(self, ciphertext):
        if len(ciphertext) != self.BLOCK_SIZE:
            raise ValueError(f"Block size must be {self.BLOCK_SIZE} bytes")
            
        a, b, c, d = [self.bytes_to_word(ciphertext[i:i+4]) for i in range(0, self.BLOCK_SIZE, 4)]
        
        # 8 rounds
        for round_num in reversed(range(self.ROUNDS)):
            b ^= self.g_function(self.modular_add(a, self.round_keys[7*round_num + 6]), 5)
            c ^= self.g_function(self.modular_add(d, self.round_keys[7*round_num + 5]), 21)
            
            a = self.reverse_word(self.modular_subtract(self.reverse_word(a),
                                         self.reverse_word(self.g_function(self.modular_add(b, self.round_keys[7*round_num + 4]), 13))))
            
            e = self.g_function(self.modular_add(b, c, self.round_keys[7*round_num + 3]), 21) ^ self.reverse_word(round_num + 1)
            
            b = self.modular_add(b, e)
            c = self.reverse_word(self.modular_subtract(self.reverse_word(c), self.reverse_word(e)))
            d = self.modular_add(d, self.g_function(self.modular_add(c, self.round_keys[7*round_num + 2]), 13))
            
            b ^= self.g_function(self.modular_add(a, self.round_keys[7*round_num + 1]), 21)
            c ^= self.g_function(self.modular_add(d, self.round_keys[7*round_num + 0]), 5)
            
            # Reverse word permutations
            a, b = b, a
            c, d = d, c
            a, d = d, a
        
        # Result
        result = []
        for word in [c, a, d, b]:
            result.extend(self.word_to_bytes(word))
            
        return result


def char_to_extended_ascii(ch):
    code = ord(ch)
    return code if code < 140 else code - 900


def extended_ascii_to_char(code):
    return chr(code) if code < 140 else chr(code + 900)


def generate_key():
    return bytes(random.randint(0, 255) for _ in range(32))


def main():
    # Read input file
    try:
        with open("input.txt", "r", encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: input.txt file not found")
        return
    except UnicodeDecodeError:
        print("Error: cannot read file in UTF-8 encoding")
        return

    original_text = text

    count = 0
    while len(text) % 16:
        text += '0'
        count += 1
    encrypted_result = []
    decrypted_result = []

    for i in range(len(text) // 16):
        arr_text = [char_to_extended_ascii(item) for item in text[16 * i: 16 * (i + 1)]]

        random_bytes = bytes([random.randint(0, 255) for _ in range(32)])
        hex_str = random_bytes.hex()
        key = list(binascii.unhexlify(hex_str))
        my_stb = STB3410131(key)
        encrypted = my_stb.encrypt_block(arr_text)
        encrypted_result.extend(encrypted)
        decrypted_result.extend(my_stb.decrypt_block(encrypted))

    encrypted_result = encrypted_result[:len(encrypted_result) - count]
    decrypted_result = decrypted_result[:len(decrypted_result) - count]
    with open("encrypted.txt", "w", encoding='utf-8') as f:
        for item in encrypted_result:
            f.write(str(item) + ' ')
    print("Encryption completed. Result in encrypted.txt")

    decrypted_text = ""
    with open("decrypted.txt", "w", encoding='utf-8') as f:
        for item in decrypted_result:
            char = extended_ascii_to_char(item)
            decrypted_text += char 
            f.write(char)
    
        print("Decryption completed. Result in decrypted.txt")

    if original_text == decrypted_text:
        print("Verification: original and decrypted texts match!")
    else:
        print("Warning: original and decrypted texts do not match!")


if __name__ == '__main__':
    main()
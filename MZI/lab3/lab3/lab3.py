import random
from sympy import isprime


class RabinCryptosystem:
    def __init__(self):
        self.N = None
        self.p = None
        self.q = None
    
    def generate_keys(self, bits=512):
        while True:
            p = random.getrandbits(bits)
            if isprime(p) and p % 4 == 3:
                break
        
        while True:
            q = random.getrandbits(bits)
            if isprime(q) and q % 4 == 3:
                break
        
        self.N = p * q
        self.p = p
        self.q = q
        return self.N, self.p, self.q
    
    def encrypt(self, message):
        if self.N is None:
            raise ValueError("Keys not generated. Please generate keys first.")
        
        m = int.from_bytes(message.encode('utf-8'), 'big')
        if m >= self.N:
            raise ValueError("The message is too large for the key size")
        
        ciphertext = pow(m, 2, self.N)
        return ciphertext
    
    def decrypt(self, ciphertext):
        if self.p is None or self.q is None:
            raise ValueError("Private keys not available. Please generate keys first.")
        
        m_p = pow(ciphertext, (self.p + 1) // 4, self.p)
        m_q = pow(ciphertext, (self.q + 1) // 4, self.q)
        
        _, yp, yq = self.extended_gcd(self.p, self.q)
        N = self.p * self.q
        
        # Calculate all four possible roots
        r1 = (yp * self.p * m_q + yq * self.q * m_p) % N
        r2 = N - r1
        r3 = (yp * self.p * m_q - yq * self.q * m_p) % N
        r4 = N - r3

        print(r1, r2, r3, r4)
        
        # Try to decode each root
        for r in [r1, r2, r3, r4]:
            try:
                decrypted_message = r.to_bytes((r.bit_length() + 7) // 8, 'big').decode('utf-8')
                print(decrypted_message)
                return decrypted_message
            except (UnicodeDecodeError, ValueError):
                continue
        
        raise ValueError("Decryption failed: none of the roots produced a valid message")
    
    # Extended Euclidean algorithm
    @staticmethod
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = RabinCryptosystem.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def save_keys(self, filename='key.txt'):
        if self.N is None or self.p is None or self.q is None:
            raise ValueError("Keys not generated")
        
        with open(filename, 'w') as f:
            f.write(f"{self.N}\n{self.p}\n{self.q}")
    
    def load_keys(self, filename='key.txt'):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.N = int(lines[0].strip())
                self.p = int(lines[1].strip())
                self.q = int(lines[2].strip())
        except (FileNotFoundError, IndexError, ValueError) as e:
            raise ValueError(f"Failed to load keys: {e}")


class FileHandler:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(data))


class RabinApp:
    def __init__(self):
        self.crypto = RabinCryptosystem()
        self.file_handler = FileHandler()
    
    def display_menu(self):
        print("\n" + "="*40)
        print("Rabin Cryptosystem")
        print("="*40)
        print("1. Generate keys")
        print("2. Encrypt file")
        print("3. Decrypt file")
        print("4. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-4): ")
        return choice
    
    def generate_keys(self):
        try:
            bits = int(input("Enter key size (e.g., 512): "))
            N, p, q = self.crypto.generate_keys(bits)
            print(f"Keys generated successfully!")
            print(f"Public key N: {N}")
            print(f"Private keys p, q: {p}, {q}")
            
            save_choice = input("Save keys to file? (y/n): ").lower()
            if save_choice == 'y':
                filename = input("Enter filename (default: key.txt): ") or 'key.txt'
                self.crypto.save_keys(filename)
                print(f"Keys saved to {filename}")
        
        except ValueError as e:
            print(f"Error: {e}")
    
    def encrypt_file(self):
        try:
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path: ")
            
            message = self.file_handler.read_file(input_file)
            ciphertext = self.crypto.encrypt(message)
            
            self.file_handler.write_file(output_file, ciphertext)
            print(f"File encrypted successfully and saved as {output_file}")
        
        except Exception as e:
            print(f"Encryption error: {e}")
    
    def decrypt_file(self):
        try:
            input_file = input("Enter input file path: ")
            output_file = input("Enter output file path: ")
            
            ciphertext = int(self.file_handler.read_file(input_file))
            message = self.crypto.decrypt(ciphertext)
            
            self.file_handler.write_file(output_file, message)
            print(f"File decrypted successfully and saved as {output_file}")
        
        except Exception as e:
            print(f"Decryption error: {e}")
    
    def run(self):
        print("Rabin Cryptosystem")
        
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                self.generate_keys()
            elif choice == "2":
                self.encrypt_file()
            elif choice == "3":
                self.decrypt_file()
            elif choice == "4":
                print("Bye bye!")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    app = RabinApp()
    app.run()


if __name__ == "__main__":
    main()
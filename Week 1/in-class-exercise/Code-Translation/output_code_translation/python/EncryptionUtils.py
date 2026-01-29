import string

class EncryptionUtils:
    def __init__(self, key: str):
        self.key = key

    def caesar_cipher(self, plaintext: str, shift: int) -> str:
        ciphertext = []
        for ch in plaintext:
            if ch.isalpha():
                ascii_offset = ord('A') if ch.isupper() else ord('a')
                shifted = (ord(ch.lower()) - ord('a') + shift) % 26
                ciphertext.append(chr(shifted + ascii_offset))
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text: str) -> str:
        encrypted = []
        key_len = len(self.key)
        key_index = 0
        for ch in plain_text:
            if ch.isalpha():
                shift = ord(self.key[key_index % key_len].lower()) - ord('a')
                base = ord('a')
                enc_char = chr((ord(ch.lower()) - base + shift) % 26 + base)
                encrypted.append(enc_char.upper() if ch.isupper() else enc_char)
                key_index += 1
            else:
                encrypted.append(ch)
        return ''.join(encrypted)

    def rail_fence_cipher(self, plain_text: str, rails: int) -> str:
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        fence = ['' for _ in range(rails)]
        direction = -1
        row = 0
        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row] += ch
            row += direction
        return ''.join(fence)

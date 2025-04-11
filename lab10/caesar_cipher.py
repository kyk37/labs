# modified lab 03 code using functions instead of a class
# Sets all characters to lowercase prior to shifting

def shift_char(c, shift):
    ''' shift the text in c by "shift" amount. '''
    result = []
    for char in c:
        if char.isalpha():
            base = ord("a")  # start at a
            new_char = chr(base + (ord(char) - base + shift) % 26)
            result.append(new_char)
        elif char in "!\"#$&'()*+,-./":
            base = ord('!')  # Start from '!' in ASCII range
            new_char = chr(base + (ord(char) - base + shift) % 15)
            result.append(new_char)
        elif char in ":;<=>?@":
            base = ord(':')  # Start from ':' in ASCII range
            new_char = chr(base + (ord(char) - base + shift) % 7)
            result.append(new_char)
        elif char in "[\\]^_`":
            base = ord('[')  # Start from '[' in ASCII range
            new_char = chr(base + (ord(char) - base + shift) % 6)
            result.append(new_char)
        else:
            result.append(char)  # Keep numbers and spaces unchanged
    return ''.join(result)    


def caesar_encrypt(text, shift):
    ''' Calls shift_char for every "Char", to encrypt the text'''
    return ''.join(map(lambda c: shift_char(c.lower(), shift), text))

def caesar_decrypt(text, shift):
    ''' Calls shift_char for every "Char", to decrypt by the shift amount '''
    return ''.join(map(lambda c: shift_char(c.lower(), -shift), text))


# Example usage
if __name__ == '__main__':
    message = "Hello, World!"
    shift = 3
    encrypted = caesar_encrypt(message, shift)
    decrypted = caesar_decrypt(encrypted, shift)

    print("Original:", message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    
    message = "zzz"
    shift = 6
    encrypted = caesar_encrypt(message, shift)
    decrypted = caesar_decrypt(encrypted, shift)
    
    print("Original:", message)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)
    
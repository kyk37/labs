
class Caesar():
    '''
        Caesar Cipher
        All Alphanumeric letters wrap back around
        Each segment of "separate groups" of ASCII characters wrap
        Numbers & spaces do nothing
    '''
    def __init__(self, shift:int = 0):
        #initialize variables
        self._key = shift # Prevent shift beyond alphabet  

    def set_key(self, value):
        # Set key
        self._key = value
    
    def encrypt(self, text:str):
        return self._algorithm(text.lower(), self._key)
    
    def decrypt(self, text:str):
        return self._algorithm(text.lower(), -self._key)

    def _algorithm(self, text:str, key: int):
        # Caesar algorithm. Alphanumerics wrap around.
        # All special characters wrap to its own section
        
        result = []
        for char in text:
            if char.isalpha():
                base = ord("a")  # start at a
                new_char = chr(base + (ord(char) - base + key) % 26)
                result.append(new_char)
            elif char in "!\"#$&'()*+,-./":
                base = ord('!')  # Start from '!' in ASCII range
                new_char = chr(base + (ord(char) - base + key) % 15)
                result.append(new_char)
            elif char in ":;<=>?@":
                base = ord(':')  # Start from ':' in ASCII range
                new_char = chr(base + (ord(char) - base + key) % 7)
                result.append(new_char)
            elif char in "[\\]^_`":
                base = ord('[')  # Start from '[' in ASCII range
                new_char = chr(base + (ord(char) - base + key) % 6)
                result.append(new_char)
            else:
                result.append(char)  # Keep numbers and spaces unchanged
        return ''.join(result)    
        


def test_function(cipher):
    print("setting key = 1")
    cipher.set_key(1)
    print("Encrypt !\"#$%&'()*+,-./ -> ", cipher.encrypt("!\"#$%&'()*+,-./"))
    print("Decrypt #$%&'()*+,-./!\" -> ", cipher.decrypt("#$%&'()*+,-./!\""))

    print("Encrypt :;<=>?@ -> ", cipher.encrypt(":;<=>?@"))
    print("Decrypt ;<=>?@: -> ", cipher.decrypt(";<=>?@:"))

    print("Encrypt [\\^_` -> ", cipher.encrypt("[\\^_`"))
    print("Decrypt \\]_`[ -> ", cipher.decrypt("\\]_`["))
    
    print("setting key = 5")
    cipher.set_key(5)
    print("Encrypt MHW !%[_] -> ", cipher.encrypt("MHW !%[_]"))
    print("Decrypt rmb &%`^\\ -> ", cipher.decrypt("rmb &%`^\\"))

    print("Encrypt Yep this works -> ", cipher.encrypt("Yep this works"))
    print("Encrypt Yep this works -> ", cipher.encrypt("Yep this works"))

if __name__ == "__main__":
    print("Kyle Kessler")
    print("INFSCI 0201 Lab 3- Caesar Cipher")
    print("-----------------")
    cipher = Caesar()
    cipher.set_key(3)
    print(cipher.encrypt("hello WORLD!"))
    print(cipher.decrypt("KHOOR zruog$"))
    
    cipher.set_key(6)
    print("Encrypt zzz -> ",cipher.encrypt("zzz"))
    print("Decrypt fff ->",cipher.decrypt("fff"))
    
    cipher.set_key(-6)
    print("Encrypt FFF -> ",cipher.encrypt("FFF"))
    
    test_function(cipher)
    
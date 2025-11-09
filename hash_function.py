"""
Custom Hash Function Implementation - SimpleHash256
A educational cryptographic hash function implementation from scratch.

Author: Naga Sri Harsha Vardhan Kanaparthi
Course Project: Security Protocol Implementation
"""

class SimpleHash256:
    """
    A custom 256-bit hash function implementation demonstrating core cryptographic concepts.
    
    This implementation uses:
    - Merkle-Damgård construction
    - Davies-Meyer compression function
    - Custom mixing operations for avalanche effect
    """
    
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    INITIAL_HASH = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    # Round constants (cube roots of first 64 primes)
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174
    ]
    
    def __init__(self):
        """Initialize the hash function with initial values."""
        self.reset()
    
    def reset(self):
        """Reset the hash state to initial values."""
        self.state = self.INITIAL_HASH.copy()
        self.buffer = b''
        self.counter = 0
    
    @staticmethod
    def _rotate_right(value, shift):
        """
        Perform circular right rotation on a 32-bit value.
        
        Args:
            value: 32-bit integer to rotate
            shift: Number of positions to rotate
            
        Returns:
            Rotated 32-bit integer
        """
        value &= 0xFFFFFFFF  # Ensure 32-bit
        return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF
    
    @staticmethod
    def _rotate_left(value, shift):
        """
        Perform circular left rotation on a 32-bit value.
        
        Args:
            value: 32-bit integer to rotate
            shift: Number of positions to rotate
            
        Returns:
            Rotated 32-bit integer
        """
        value &= 0xFFFFFFFF  # Ensure 32-bit
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF
    
    def _pad_message(self, message):
        """
        Pad the message according to Merkle-Damgård padding scheme.
        
        Padding format:
        - Original message
        - Bit '1' followed by zeros
        - 64-bit message length (in bits) at the end
        - Total padded length is multiple of 512 bits (64 bytes)
        
        Args:
            message: bytes to be padded
            
        Returns:
            Padded message as bytes
        """
        msg_len = len(message)
        message += b'\x80'  # Append bit '1' (10000000 in binary)
        
        # Calculate padding: message + 1 byte + padding + 8 bytes (length) = multiple of 64
        padding_len = (56 - (msg_len + 1) % 64) % 64
        message += b'\x00' * padding_len
        
        # Append original length in bits as 64-bit big-endian integer
        message += (msg_len * 8).to_bytes(8, byteorder='big')
        
        return message
    
    def _mixing_function(self, a, b, c):
        """
        Custom mixing function for creating avalanche effect.
        
        Uses combination of XOR, rotation, and addition to mix values.
        
        Args:
            a, b, c: 32-bit integers to mix
            
        Returns:
            Mixed 32-bit integer
        """
        x = (a ^ b) & 0xFFFFFFFF
        x = self._rotate_left(x, 7) & 0xFFFFFFFF
        x = (x + c) & 0xFFFFFFFF
        x = (x ^ self._rotate_right(b, 11)) & 0xFFFFFFFF
        return x
    
    def _compress_block(self, block):
        """
        Compress a 512-bit (64-byte) block into the hash state.
        
        This is the core of the hash function where the actual mixing happens.
        
        Args:
            block: 64 bytes to compress
        """
        # Convert block to 16 32-bit words
        words = []
        for i in range(0, 64, 4):
            word = int.from_bytes(block[i:i+4], byteorder='big')
            words.append(word)
        
        # Extend 16 words to 64 words using message schedule
        for i in range(16, 64):
            s0 = self._rotate_right(words[i-15], 7) ^ self._rotate_right(words[i-15], 18) ^ (words[i-15] >> 3)
            s1 = self._rotate_right(words[i-2], 17) ^ self._rotate_right(words[i-2], 19) ^ (words[i-2] >> 10)
            words.append((words[i-16] + s0 + words[i-7] + s1) & 0xFFFFFFFF)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self.state
        
        # Main compression loop (64 rounds)
        for i in range(64):
            # Calculate round functions
            S1 = self._rotate_right(e, 6) ^ self._rotate_right(e, 11) ^ self._rotate_right(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + self.K[i % 16] + words[i]) & 0xFFFFFFFF
            
            S0 = self._rotate_right(a, 2) ^ self._rotate_right(a, 13) ^ self._rotate_right(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF
            
            # Update working variables
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        # Add compressed block to state
        self.state[0] = (self.state[0] + a) & 0xFFFFFFFF
        self.state[1] = (self.state[1] + b) & 0xFFFFFFFF
        self.state[2] = (self.state[2] + c) & 0xFFFFFFFF
        self.state[3] = (self.state[3] + d) & 0xFFFFFFFF
        self.state[4] = (self.state[4] + e) & 0xFFFFFFFF
        self.state[5] = (self.state[5] + f) & 0xFFFFFFFF
        self.state[6] = (self.state[6] + g) & 0xFFFFFFFF
        self.state[7] = (self.state[7] + h) & 0xFFFFFFFF
    
    def update(self, data):
        """
        Update the hash with new data.
        
        Args:
            data: bytes or string to hash
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buffer += data
        self.counter += len(data)
        
        # Process complete 64-byte blocks
        while len(self.buffer) >= 64:
            block = self.buffer[:64]
            self.buffer = self.buffer[64:]
            self._compress_block(block)
    
    def digest(self):
        """
        Produce the final hash digest.
        
        Returns:
            32-byte hash digest
        """
        # Work with a copy to allow continued updates
        final_state = self.state.copy()
        final_buffer = self.buffer
        
        # Pad and process remaining data
        padded = self._pad_message(final_buffer)
        
        # Process all blocks from padded message
        temp_state = self.state.copy()
        for i in range(0, len(padded), 64):
            block = padded[i:i+64]
            self._compress_block(block)
        
        # Get final hash
        result = b''
        for word in self.state:
            result += word.to_bytes(4, byteorder='big')
        
        # Restore state for potential continued updates
        self.state = temp_state
        
        return result
    
    def hexdigest(self):
        """
        Produce the final hash digest as hexadecimal string.
        
        Returns:
            64-character hexadecimal string
        """
        return self.digest().hex()


def hash_string(message):
    """
    Convenience function to hash a string in one call.
    
    Args:
        message: String or bytes to hash
        
    Returns:
        Hexadecimal hash string
    """
    hasher = SimpleHash256()
    hasher.update(message)
    return hasher.hexdigest()


def hash_file(filename):
    """
    Hash the contents of a file.
    
    Args:
        filename: Path to file to hash
        
    Returns:
        Hexadecimal hash string
    """
    hasher = SimpleHash256()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == "__main__":
    # Quick demonstration
    print("SimpleHash256 - Custom Hash Function Implementation")
    print("=" * 60)
    
    # Test 1: Empty string
    print("\nTest 1: Empty string")
    print(f"Hash: {hash_string('')}")
    
    # Test 2: Simple message
    print("\nTest 2: 'Hello, World!'")
    print(f"Hash: {hash_string('Hello, World!')}")
    
    # Test 3: Avalanche effect demonstration
    print("\nTest 3: Avalanche Effect")
    msg1 = "Hello, World!"
    msg2 = "Hello, World."  # One character different
    hash1 = hash_string(msg1)
    hash2 = hash_string(msg2)
    print(f"Message 1: '{msg1}'")
    print(f"Hash 1:    {hash1}")
    print(f"Message 2: '{msg2}'")
    print(f"Hash 2:    {hash2}")
    
    # Calculate bit differences
    bits_diff = bin(int(hash1, 16) ^ int(hash2, 16)).count('1')
    print(f"Bits different: {bits_diff}/256 ({bits_diff/256*100:.1f}%)")
    
    # Test 4: Deterministic property
    print("\nTest 4: Deterministic Property")
    hash_a = hash_string("Test message")
    hash_b = hash_string("Test message")
    print(f"Hash A: {hash_a}")
    print(f"Hash B: {hash_b}")
    print(f"Same: {hash_a == hash_b}")
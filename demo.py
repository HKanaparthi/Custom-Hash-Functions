"""
Interactive Demo for SimpleHash256 Custom Hash Function

This script provides an interactive interface to demonstrate the hash function capabilities.
"""

from hash_function import SimpleHash256, hash_string, hash_file
import os
import sys


def print_header():
    """Print demo header."""
    print("\n" + "="*70)
    print(" "*15 + "SimpleHash256 - Interactive Demo")
    print("="*70)
    print("\nA custom cryptographic hash function implementation from scratch")
    print("Features: 256-bit output, Avalanche effect, Collision resistance\n")


def demo_basic_hashing():
    """Demonstrate basic hashing functionality."""
    print("\n" + "-"*70)
    print("DEMO 1: Basic Hashing")
    print("-"*70)
    
    while True:
        message = input("\nEnter a message to hash (or 'back' to return): ")
        if message.lower() == 'back':
            break
        
        hash_val = hash_string(message)
        
        print(f"\nMessage: '{message}'")
        print(f"Length:  {len(message)} characters")
        print(f"Hash:    {hash_val}")
        print(f"Binary:  {bin(int(hash_val, 16))[2:].zfill(256)[:64]}...")
        
        # Show hash properties
        print("\nHash Properties:")
        print(f"  • Output length: 256 bits (64 hex characters)")
        print(f"  • Deterministic: Same input always produces same hash")
        print(f"  • One-way: Cannot reverse hash to get original message")


def demo_avalanche_effect():
    """Demonstrate avalanche effect."""
    print("\n" + "-"*70)
    print("DEMO 2: Avalanche Effect")
    print("-"*70)
    print("\nThe avalanche effect means a small change in input causes")
    print("a large change in output (~50% of bits should flip)")
    
    while True:
        print("\n" + "="*70)
        msg1 = input("Enter first message (or 'back' to return): ")
        if msg1.lower() == 'back':
            break
        
        msg2 = input("Enter second message (slightly different): ")
        
        hash1 = hash_string(msg1)
        hash2 = hash_string(msg2)
        
        # Calculate differences
        int1 = int(hash1, 16)
        int2 = int(hash2, 16)
        xor = int1 ^ int2
        bits_diff = bin(xor).count('1')
        percent_diff = (bits_diff / 256) * 100
        
        print(f"\nMessage 1: '{msg1}'")
        print(f"Hash 1:    {hash1}\n")
        
        print(f"Message 2: '{msg2}'")
        print(f"Hash 2:    {hash2}\n")
        
        print("="*70)
        print(f"Bits different: {bits_diff} out of 256 ({percent_diff:.2f}%)")
        print(f"Expected: ~50% for good avalanche effect")
        
        # Visual representation
        print("\nVisual Difference (first 64 bits):")
        bin1 = bin(int1)[2:].zfill(256)[:64]
        bin2 = bin(int2)[2:].zfill(256)[:64]
        diff = ''.join(['█' if b1 != b2 else '░' for b1, b2 in zip(bin1, bin2)])
        print(f"Hash 1: {bin1}")
        print(f"Hash 2: {bin2}")
        print(f"Diff:   {diff}")
        print(f"(█ = different bit, ░ = same bit)")
        
        if 45 <= percent_diff <= 55:
            print("\n✓ Excellent avalanche effect!")
        elif 40 <= percent_diff <= 60:
            print("\n✓ Good avalanche effect")
        else:
            print("\n⚠ Avalanche effect outside expected range")


def demo_collision_test():
    """Demonstrate collision resistance."""
    print("\n" + "-"*70)
    print("DEMO 3: Collision Resistance Test")
    print("-"*70)
    print("\nA good hash function should not produce collisions")
    print("(different inputs producing the same hash)")
    
    try:
        num_tests = int(input("\nHow many random strings to test? (100-10000): "))
        num_tests = max(100, min(10000, num_tests))
    except ValueError:
        num_tests = 1000
    
    print(f"\nGenerating and hashing {num_tests} random strings...")
    
    import random
    import string
    
    hashes = {}
    collisions = []
    
    for i in range(num_tests):
        # Generate random string
        length = random.randint(5, 50)
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        hash_val = hash_string(msg)
        
        if hash_val in hashes:
            collisions.append((msg, hashes[hash_val], hash_val))
        else:
            hashes[hash_val] = msg
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"  Processed: {i + 1}/{num_tests}")
    
    print("\n" + "="*70)
    print(f"Total strings tested: {num_tests}")
    print(f"Unique hashes:        {len(hashes)}")
    print(f"Collisions found:     {len(collisions)}")
    
    if len(collisions) == 0:
        print("\n✓ No collisions found! Hash function passed the test.")
    else:
        print(f"\n⚠ {len(collisions)} collision(s) detected!")
        for msg1, msg2, hash_val in collisions[:3]:
            print(f"\n  Message 1: '{msg1}'")
            print(f"  Message 2: '{msg2}'")
            print(f"  Same hash: {hash_val}")


def demo_file_hashing():
    """Demonstrate file hashing."""
    print("\n" + "-"*70)
    print("DEMO 4: File Hashing")
    print("-"*70)
    print("\nThis demo shows how to hash file contents")
    
    # Create a sample file
    sample_file = "sample_text.txt"
    sample_content = """This is a sample file for demonstrating file hashing.
The hash function can process files of any size.
Each file will have a unique 256-bit hash value."""
    
    with open(sample_file, 'w') as f:
        f.write(sample_content)
    
    print(f"\nCreated sample file: {sample_file}")
    print(f"Content preview:\n{sample_content[:100]}...\n")
    
    hash_val = hash_file(sample_file)
    
    print(f"File hash: {hash_val}")
    print(f"\nThis hash can be used for:")
    print("  • Verifying file integrity")
    print("  • Detecting file modifications")
    print("  • Creating checksums")
    
    # Cleanup
    os.remove(sample_file)
    print(f"\n(Sample file removed)")


def demo_incremental_hashing():
    """Demonstrate incremental hashing."""
    print("\n" + "-"*70)
    print("DEMO 5: Incremental Hashing")
    print("-"*70)
    print("\nHash functions can process data in chunks (useful for large data)")
    
    message = "The quick brown fox jumps over the lazy dog"
    
    # One-shot hashing
    hash_oneshot = hash_string(message)
    
    # Incremental hashing
    hasher = SimpleHash256()
    chunks = ["The quick brown ", "fox jumps over ", "the lazy dog"]
    
    print(f"\nOriginal message: '{message}'")
    print(f"\nProcessing in chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: '{chunk}'")
        hasher.update(chunk)
    
    hash_incremental = hasher.hexdigest()
    
    print(f"\nOne-shot hash:    {hash_oneshot}")
    print(f"Incremental hash: {hash_incremental}")
    print(f"\nResult: {'✓ MATCH' if hash_oneshot == hash_incremental else '✗ MISMATCH'}")


def demo_comparison():
    """Compare with well-known hash functions."""
    print("\n" + "-"*70)
    print("DEMO 6: Comparison with Standard Hash Functions")
    print("-"*70)
    print("\nThis shows how SimpleHash256 compares to standard algorithms")
    
    import hashlib
    
    message = input("\nEnter a message to hash: ")
    
    # Our hash
    hash_custom = hash_string(message)
    
    # Standard hashes
    hash_md5 = hashlib.md5(message.encode()).hexdigest()
    hash_sha256 = hashlib.sha256(message.encode()).hexdigest()
    
    print(f"\nMessage: '{message}'")
    print("="*70)
    print(f"MD5 (128-bit):         {hash_md5}")
    print(f"SHA-256 (256-bit):     {hash_sha256}")
    print(f"SimpleHash256 (256b):  {hash_custom}")
    print("="*70)
    
    print("\nNote: SimpleHash256 is educational and should NOT be used")
    print("      for production security. Use SHA-256 or SHA-3 instead.")


def main_menu():
    """Display main menu and handle user choices."""
    print_header()
    
    demos = {
        '1': ('Basic Hashing', demo_basic_hashing),
        '2': ('Avalanche Effect', demo_avalanche_effect),
        '3': ('Collision Resistance', demo_collision_test),
        '4': ('File Hashing', demo_file_hashing),
        '5': ('Incremental Hashing', demo_incremental_hashing),
        '6': ('Comparison with Standards', demo_comparison),
    }
    
    while True:
        print("\n" + "="*70)
        print("DEMO MENU")
        print("="*70)
        for key, (name, _) in demos.items():
            print(f"  {key}. {name}")
        print("  q. Quit")
        print("="*70)
        
        choice = input("\nSelect a demo (1-6) or 'q' to quit: ").strip().lower()
        
        if choice == 'q':
            print("\nThank you for trying SimpleHash256!")
            print("Remember: This is for educational purposes only.\n")
            break
        elif choice in demos:
            demos[choice][1]()
        else:
            print("\n⚠ Invalid choice. Please enter 1-6 or 'q'")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
        sys.exit(0)
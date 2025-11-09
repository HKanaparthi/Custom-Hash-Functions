"""
Example Usage of SimpleHash256 Hash Function

This file demonstrates various ways to use the custom hash function
in practical scenarios.
"""

from hash_function import SimpleHash256, hash_string, hash_file


def example_1_basic_hashing():
    """Example 1: Basic string hashing"""
    print("=" * 60)
    print("Example 1: Basic String Hashing")
    print("=" * 60)
    
    messages = [
        "Hello, World!",
        "Python Programming",
        "Cryptography is fascinating",
        ""  # Empty string
    ]
    
    for msg in messages:
        hash_val = hash_string(msg)
        print(f"Message: '{msg}'")
        print(f"Hash:    {hash_val}\n")


def example_2_password_verification():
    """Example 2: Simulated password verification (educational only!)"""
    print("=" * 60)
    print("Example 2: Password Verification Simulation")
    print("=" * 60)
    print("Note: This is for demonstration only. Use bcrypt/argon2 in production!\n")
    
    # Simulate storing a password hash
    stored_password = "my_secure_password_123"
    stored_hash = hash_string(stored_password)
    
    print(f"Stored password hash: {stored_hash[:32]}...\n")
    
    # Simulate login attempts
    attempts = [
        ("my_secure_password_123", "Correct password"),
        ("my_secure_password_124", "Wrong password (1 char different)"),
        ("wrong_password", "Completely wrong"),
    ]
    
    for attempt, description in attempts:
        attempt_hash = hash_string(attempt)
        match = (attempt_hash == stored_hash)
        status = "✓ ACCESS GRANTED" if match else "✗ ACCESS DENIED"
        print(f"{description}: {status}")


def example_3_data_integrity():
    """Example 3: Verify data integrity"""
    print("\n" + "=" * 60)
    print("Example 3: Data Integrity Check")
    print("=" * 60)
    
    # Original document
    original_doc = "This is an important contract document."
    original_hash = hash_string(original_doc)
    
    print(f"Original document: '{original_doc}'")
    print(f"Original hash: {original_hash}\n")
    
    # Simulate transmission/storage
    received_doc = "This is an important contract document."
    received_hash = hash_string(received_doc)
    
    print(f"Received document: '{received_doc}'")
    print(f"Received hash: {received_hash}\n")
    
    if original_hash == received_hash:
        print("✓ Data integrity verified! Document unchanged.")
    else:
        print("✗ Warning! Document has been modified!")
    
    # Simulate tampering
    print("\n--- Simulating Tampering ---")
    tampered_doc = "This is an important contract document!"  # Added '!'
    tampered_hash = hash_string(tampered_doc)
    
    print(f"Tampered document: '{tampered_doc}'")
    print(f"Tampered hash: {tampered_hash}\n")
    
    if original_hash == tampered_hash:
        print("✓ Data integrity verified!")
    else:
        print("✗ TAMPERING DETECTED! Hashes don't match!")


def example_4_deduplication():
    """Example 4: File deduplication using hashes"""
    print("\n" + "=" * 60)
    print("Example 4: Duplicate Detection")
    print("=" * 60)
    
    # Simulate a file storage system
    files = {
        "document1.txt": "The quick brown fox",
        "document2.txt": "jumps over the lazy dog",
        "document3.txt": "The quick brown fox",  # Duplicate of document1
        "document4.txt": "Hello World",
        "document5.txt": "Hello World",  # Duplicate of document4
    }
    
    # Create hash table
    hash_table = {}
    duplicates = []
    
    for filename, content in files.items():
        file_hash = hash_string(content)
        
        if file_hash in hash_table:
            # Duplicate found!
            duplicates.append((filename, hash_table[file_hash]))
            print(f"DUPLICATE: '{filename}' is identical to '{hash_table[file_hash]}'")
        else:
            hash_table[file_hash] = filename
            print(f"UNIQUE: '{filename}' - Hash: {file_hash[:16]}...")
    
    print(f"\nTotal files: {len(files)}")
    print(f"Unique files: {len(hash_table)}")
    print(f"Duplicates found: {len(duplicates)}")


def example_5_incremental_hashing():
    """Example 5: Hashing large data in chunks"""
    print("\n" + "=" * 60)
    print("Example 5: Incremental Hashing (Large Data)")
    print("=" * 60)
    
    # Simulate processing large data in chunks
    print("Processing data in 3 chunks...\n")
    
    hasher = SimpleHash256()
    
    chunks = [
        "This is the first chunk of data. ",
        "This is the second chunk of data. ",
        "This is the third and final chunk."
    ]
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}: '{chunk[:30]}...'")
        hasher.update(chunk)
    
    final_hash = hasher.hexdigest()
    print(f"\nFinal hash: {final_hash}")
    
    # Verify it's the same as hashing all at once
    all_at_once = "".join(chunks)
    verify_hash = hash_string(all_at_once)
    
    print(f"\nVerification (all at once): {verify_hash}")
    print(f"Hashes match: {final_hash == verify_hash}")


def example_6_hash_chain():
    """Example 6: Creating a hash chain (simplified blockchain concept)"""
    print("\n" + "=" * 60)
    print("Example 6: Hash Chain (Simplified Blockchain)")
    print("=" * 60)
    
    # Simulate a simple blockchain
    blocks = []
    previous_hash = "0" * 64  # Genesis block
    
    transactions = [
        "Alice sends 10 BTC to Bob",
        "Bob sends 5 BTC to Charlie",
        "Charlie sends 3 BTC to Alice",
    ]
    
    print("Building hash chain...\n")
    
    for i, transaction in enumerate(transactions, 1):
        # Create block data (previous hash + transaction)
        block_data = previous_hash + transaction
        current_hash = hash_string(block_data)
        
        blocks.append({
            'block_number': i,
            'transaction': transaction,
            'previous_hash': previous_hash[:16] + "...",
            'current_hash': current_hash[:16] + "..."
        })
        
        print(f"Block {i}:")
        print(f"  Transaction: {transaction}")
        print(f"  Previous hash: {previous_hash[:16]}...")
        print(f"  Current hash:  {current_hash[:16]}...")
        print()
        
        previous_hash = current_hash
    
    print("Hash chain created successfully!")
    print("Each block is cryptographically linked to the previous one.")


def example_7_compare_similar_strings():
    """Example 7: Demonstrate avalanche effect with similar inputs"""
    print("\n" + "=" * 60)
    print("Example 7: Avalanche Effect Demonstration")
    print("=" * 60)
    
    pairs = [
        ("cat", "bat"),
        ("Hello123", "Hello124"),
        ("password", "Password"),
    ]
    
    for str1, str2 in pairs:
        hash1 = hash_string(str1)
        hash2 = hash_string(str2)
        
        # Calculate bit difference
        int1 = int(hash1, 16)
        int2 = int(hash2, 16)
        diff = bin(int1 ^ int2).count('1')
        percent = (diff / 256) * 100
        
        print(f"\nString 1: '{str1}'")
        print(f"Hash 1:   {hash1[:32]}...")
        print(f"String 2: '{str2}'")
        print(f"Hash 2:   {hash2[:32]}...")
        print(f"Difference: {diff}/256 bits ({percent:.1f}%)")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "SimpleHash256 Usage Examples" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    example_1_basic_hashing()
    example_2_password_verification()
    example_3_data_integrity()
    example_4_deduplication()
    example_5_incremental_hashing()
    example_6_hash_chain()
    example_7_compare_similar_strings()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
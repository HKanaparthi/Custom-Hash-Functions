"""
Test Suite for SimpleHash256 Custom Hash Function

This file contains comprehensive tests to verify the properties of the hash function:
1. Determinism
2. Avalanche Effect
3. Collision Resistance
4. Performance
"""

from hash_function import SimpleHash256, hash_string, hash_file
import time
import random
import string


def test_determinism():
    """Test that same input always produces same output."""
    print("\n" + "="*60)
    print("TEST 1: DETERMINISM")
    print("="*60)
    
    test_messages = [
        "",
        "a",
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "A" * 1000,  # Long message
        "🎉 Unicode test! 你好世界"
    ]
    
    all_passed = True
    for msg in test_messages:
        hash1 = hash_string(msg)
        hash2 = hash_string(msg)
        hash3 = hash_string(msg)
        
        passed = (hash1 == hash2 == hash3)
        all_passed &= passed
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: '{msg[:50]}...' -> {hash1[:16]}...")
    
    print(f"\nDeterminism Test: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_avalanche_effect():
    """Test that small input changes cause large output changes."""
    print("\n" + "="*60)
    print("TEST 2: AVALANCHE EFFECT")
    print("="*60)
    print("Small input change should cause ~50% of output bits to flip\n")
    
    test_cases = [
        ("Hello, World!", "Hello, World?"),  # Last char change
        ("password", "Password"),  # Case change
        ("12345678", "12345679"),  # Single digit
        ("a" * 100, "a" * 99 + "b"),  # End change in long string
    ]
    
    total_diff_percent = 0
    for msg1, msg2 in test_cases:
        hash1 = hash_string(msg1)
        hash2 = hash_string(msg2)
        
        # Calculate bit difference
        int1 = int(hash1, 16)
        int2 = int(hash2, 16)
        xor_result = int1 ^ int2
        bits_different = bin(xor_result).count('1')
        diff_percent = (bits_different / 256) * 100
        total_diff_percent += diff_percent
        
        print(f"Message 1: '{msg1[:30]}'")
        print(f"Hash 1:    {hash1}")
        print(f"Message 2: '{msg2[:30]}'")
        print(f"Hash 2:    {hash2}")
        print(f"Difference: {bits_different}/256 bits ({diff_percent:.1f}%)")
        print()
    
    avg_diff = total_diff_percent / len(test_cases)
    print(f"Average difference: {avg_diff:.1f}%")
    print(f"Expected: ~50% (good avalanche effect)")
    
    # Good avalanche effect is typically 45-55%
    passed = 40 <= avg_diff <= 60
    print(f"\nAvalanche Test: {'PASSED' if passed else 'WARNING - May need improvement'}")
    return passed


def test_collision_resistance():
    """Test that different inputs produce different outputs."""
    print("\n" + "="*60)
    print("TEST 3: COLLISION RESISTANCE")
    print("="*60)
    
    # Generate random test strings
    num_tests = 1000
    print(f"Generating {num_tests} random strings and checking for collisions...\n")
    
    hashes = set()
    messages = []
    
    for i in range(num_tests):
        # Generate random string of random length
        length = random.randint(1, 100)
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        messages.append(msg)
        
        hash_val = hash_string(msg)
        hashes.add(hash_val)
    
    collisions = num_tests - len(hashes)
    
    print(f"Messages tested: {num_tests}")
    print(f"Unique hashes:   {len(hashes)}")
    print(f"Collisions:      {collisions}")
    
    passed = (collisions == 0)
    print(f"\nCollision Resistance Test: {'PASSED' if passed else 'FAILED'}")
    
    if collisions > 0:
        print("WARNING: Collisions detected! This should not happen with good hash functions.")
    
    return passed


def test_output_length():
    """Test that output is always 256 bits (64 hex characters)."""
    print("\n" + "="*60)
    print("TEST 4: FIXED OUTPUT LENGTH")
    print("="*60)
    
    test_messages = [
        "",
        "a",
        "short",
        "This is a medium length message for testing purposes.",
        "A" * 10000,  # Very long message
    ]
    
    all_passed = True
    for msg in test_messages:
        hash_val = hash_string(msg)
        length = len(hash_val)
        passed = (length == 64)  # 256 bits = 64 hex characters
        all_passed &= passed
        
        status = "✓" if passed else "✗"
        print(f"{status} Input length: {len(msg):5d} | Output length: {length} hex chars | {len(hash_val)*4} bits")
    
    print(f"\nFixed Output Length Test: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def test_performance():
    """Test hash function performance."""
    print("\n" + "="*60)
    print("TEST 5: PERFORMANCE")
    print("="*60)
    
    test_sizes = [
        (100, "100 bytes"),
        (1000, "1 KB"),
        (10000, "10 KB"),
        (100000, "100 KB"),
        (1000000, "1 MB"),
    ]
    
    print("\nHashing speed for different input sizes:\n")
    
    for size, label in test_sizes:
        # Generate test data
        data = "A" * size
        
        # Time the hashing
        start = time.time()
        hash_val = hash_string(data)
        end = time.time()
        
        elapsed_ms = (end - start) * 1000
        throughput = size / (1024 * 1024 * (end - start)) if (end - start) > 0 else 0
        
        print(f"{label:10s}: {elapsed_ms:8.2f} ms | {throughput:8.2f} MB/s")
    
    return True


def test_special_cases():
    """Test edge cases and special inputs."""
    print("\n" + "="*60)
    print("TEST 6: SPECIAL CASES")
    print("="*60)
    
    test_cases = {
        "Empty string": "",
        "Null bytes": "\x00\x00\x00",
        "All ones": "\xff\xff\xff",
        "Unicode": "Hello 世界 🌍",
        "Long ASCII": "A" * 10000,
        "Newlines": "Line1\nLine2\nLine3",
        "Special chars": "!@#$%^&*()_+-=[]{}|;:',.<>?/~`",
    }
    
    for name, msg in test_cases.items():
        hash_val = hash_string(msg)
        print(f"✓ {name:20s}: {hash_val[:32]}...")
    
    print("\nSpecial Cases Test: PASSED")
    return True


def test_incremental_hashing():
    """Test that incremental hashing gives same result as one-shot hashing."""
    print("\n" + "="*60)
    print("TEST 7: INCREMENTAL HASHING")
    print("="*60)
    
    message = "The quick brown fox jumps over the lazy dog"
    
    # One-shot hashing
    hash_oneshot = hash_string(message)
    
    # Incremental hashing
    hasher = SimpleHash256()
    hasher.update("The quick brown ")
    hasher.update("fox jumps over ")
    hasher.update("the lazy dog")
    hash_incremental = hasher.hexdigest()
    
    print(f"Original message: '{message}'")
    print(f"One-shot hash:    {hash_oneshot}")
    print(f"Incremental hash: {hash_incremental}")
    
    passed = (hash_oneshot == hash_incremental)
    print(f"\nIncremental Hashing Test: {'PASSED' if passed else 'FAILED'}")
    return passed


def run_all_tests():
    """Run all test suites."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "SIMPLEHASH256 TEST SUITE" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    results.append(("Determinism", test_determinism()))
    results.append(("Avalanche Effect", test_avalanche_effect()))
    results.append(("Collision Resistance", test_collision_resistance()))
    results.append(("Fixed Output Length", test_output_length()))
    results.append(("Performance", test_performance()))
    results.append(("Special Cases", test_special_cases()))
    results.append(("Incremental Hashing", test_incremental_hashing()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Hash function is working correctly.")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Review implementation.")


if __name__ == "__main__":
    run_all_tests()
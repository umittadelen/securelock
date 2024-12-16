from securelock import lock, unlock

# Test cases to push the limits of SecureLock

def run_tests():
    print("Starting tests...")

    # Test 1: Simple text
    text = "hello"
    password = "password"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 1 failed!"
    print("Test 1 passed.")

    # Test 2: Long text
    text = "a" * 10000
    password = "longpassword"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 2 failed!"
    print("Test 2 passed.")

    # Test 3: Unicode characters
    text = "😀🌍📚✨"
    password = "unicode"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 3 failed!"
    print("Test 3 passed.")

    # Test 4: Special characters
    text = "!@#$%^&*()_+-=[]{}|;':\",.<>?/"
    password = "specialchars"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 4 failed!"
    print("Test 4 passed.")

    # Test 5: Empty text
    text = ""
    password = "emptypass"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 5 failed!"
    print("Test 5 passed.")

    # Test 6: Mismatched password
    text = "secure text"
    password = "correctpassword"
    wrong_password = "wrongpassword"
    locked = lock(text, password)
    try:
        unlock(locked, wrong_password)
    except Exception:
        print("Test 6 passed (decryption failed as expected with wrong password).")
    else:
        assert False, "Test 6 failed!"

    # Test 7: Extremely long password
    text = "secure text"
    password = "p" * 1000
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 7 failed!"
    print("Test 7 passed.")

    # Test 8: Edge case with repeating characters
    text = "aaaaaaa"
    password = "repeating"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 8 failed!"
    print("Test 8 passed.")

    # Test 9: Large Unicode text
    text = "𐍈" * 1000  # Rare Gothic character repeated
    password = "unicode_password"
    locked = lock(text, password)
    unlocked = unlock(locked, password)
    assert text == unlocked, "Test 9 failed!"
    print("Test 9 passed.")

    print("All tests completed.")

if __name__ == "__main__":
    run_tests()

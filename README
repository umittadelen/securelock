# SecureLock

SecureLock is a lightweight Python library for securely encrypting and decrypting text using a password. It utilizes salted key derivation and XOR-based encryption to ensure the integrity and security of your data.

## Features
- Compact design: Only two functions, `lock()` and `unlock()`.
- Salted encryption: Each encryption is unique due to a randomly generated salt.
- Key stretching: Uses SHA-256 hashing to derive a secure encryption key from the password.
- Supports all Unicode characters.

## Installation
```bash
pip install securelock
```

## Usage
### Encrypting Text
```python
from securelock import lock

password = "strongpassword"
text = "This is a secret message!"

# Encrypt the text
locked_text = lock(text, password)
print("Locked Text:", locked_text)
```

### Decrypting Text
```python
from securelock import unlock

# Decrypt the text
unlocked_text = unlock(locked_text, password)
print("Unlocked Text:", unlocked_text)
```

### Example Output
```plaintext
Locked Text: 4a6f1c2b... (encrypted hex string)
Unlocked Text: This is a secret message!
```

## Security Notes
- **Strong Passwords**: Always use strong and unpredictable passwords for maximum security.
- **Key Derivation**: SecureLock uses SHA-256 with a randomly generated 32-byte salt, ensuring each encryption is unique.
- **Brute-Force Resistance**: The implementation is designed to make brute-forcing computationally expensive.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing
Feel free to submit issues or feature requests. Contributions are welcome!
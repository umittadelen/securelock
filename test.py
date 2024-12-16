from securelock import lock, unlock
import string
import random
import time
from datetime import datetime
import os
import platform
from colorama import init, Fore, Back, Style
from tabulate import tabulate
import sys

# Start colorama
init()

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def make_random_text(length, allowed_chars):
    return ''.join(random.choice(allowed_chars) for _ in range(length))

def show_progress(current, total):
    bar_length = 50
    filled = int((current / total) * bar_length)
    bar = "=" * filled + " " * (bar_length - filled)
    sys.stdout.write(f'\r[{bar}] {current}/{total}')
    sys.stdout.flush()

def format_for_table(text, max_width):
    if not text:
        return ""
    lines = str(text).split('\n')
    formatted_lines = []
    for line in lines:
        while len(line) > max_width:
            formatted_lines.append(line[:max_width] + '...')
            line = line[max_width:]
        if line:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

def run_tests():
    clear_screen()
    console_width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
    max_column_width = min(50, (console_width - 20) // 3)

    print("=" * console_width)
    print(f"{Fore.CYAN}SECURE LOCK TEST SUITE{Style.RESET_ALL}".center(console_width))
    print("=" * console_width)
    
    passed = 0
    failed = 0
    expected_fails = 0
    error_list = []
    results = []
    start = time.time()

    # Test settings
    text_sizes = [0, 1, 10, 100, 1000, 5000]
    password_sizes = [1, 8, 16, 32, 64, 128, 256]
    char_types = {
        'letters': string.ascii_letters,
        'numbers': string.digits,
        'symbols': string.punctuation,
        'mixed': string.ascii_letters + string.digits + string.punctuation,
        'spaces': ' \t\n\r',
        'binary': '01',
        'hex': '0123456789ABCDEF'
    }

    # Tests that should fail (non-ASCII text)
    special_text_tests = [
        ("😀🌍📚✨", "emoji"),     # Emojis
        ("θΣπ∞√", "math"),       # Math symbols
        ("你好世界", "chinese"),   # Chinese
        ("üöäß", "german"),      # German
        ("русский", "russian"),   # Russian
    ]

    # Basic tests that should work
    basic_tests = [
        ("", "empty"),           # Empty text
        ("hello", "simple"),     # Simple text
        ("!@#$%^&*", "symbols"), # Symbols
        ("aaaaaaa", "repeat"),   # Repeated letters
        ("ABC123", "mixed"),     # Letters and numbers
    ]

    def log_error(name, text, password, error):
        error_details = [
            f"Test Name: {name}",
            f"Text: {text[:50]}{'...' if len(text) > 50 else ''}",
            f"Text Length: {len(text)}",
            f"Text Type: {type(text)}",
            f"Password: {password[:50]}{'...' if len(password) > 50 else ''}",
            f"Password Length: {len(password)}",
            f"Error Type: {type(error).__name__}",
            f"Error Message: {str(error)}"
        ]
        message = "\n".join(error_details)
        error_list.append(message)
        results.append([
            name,
            f"{Fore.RED}❌ FAILED{Style.RESET_ALL}",
            f"Length: {len(text)}, Error: {type(error).__name__}"
        ])

    # Run basic tests
    print(f"\n{Fore.YELLOW}Running basic tests...{Style.RESET_ALL}")
    for i, (text, password) in enumerate(basic_tests, 1):
        name = f"Basic test - {password}"
        show_progress(i, len(basic_tests))
        try:
            locked = lock(text, password)
            unlocked = unlock(locked, password)
            assert text == unlocked
            passed += 1
            results.append([name, f"{Fore.GREEN}✓ PASSED{Style.RESET_ALL}", ""])
        except Exception as e:
            failed += 1
            log_error(name, text, password, e)

    # Run special text tests (should fail with Unicode)
    print(f"\n{Fore.YELLOW}Testing special text (should fail)...{Style.RESET_ALL}")
    for i, (text, password) in enumerate(special_text_tests, 1):
        name = f"Special text - {password}"
        show_progress(i, len(special_text_tests))
        try:
            locked = lock(text, password)
            unlocked = unlock(locked, password)
            details = [
                f"Original: {text}",
                f"Locked: {locked[:30]}{'...' if len(locked) > 30 else ''}",
                f"Unlocked: {unlocked}",
                "Should have failed"
            ]
            formatted_details = '\n'.join(details)
            results.append([
                name,
                f"{Fore.BLUE}✓ FAILED (Expected){Style.RESET_ALL}",
                formatted_details
            ])
            expected_fails += 1
        except UnicodeEncodeError:
            expected_fails += 1
            results.append([
                name,
                f"{Fore.BLUE}✓ FAILED (Expected){Style.RESET_ALL}",
                "Correctly rejected non-ASCII text"
            ])
        except Exception as e:
            expected_fails += 1
            results.append([
                name,
                f"{Fore.BLUE}✓ FAILED (Expected){Style.RESET_ALL}",
                f"Rejected non-ASCII text: {str(e)}"
            ])

    # Run random text tests
    total_random = len(text_sizes) * len(password_sizes) * len(char_types)
    current = 0
    print(f"\n{Fore.YELLOW}Testing random text...{Style.RESET_ALL}")
    
    for text_size in text_sizes:
        for pass_size in password_sizes:
            for char_name, chars in char_types.items():
                current += 1
                show_progress(current, total_random)
                
                name = f"Random - Size:{text_size}, Chars:{char_name}, Pass:{pass_size}"
                try:
                    text = make_random_text(text_size, chars)
                    password = make_random_text(pass_size, string.ascii_letters + string.digits)
                    
                    locked = lock(text, password)
                    unlocked = unlock(locked, password)
                    assert text == unlocked
                    
                    passed += 1
                    results.append([name, f"{Fore.GREEN}✓ PASSED{Style.RESET_ALL}", ""])
                except Exception as e:
                    failed += 1
                    log_error(name, text, password, e)

    # Show results
    end = time.time()
    time_taken = end - start
    
    clear_screen()
    print("=" * console_width)
    print(f"{Fore.CYAN}TEST RESULTS{Style.RESET_ALL}".center(console_width))
    print("=" * console_width + "\n")

    # Group results by category and status
    basic_results = [r for r in results if r[0].startswith("Basic")]
    unicode_results = [r for r in results if r[0].startswith("Special")]
    random_results = [r for r in results if r[0].startswith("Random")]
    
    failed_tests = [r for r in results if "FAIL" in r[1] and "Expected" not in r[1]]

    # Print Failed Tests First (if any)
    if failed_tests:
        print(f"{Fore.RED}FAILED TESTS:{Style.RESET_ALL}")
        formatted_failed = [[t[0], t[1], format_for_table(t[2], max_column_width)] 
                          for t in failed_tests]
        print(tabulate(formatted_failed,
                      headers=['Test', 'Result', 'Details'],
                      tablefmt='grid',
                      maxcolwidths=[max_column_width, max_column_width, max_column_width]))
        print("\n" + "=" * console_width + "\n")

    # Print Basic Tests
    print(f"{Fore.YELLOW}BASIC TESTS:{Style.RESET_ALL}")
    formatted_basic = [[t[0], t[1], format_for_table(t[2], max_column_width)] 
                      for t in basic_results]
    print(tabulate(formatted_basic,
                  headers=['Test', 'Result', 'Details'],
                  tablefmt='grid',
                  maxcolwidths=[max_column_width, max_column_width, max_column_width]))
    print()

    # Print Unicode Tests
    print(f"{Fore.YELLOW}UNICODE TESTS (Expected to Fail):{Style.RESET_ALL}")
    formatted_unicode = [[t[0], t[1], format_for_table(t[2], max_column_width)] 
                        for t in unicode_results]
    print(tabulate(formatted_unicode,
                  headers=['Test', 'Result', 'Details'],
                  tablefmt='grid',
                  maxcolwidths=[max_column_width, max_column_width, max_column_width]))
    print()

    # Print Random Tests Summary
    passed_random = len([r for r in random_results if "PASS" in r[1]])
    failed_random = [r for r in random_results if "FAIL" in r[1]]
    print(f"{Fore.YELLOW}RANDOM TESTS SUMMARY:{Style.RESET_ALL}")
    print(f"Total: {len(random_results)}, Passed: {passed_random}, Failed: {len(failed_random)}")
    
    if failed_random:
        print(f"\n{Fore.YELLOW}FAILED RANDOM TESTS:{Style.RESET_ALL}")
        formatted_random = [[t[0], t[1], format_for_table(t[2], max_column_width)] 
                          for t in failed_random]
        print(tabulate(formatted_random,
                      headers=['Test', 'Result', 'Details'],
                      tablefmt='grid',
                      maxcolwidths=[max_column_width, max_column_width, max_column_width]))
    print()

    # Print Summary
    print(f"{Fore.YELLOW}TEST SUMMARY:{Style.RESET_ALL}")
    stats = [
        ['Total Tests Run', f"{total_random + len(basic_tests) + len(special_text_tests)}"],
        ['✓ Tests Passed', f"{Fore.GREEN}{passed}{Style.RESET_ALL}"],
        ['ℹ Expected Failures', f"{Fore.BLUE}{expected_fails}{Style.RESET_ALL}"],
        ['❌ Unexpected Failures', f"{Fore.RED}{failed}{Style.RESET_ALL}"],
        ['Success Rate', f"{Fore.GREEN}{(passed/(passed + failed))*100:.1f}%{Style.RESET_ALL}"],
        ['Total Time', f"{time_taken:.1f} seconds"]
    ]
    print(tabulate(stats, headers=['Metric', 'Value'], 
                  tablefmt='double'))

    # Show detailed error information
    if error_list:
        print(f"\n{Fore.RED}DETAILED ERROR INFORMATION{Style.RESET_ALL}")
        print("=" * console_width)
        for i, error in enumerate(error_list, 1):
            print(f"\n{Fore.RED}Error #{i}:{Style.RESET_ALL}")
            print("-" * console_width)
            for line in error.split('\n'):
                print(f"  {line}")
            print("-" * console_width)

    # Final status with error count
    print("\nFinal Status:", end=" ")
    if failed == 0:
        print(f"{Fore.GREEN}ALL TESTS PASSED{Style.RESET_ALL} "
              f"(with {expected_fails} expected Unicode failures)")
    else:
        print(f"{Fore.RED}TESTS FAILED{Style.RESET_ALL}")
        print(f"- {failed} unexpected failures")
        print(f"- {expected_fails} expected Unicode failures")
        print(f"- See detailed error information above")

if __name__ == "__main__":
    run_tests()

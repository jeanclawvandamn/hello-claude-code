#!/usr/bin/env python3
"""A simple calculator with a clean CLI interface."""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def get_number(prompt: str) -> float:
    """Get a valid number from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_menu() -> None:
    """Display the calculator menu."""
    print("\n" + "=" * 30)
    print("       CALCULATOR MENU")
    print("=" * 30)
    print("  1. Addition (+)")
    print("  2. Subtraction (-)")
    print("  3. Multiplication (*)")
    print("  4. Division (/)")
    print("  5. Exit")
    print("=" * 30)


def main() -> None:
    """Main calculator loop."""
    operations = {
        "1": ("Addition", add, "+"),
        "2": ("Subtraction", subtract, "-"),
        "3": ("Multiplication", multiply, "*"),
        "4": ("Division", divide, "/"),
    }

    print("\nWelcome to the Calculator!")

    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "5":
            print("\nThank you for using the Calculator. Goodbye!\n")
            break

        if choice not in operations:
            print("\nInvalid choice. Please select 1-5.")
            continue

        name, operation, symbol = operations[choice]
        print(f"\n--- {name} ---")

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            result = operation(a, b)
            print(f"\nResult: {a} {symbol} {b} = {result}")
        except ValueError as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()

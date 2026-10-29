
print("=== SIMPLE CLI CALCULATOR ===")
print("Type 'q' at any time to quit.")

while True:
    num1 = input("\nEnter first number: ")

    if num1.lower() == "q":
        print("Calculator closed.")
        break

    try:
        num1 = float(num1)
    except ValueError:
        print(ValueError)
        continue

    operator = input("Enter an operator (+, -, *, /): ")

    if operator.lower() == "q":
        print("Calculator closed.")
        break

    if operator not in ["+", "-", "*", "/"]:
        print("Invalid operation.")
        continue

    num2 = input("Enter second number: ")

    if num2.lower() == "q":
        print("Calculator closed.")
        break

    try:
        num2 = float(num2)
    except ValueError:
        print("Invalid number.")
        continue

    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*":
        result = num1 * num2

    elif operator == "/":
        if num2 == 0:
            print("Error: Cannot divide by zero.")
            continue
        result = num1 / num2

    print("Result:", result)

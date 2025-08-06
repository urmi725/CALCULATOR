def calculate(num1, num2, operator):
    """Performs a calculation based on two numbers and an operator."""
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            return "Error: Division by zero is not allowed."
        return num1 / num2
    else:
        return "Error: Invalid operator."

def main():
    """Main function to run the calculator application."""
    print("Welcome to the Simple Calculator!")
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    operator = input("Enter an operation (+, -, *, /): ")

    result = calculate(num1, num2, operator)
    print(f"The result is: {result}")

if __name__ == "__main__":
    main()

def customized_greeting(name):
    print(f"Hello, {name}")

def print_year_of_birth(age):
    print(2025 - age)

name = input("What is your name? ")
customized_greeting(name)

age = int(input("What is your age? "))
print_year_of_birth(age)
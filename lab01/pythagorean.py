import math
'''
Calculate the hypotenuse of a triangle.
'''

def get_input():
    a = input("What is the length of side A of the triangle?")
    b = input("What is the length of side B of the traingle?")
    a = float(a)
    b = float(b)
    return a, b
    
def calculate_hypotenuse(a,b):
    temp = a**2 + b**2
    c = math.sqrt(temp)
    return c


if __name__ == "__main__":
    a, b = get_input()
    c = calculate_hypotenuse(a,b)
    
    print(f"The hypotenuse is of length {c:.2f}.")
    
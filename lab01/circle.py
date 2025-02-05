import math
'''
Calculate the area and perimter of a circle
- assumes user input may not be integer, check for errors
'''

def user_input():
    # check for improper variables
    while True:
        try:
            radius = float(input("What is the radius of the circle? "))
            break
        except ValueError:
            print("Please Enter a number. d")
    
    return radius
        
def calculate_perimeter(radius):
    perimeter = 2 * math.pi * radius
    return perimeter


def calculate_area(radius):
    area = math.pi * radius**2
    return area

if __name__ == "__main__":
    radius = user_input()
    
    area = calculate_area(radius)
    perimeter = calculate_perimeter(radius)
    
    print(f"The Area is {area:.2f}, and perimeter is {perimeter:.2f}")
    
    
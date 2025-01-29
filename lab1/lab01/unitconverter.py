import math

def user_input():
    while True:
        try:
            data_in = input("Type in a number, followed by a space, and the unit of measurement: ")
            parts = data_in.split()
            try:
                value, unit = float(parts[0]), str(parts[1])
                print(f"Data received | value: {value} || unit: {unit}")
                break
            except ValueError:
                print("Enter a number followed by a space, and the unit. (ex: '5 in')")
        except ValueError:
            print("Enter a number followed by a space, and the unit. (ex: '5 in')")
    
    return value, unit

def conversion(value, unit):
    
    match unit:
        case "in":
            # inches -> cm
            result = value * 2.54
            print(f"{value} {unit} = {result:.2f} cm")
        case "cm":
            # cm -> inches
            result = value / 2.54
            print(f"{value} {unit} = {result:.2f} in")     
        case "yd":
            # yards -> meters
            result = value * 0.9144
            print(f"{value} {unit} = {result:.2f} m ")
        case "m":
            # meters -> yards
            result = value / 0.9144
            print(f"{value} {unit} = {result:.2f} yd")
        case "oz":
            # oz -> grams
            result = value * 28.349523125
            print(f"{value} {unit} = {result:.2f} g")
        case "g":
            # grams -> oz
            result = value / 28.349523125
            print(f"{value} {unit} = {result:.2f} oz ")
        case "kg":
            # kg -> lbs
            result = value / 0.45359237
            print(f"{value} {unit} = {result:.2f} lbs")
        case "lb":
            # lbs -> kg
            result = value * 0.45359237
            print(f"{value} {unit} = {result:.2f} kg")
        case _:
            print("Invalid unit. Try again.")
            user_input()
            

if __name__ == "__main__":
    
    value, unit = user_input()
    
    conversion(value, unit)
    
    
import Expression as Expr

def main():
    while True:
        expr = input("\nEnter the expression, or hit return to quit => ")
        if not expr:
            break
        vars = []
        arrays = []
        Expr.makeVariableLists(expr, vars, arrays)
        in_filename = input("Enter variable values' file name, or hit return if no variables => ")
        if in_filename:
            with open(in_filename, "r") as file:
                Expr.loadVariableValues(file, vars, arrays)
        print("Value of expression = " + str(Expr.evaluate(expr, vars, arrays)))

if __name__ == "__main__":
    main()
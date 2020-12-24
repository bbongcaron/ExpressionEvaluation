import Expression as Expr

def main():
    #expr = "3+(4*5)"
    expr = "a - (b+A[B[2]])*d + 3"
    #expr = "(varx + vary*varz[(vara+varb[(a+b)/10])])/55"
    vars = []
    arrays = []
    Expr.makeVariableLists(expr, vars, arrays)
    for v in vars:
        print(v.name + " is a variable!")
    for a in arrays:
        print(a.name + " is an array!")
    
    with open("etest1.txt", 'r') as file:
        Expr.loadVariableValues(file, vars, arrays)

    for v in vars:
        print(v.toString())
    for a in arrays:
        print(a.toString())
    #test = 50
    #if 2 <= test <= 30:
       # print('YES!')

    Expr.evaluate(expr, vars, arrays)
if __name__ == "__main__":
    main()
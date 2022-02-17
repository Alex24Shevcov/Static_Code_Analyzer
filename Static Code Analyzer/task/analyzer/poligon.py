import ast
import re

PATH = "./for_test.py"


def S010(line):
    template = r"[a-z_][a-z0-9_]*"
    tree = ast.parse(line)
    # print(ast.dump(tree))
    nodes = ast.walk(tree)
    for node in nodes:
        # if isinstance(node, ast.ClassDef):
        #     function = node.body[0]
        if isinstance(node, ast.FunctionDef):
            function = node
        else:
             continue

        for i in range(len(function.args.args)):
            # print(function.args.args[i].arg)
            parameter = function.args.args[i].arg
            line = function.args.args[i].lineno
            if re.match(template, parameter) is None:
                print(f"{PATH}: Line {line}: S010 Argument name {parameter} should be written in snake_case;")


def S011(line):
    template = r"[a-z_][a-z0-9_]*$"
    tree = ast.parse(line)
    # print(ast.dump(tree))
    nodes = ast.walk(tree)
    for node in nodes:
        if isinstance(node, ast.FunctionDef):
            for i in range(len(node.body)):
                try:
                    variable = node.body[i].targets[0].id
                    line = node.body[i].lineno
                    if re.match(template, variable) is None:
                        print(f"{PATH}: Line {line}: S010 Argument name {variable} should be written in snake_case;")
                except AttributeError:
                    pass


def S012(line):
    tree = ast.parse(line)
    # print(ast.dump(tree))
    nodes = ast.walk(tree)
    for node in nodes:
        if isinstance(node, ast.FunctionDef):
            for i in range(len(node.args.args)):
                line = node.args.args[i].lineno
                try:
                    is_constant = isinstance(node.args.defaults[i], ast.Constant)
                    if not is_constant:
                        print(f"{PATH}: Line {line}: S012  The default argument value is mutable.")
                        break
                except IndexError:
                    pass


with open(PATH, "r") as file:
        S010(file.read())
        file.seek(0)
        S011(file.read())
        file.seek(0)
        S012(file.read())

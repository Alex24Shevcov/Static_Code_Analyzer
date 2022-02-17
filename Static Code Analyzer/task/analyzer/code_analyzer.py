# write your code here
import ast
import os
import sys
import re

PATH = sys.argv[1]
# PATH = "/home/ivan/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/test/this_stage"


class CodeAnalizer:
    _count_empty_rows = 0

    def __init__(self, path) -> None:
        self.path = path

    def _find_letter(self, line):
        return True if re.search("[a-zA-Z]", line) else False

    def _find_digit(self, line):
        return True if re.search("\d", line) else False

    def _count_start_line_spaces(self, line):
        count = 0
        for i in line:
            if i == " ":
                count += 1
            else:
                return count

    def S003(self, f_path, number_of_line, line) -> None:
        if re.search(";", line):
            if re.search(r"['\"].*['\"].*;.*#", line):
                print(f"{f_path}: Line {number_of_line}: S003 Unnecessary semicolon")

            elif re.search(r"['\"].*#.*;.*['\"]", line):
                return

            elif re.search(r"#.*;", line):
                return

            elif re.search(r"['\"].*;.*['\"]", line):
                return

            elif re.search(r"['\"].*['\"].*#.*;.*", line):
                return

            else:
                print(f"{f_path}: Line {number_of_line}: S003 Unnecessary semicolon")

    def S005(self, f_path, number_of_line, line) -> None:
        template = r"#.*\s?TODO\s?[\n]?"
        line = line.upper()
        if re.search(template, line):
            print(f"{f_path}: Line {number_of_line}: S005 TODO found")

    def S006(self, f_path, number_of_line, line) -> None:
        if (self._find_letter(line)) or (self._find_digit(line)):
            if self._count_empty_rows > 2:
                print(f"{f_path}: Line {number_of_line}: S006 More than two blank lines used before this line")
            self._count_empty_rows = 0
        else:
            self._count_empty_rows += 1


    def S004(self, f_path, number_of_line, line):
        index_grid = line.find("#")
        if index_grid > 0:
            if (line[index_grid - 1] != " ") or (line[index_grid - 2] != " "):
                print(f"{f_path}: Line {number_of_line}: S004 At least two spaces required before inline comments")


    def S001(self, f_path, number_of_line, line) -> None:
        if len(line) > 79:
            print(f"{f_path}: Line {number_of_line}: S001 Too long")

    def S002(self, f_path, number_of_line, line) -> None:
        count_spaces_line = self._count_start_line_spaces(line)
        if count_spaces_line % 4 != 0:
            print(f"{f_path}: Line {number_of_line}: S002 Indentation is not a multiple of four")


    def _recourseve_find_files(self, path) -> list:
        arr = [i for i in os.walk(path)]
        arr_absolut_path = []
        for i in arr:
            if len(i[-1]) == 1:
                arr_absolut_path.append(i[0] + "/" + ''.join(i[-1]))
            elif len(i[-1]) > 1:
                for j in i[-1]:
                    arr_absolut_path.append(i[0] + "/" + j)

        return arr_absolut_path

    def _find_python_files(self, path) -> list:
        if re.search('.py$', path) is not None:
            return [path]

        arr = self._recourseve_find_files(path)
        arr_python_files = []
        for i in arr:
            if re.search('.py$', i) is not None:
                arr_python_files.append(i)
        return sorted(arr_python_files)

    def S007(self, f_path, number_of_line, line) -> None:
        template_class = r"class  "
        template_def = r"def  "
        if re.match(template_class, line) is not None:
            print(f"{f_path}: Line {number_of_line}: S007 Too many spaces after 'class' or 'def'")
        elif re.search(template_def, line) is not None:
            print(f"{f_path}: Line {number_of_line}: S007 Too many spaces after 'class' or 'def'")

    def S008(self, f_path, number_of_line, line):
        if re.match("class", line):
            template = r"class\s+[A-Z][a-zA-Z0-9]*\(?([A-Z][a-zA-Z0-9]*)?\)?:$"
            if re.match(template, line) is None:
                print(f"{f_path}: Line {number_of_line}: S008 Class name should use CamelCase")

    def S009(self, f_path, number_of_line, line):
        if re.search("def", line):
            template = r"def\s+[a-z_][a-z0-9_]*\("
            if re.search(template, line) is None:
                print(f"{f_path}: Line {number_of_line}: S009 Function name should use snake_case")


    def S010(self, f_path, code):
        template = r"[a-z_][a-z0-9_]*"
        tree = ast.parse(code)
        nodes = ast.walk(tree)
        for node in nodes:
            if isinstance(node, ast.FunctionDef):
                for i in range(len(node.args.args)):
                    parameter = node.args.args[i].arg
                    code = node.args.args[i].lineno
                    if re.match(template, parameter) is None:
                        print(f"{f_path}: Line {code}: S010 Argument name {parameter} should be written in snake_case;")

    def S011(self, f_path,  code):
        template = r"[a-z_][a-z0-9_]*$"
        tree = ast.parse(code)
        nodes = ast.walk(tree)
        for node in nodes:
            if isinstance(node, ast.FunctionDef):
                for i in range(len(node.body)):
                    try:
                        variable = node.body[i].targets[0].id
                        code = node.body[i].lineno
                        if re.match(template, variable) is None:
                            print(
                                f"{f_path}: Line {code}: S011 Argument name {variable} should be written in snake_case;")
                    except AttributeError:
                        pass

    def S012(self, f_path, line):
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
                            print(f"{f_path}: Line {line}: S012  The default argument value is mutable.")
                            break
                    except IndexError:
                        pass

    def main(self):
        file_path = self._find_python_files(self.path)
        for f_path in file_path:
            with open(f_path, "r") as file:
                arr_lines = file.readlines()
                i = 0
                while i < len(arr_lines):
                    # print(arr_lines[i], end="")
                    self.S001(f_path, i + 1, arr_lines[i])

                    self.S002(f_path, i + 1, arr_lines[i])

                    self.S003(f_path, i + 1, arr_lines[i])

                    self.S004(f_path, i + 1, arr_lines[i])

                    self.S005(f_path, i + 1, arr_lines[i])

                    self.S006(f_path, i + 1, arr_lines[i])

                    self.S007(f_path, i + 1, arr_lines[i])

                    self.S008(f_path, i + 1, arr_lines[i])

                    self.S009(f_path, i + 1, arr_lines[i])

                    i += 1

                file.seek(0)
                self.S010(file.name, file.read())
                file.seek(0)
                self.S011(file.name, file.read())
                file.seek(0)
                self.S012(file.name, file.read())
                file.seek(0)


p = CodeAnalizer(PATH)
p.main()

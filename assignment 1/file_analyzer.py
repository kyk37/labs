import ast
import os
import re

class StyleChecker:
    def __init__(self, file_path:str):
        self.file_path = file_path
        self.tree = self._parse_file()
        self.report_lines = []
        self.source_lines = []

    def _parse_file(self):
        ''' Parses the Python file and returns AST, also storing source lines '''
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.source_lines = content.splitlines()
                return ast.parse(content)
        except Exception as e:
            print(f"Error reading file {self.file_path}: {e}")
            return None
    
    def _analyze_structure(self):
        ''' Analyzes structure of the Python file and appends to what will be put in the output file '''
        total_lines = sum(1 for _ in open(self.file_path, 'r', encoding='utf-8'))
        imports = []
        classes = {}
        class_methfunc = {}
        functionsout = []
        missing_annotations = set()
        has_annotations = set()

        
        for node in self.tree.body:
            # Identify imports
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                imports.append(self._get_import_string(node))
            
            # Get the list of classes
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                classes[class_name] = class_name
                class_methfunc[class_name] = []
                
                # Get the functions in each class
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = f"{class_name}_{item.name}"
                        class_methfunc[class_name].append(method_name)

                        # Check annotations for methods
                        has_return_annotation = item.returns is not None
                        if has_return_annotation:
                            has_annotations.add(method_name)
                        else:
                            missing_annotations.add(method_name)

            elif isinstance(node, ast.FunctionDef):
                # check for functions outside of classes
                functionsout.append(node.name)
                
                # get any annotations
                has_return_annotation = node.returns is not None
                if has_return_annotation:
                    has_annotations.add(node.name)
                else:
                    missing_annotations.add(node.name)

        # Add file information to the file
        self.report_lines.append("File structure")
        self.report_lines.append(f"Total number of lines of code: {total_lines}\n")
        
        self.report_lines.append("List of packages imported:")
        temp = []
        temp.extend(imports or ["None"])
        #self.report_lines.extend(imports or ["None"])
        self.report_lines.extend(f'\t{imp}' for imp in imports)
        self.report_lines.append("")
        
        self.report_lines.append("List of Classes:")
        self.report_lines.extend([f"\t{''.join(cls)}" 
                                for cls in classes])
        self.report_lines.append("")

        self.report_lines.append("List of Functions Inside Classes:")
        self.report_lines.append("Note: functions inside classes have Classname_functioname identification")
        self.report_lines.extend([f"Class {cls}: \n\t{', \n\t'.join(methods) if methods else 'No methods'}\n" 
                                for cls, methods in class_methfunc.items()] or ["None"])
        self.report_lines.append("")
        
        self.report_lines.append("List of Functions Outside Classes:")
        self.report_lines.extend([f"\t{''.join(func)}" 
                                for func in functionsout] or ["\tNone"])
        self.report_lines.append("")
        
        # Check the dockstrings and report
        self._check_docstrings(class_methfunc)

        # check type annotations and report
        self._check_type_annotations(missing_annotations, has_annotations)

        # check for naming convetions and report
        self._check_naming_conventions(classes, functionsout, class_methfunc)

    def _get_import_string(self, node):
        ''' Converts import nodes to readable strings '''
        if isinstance(node, ast.Import):
            return ", ".join(name.name for name in node.names)
        elif isinstance(node, ast.ImportFrom):
            return f"from {node.module} import {', '.join(name.name for name in node.names)}"
        return ""

    def _check_docstrings(self, class_methfunc):
        ''' Extracts and reports docstrings for classes and functions '''
        self.report_lines.append("List of all Doc Strings and their associated class/method/function")
        
        # Build a mapping of class methods from class_methfunc for quick lookup
        class_methods = {}
        for cls in class_methfunc:
            for method in class_methfunc[cls]:
                method_name = method.split('_', 1)[1]  # Get the method part (e.g., 'get_inventory')
                class_methods[method_name] = cls  # Map method name to its class

        # Scan the tree for classes and functions
        for node in ast.walk(self.tree):
            # get dockstrings of all the classes
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                name = node.name
                self.report_lines.append(f"{name}: \n\t{docstring if docstring else 'DocString not found.'}")
            
            # get the docstring of every function
            elif isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                name = node.name
                # Check if this function is inside a class
                if name in class_methods:
                    # If it's a method, add class name to front
                    class_name = class_methods[name]
                    full_name = f"{class_name}_{name}"
                else:
                    # If it's a standalone function, use just the name
                    full_name = name
                self.report_lines.append(f"{full_name}: \n\t{docstring if docstring else 'DocString not found.'}")
        
        self.report_lines.append("")

    def _check_type_annotations(self, no_annotations, with_annotations):
        ''' Reports on type annotation usage '''
        
        self.report_lines.append("Type Annotation Check")
        self.report_lines.append("Without Annotations")
        if no_annotations:
            self.report_lines.extend(f'\t{imp}' for imp in no_annotations)
        else:
            self.report_lines.append("\tNone")

        self.report_lines.append("With_annotations:")
        if with_annotations:
            self.report_lines.extend(f'\t{imp}' for imp in with_annotations)
        else:
            self.report_lines.append("\tNone")
        if not no_annotations:
            self.report_lines.append("\n---> Type annotation is used in all functions and methods. <--- ")
        self.report_lines.append("")

    def _is_snake_case(self, name):
        ''' Checks if a name follows snake_case (lower_case_with_underscores) '''
        if not self._is_special_method(name):
            return bool(re.match(r'^[a-z][a-z0-9_]+$', name))  # Requires at least one underscore
        else:
            return False
        
    def _is_camel_case(self, name):
        ''' Checks if a name follows camelCase (startsWithLowerThenUpper) '''
        if not self._is_special_method(name):
            return bool(re.match(r'^[a-z]+[A-Z][a-zA-Z0-9]*$', name))
        else:
            return False
        
    def _is_pascal_case(self, name):
        ''' Checks if a name follows PascalCase (CapitalizedWords) '''
        if not self._is_special_method(name):
            return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))
        else:
            return False
        
    def _is_lower_case(self, name):
        ''' Checks if a name is a single lowercase word (no underscores) '''
        if not self._is_special_method(name):
            return bool(re.match(r'^[a-z]+$', name))
        else:
            return False
        
    def _is_special_method(self, name):
        ''' Checks if name is a special function '''
        return name.startswith('__') and name.endswith('__')
    
    def _check_naming_conventions(self, classes, functionsout, class_methfunc):
        ''' Checks naming conventions and identifies specific cases used '''
        self.report_lines.append("Naming Convention Check")
        
        # Create a dictionary for classes of different cases
        class_styles = {
            "snake_case": [],
            "camelCase": [],
            "PascalCase": [],
            "Other": []
        }

        non_pascal_classes = []  # Classes not adhering to PascalCase
        non_snake_functions = []  # Functions/methods not adhering to snake_case or lower_case
        special_functions = []  # Special methods that start and end with '__'

        for cls in classes:
            if self._is_snake_case(cls):
                class_styles["snake_case"].append(cls)
                non_pascal_classes.append(cls)
            elif self._is_camel_case(cls):
                class_styles["camelCase"].append(cls)
                non_pascal_classes.append(cls)
            elif self._is_pascal_case(cls):
                class_styles["PascalCase"].append(cls)
            else:
                class_styles["Other"].append(cls)
                non_pascal_classes.append(cls)
        
        # Create dictionary for functions of different cases
        func_styles = {
            "snake_case": [],
            "camelCase": [],
            "PascalCase": [],
            "lower_case": [],
            "special_case": [],  # New category for special methods
            "Other": []          # Only for non-adhering non-special methods
        }

        # Standalone functions (outside classes)
        for func in functionsout:
            if self._is_special_method(func):
                func_styles["special_case"].append(func)
            elif self._is_snake_case(func):
                func_styles["snake_case"].append(func)
                special_functions.append(func)
            elif self._is_camel_case(func):
                func_styles["camelCase"].append(func)
                non_snake_functions.append(func)
            elif self._is_pascal_case(func):
                func_styles["PascalCase"].append(func)
                non_snake_functions.append(func)
            elif self._is_lower_case(func):
                func_styles["lower_case"].append(func)
            else:
                if not self._is_special_method(func):
                    func_styles["Other"].append(func)
                    non_snake_functions.append(func)

        # Methods inside classes (from class_methfunc)
        for cls in class_methfunc:
            for method in class_methfunc[cls]:
                if method.startswith(cls + '_'):
                    method_name = method[len(cls) + 1:]  # Remove class name and the underscore
                else:
                    method_name = method  # Fallback if class name isn't found (shouldn't happen)
                full_name = method
                if self._is_special_method(method_name):
                    func_styles["special_case"].append(full_name)
                elif self._is_snake_case(method_name):
                    func_styles["snake_case"].append(full_name)
                elif self._is_camel_case(method_name):
                    func_styles["camelCase"].append(full_name)
                    non_snake_functions.append(full_name)
                elif self._is_pascal_case(method_name):
                    func_styles["PascalCase"].append(full_name)
                    non_snake_functions.append(full_name)
                elif self._is_lower_case(method_name):
                    func_styles["lower_case"].append(full_name)
                else:
                    func_styles["Other"].append(full_name)
                    non_snake_functions.append(full_name)
        
        # Report class naming conventions
        self.report_lines.append("Class Naming Conventions:")
        if not classes:
            self.report_lines.append("No classes found.")
        else:
            for style, names in class_styles.items():
                if names:
                    self.report_lines.append(f"\t{style}: {', '.join(names)}")
            used_styles = [s for s, n in class_styles.items() if n]
            if len(used_styles) > 1:
                self.report_lines.append("Warning: Multiple naming conventions detected in classes.")
        
        # Report classes not adhering to PascalCase
        self.report_lines.append("\nClasses not adhering to CapitalizedWords (PascalCase) style:")
        if non_pascal_classes:
            self.report_lines.extend(f'\t{cls}' for cls in non_pascal_classes)
        else:
            self.report_lines.append('\tNone')
        
        # Report function/method naming conventions
        self.report_lines.append("\nFunction/Method Naming Conventions:")
        if not (functionsout or class_methfunc):
            self.report_lines.append("No functions or methods found.")
        else:
            for style, names in func_styles.items():
                if names:
                    self.report_lines.append(f"\t{style}: {', '.join(sorted(names))}")
            used_styles = [s for s, n in func_styles.items() if n and s != "special_case"]
            if len(used_styles) > 1:
                self.report_lines.append("Warning: Multiple naming conventions detected in functions/methods (excluding special_case).")
        
        # Report functions/methods not adhering to snake_case or lower_case
        self.report_lines.append("\nFunctions and methods not adhering to lower_case_with_underscores style (~ignores special functions):")
        if non_snake_functions:
            self.report_lines.extend(f'\t{func}' for func in sorted(non_snake_functions))
        else:
            self.report_lines.append('\tNone')
        self.report_lines.append("Note: Single lowercase words (e.g., 'lower') are considered valid.")
        
        # Check if all names adhere to specified conventions
        if not non_pascal_classes and not non_snake_functions:
            self.report_lines.append("\nAll names adhere to the specified naming conventions.")
        
        self.report_lines.append("")

    def _generate_report(self):
        ''' Writes the style report to a file '''
        report_path = os.path.join(os.path.dirname(self.file_path),
                                 f"style_report_{os.path.basename(self.file_path).replace('.py', '.txt')}")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.report_lines))
        print(f"Report generated: {report_path}")

    def run(self):
        ''' Execute Analysis and generate report'''
        if self.tree:
            self._analyze_structure()
            self._generate_report()

if __name__ == "__main__":
    file_to_check = "potion.py"
    checker = StyleChecker(file_to_check)
    checker.run()
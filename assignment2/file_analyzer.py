import ast
import os
import re
from typing import List, Tuple, Dict, Set

def parse_file(file_path: str) -> Tuple[ast.Module, List[str]]:
    ''' Parse the file input in cls'''
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    source_lines = content.splitlines()
    tree = ast.parse(content)
    return tree, source_lines

def get_total_lines(file_path: str) -> int:
    '''get the total number of lines in the file being read'''
    with open(file_path, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def get_imports(tree: ast.Module) -> Tuple[str, ...]:
    '''get import nodes'''
    def format_import(node):
        if isinstance(node, ast.Import):
            return ", ".join(name.name for name in node.names)
        elif isinstance(node, ast.ImportFrom):
            return f"from {node.module} import {', '.join(name.name for name in node.names)}"
        return None
    return tuple(filter(None, map(format_import, filter(lambda n: isinstance(n, (ast.Import, ast.ImportFrom)), tree.body))))

def get_classes_and_methods(tree: ast.Module) -> Dict[str, List[str]]:
    ''' return a list of mapped classes and methods '''
    return {
        node.name: list(map(lambda item: f"{node.name}_{item.name}", filter(lambda item: isinstance(item, ast.FunctionDef), node.body)))
        for node in tree.body if isinstance(node, ast.ClassDef)
    }

def get_functions_outside_classes(tree: ast.Module) -> List[str]:
    ''' get all the functions not inside classes '''
    return list(map(lambda node: node.name, filter(lambda node: isinstance(node, ast.FunctionDef), tree.body)))

def get_type_annotations(tree: ast.Module, class_methods: Dict[str, List[str]], functions_out: List[str]) -> Tuple[Set[str], Set[str]]:
    ''' Get all annotations'''
    def qualified_name(node):
        name = node.name
        for cls, methods in class_methods.items():
            if f"{cls}_{name}" in methods:
                return f"{cls}_{name}"
        return name

    return (
        set(map(qualified_name, filter(lambda n: isinstance(n, ast.FunctionDef) and n.returns is None, ast.walk(tree)))),
        set(map(qualified_name, filter(lambda n: isinstance(n, ast.FunctionDef) and n.returns is not None, ast.walk(tree))))
    )

def extract_docstrings(tree: ast.Module, class_methods: Dict[str, List[str]]) -> List[str]:
    ''' Pull the docstrings from classes and functions '''
    method_lookup = {m.split('_', 1)[1]: c for c, methods in class_methods.items() for m in methods}

    def format_doc(node):
        if isinstance(node, ast.ClassDef):
            return f"{node.name}: \n\t{ast.get_docstring(node) or 'DocString not found.'}"
        elif isinstance(node, ast.FunctionDef):
            base = node.name
            prefix = method_lookup.get(base, '')
            qualified = f"{prefix}_{base}" if prefix else base
            return f"{qualified}: \n\t{ast.get_docstring(node) or 'DocString not found.'}"
        return None

    return list(filter(None, map(format_doc, ast.walk(tree))))

def check_naming_conventions(classes: List[str], functions: List[str], methods: List[str]) -> List[str]:
    ''' Check all the functions and classes naming conventions, and sort them accordingly '''
    def is_snake(name: str) -> bool:
        return bool(re.match(r'^_*[a-z][a-z0-9_]*$', name))
    
    def is_pascal(name: str) -> bool:
        return bool(re.match(r'^[A-Z][a-z0-9]*[a-z][a-z0-9]*(?:[A-Z][a-z0-9]*)*$', name) and '_' not in name)
    
    def is_lower(name: str) -> bool:
        return bool(re.match(r'^[a-z]+$', name))
    
    def is_special(name: str) -> bool:
        return name.count('__') == 2
    
    def is_camel(name: str) -> bool:
        return bool(re.match(r'^[a-z]+[A-Z][a-z0-9]*$', name) and '_' not in name)

    def categorize_name(name: str, is_method: bool = False) -> str:
        if is_special(name):
            return "special_case"
        base_name = name.split('_', 1)[-1] if is_method and '_' in name else name
        if is_snake(base_name):
            return "snake_case"
        elif is_lower(base_name):
            return "lower_case"
        elif is_pascal(base_name):
            return "PascalCase"
        elif is_camel(base_name):
            return "camelCase"
        return "Other"

    # Categorize classes
    class_styles = {"PascalCase": [], "Other": []}
    non_pascal_classes = []
    for cls in classes:
        style = "PascalCase" if is_pascal(cls) else "Other"
        class_styles[style].append(cls)
        if style != "PascalCase":
            non_pascal_classes.append(cls)

    # Categorize functions and methods, excluding special methods from non_snake_funcs
    func_styles = {"snake_case": [], "lower_case": [], "special_case": [], "PascalCase": [], "camelCase": [], "Other": []}
    non_snake_funcs = []
    for name in functions + methods:
        is_method = '_' in name and name in methods
        style = categorize_name(name, is_method)
        func_styles[style].append(name)
        # Only include names that are not snake_case, lower_case, or special_case
        if style not in ("snake_case", "lower_case", "special_case"):
            non_snake_funcs.append(name)

    # Build report
    output = ["\nNaming Convention Check"]

    # Naming conventions
    output.append("Class Naming Conventions:")
    if not classes:
        output.append("\tNo classes found.")
    else:
        for style, names in class_styles.items():
            if names:
                output.append(f"\t{style}: {', '.join(sorted(names))}")
        if len([s for s, n in class_styles.items() if n]) > 1:
            output.append("\tWarning: Multiple naming conventions detected in classes.")

    output.append("\nClasses not adhering to CapitalizedWords (PascalCase):")
    output.extend(map(lambda cls: f"\t{cls}", sorted(non_pascal_classes)) if non_pascal_classes else ["\tNone"])

    # function/method naming conventions
    output.append("\nFunction/Method Naming Conventions:")
    if not (functions or methods):
        output.append("\tNo functions or methods found.")
    else:
        for style, names in func_styles.items():
            if names:
                output.append(f"\t{style}: {', '.join(sorted(names))}")
        used_styles = [s for s, n in func_styles.items() if n and s != "special_case"]
        if len(used_styles) > 1:
            output.append("\tWarning: Multiple naming conventions detected in functions/methods (excluding special_case).")

    output.append("\nFunctions and methods not adhering to lower_case_with_underscores style (excluding special methods):")
    output.extend(map(lambda f: f"\t{f}", sorted(non_snake_funcs)) if non_snake_funcs else ["\tNone"])
    output.append("\tNote: Single lowercase words (e.g., 'lower') are considered valid; special methods (e.g., '__init__') are excluded.")

    if not non_pascal_classes and not non_snake_funcs:
        output.append("\nAll names adhere to the specified naming conventions.")

    return output

def generate_report(file_path: str, lines: List[str]) -> None:
    out_path = os.path.join(
        os.path.dirname(file_path),
        f"style_report_{os.path.basename(file_path).replace('.py', '.txt')}"
    )
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Report generated: {out_path}")
    
def compute_report(file_path: str, tree: ast.Module, source_lines: List[str]) -> List[str]:
    total_lines = get_total_lines(file_path)  # Impure, but isolated
    imports = get_imports(tree)
    class_methods = get_classes_and_methods(tree)
    functions_out = get_functions_outside_classes(tree)
    missing_annots, present_annots = get_type_annotations(tree, class_methods, functions_out)
    docstrings = extract_docstrings(tree, class_methods)
    naming_issues = check_naming_conventions(list(class_methods.keys()), functions_out, [m for methods in class_methods.values() for m in methods])
    
    report = []
    report.append("File structure")
    report.append(f"Total number of lines of code: {total_lines}\n")
    report.append("List of packages imported:")
    report.extend(list(map(lambda i: f"\t{i}", imports or ["None"])))
    report.append("\nList of Classes:")
    report.extend(list(map(lambda c: f"\t{c}", class_methods or ["None"])))
    report.append("\nList of Functions Inside Classes:")
    report.extend(list(map(lambda kv: f"Class {kv[0]}:\n\t{', '.join(kv[1]) if kv[1] else 'No methods'}", class_methods.items())))
    report.append("\nList of Functions Outside Classes:")
    report.extend(list(map(lambda f: f"\t{f}", functions_out or ["None"])))
    report.append("\nList of all Doc Strings and their associated class/method/function")
    report.extend(docstrings)
    report.append("\nType Annotation Check")
    report.append("Without Annotations:")
    report.extend(list(map(lambda a: f"\t{a}", missing_annots or ["None"])))
    report.append("With Annotations:")
    report.extend(list(map(lambda a: f"\t{a}", present_annots or ["None"])))
    if not missing_annots:
        report.append("\n---> Type annotation is used in all functions and methods. <---")
    report.extend(naming_issues)
    return report

def main():
    file_path = input("Enter path to Python file: ").strip()
    try:
        tree, source_lines = parse_file(file_path)
        report = compute_report(file_path, tree, source_lines)
        generate_report(file_path, report)
        exit()
    except Exception as e:
        print(f"Error parsing file: {e}")
        
        
for __name__ in "__main__":
    main()
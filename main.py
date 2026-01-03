import ast
import sys
sys.path.append('./Frontend')
from Frontend.Python_ast import parse_python
from Frontend.SemanticAnalyzerComponet import SemanticAnalyzer
from Frontend.IR.Ir_builder import IRBuilder
from Frontend.IR.Ir_printer import IRPrinter

with open("Input/Example.py", "r") as f:
    code = f.read()

tree = parse_python(code)
print("=========AST Tree========== \n")
print(ast.dump(tree, indent=4))

analyzer = SemanticAnalyzer()
analyzer.visit(tree)
analyzer.analyze_memory_effects()

report = analyzer.generate_report()
print(report)

ir_tree= IRBuilder().build(tree) 
printer = IRPrinter()
print("============IR============")
printer.visit(ir_tree)
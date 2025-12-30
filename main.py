import sys
sys.path.append('./Frontend')
from Frontend.Python_ast import parse_python
from Frontend.SemanticAnalyzerComponet import SemanticAnalyzer

with open("Input/Example.py", "r") as f:
    code = f.read()

tree = parse_python(code)

analyzer = SemanticAnalyzer()
analyzer.visit(tree)
analyzer.analyze_memory_effects()

report = analyzer.generate_report()
print(report)
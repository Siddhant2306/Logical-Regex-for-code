"""
Function definition and call analysis
"""

import ast
from Frontend.DataStructure import FunctionInfo, VariableInfo, VariableType


class FunctionAnalyzer:
    """Analyzes function definitions and calls"""
    
    def __init__(self, symbol_table, functions, mutated_vars):
        self.symbol_table = symbol_table
        self.functions = functions
        self.mutated_vars = mutated_vars
    
    def handle_function_def(self, node: ast.FunctionDef, current_scope, type_inferencer):
        """Process function definition"""
        func_name = node.name
        
        # Process parameters
        parameters = []
        for arg in node.args.args:
            param_info = VariableInfo(
                name=arg.arg,
                var_type=VariableType.UNKNOWN,
                scope=current_scope(),
                is_parameter=True,
                is_mutable=True
            )
            parameters.append(param_info)
            self.symbol_table[arg.arg] = param_info
        
        # Create function info
        func_info = FunctionInfo(
            name=func_name,
            parameters=parameters,
            return_type=None
        )
        self.functions[func_name] = func_info
        
        return func_info
    
    def finalize_function(self, func_name):
        """Analyze which parameters were mutated"""
        if func_name in self.functions:
            func_info = self.functions[func_name]
            for param in func_info.parameters:
                if param.name in self.mutated_vars:
                    func_info.modifies_params.add(param.name)
    
    def handle_return(self, node: ast.Return, current_function, type_inferencer):
        """Handle return statement"""
        if current_function and node.value:
            return_type, _ = type_inferencer.infer_type(node.value)
            self.functions[current_function].return_type = return_type
    
    def handle_call(self, node: ast.Call, current_function):
        """Track function calls"""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if current_function and current_function in self.functions:
                self.functions[current_function].calls_functions.append(func_name)


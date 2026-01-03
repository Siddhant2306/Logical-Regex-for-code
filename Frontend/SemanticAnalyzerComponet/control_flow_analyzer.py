
import ast
from Frontend.DataStructure import VariableInfo, VariableType


class ControlFlowAnalyzer:
    """Analyzes control flow structures"""
    
    def __init__(self, symbol_table, loop_variables):
        self.symbol_table = symbol_table
        self.loop_variables = loop_variables
        self.in_loop = False
    
    def handle_for_loop(self, node: ast.For, current_scope, type_inferencer):
        """Process for loop"""
        self.in_loop = True
        
        # Get loop variable
        if isinstance(node.target, ast.Name):
            loop_var = node.target.id
            self.loop_variables.add(loop_var)
            
            # Infer loop variable type from iterable
            iter_type, elem_type = type_inferencer.infer_type(node.iter)
            
            var_info = VariableInfo(
                name=loop_var,
                var_type=elem_type or VariableType.UNKNOWN,
                scope=current_scope(),
                first_assignment_line=node.lineno
            )
            self.symbol_table[loop_var] = var_info
        
        return True  # Signal we're in loop
    
    def exit_loop(self):
        """Exit loop context"""
        self.in_loop = False
    
    def handle_while_loop(self, node: ast.While):
        """Process while loop"""
        self.in_loop = True
        return True


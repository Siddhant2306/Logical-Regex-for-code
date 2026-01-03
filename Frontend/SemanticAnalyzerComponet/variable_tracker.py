
import ast
from typing import Dict, List
from Frontend.DataStructure import VariableInfo, TypeConstraint, VariableType


class VariableTracker:
    """Tracks variable assignments and usage"""
    
    def __init__(self, symbol_table, type_constraints, current_scope, type_inferencer):
        self.symbol_table = symbol_table
        self.type_constraints = type_constraints
        self.current_scope = current_scope
        self.type_inferencer = type_inferencer
    
    def handle_assign(self, node: ast.Assign, alias_tracker):
        """Handle variable assignment"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                
                # Determine type from right-hand side
                var_type, element_type = self.type_inferencer.infer_type(node.value)
                
                # Check if this is an aliasing assignment
                is_alias = isinstance(node.value, ast.Name)
                
                if var_name in self.symbol_table:
                    # Update existing variable
                    var_info = self.symbol_table[var_name]
                    
                    if var_info.var_type != var_type:
                        var_info.is_reassigned = True
                        var_info.var_type = var_type
                else:
                    # Create new variable
                    var_info = VariableInfo(
                        name=var_name,
                        var_type=var_type,
                        element_type=element_type,
                        scope=self.current_scope(),
                        first_assignment_line=node.lineno
                    )
                    self.symbol_table[var_name] = var_info
                
                # Track aliasing
                if is_alias:
                    source_var = node.value.id
                    alias_tracker.track_alias(var_name, source_var)
                
                # Add type constraint
                self.type_constraints.append(TypeConstraint(
                    variable=var_name,
                    constraint_type=var_type,
                    reason=f"assigned at line {node.lineno}"
                ))
    
    def handle_name_usage(self, node: ast.Name):
        """Track variable usage"""
        var_name = node.id
        if var_name in self.symbol_table:
            self.symbol_table[var_name].usage_lines.append(node.lineno)
    
    def handle_aug_assign(self, node: ast.AugAssign, mutated_vars):
        """Handle augmented assignment (+=, -=, etc.)"""
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            
            mutated_vars.add(var_name)
            
            if var_name in self.symbol_table:
                if 'augmented_assign' not in self.symbol_table[var_name].mutations:
                    self.symbol_table[var_name].mutations.append('augmented_assign')

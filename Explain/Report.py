# Explain/report.py
"""
Report generation for semantic analysis results
"""


class ReportGenerator:
    """Generates human-readable reports"""
    
    def __init__(self, symbol_table, functions, aliases, mutated_vars, type_constraints):
        self.symbol_table = symbol_table
        self.functions = functions
        self.aliases = aliases
        self.mutated_vars = mutated_vars
        self.type_constraints = type_constraints
    
    def generate_report(self) -> str:
        """Generate complete analysis report"""
        lines = ["="*70]
        lines.append("SEMANTIC ANALYSIS REPORT")
        lines.append("="*70)
        
        lines.extend(self._generate_symbol_table_section())
        lines.extend(self._generate_functions_section())
        lines.extend(self._generate_aliasing_section())
        lines.extend(self._generate_mutations_section())
        
        lines.append("\n" + "="*70)
        return "\n".join(lines)
    
    def _generate_symbol_table_section(self):
        """Generate symbol table section"""
        lines = ["\n📊 SYMBOL TABLE", "-"*70]
        
        for var_name, var_info in self.symbol_table.items():
            lines.append(f"\nVariable: {var_name}")
            lines.append(f"  Type: {var_info.var_type.value}")
            if var_info.element_type:
                lines.append(f"  Element Type: {var_info.element_type.value}")
            lines.append(f"  Scope: {var_info.scope}")
            lines.append(f"  Mutable: {var_info.is_mutable}")
            lines.append(f"  Reassigned: {var_info.is_reassigned}")
            if hasattr(var_info, 'memory_effect') and var_info.memory_effect:
                lines.append(f"  Memory Effect: {var_info.memory_effect.value}")
            if var_info.aliases:
                lines.append(f"  Aliases: {var_info.aliases}")
            if var_info.mutations:
                lines.append(f"  Mutations: {', '.join(var_info.mutations)}")
            if var_info.usage_lines:
                lines.append(f"  Used at lines: {var_info.usage_lines}")
        
        return lines
    
    def _generate_functions_section(self):
        """Generate functions section"""
        lines = ["\n\n🔧 FUNCTIONS", "-"*70]
        
        for func_name, func_info in self.functions.items():
            lines.append(f"\nFunction: {func_name}")
            lines.append(f"  Parameters: {[p.name for p in func_info.parameters]}")
            lines.append(f"  Return Type: {func_info.return_type}")
            if func_info.modifies_params:
                lines.append(f"  Modifies: {func_info.modifies_params}")
            if func_info.calls_functions:
                lines.append(f"  Calls: {func_info.calls_functions}")
        
        return lines
    
    def _generate_aliasing_section(self):
        """Generate aliasing section"""
        lines = ["\n\n🔗 ALIASING", "-"*70]
        
        seen = set()
        for var, aliases in self.aliases.items():
            if len(aliases) > 1 and var not in seen:
                lines.append(f"  {aliases}")
                seen.update(aliases)
        
        if not seen:
            lines.append("  None detected")
        
        return lines
    
    def _generate_mutations_section(self):
        """Generate mutations section"""
        lines = ["\n\n🔄 MUTATIONS", "-"*70]
        
        if self.mutated_vars:
            for var in self.mutated_vars:
                lines.append(f"  {var}")
        else:
            lines.append("  None detected")
        
        return lines
#!/usr/bin/env python3
"""
Deep Dependency Analyzer - Granular bi-directional dependency mapping
Maps file-to-file, function-to-function, and class relationships with impact analysis
"""

import os
import ast
import json
import click
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
import logging
from collections import defaultdict, deque


class DeepDependencyAnalyzer:
    """Analyzes granular dependencies and relationships between code elements"""
    
    def __init__(self):
        self.dependency_graph = defaultdict(lambda: {
            'imports_from': set(),
            'imported_by': set(),
            'functions_used': defaultdict(set),  # {source_file: {functions_used}}
            'functions_providing': defaultdict(set),  # {target_file: {functions_provided}}
            'classes_used': defaultdict(set),
            'classes_providing': defaultdict(set)
        })
        self.function_usage_graph = defaultdict(lambda: {
            'calls_functions': set(),
            'called_by_functions': set(),
            'defined_in_file': None
        })
        self.impact_graph = defaultdict(set)
        self.circular_dependencies = []
        
    def analyze_project_dependencies(self, project_path: str, file_inventory: Dict = None) -> Dict[str, Any]:
        """Analyze all dependencies in the project with granular detail"""
        project_path = Path(project_path).resolve()
        
        # If no file inventory provided, do a basic scan
        if file_inventory is None:
            file_inventory = self._basic_file_scan(project_path)
        
        print(f"🔗 Analyzing dependencies for {len(file_inventory)} files...")
        
        # Phase 1: Extract all imports and function definitions
        for file_path, file_info in file_inventory.items():
            self._analyze_file_dependencies(project_path / file_path, file_path, file_info)
        
        # Phase 2: Map function-level usage
        for file_path, file_info in file_inventory.items():
            self._analyze_function_usage(project_path / file_path, file_path, file_info)
        
        # Phase 3: Build impact analysis
        self._build_impact_analysis()
        
        # Phase 4: Detect circular dependencies
        self._detect_circular_dependencies()
        
        return self._compile_results()
    
    def _basic_file_scan(self, project_path: Path) -> Dict[str, Any]:
        """Basic scan if no file inventory is provided"""
        file_inventory = {}
        source_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cs'}
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}]
            
            for file in files:
                if Path(file).suffix.lower() in source_extensions:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    file_inventory[str(relative_path)] = {
                        'extension': file_path.suffix.lower(),
                        'size_bytes': file_path.stat().st_size if file_path.exists() else 0
                    }
        
        return file_inventory
    
    def _analyze_file_dependencies(self, file_path: Path, relative_path: str, file_info: Dict):
        """Analyze imports and exports for a single file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            logging.warning(f"Could not read {relative_path}: {e}")
            return
        
        extension = file_info.get('extension', file_path.suffix.lower())
        
        if extension == '.py':
            self._analyze_python_imports(content, relative_path)
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            self._analyze_js_imports(content, relative_path)
        elif extension == '.java':
            self._analyze_java_imports(content, relative_path)
        elif extension == '.cs':
            self._analyze_csharp_imports(content, relative_path)
        elif extension == '.go':
            self._analyze_go_imports(content, relative_path)
        elif extension == '.rs':
            self._analyze_rust_imports(content, relative_path)
        elif extension in {'.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx'}:
            self._analyze_cpp_imports(content, relative_path)
        elif extension == '.rb':
            self._analyze_ruby_imports(content, relative_path)
        elif extension == '.php':
            self._analyze_php_imports(content, relative_path)
    
    def _analyze_python_imports(self, content: str, file_path: str):
        """Analyze Python imports with function-level detail"""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_dependency(file_path, alias.name, 'import')
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_path = self._resolve_python_import_path(node.module, file_path)
                        if module_path:
                            self._add_dependency(file_path, module_path, 'import_from')
                            
                            # Track specific functions/classes imported
                            for alias in node.names:
                                if alias.name != '*':
                                    self.dependency_graph[file_path]['functions_used'][module_path].add(alias.name)
                                    self.dependency_graph[module_path]['functions_providing'][file_path].add(alias.name)
        
        except Exception as e:
            logging.warning(f"Could not parse Python file {file_path}: {e}")
    
    def _analyze_js_imports(self, content: str, file_path: str):
        """Analyze JavaScript/TypeScript imports"""
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            
            # ES6 imports: import { func1, func2 } from './module'
            import_match = re.search(r"import\s*\{([^}]+)\}\s*from\s*['\"](.+)['\"]", line)
            if import_match:
                functions = [f.strip() for f in import_match.group(1).split(',')]
                module_path = self._resolve_js_import_path(import_match.group(2), file_path)
                if module_path:
                    self._add_dependency(file_path, module_path, 'import')
                    for func in functions:
                        self.dependency_graph[file_path]['functions_used'][module_path].add(func)
                        self.dependency_graph[module_path]['functions_providing'][file_path].add(func)
                continue
            
            # Default imports: import Module from './module'
            import_match = re.search(r"import\s+(\w+)\s*from\s*['\"](.+)['\"]", line)
            if import_match:
                module_name = import_match.group(1)
                module_path = self._resolve_js_import_path(import_match.group(2), file_path)
                if module_path:
                    self._add_dependency(file_path, module_path, 'import')
                    self.dependency_graph[file_path]['functions_used'][module_path].add(module_name)
                continue
            
            # require statements
            require_match = re.search(r"require\s*\(\s*['\"](.+)['\"]\s*\)", line)
            if require_match:
                module_path = self._resolve_js_import_path(require_match.group(1), file_path)
                if module_path:
                    self._add_dependency(file_path, module_path, 'require')
    
    def _analyze_java_imports(self, content: str, file_path: str):
        """Analyze Java imports"""
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('import ') and not line.startswith('import static'):
                match = re.search(r'import\s+([^;]+);', line)
                if match:
                    import_path = match.group(1)
                    # Convert Java package notation to file path
                    java_path = import_path.replace('.', '/') + '.java'
                    self._add_dependency(file_path, java_path, 'import')
    
    def _analyze_csharp_imports(self, content: str, file_path: str):
        """Analyze C# using statements"""
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('using ') and ';' in line:
                match = re.search(r'using\s+([^;]+);', line)
                if match:
                    namespace = match.group(1)
                    # This is a simplification - real C# analysis would need more context
                    self._add_dependency(file_path, namespace, 'using')
    
    def _analyze_go_imports(self, content: str, file_path: str):
        """Analyze Go import statements"""
        lines = content.splitlines()
        in_import_block = False
        
        for line in lines:
            line = line.strip()
            
            # Single import
            if line.startswith('import "'):
                match = re.search(r'import\s+"([^"]+)"', line)
                if match:
                    import_path = match.group(1)
                    self._add_dependency(file_path, import_path, 'import')
            
            # Import block start
            elif line.startswith('import ('):
                in_import_block = True
            
            # Import block end
            elif line == ')' and in_import_block:
                in_import_block = False
            
            # Inside import block
            elif in_import_block and line.startswith('"'):
                match = re.search(r'"([^"]+)"', line)
                if match:
                    import_path = match.group(1)
                    self._add_dependency(file_path, import_path, 'import')
    
    def _analyze_rust_imports(self, content: str, file_path: str):
        """Analyze Rust use statements"""
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('use ') and ';' in line:
                match = re.search(r'use\s+([^;]+);', line)
                if match:
                    use_path = match.group(1)
                    # Handle different use patterns like use crate::module, use super::, etc.
                    if '::' in use_path:
                        # Extract the main crate or module
                        main_module = use_path.split('::')[0]
                        self._add_dependency(file_path, main_module, 'use')
                    else:
                        self._add_dependency(file_path, use_path, 'use')
            
            # External crate dependencies
            elif line.startswith('extern crate '):
                match = re.search(r'extern crate\s+([^;]+);', line)
                if match:
                    crate_name = match.group(1)
                    self._add_dependency(file_path, crate_name, 'extern_crate')
    
    def _analyze_cpp_imports(self, content: str, file_path: str):
        """Analyze C/C++ #include statements"""
        for line in content.splitlines():
            line = line.strip()
            if line.startswith('#include'):
                # System includes with < >
                match = re.search(r'#include\s*<([^>]+)>', line)
                if match:
                    header = match.group(1)
                    self._add_dependency(file_path, header, 'system_include')
                
                # Local includes with " "
                match = re.search(r'#include\s*"([^"]+)"', line)
                if match:
                    header = match.group(1)
                    self._add_dependency(file_path, header, 'local_include')
    
    def _analyze_ruby_imports(self, content: str, file_path: str):
        """Analyze Ruby require / require_relative statements"""
        for line in content.splitlines():
            stripped = line.strip()
            # require_relative (local dependency)
            rel_match = re.search(r"require_relative\s+['\"](.+)['\"]", stripped)
            if rel_match:
                local_path = rel_match.group(1)
                if not local_path.endswith('.rb'):
                    local_path += '.rb'
                # Resolve relative to current file
                resolved = str(Path(file_path).parent / local_path)
                self._add_dependency(file_path, resolved, 'require_relative')
                continue
            # require (gem or stdlib)
            req_match = re.search(r"require\s+['\"](.+)['\"]", stripped)
            if req_match:
                module = req_match.group(1)
                self._add_dependency(file_path, module, 'require')
    
    def _analyze_php_imports(self, content: str, file_path: str):
        """Analyze PHP use, require, and include statements"""
        for line in content.splitlines():
            stripped = line.strip()
            # use statements (namespaced classes)
            use_match = re.search(r'^use\s+([^;]+);', stripped)
            if use_match:
                fqn = use_match.group(1).split(' as ')[0].strip().lstrip('\\')
                # Convert namespace separator to path
                php_path = fqn.replace('\\', '/') + '.php'
                self._add_dependency(file_path, php_path, 'use')
                continue
            # require / include
            inc_match = re.search(r"(?:require|include)(?:_once)?\s*[\(]?\s*['\"](.+?)['\"]\s*[\)]?\s*;", stripped)
            if inc_match:
                included = inc_match.group(1)
                self._add_dependency(file_path, included, 'include')
        """Resolve Python import to actual file path"""
        if module.startswith('.'):
            # Relative import
            current_dir = str(Path(current_file).parent)
            if module == '.':
                return current_dir + '/__init__.py'
            else:
                # Remove leading dots and convert to path
                relative_path = module.lstrip('.')
                if current_dir == '.':
                    resolved = relative_path.replace('.', '/') + '.py'
                else:
                    resolved = current_dir + '/' + relative_path.replace('.', '/') + '.py'
                return resolved
        else:
            # Absolute import - could be internal or external
            # For internal imports, convert package notation to path
            internal_path = module.replace('.', '/') + '.py'
            return internal_path
        
        return None
    
    def _resolve_js_import_path(self, import_path: str, current_file: str) -> Optional[str]:
        """Resolve JavaScript import to actual file path"""
        if import_path.startswith('./') or import_path.startswith('../'):
            # Relative import
            current_dir = Path(current_file).parent
            resolved = current_dir / import_path
            
            # Try different extensions
            for ext in ['', '.js', '.jsx', '.ts', '.tsx', '/index.js', '/index.ts']:
                candidate = str(resolved) + ext
                if Path(candidate).exists() or ext == '':  # Return path even if file doesn't exist locally
                    return candidate.replace('\\', '/')
        
        return import_path  # External module or absolute path
    
    def _add_dependency(self, from_file: str, to_file: str, dependency_type: str):
        """Add a dependency relationship"""
        self.dependency_graph[from_file]['imports_from'].add(to_file)
        self.dependency_graph[to_file]['imported_by'].add(from_file)
    
    def _analyze_function_usage(self, file_path: Path, relative_path: str, file_info: Dict):
        """Analyze function-level usage within files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            return
        
        extension = file_info.get('extension', file_path.suffix.lower())
        
        if extension == '.py':
            self._analyze_python_function_calls(content, relative_path)
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            self._analyze_js_function_calls(content, relative_path)
    
    def _analyze_python_function_calls(self, content: str, file_path: str):
        """Analyze Python function calls and definitions"""
        try:
            tree = ast.parse(content)
            
            # Track function definitions in this file
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = f"{file_path}::{node.name}"
                    self.function_usage_graph[func_name]['defined_in_file'] = file_path
                
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        # Direct function call: func()
                        called_func = node.func.id
                        caller_context = f"{file_path}::caller"
                        self.function_usage_graph[caller_context]['calls_functions'].add(called_func)
                        self.function_usage_graph[called_func]['called_by_functions'].add(caller_context)
                    
                    elif isinstance(node.func, ast.Attribute):
                        # Method call: obj.method()
                        if isinstance(node.func.value, ast.Name):
                            method_call = f"{node.func.value.id}.{node.func.attr}"
                            caller_context = f"{file_path}::caller"
                            self.function_usage_graph[caller_context]['calls_functions'].add(method_call)
                            self.function_usage_graph[method_call]['called_by_functions'].add(caller_context)
        
        except Exception as e:
            logging.warning(f"Could not analyze function calls in {file_path}: {e}")
    
    def _analyze_js_function_calls(self, content: str, file_path: str):
        """Analyze JavaScript function calls"""
        # Simplified analysis - would need full AST parsing for complete accuracy
        lines = content.splitlines()
        
        for line in lines:
            # Look for function calls: func() or obj.method()
            func_calls = re.findall(r'(\w+(?:\.\w+)*)\s*\(', line)
            for call in func_calls:
                caller_context = f"{file_path}::caller"
                self.function_usage_graph[caller_context]['calls_functions'].add(call)
                self.function_usage_graph[call]['called_by_functions'].add(caller_context)
    
    def _build_impact_analysis(self):
        """Build impact analysis - what affects what"""
        for file_path, deps in self.dependency_graph.items():
            # If this file changes, what else is affected?
            for dependent_file in deps['imported_by']:
                self.impact_graph[file_path].add(dependent_file)
                
            # Transitive dependencies - if this file's dependencies change
            for dependency in deps['imports_from']:
                self.impact_graph[dependency].add(file_path)
    
    def _detect_circular_dependencies(self):
        """Detect circular dependencies using DFS"""
        visited = set()
        rec_stack = set()
        
        def dfs(file_path, path):
            if file_path in rec_stack:
                # Found a cycle
                if file_path in path:
                    cycle_start = path.index(file_path)
                    cycle = path[cycle_start:] + [file_path]
                    self.circular_dependencies.append(cycle)
                return True
            
            if file_path in visited:
                return False
            
            visited.add(file_path)
            rec_stack.add(file_path)
            
            for dependency in self.dependency_graph[file_path]['imports_from']:
                if dfs(dependency, path + [file_path]):
                    return True
            
            rec_stack.remove(file_path)
            return False
        
        for file_path in self.dependency_graph.keys():
            if file_path not in visited:
                dfs(file_path, [])
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile all analysis results into structured output"""
        
        # Convert sets to lists for JSON serialization
        dependency_graph_serializable = {}
        for file_path, deps in self.dependency_graph.items():
            dependency_graph_serializable[file_path] = {
                'imports_from': list(deps['imports_from']),
                'imported_by': list(deps['imported_by']),
                'functions_used': {k: list(v) for k, v in deps['functions_used'].items()},
                'functions_providing': {k: list(v) for k, v in deps['functions_providing'].items()},
                'classes_used': {k: list(v) for k, v in deps['classes_used'].items()},
                'classes_providing': {k: list(v) for k, v in deps['classes_providing'].items()}
            }
        
        function_graph_serializable = {}
        for func_name, usage in self.function_usage_graph.items():
            function_graph_serializable[func_name] = {
                'calls_functions': list(usage['calls_functions']),
                'called_by_functions': list(usage['called_by_functions']),
                'defined_in_file': usage['defined_in_file']
            }
        
        impact_graph_serializable = {k: list(v) for k, v in self.impact_graph.items()}
        
        return {
            'dependency_graph': dependency_graph_serializable,
            'function_dependencies': function_graph_serializable,
            'impact_analysis': impact_graph_serializable,
            'circular_dependencies': self.circular_dependencies,
            'statistics': {
                'total_files': len(dependency_graph_serializable),
                'total_dependencies': sum(len(deps['imports_from']) for deps in dependency_graph_serializable.values()),
                'circular_dependency_count': len(self.circular_dependencies),
                'average_dependencies_per_file': sum(len(deps['imports_from']) for deps in dependency_graph_serializable.values()) / max(len(dependency_graph_serializable), 1)
            }
        }


@click.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='Output directory for dependency analysis')
@click.option('--file-inventory', help='Path to file inventory JSON (optional)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(project_path, output, file_inventory, verbose):
    """Analyze granular dependencies and relationships in a codebase"""
    
    if verbose:
        logging.basicConfig(level=logging.INFO)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load file inventory if provided
    inventory_data = None
    if file_inventory:
        with open(file_inventory, 'r') as f:
            inventory_data = json.load(f)
    
    analyzer = DeepDependencyAnalyzer()
    
    print(f"🔍 Analyzing dependencies in: {project_path}")
    results = analyzer.analyze_project_dependencies(project_path, inventory_data)
    
    # Save dependency graph
    dep_graph_file = output_path / 'dependency-graph.json'
    with open(dep_graph_file, 'w') as f:
        json.dump(results['dependency_graph'], f, indent=2)
    print(f"📊 Dependency graph saved to: {dep_graph_file}")
    
    # Save function dependencies
    func_deps_file = output_path / 'function-dependencies.json'
    with open(func_deps_file, 'w') as f:
        json.dump(results['function_dependencies'], f, indent=2)
    print(f"🔧 Function dependencies saved to: {func_deps_file}")
    
    # Save impact analysis
    impact_file = output_path / 'impact-analysis.json'
    with open(impact_file, 'w') as f:
        json.dump(results['impact_analysis'], f, indent=2)
    print(f"⚡ Impact analysis saved to: {impact_file}")
    
    # Save circular dependencies
    circular_file = output_path / 'circular-dependencies.json'
    with open(circular_file, 'w') as f:
        json.dump(results['circular_dependencies'], f, indent=2)
    print(f"🔄 Circular dependencies saved to: {circular_file}")
    
    # Print statistics
    stats = results['statistics']
    print(f"\n📈 Dependency Analysis Statistics:")
    print(f"   Total files analyzed: {stats['total_files']}")
    print(f"   Total dependencies: {stats['total_dependencies']}")
    print(f"   Circular dependencies found: {stats['circular_dependency_count']}")
    print(f"   Average dependencies per file: {stats['average_dependencies_per_file']:.1f}")
    
    if results['circular_dependencies']:
        print(f"\n⚠️  Circular dependencies found:")
        for i, cycle in enumerate(results['circular_dependencies'], 1):
            print(f"   {i}. {' → '.join(cycle)}")


if __name__ == '__main__':
    main()
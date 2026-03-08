#!/usr/bin/env python3
"""
Dependency Analysis Script for Codebase Architecture Analyst

This script analyzes a codebase to extract and map dependencies between files,
modules, and external packages. It supports multiple programming languages
and provides structured output for architecture documentation.
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict

class DependencyAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.dependencies = defaultdict(set)
        self.external_dependencies = defaultdict(set)
        self.internal_dependencies = defaultdict(set)
        self.file_types = defaultdict(int)
        
    def analyze_project(self) -> Dict:
        """Analyze the entire project for dependencies."""
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and not self._should_skip_file(file_path):
                self._analyze_file(file_path)
        
        return {
            'external_dependencies': dict(self.external_dependencies),
            'internal_dependencies': dict(self.internal_dependencies),
            'file_types': dict(self.file_types),
            'dependency_graph': self._build_dependency_graph()
        }
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during analysis."""
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'venv', 'env'}
        skip_extensions = {'.pyc', '.log', '.tmp', '.cache'}
        
        # Check if file is in skip directory
        if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
            return True
            
        # Check file extension
        if file_path.suffix in skip_extensions:
            return True
            
        return False
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single file for dependencies."""
        relative_path = file_path.relative_to(self.project_root)
        file_extension = file_path.suffix
        self.file_types[file_extension] += 1
        
        try:
            if file_extension == '.py':
                self._analyze_python_file(file_path, relative_path)
            elif file_extension in ['.js', '.ts', '.jsx', '.tsx']:
                self._analyze_javascript_file(file_path, relative_path)
            elif file_extension in ['.java']:
                self._analyze_java_file(file_path, relative_path)
            elif file_extension in ['.cs']:
                self._analyze_csharp_file(file_path, relative_path)
            elif file_path.name in ['package.json', 'requirements.txt', 'Pipfile', 'pom.xml']:
                self._analyze_dependency_file(file_path, relative_path)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def _analyze_python_file(self, file_path: Path, relative_path: Path):
        """Analyze Python file for imports."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._add_dependency(relative_path, alias.name, 'python')
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    self._add_dependency(relative_path, module, 'python')
                    
        except Exception as e:
            # Fallback to regex parsing if AST fails
            self._analyze_python_file_regex(file_path, relative_path)
    
    def _analyze_python_file_regex(self, file_path: Path, relative_path: Path):
        """Fallback regex-based Python analysis."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Match import statements
            import_patterns = [
                r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)',
                r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import'
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    self._add_dependency(relative_path, match, 'python')
                    
        except Exception as e:
            print(f"Error in regex analysis for {file_path}: {e}")
    
    def _analyze_javascript_file(self, file_path: Path, relative_path: Path):
        """Analyze JavaScript/TypeScript file for imports.""" 
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ES6 imports and CommonJS requires
            patterns = [
                r"import\s+.*?from\s+['\"]([^'\"]+)['\"]",
                r"import\s+['\"]([^'\"]+)['\"]",
                r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
                r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"  # Dynamic imports
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    self._add_dependency(relative_path, match, 'javascript')
                    
        except Exception as e:
            print(f"Error analyzing JavaScript file {file_path}: {e}")
    
    def _analyze_java_file(self, file_path: Path, relative_path: Path):
        """Analyze Java file for imports."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Java import statements
            import_pattern = r'import\s+(?:static\s+)?([a-zA-Z_][a-zA-Z0-9_.]*(?:\.\*)?);'
            matches = re.findall(import_pattern, content)
            
            for match in matches:
                self._add_dependency(relative_path, match, 'java')
                
        except Exception as e:
            print(f"Error analyzing Java file {file_path}: {e}")
    
    def _analyze_csharp_file(self, file_path: Path, relative_path: Path):
        """Analyze C# file for using statements."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # C# using statements
            using_pattern = r'using\s+([a-zA-Z_][a-zA-Z0-9_.]*);'
            matches = re.findall(using_pattern, content)
            
            for match in matches:
                self._add_dependency(relative_path, match, 'csharp')
                
        except Exception as e:
            print(f"Error analyzing C# file {file_path}: {e}")
    
    def _analyze_dependency_file(self, file_path: Path, relative_path: Path):
        """Analyze package/dependency definition files."""
        try:
            if file_path.name == 'package.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                deps = {}
                deps.update(data.get('dependencies', {}))
                deps.update(data.get('devDependencies', {}))
                
                for dep_name in deps.keys():
                    self.external_dependencies[str(relative_path)].add(dep_name)
                    
            elif file_path.name in ['requirements.txt', 'Pipfile']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract package names (basic parsing)
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        package = re.split(r'[>=<!\s]', line)[0]
                        if package:
                            self.external_dependencies[str(relative_path)].add(package)
                            
        except Exception as e:
            print(f"Error analyzing dependency file {file_path}: {e}")
    
    def _add_dependency(self, source_file: Path, dependency: str, language: str):
        """Add a dependency to the appropriate collection."""
        source_str = str(source_file)
        
        # Determine if dependency is internal or external
        if self._is_internal_dependency(dependency, language):
            self.internal_dependencies[source_str].add(dependency)
        else:
            self.external_dependencies[source_str].add(dependency)
    
    def _is_internal_dependency(self, dependency: str, language: str) -> bool:
        """Check if a dependency is internal to the project."""
        if language == 'python':
            # Check if it's a relative import or local module
            if dependency.startswith('.'):
                return True
            # Check if corresponding file exists in project
            possible_paths = [
                self.project_root / f"{dependency.replace('.', '/')}.py",
                self.project_root / dependency.replace('.', '/') / '__init__.py'
            ]
            return any(p.exists() for p in possible_paths)
            
        elif language == 'javascript':
            # Relative imports are internal
            if dependency.startswith('.') or dependency.startswith('/'):
                return True
            # Check if it exists in project
            base_dir = self.project_root / 'src' if (self.project_root / 'src').exists() else self.project_root
            possible_paths = [
                base_dir / f"{dependency}.js",
                base_dir / f"{dependency}.ts", 
                base_dir / dependency / 'index.js',
                base_dir / dependency / 'index.ts'
            ]
            return any(p.exists() for p in possible_paths)
            
        return False
    
    def _build_dependency_graph(self) -> Dict:
        """Build a graph representation of dependencies."""
        graph = {
            'nodes': [],
            'edges': []
        }
        
        all_files = set()
        all_files.update(self.internal_dependencies.keys())
        all_files.update(self.external_dependencies.keys())
        
        # Add file nodes
        for file_path in all_files:
            graph['nodes'].append({
                'id': file_path,
                'type': 'file',
                'label': Path(file_path).name
            })
        
        # Add dependency edges
        for source_file, deps in self.internal_dependencies.items():
            for dep in deps:
                graph['edges'].append({
                    'source': source_file,
                    'target': dep,
                    'type': 'internal'
                })
        
        for source_file, deps in self.external_dependencies.items():
            for dep in deps:
                # Add external dependency node if not exists
                dep_node_id = f"external:{dep}"
                if not any(node['id'] == dep_node_id for node in graph['nodes']):
                    graph['nodes'].append({
                        'id': dep_node_id,
                        'type': 'external',
                        'label': dep
                    })
                
                graph['edges'].append({
                    'source': source_file,
                    'target': dep_node_id,
                    'type': 'external'
                })
        
        return graph

def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze codebase dependencies')
    parser.add_argument('project_path', help='Path to the project root')
    parser.add_argument('--output', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    analyzer = DependencyAnalyzer(args.project_path)
    results = analyzer.analyze_project()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))

if __name__ == '__main__':
    main()
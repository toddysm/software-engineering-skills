#!/usr/bin/env python3
"""
Dependency Query Engine - Interactive exploration of codebase dependencies
Answers specific questions about file and function relationships
"""

import json
import click
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
from collections import defaultdict, deque


class DependencyQueryEngine:
    """Interactive query engine for exploring codebase dependencies"""
    
    def __init__(self):
        self.dependency_graph = {}
        self.function_dependencies = {}
        self.impact_analysis = {}
        self.circular_dependencies = []
        self.file_inventory = {}
        self.reverse_lookup = {}  # For fuzzy file matching
        self.loaded = False
    
    def load_analysis_data(self, analysis_dir: str):
        """Load all analysis data from directory"""
        analysis_path = Path(analysis_dir)
        
        # Load dependency graph
        dep_file = analysis_path / 'dependencies' / 'dependency-graph.json'
        if dep_file.exists():
            with open(dep_file, 'r') as f:
                self.dependency_graph = json.load(f)
        
        # Load function dependencies
        func_file = analysis_path / 'dependencies' / 'function-dependencies.json'
        if func_file.exists():
            with open(func_file, 'r') as f:
                self.function_dependencies = json.load(f)
        
        # Load impact analysis
        impact_file = analysis_path / 'dependencies' / 'impact-analysis.json'
        if impact_file.exists():
            with open(impact_file, 'r') as f:
                self.impact_analysis = json.load(f)
        
        # Load circular dependencies
        circular_file = analysis_path / 'dependencies' / 'circular-dependencies.json'
        if circular_file.exists():
            with open(circular_file, 'r') as f:
                self.circular_dependencies = json.load(f)
        
        # Load file inventory
        inventory_file = analysis_path / 'source-files' / 'file-inventory.json'
        if inventory_file.exists():
            with open(inventory_file, 'r') as f:
                self.file_inventory = json.load(f)
        
        # Build reverse lookup for fuzzy matching
        self._build_reverse_lookup()
        self.loaded = True
        print(f"✅ Loaded analysis data from {analysis_dir}")
    
    def _build_reverse_lookup(self):
        """Build reverse lookup tables for fuzzy file and function matching"""
        self.reverse_lookup = {
            'files_by_name': {},
            'files_by_partial': defaultdict(list),
            'functions_by_name': defaultdict(list),
            'classes_by_name': defaultdict(list)
        }
        
        # Index files
        for file_path in self.dependency_graph.keys():
            filename = Path(file_path).name
            self.reverse_lookup['files_by_name'][filename] = file_path
            
            # Index partial matches
            parts = file_path.lower().replace('/', ' ').replace('_', ' ').split()
            for part in parts:
                if len(part) > 2:
                    self.reverse_lookup['files_by_partial'][part].append(file_path)
        
        # Index functions and classes from file inventory
        for file_path, file_info in self.file_inventory.items():
            if 'functions' in file_info:
                for func in file_info['functions']:
                    self.reverse_lookup['functions_by_name'][func['name']].append(f"{file_path}::{func['name']}")
            
            if 'classes' in file_info:
                for cls in file_info['classes']:
                    self.reverse_lookup['classes_by_name'][cls['name']].append(f"{file_path}::{cls['name']}")
    
    def find_file(self, query: str) -> List[str]:
        """Find files matching a query (exact, filename, or partial match)"""
        if not self.loaded:
            return []
        
        matches = []
        query_lower = query.lower()
        
        # Exact match
        if query in self.dependency_graph:
            return [query]
        
        # Filename match
        if query in self.reverse_lookup['files_by_name']:
            matches.append(self.reverse_lookup['files_by_name'][query])
        
        # Partial matches
        for file_path in self.dependency_graph.keys():
            if query_lower in file_path.lower():
                matches.append(file_path)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_matches = []
        for match in matches:
            if match not in seen:
                seen.add(match)
                unique_matches.append(match)
        
        return unique_matches
    
    def query_what_depends_on(self, target_file: str) -> Dict[str, Any]:
        """Answer: What files depend on this file?"""
        files = self.find_file(target_file)
        if not files:
            return {'error': f"File '{target_file}' not found"}
        
        if len(files) > 1:
            return {
                'error': f"Multiple files match '{target_file}'",
                'candidates': files,
                'suggestion': "Please be more specific"
            }
        
        file_path = files[0]
        dependencies = self.dependency_graph.get(file_path, {})
        
        result = {
            'target_file': file_path,
            'imported_by': dependencies.get('imported_by', []),
            'functions_used_by': {},
            'impact_scope': self.impact_analysis.get(file_path, [])
        }
        
        # Add function-level details
        for importing_file in result['imported_by']:
            functions_used = dependencies.get('functions_providing', {}).get(importing_file, [])
            if functions_used:
                result['functions_used_by'][importing_file] = functions_used
        
        return result
    
    def query_what_does_depend_on(self, source_file: str) -> Dict[str, Any]:
        """Answer: What does this file depend on?"""
        files = self.find_file(source_file)
        if not files:
            return {'error': f"File '{source_file}' not found"}
        
        if len(files) > 1:
            return {
                'error': f"Multiple files match '{source_file}'",
                'candidates': files,
                'suggestion': "Please be more specific"
            }
        
        file_path = files[0]
        dependencies = self.dependency_graph.get(file_path, {})
        
        result = {
            'source_file': file_path,
            'imports_from': dependencies.get('imports_from', []),
            'functions_used_from': dependencies.get('functions_used', {}),
            'classes_used_from': dependencies.get('classes_used', {})
        }
        
        return result
    
    def query_dependency_tree(self, root_file: str, max_depth: int = 3) -> Dict[str, Any]:
        """Show hierarchical dependency tree for a component"""
        files = self.find_file(root_file)
        if not files:
            return {'error': f"File '{root_file}' not found"}
        
        if len(files) > 1:
            return {
                'error': f"Multiple files match '{root_file}'",
                'candidates': files,
                'suggestion': "Please be more specific"
            }
        
        root_path = files[0]
        tree = self._build_dependency_tree(root_path, max_depth)
        
        return {
            'root_file': root_path,
            'dependency_tree': tree,
            'max_depth': max_depth
        }
    
    def _build_dependency_tree(self, root_file: str, max_depth: int, current_depth: int = 0, visited: Set[str] = None) -> Dict[str, Any]:
        """Recursively build dependency tree"""
        if visited is None:
            visited = set()
        
        if current_depth >= max_depth or root_file in visited:
            return {'file': root_file, 'dependencies': [], 'truncated': current_depth >= max_depth}
        
        visited.add(root_file)
        dependencies = self.dependency_graph.get(root_file, {})
        
        tree = {
            'file': root_file,
            'dependencies': [],
            'functions_used': dependencies.get('functions_used', {}),
            'depth': current_depth
        }
        
        for dep_file in dependencies.get('imports_from', []):
            subtree = self._build_dependency_tree(dep_file, max_depth, current_depth + 1, visited.copy())
            tree['dependencies'].append(subtree)
        
        return tree
    
    def query_impact_analysis(self, target_file: str) -> Dict[str, Any]:
        """Answer: If I change this file, what else is affected?"""
        files = self.find_file(target_file)
        if not files:
            return {'error': f"File '{target_file}' not found"}
        
        if len(files) > 1:
            return {
                'error': f"Multiple files match '{target_file}'",
                'candidates': files,
                'suggestion': "Please be more specific"
            }
        
        file_path = files[0]
        
        # Direct impact
        direct_impact = self.dependency_graph.get(file_path, {}).get('imported_by', [])
        
        # Transitive impact (files that depend on files that depend on this file)
        transitive_impact = set()
        queue = deque(direct_impact)
        visited = {file_path}
        
        while queue:
            current_file = queue.popleft()
            if current_file in visited:
                continue
                
            visited.add(current_file)
            transitive_impact.add(current_file)
            
            # Add files that depend on this file
            next_level = self.dependency_graph.get(current_file, {}).get('imported_by', [])
            for next_file in next_level:
                if next_file not in visited:
                    queue.append(next_file)
        
        return {
            'target_file': file_path,
            'direct_impact': direct_impact,
            'transitive_impact': list(transitive_impact - set(direct_impact)),
            'total_affected_files': len(transitive_impact),
            'risk_assessment': self._assess_change_risk(len(direct_impact), len(transitive_impact))
        }
    
    def _assess_change_risk(self, direct_count: int, total_count: int) -> str:
        """Assess risk level of changing a file"""
        if total_count == 0:
            return "Low - No dependencies"
        elif total_count <= 3:
            return "Low - Few dependencies"
        elif total_count <= 10:
            return "Medium - Moderate dependencies"
        elif total_count <= 25:
            return "High - Many dependencies"
        else:
            return "Very High - Extensive dependencies"
    
    def query_function_usage(self, source_file: str, target_file: str) -> Dict[str, Any]:
        """Answer: What functions from source_file are used by target_file?"""
        source_files = self.find_file(source_file)
        target_files = self.find_file(target_file)
        
        if not source_files:
            return {'error': f"Source file '{source_file}' not found"}
        if not target_files:
            return {'error': f"Target file '{target_file}' not found"}
        
        if len(source_files) > 1 or len(target_files) > 1:
            return {
                'error': "Multiple files match",
                'source_candidates': source_files if len(source_files) > 1 else [source_files[0]],
                'target_candidates': target_files if len(target_files) > 1 else [target_files[0]]
            }
        
        source_path = source_files[0]
        target_path = target_files[0]
        
        # Check if target imports from source
        target_deps = self.dependency_graph.get(target_path, {})
        
        if source_path not in target_deps.get('imports_from', []):
            return {
                'source_file': source_path,
                'target_file': target_path,
                'functions_used': [],
                'relationship': 'No direct dependency'
            }
        
        functions_used = target_deps.get('functions_used', {}).get(source_path, [])
        
        return {
            'source_file': source_path,
            'target_file': target_path,
            'functions_used': functions_used,
            'function_count': len(functions_used),
            'relationship': 'Direct dependency'
        }
    
    def query_circular_dependencies(self) -> Dict[str, Any]:
        """Show all circular dependencies in the codebase"""
        return {
            'circular_dependencies': self.circular_dependencies,
            'count': len(self.circular_dependencies),
            'affected_files': list(set(file for cycle in self.circular_dependencies for file in cycle))
        }
    
    def query_entry_points(self) -> Dict[str, Any]:
        """Find entry points (files with no dependencies or main files)"""
        entry_points = []
        
        for file_path, deps in self.dependency_graph.items():
            imports = deps.get('imports_from', [])
            
            # Files with no internal dependencies
            internal_imports = [imp for imp in imports if not imp.startswith('.') and '/' in imp]
            
            if not internal_imports or len(internal_imports) == 0:
                entry_points.append({
                    'file': file_path,
                    'reason': 'No internal dependencies'
                })
            
            # Check for main-like patterns
            filename = Path(file_path).name.lower()
            if filename in ['main.py', 'app.py', 'index.js', 'server.js', '__main__.py']:
                entry_points.append({
                    'file': file_path,
                    'reason': f'Main file pattern: {filename}'
                })
        
        return {
            'entry_points': entry_points,
            'count': len(entry_points)
        }
    
    def process_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process natural language dependency queries"""
        query_lower = query.lower().strip()
        
        # Parse common query patterns
        if re.search(r'what.*depend.*on.*(\S+)', query_lower):
            match = re.search(r'what.*depend.*on.*(\S+)', query_lower)
            target_file = match.group(1)
            return self.query_what_depends_on(target_file)
        
        elif re.search(r'what.*does.*(\S+).*depend', query_lower):
            match = re.search(r'what.*does.*(\S+).*depend', query_lower)
            source_file = match.group(1)
            return self.query_what_does_depend_on(source_file)
        
        elif 'dependency tree' in query_lower or 'dep tree' in query_lower:
            match = re.search(r'(?:for|of)\s+(\S+)', query_lower)
            if match:
                root_file = match.group(1)
                return self.query_dependency_tree(root_file)
        
        elif 'impact' in query_lower and 'change' in query_lower:
            match = re.search(r'(?:change|modify|edit)\s+(\S+)', query_lower)
            if match:
                target_file = match.group(1)
                return self.query_impact_analysis(target_file)
        
        elif 'circular' in query_lower:
            return self.query_circular_dependencies()
        
        elif 'entry point' in query_lower:
            return self.query_entry_points()
        
        else:
            return {
                'error': 'Query not recognized',
                'suggestion': 'Try queries like: "What depends on UserService?", "What does main.py depend on?", "Show me circular dependencies"'
            }


@click.command()
@click.argument('analysis_dir', type=click.Path(exists=True))
@click.option('--query', '-q', help='Natural language query about dependencies')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive query session')
@click.option('--examples', is_flag=True, help='Show query examples')
def main(analysis_dir, query, interactive, examples):
    """Interactive dependency query engine"""
    
    if examples:
        print("📝 Dependency Query Examples:")
        print("  • What files depend on UserService.py?")
        print("  • What does main.py depend on?")
        print("  • Show me the dependency tree for authentication")
        print("  • If I change DatabaseService, what else is affected?")
        print("  • What functions from utils.py are used by app.py?")
        print("  • Show me all circular dependencies")
        print("  • What are the entry points to the system?")
        return
    
    engine = DependencyQueryEngine()
    engine.load_analysis_data(analysis_dir)
    
    if not engine.loaded:
        print("❌ Could not load analysis data")
        return
    
    if query:
        # Single query mode
        result = engine.process_natural_language_query(query)
        print(json.dumps(result, indent=2))
    
    elif interactive:
        # Interactive mode
        print("🔍 Interactive Dependency Query Engine")
        print("Type 'help' for examples, 'quit' to exit\n")
        
        while True:
            try:
                user_query = input("🤔 Query: ").strip()
                
                if user_query.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_query.lower() in ['help', 'h']:
                    print("📝 Query Examples:")
                    print("  • What depends on UserService?")
                    print("  • What does main.py depend on?")
                    print("  • dependency tree for auth")
                    print("  • impact of changing DatabaseService")
                    print("  • circular dependencies")
                    print("  • entry points")
                    continue
                
                if not user_query:
                    continue
                
                result = engine.process_natural_language_query(user_query)
                print(json.dumps(result, indent=2))
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    else:
        # Generate query examples file
        examples_content = {
            'sample_queries': [
                'What files depend on UserService.py?',
                'What does main.py depend on?',
                'Show me the dependency tree for authentication',
                'If I change DatabaseService, what else is affected?',
                'What functions from utils.py are used by app.py?',
                'Show me all circular dependencies',
                'What are the entry points to the system?'
            ],
            'query_patterns': {
                'dependency_queries': [
                    'What depends on {filename}?',
                    'What does {filename} depend on?'
                ],
                'tree_queries': [
                    'dependency tree for {component}',
                    'Show dependencies of {filename}'
                ],
                'impact_queries': [
                    'If I change {filename}, what is affected?',
                    'Impact of modifying {filename}'
                ],
                'usage_queries': [
                    'What functions from {file1} are used by {file2}?',
                    'How is {filename} used?'
                ],
                'system_queries': [
                    'Show circular dependencies',
                    'What are the entry points?',
                    'Find main files'
                ]
            }
        }
        
        examples_file = Path(analysis_dir) / 'interactive' / 'query-examples.md'
        examples_file.parent.mkdir(exist_ok=True)
        
        with open(examples_file, 'w') as f:
            f.write("# Dependency Query Examples\n\n")
            f.write("## Sample Queries\n")
            for query in examples_content['sample_queries']:
                f.write(f"- {query}\n")
            
            f.write("\n## Query Patterns\n")
            for category, patterns in examples_content['query_patterns'].items():
                f.write(f"\n### {category.replace('_', ' ').title()}\n")
                for pattern in patterns:
                    f.write(f"- {pattern}\n")
        
        print(f"📝 Query examples saved to: {examples_file}")


if __name__ == '__main__':
    main()
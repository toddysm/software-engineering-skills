#!/usr/bin/env python3
"""
Source File Analysis Script - Deep understanding of individual source files
Extracts documentation, analyzes code structure, and determines file purpose
"""

import os
import ast
import json
import click
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
import logging


class SourceFileAnalyzer:
    """Analyzes individual source files for deep understanding"""
    
    def __init__(self):
        self.file_inventory = {}
        self.documentation_map = {}
        self.function_catalog = {}
        
    def analyze_all_files(self, project_path: str) -> Dict[str, Any]:
        """Analyze all source files in a project for deep understanding"""
        project_path = Path(project_path).resolve()
        
        # Find all source files
        source_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cs', '.cpp', '.cxx', 
                           '.cc', '.c', '.h', '.hpp', '.hxx', '.php', '.rb', '.go', '.rs', 
                           '.swift', '.kt', '.scala', '.clj', '.elm'}
        
        for root, dirs, files in os.walk(project_path):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 
                       'venv', 'build', 'dist', '.next', 'target'}]
            
            for file in files:
                if Path(file).suffix.lower() in source_extensions:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    try:
                        analysis = self.analyze_single_file(file_path, relative_path)
                        self.file_inventory[str(relative_path)] = analysis
                    except Exception as e:
                        logging.warning(f"Could not analyze {relative_path}: {e}")
        
        return {
            'file_inventory': self.file_inventory,
            'documentation_map': self.documentation_map,
            'function_catalog': self.function_catalog,
            'total_files': len(self.file_inventory)
        }
    
    def analyze_single_file(self, file_path: Path, relative_path: Path) -> Dict[str, Any]:
        """Deep analysis of a single source file"""
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        analysis = {
            'path': str(relative_path),
            'extension': file_path.suffix.lower(),
            'size_bytes': len(content.encode('utf-8')),
            'line_count': len(content.splitlines()),
            'documentation': self.extract_documentation(content, file_path.suffix),
            'purpose': self.determine_file_purpose(content, relative_path),
            'exports': self.extract_exports(content, file_path.suffix),
            'imports': self.extract_imports(content, file_path.suffix),
            'functions': self.extract_functions(content, file_path.suffix),
            'classes': self.extract_classes(content, file_path.suffix),
            'complexity_score': self.calculate_complexity(content),
            'responsibility': self.analyze_responsibility(content, relative_path)
        }
        
        # Store in documentation map for quick lookup
        self.documentation_map[str(relative_path)] = analysis['documentation']
        
        # Store functions in catalog for cross-reference
        if analysis['functions']:
            self.function_catalog[str(relative_path)] = analysis['functions']
            
        return analysis
    
    def extract_documentation(self, content: str, extension: str) -> Dict[str, Any]:
        """Extract all forms of documentation from file"""
        docs = {
            'file_docstring': None,
            'header_comments': [],
            'inline_comments': [],
            'todo_comments': [],
            'has_readme_style_header': False
        }
        
        lines = content.splitlines()
        
        if extension == '.py':
            # Python docstrings and comments
            try:
                tree = ast.parse(content)
                if (tree.body and isinstance(tree.body[0], ast.Expr) and 
                    isinstance(tree.body[0].value, ast.Constant) and 
                    isinstance(tree.body[0].value.value, str)):
                    docs['file_docstring'] = tree.body[0].value.value.strip()
                # Also extract function/class docstrings for overview
                docstrings = []
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        d = ast.get_docstring(node)
                        if d:
                            docstrings.append(f'{node.name}: {d[:80]}')
                docs['member_docstrings'] = docstrings[:10]  # Top 10 members
            except:
                pass
                
            # Extract comments
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('#'):
                    comment = stripped[1:].strip()
                    if i < 10:  # Header comments
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        elif extension == '.java':
            # Java Javadoc and comments
            in_javadoc = False
            current_javadoc = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('/**'):
                    in_javadoc = True
                    current_javadoc = []
                elif stripped.endswith('*/') and in_javadoc:
                    in_javadoc = False
                    doc_text = ' '.join(current_javadoc)
                    if i < 20:
                        docs['file_docstring'] = doc_text
                    else:
                        docs['inline_comments'].append(doc_text)
                    current_javadoc = []
                elif in_javadoc:
                    cleaned = re.sub(r'^\*\s*', '', stripped)
                    if cleaned:
                        current_javadoc.append(cleaned)
                elif stripped.startswith('//'):
                    comment = stripped[2:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            # JavaScript/TypeScript comments with JSDoc extraction
            in_jsdoc = False
            current_jsdoc = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('/**'):
                    in_jsdoc = True
                    current_jsdoc = []
                elif stripped.endswith('*/') and in_jsdoc:
                    in_jsdoc = False
                    doc_text = ' '.join(current_jsdoc)
                    if i < 20:
                        docs['file_docstring'] = doc_text
                    else:
                        docs['inline_comments'].append(doc_text)
                    current_jsdoc = []
                elif in_jsdoc:
                    cleaned = re.sub(r'^\*\s*', '', stripped)
                    if cleaned:
                        current_jsdoc.append(cleaned)
                elif stripped.startswith('//'):
                    comment = re.sub(r'^//\s*', '', stripped).strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        elif extension == '.rb':
            # Ruby comments
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('#'):
                    comment = stripped[1:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
            # Check for =begin ... =end documentation blocks
            content_rb = re.findall(r'=begin(.+?)=end', content, re.DOTALL)
            if content_rb:
                docs['file_docstring'] = content_rb[0].strip()
        
        elif extension == '.php':
            # PHP DocBlock and comments
            in_docblock = False
            current_docblock = []
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('/**'):
                    in_docblock = True
                    current_docblock = []
                elif stripped.endswith('*/') and in_docblock:
                    in_docblock = False
                    doc_text = ' '.join(current_docblock)
                    if i < 20:
                        docs['file_docstring'] = doc_text
                    else:
                        docs['inline_comments'].append(doc_text)
                    current_docblock = []
                elif in_docblock:
                    cleaned = re.sub(r'^\*\s*', '', stripped)
                    if cleaned:
                        current_docblock.append(cleaned)
                elif stripped.startswith('//'):
                    comment = stripped[2:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
                elif stripped.startswith('#'):
                    comment = stripped[1:].strip()
                    if 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        elif extension == '.go':
            # Go comments
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('//'):
                    comment = stripped[2:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
                elif stripped.startswith('/*') and stripped.endswith('*/'):
                    comment = re.sub(r'^/\*\s*|\s*\*/$', '', stripped)
                    docs['inline_comments'].append(comment)
        
        elif extension == '.rs':
            # Rust comments
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('///'):
                    comment = stripped[3:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
                elif stripped.startswith('//'):
                    comment = stripped[2:].strip()
                    if 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        elif extension in {'.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx'}:
            # C/C++ comments
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('//'):
                    comment = stripped[2:].strip()
                    if i < 10:
                        docs['header_comments'].append(comment)
                    elif 'todo' in comment.lower() or 'fixme' in comment.lower():
                        docs['todo_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
                elif stripped.startswith('/*') and '*/' in stripped:
                    comment = re.sub(r'/\*\s*|\s*\*/', '', stripped)
                    if i < 10:
                        docs['header_comments'].append(comment)
                    else:
                        docs['inline_comments'].append(comment)
        
        # Check for README-style header (multiple comment lines at top)
        if len(docs['header_comments']) >= 3:
            docs['has_readme_style_header'] = True
            
        return docs
    
    def determine_file_purpose(self, content: str, relative_path: Path) -> Dict[str, Any]:
        """Determine the primary purpose and role of this file"""
        
        path_str = str(relative_path).lower()
        filename = relative_path.name.lower()
        
        purpose = {
            'primary_role': 'unknown',
            'secondary_roles': [],
            'confidence': 0.0,
            'indicators': []
        }
        
        # Analyze path-based indicators
        if 'test' in path_str or filename.startswith('test_') or filename.endswith('.test.'):
            purpose['primary_role'] = 'test'
            purpose['confidence'] = 0.9
            purpose['indicators'].append('test file naming pattern')
        elif 'config' in path_str or 'settings' in path_str:
            purpose['primary_role'] = 'configuration'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('config/settings path')
        elif 'util' in path_str or 'helper' in path_str:
            purpose['primary_role'] = 'utility'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('utility/helper path')
        elif 'model' in path_str or 'schema' in path_str:
            purpose['primary_role'] = 'data_model'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('model/schema path')
        elif 'controller' in path_str or 'handler' in path_str:
            purpose['primary_role'] = 'controller'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('controller/handler path')
        elif 'service' in path_str:
            purpose['primary_role'] = 'service'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('service path')
        elif 'api' in path_str or 'endpoint' in path_str:
            purpose['primary_role'] = 'api'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('api/endpoint path')
        elif 'component' in path_str or 'view' in path_str:
            purpose['primary_role'] = 'ui_component'
            purpose['confidence'] = 0.8
            purpose['indicators'].append('component/view path')
            
        # Analyze content-based indicators
        content_lower = content.lower()
        
        # Look for specific patterns
        if re.search(r'class\s+\w*[Tt]est|def test_|it\(|describe\(|@test|#\[test\]', content):
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'test'
                purpose['confidence'] = 0.85
            purpose['indicators'].append('test class/function patterns')
        elif 'express(' in content_lower or "app.get('" in content_lower or '@app.route' in content_lower or '@get(' in content_lower or '@route(' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'web_server'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('web server route patterns')
        elif 'import react' in content_lower or 'from react' in content_lower or 'from \'react\'' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'react_component'
                purpose['confidence'] = 0.85
            purpose['indicators'].append('React import patterns')
        elif 'class.*model' in content_lower or 'sqlalchemy' in content_lower or 'activerecord::base' in content_lower or 'eloquent\\model' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'data_model'
                purpose['confidence'] = 0.85
            purpose['indicators'].append('data model / ORM patterns')
        elif re.search(r'\bif\s+__name__\s*==\s*["\']__main__["\']|\bpublic\s+static\s+void\s+main|\bfunc\s+main\(|\bfn\s+main\(|int\s+main\s*\(', content):
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'entry_point'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('main/entry-point function detected')
        elif 'gin.engine' in content_lower or 'http.servemux' in content_lower or 'http.newservemux' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'web_server'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('Go web server patterns')
        elif 'actix_web' in content_lower or 'warp::' in content_lower or 'rocket::' in content_lower or 'axum::' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'web_server'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('Rust web framework patterns')
        elif '#include <iostream>' in content_lower or '#include <stdio.h>' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'application'
                purpose['confidence'] = 0.8
            purpose['indicators'].append('C/C++ application patterns')
        elif 'using system;' in content_lower or ('namespace ' in content_lower and extension == '.cs'):
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'application'
                purpose['confidence'] = 0.8
            purpose['indicators'].append('C# namespace patterns')
        elif 'rails::application' in content_lower or 'actioncontroller::base' in content_lower or 'actionmailer::base' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'rails_component'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('Ruby on Rails patterns')
        elif '<?php' in content_lower or '<?=' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'php_script'
                purpose['confidence'] = 0.8
            purpose['indicators'].append('PHP script patterns')
        elif 'illuminate\\' in content_lower or 'laravel\\' in content_lower:
            if purpose['primary_role'] == 'unknown':
                purpose['primary_role'] = 'laravel_component'
                purpose['confidence'] = 0.9
            purpose['indicators'].append('Laravel framework patterns')
            
        # Special files
        special_files = {
            'main.py': 'entry_point',
            'app.py': 'application',
            'wsgi.py': 'application',
            'asgi.py': 'application',
            'manage.py': 'cli_entry_point',
            'settings.py': 'configuration',
            'urls.py': 'routing',
            'models.py': 'data_model',
            'views.py': 'controller',
            'serializers.py': 'data_serialization',
            'index.js': 'entry_point',
            'index.ts': 'entry_point',
            'server.js': 'web_server',
            'server.ts': 'web_server',
            'app.js': 'application',
            'app.ts': 'application',
            'main.go': 'entry_point',
            'main.rs': 'entry_point',
            'lib.rs': 'library',
            'mod.rs': 'module',
            'main.c': 'entry_point',
            'main.cpp': 'entry_point',
            'program.cs': 'entry_point',
            'startup.cs': 'application',
            'application.rb': 'application',
            'routes.rb': 'routing',
            'schema.rb': 'data_model',
            'gemfile': 'dependencies',
            'index.php': 'entry_point',
            'artisan': 'cli_entry_point',
            'package.json': 'configuration',
            'cargo.toml': 'configuration',
            'go.mod': 'configuration',
            'csproj': 'configuration',
            'makefile': 'build_script',
            'cmake': 'build_script',
            'requirements.txt': 'dependencies',
            'composer.json': 'dependencies',
            'dockerfile': 'deployment'
        }
        
        if filename in special_files:
            purpose['primary_role'] = special_files[filename]
            purpose['confidence'] = 0.95
            purpose['indicators'].append(f'special file: {filename}')
        
        return purpose
    
    def extract_exports(self, content: str, extension: str) -> List[str]:
        """Extract exported functions, classes, or variables"""
        exports = []
        
        if extension == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if not node.name.startswith('_'):  # Public functions/classes
                            exports.append(node.name)
            except:
                pass
                
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            # JavaScript/TypeScript exports
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('export '):
                    # Extract function/class names from export statements
                    match = re.search(r'export\s+(?:function|class|const|let|var)\s+(\w+)', line)
                    if match:
                        exports.append(match.group(1))
                elif line.startswith('module.exports'):
                    # CommonJS exports
                    match = re.search(r'module\.exports\s*=\s*(\w+)', line)
                    if match:
                        exports.append(match.group(1))
        
        elif extension == '.java':
            # Java public members
            for line in content.splitlines():
                stripped = line.strip()
                if 'public ' in stripped and not stripped.startswith('//') and not stripped.startswith('*'):
                    class_match = re.search(r'public\s+(?:class|interface|enum|record)\s+(\w+)', stripped)
                    if class_match:
                        exports.append(class_match.group(1))
                    method_match = re.search(r'public\s+(?:static\s+)?(?:\w+[\[\]]*)\s+(\w+)\s*\(', stripped)
                    if method_match and method_match.group(1) not in ('class', 'interface', 'enum'):
                        exports.append(method_match.group(1))
        
        elif extension == '.rb':
            # Ruby public methods and constants (uppercase = constant/class)
            for line in content.splitlines():
                stripped = line.strip()
                # Module/Class definitions
                mod_match = re.search(r'^(?:class|module)\s+([A-Z][\w:]*)', stripped)
                if mod_match:
                    exports.append(mod_match.group(1))
                # Constants
                const_match = re.search(r'^([A-Z_][A-Z0-9_]*)\s*=', stripped)
                if const_match:
                    exports.append(const_match.group(1))
                # Public method definitions
                def_match = re.search(r'^def\s+(\w+[?!]?)', stripped)
                if def_match and stripped.startswith('def '):
                    exports.append(def_match.group(1))
        
        elif extension == '.php':
            # PHP public members
            for line in content.splitlines():
                stripped = line.strip()
                if not stripped.startswith('//') and not stripped.startswith('*'):
                    class_match = re.search(r'(?:class|interface|trait|enum)\s+(\w+)', stripped)
                    if class_match:
                        exports.append(class_match.group(1))
                    pub_match = re.search(r'public\s+(?:static\s+)?function\s+(\w+)', stripped)
                    if pub_match:
                        exports.append(pub_match.group(1))
                    func_match = re.search(r'^function\s+(\w+)', stripped)
                    if func_match:
                        exports.append(func_match.group(1))
        
        elif extension == '.go':
            # Go exports (capitalized identifiers are public)
            for line in content.splitlines():
                line = line.strip()
                # Function exports
                func_match = re.search(r'func\s+([A-Z]\w*)', line)
                if func_match:
                    exports.append(func_match.group(1))
                # Type exports
                type_match = re.search(r'type\s+([A-Z]\w*)\s+', line)
                if type_match:
                    exports.append(type_match.group(1))
                # Var/const exports
                var_match = re.search(r'(?:var|const)\s+([A-Z]\w*)', line)
                if var_match:
                    exports.append(var_match.group(1))
        
        elif extension == '.rs':
            # Rust exports (pub items)
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('pub '):
                    # Extract function/struct/enum names
                    match = re.search(r'pub\s+(?:fn|struct|enum|const|static)\s+(\w+)', line)
                    if match:
                        exports.append(match.group(1))
        
        elif extension in {'.c', '.h'}:
            # C exports (functions and global variables in headers)
            if extension == '.h':  # Header files typically contain exports
                for line in content.splitlines():
                    line = line.strip()
                    # Function declarations
                    func_match = re.search(r'\w+\s+(\w+)\s*\([^)]*\)\s*;', line)
                    if func_match and not line.startswith('static'):
                        exports.append(func_match.group(1))
        
        elif extension in {'.cpp', '.cxx', '.cc', '.hpp', '.hxx'}:
            # C++ exports
            if extension in {'.hpp', '.hxx'}:  # Header files
                for line in content.splitlines():
                    line = line.strip()
                    # Class declarations
                    class_match = re.search(r'class\s+(\w+)', line)
                    if class_match and not line.startswith('//') and 'public:' not in line:
                        exports.append(class_match.group(1))
                    # Function declarations
                    func_match = re.search(r'\w+\s+(\w+)\s*\([^)]*\)\s*;', line)
                    if func_match and not line.startswith('static') and not line.startswith('private'):
                        exports.append(func_match.group(1))
        
        elif extension == '.cs':
            # C# exports (public members)
            for line in content.splitlines():
                line = line.strip()
                if 'public ' in line:
                    # Classes
                    class_match = re.search(r'public\s+class\s+(\w+)', line)
                    if class_match:
                        exports.append(class_match.group(1))
                    # Methods
                    method_match = re.search(r'public\s+\w+\s+(\w+)\s*\(', line)
                    if method_match:
                        exports.append(method_match.group(1))
        
        return list(set(exports))  # Remove duplicates
    
    def extract_imports(self, content: str, extension: str) -> Dict[str, List[str]]:
        """Extract imported modules and dependencies"""
        imports = {
            'internal': [],  # Local project files
            'external': [],  # Third-party packages
            'standard': []   # Standard library
        }
        
        if extension == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports['external'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            if node.module.startswith('.'):
                                imports['internal'].append(node.module)
                            else:
                                imports['external'].append(node.module)
            except:
                pass
                
        elif extension == '.java':
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith('import '):
                    match = re.search(r'import\s+(?:static\s+)?([^;]+);', stripped)
                    if match:
                        fqn = match.group(1)
                        # Heuristic: if starts with common std library packages
                        std_prefixes = ('java.', 'javax.', 'sun.', 'com.sun.')
                        if fqn.startswith(std_prefixes):
                            imports['standard'].append(fqn)
                        elif fqn.startswith('.'):
                            imports['internal'].append(fqn)
                        else:
                            imports['external'].append(fqn)
        
        elif extension == '.rb':
            for line in content.splitlines():
                stripped = line.strip()
                # require and require_relative
                req_match = re.search(r"require_relative\s+['\"](.+)['\"]", stripped)
                if req_match:
                    imports['internal'].append(req_match.group(1))
                else:
                    req_match = re.search(r"require\s+['\"](.+)['\"]", stripped)
                    if req_match:
                        module = req_match.group(1)
                        # Stdlib modules are usually simple names without slashes
                        std_gems = {'json', 'yaml', 'csv', 'net/http', 'uri', 'date', 'time', 
                                    'fileutils', 'pathname', 'open-uri', 'logger', 'ostruct'}
                        if module in std_gems or module.startswith('net/'):
                            imports['standard'].append(module)
                        elif module.startswith('./'):
                            imports['internal'].append(module)
                        else:
                            imports['external'].append(module)
                # include and extend (mixins)
                mixin_match = re.search(r'^(?:include|extend|prepend)\s+(\w[\w:]*)', stripped)
                if mixin_match:
                    imports['external'].append(mixin_match.group(1))
        
        elif extension == '.php':
            for line in content.splitlines():
                stripped = line.strip()
                # use statements
                use_match = re.search(r'^use\s+([^;]+);', stripped)
                if use_match:
                    fqn = use_match.group(1).split(' as ')[0].strip()
                    if fqn.startswith('\\'):
                        fqn = fqn[1:]
                    imports['external'].append(fqn)
                # require / include
                inc_match = re.search(r"(?:require|include)(?:_once)?\s*[('\"](.*?)['\"]", stripped)
                if inc_match:
                    imports['internal'].append(inc_match.group(1))
        
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            for line in content.splitlines():
                line = line.strip()
                # ES6 imports
                match = re.search(r"import.*from\s+['\"](.+)['\"]", line)
                if match:
                    module = match.group(1)
                    if module.startswith('./') or module.startswith('../'):
                        imports['internal'].append(module)
                    else:
                        imports['external'].append(module)
                # require statements
                match = re.search(r"require\s*\(\s*['\"](.+)['\"]\s*\)", line)
                if match:
                    module = match.group(1)
                    if module.startswith('./') or module.startswith('../'):
                        imports['internal'].append(module)
                    else:
                        imports['external'].append(module)
        
        elif extension == '.go':
            for line in content.splitlines():
                line = line.strip()
                # Single import
                single_match = re.search(r'import\s+"([^"]+)"', line)
                if single_match:
                    module = single_match.group(1)
                    if '/' in module and not module.startswith('.'):
                        imports['external'].append(module)
                    else:
                        imports['internal'].append(module)
                # Multi-line import block
                if line.startswith('import ('):
                    # This would need more complex parsing for full support
                    pass
        
        elif extension == '.rs':
            for line in content.splitlines():
                line = line.strip()
                # use statements
                use_match = re.search(r'use\s+([^;]+);', line)
                if use_match:
                    module = use_match.group(1)
                    if module.startswith('crate::') or module.startswith('super::') or module.startswith('self::'):
                        imports['internal'].append(module)
                    elif module.startswith('std::'):
                        imports['standard'].append(module)
                    else:
                        imports['external'].append(module)
        
        elif extension in {'.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx'}:
            for line in content.splitlines():
                line = line.strip()
                # #include statements
                include_match = re.search(r'#include\s*[<"]([^>"]+)[>"]', line)
                if include_match:
                    header = include_match.group(1)
                    if line.find('<') != -1:  # System headers
                        imports['standard'].append(header)
                    else:  # Local headers
                        imports['internal'].append(header)
        
        elif extension == '.cs':
            for line in content.splitlines():
                line = line.strip()
                # using statements
                using_match = re.search(r'using\s+([^;]+);', line)
                if using_match:
                    namespace = using_match.group(1)
                    if namespace.startswith('System'):
                        imports['standard'].append(namespace)
                    elif '.' in namespace:
                        imports['external'].append(namespace)
                    else:
                        imports['internal'].append(namespace)
        
        return imports
    
    def extract_functions(self, content: str, extension: str) -> List[Dict[str, str]]:
        """Extract function definitions with documentation"""
        functions = []
        
        if extension == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        func_doc = ast.get_docstring(node) or "No documentation"
                        # Extract decorator names
                        decorators = []
                        for d in node.decorator_list:
                            if isinstance(d, ast.Name):
                                decorators.append(d.id)
                            elif isinstance(d, ast.Attribute):
                                decorators.append(f'{d.value.id}.{d.attr}' if isinstance(d.value, ast.Name) else d.attr)
                        # Extract argument names and type annotations
                        args = [a.arg for a in node.args.args]
                        returns = None
                        if node.returns and isinstance(node.returns, ast.Name):
                            returns = node.returns.id
                        functions.append({
                            'name': node.name,
                            'line': node.lineno,
                            'doc': func_doc,
                            'is_public': not node.name.startswith('_'),
                            'is_async': isinstance(node, ast.AsyncFunctionDef),
                            'decorators': decorators,
                            'args': args,
                            'returns': returns
                        })
            except:
                pass
        
        elif extension == '.java':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                # Java method declarations
                method_match = re.search(
                    r'(public|private|protected|package)?\s*(?:static\s+)?(?:\w+[\[\]<>]*\s+)+(\w+)\s*\([^)]*\)\s*(?:throws\s+\w+\s*)?[{;]',
                    stripped
                )
                if method_match and not stripped.startswith('//') and not stripped.startswith('*'):
                    access = method_match.group(1) or 'package'
                    method_name = method_match.group(2)
                    if method_name not in ('if', 'for', 'while', 'switch', 'catch', 'class'):
                        doc = "No documentation"
                        # Look for Javadoc above
                        j = i - 1
                        while j >= 0 and lines[j].strip().startswith('*'):
                            j -= 1
                        if j >= 0 and lines[j].strip().startswith('/**'):
                            block = ' '.join(lines[j+1:i])
                            doc = re.sub(r'[/*@]', '', block).strip()[:120]
                        # Also check single-line comment
                        elif i > 0 and lines[i-1].strip().startswith('//'):
                            doc = lines[i-1].strip()[2:].strip()
                        # Extract annotations
                        annotations = []
                        k = i - 1
                        while k >= 0 and lines[k].strip().startswith('@'):
                            annotations.append(lines[k].strip()[1:])
                            k -= 1
                        functions.append({
                            'name': method_name,
                            'line': i + 1,
                            'doc': doc,
                            'is_public': access == 'public',
                            'annotations': annotations
                        })
        
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                doc = "No documentation"
                # Look for JSDoc comment above
                if i > 0:
                    prev = lines[i-1].strip()
                    if prev.endswith('*/'):
                        # Collect the JSDoc block
                        j = i - 1
                        while j >= 0 and not lines[j].strip().startswith('/**'):
                            j -= 1
                        if j >= 0:
                            block = ' '.join(lines[j+1:i])
                            doc = re.sub(r'[/*@]\w*', '', block).strip()[:120]
                    elif prev.startswith('//'):
                        doc = prev[2:].strip()
                
                # Function declarations
                match = re.search(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*(?:<[^>]*>)?\s*\(', line)
                if match:
                    functions.append({
                        'name': match.group(1),
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'export' in line,
                        'is_async': 'async ' in line
                    })
                    continue
                
                # Arrow functions / const methods
                match = re.search(r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(', line)
                if match and '=>' in line:
                    functions.append({
                        'name': match.group(1),
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'export' in line,
                        'is_async': 'async ' in line
                    })
                    continue
                
                # Class method declarations (TypeScript/JS classes)
                match = re.search(r'^\s*(?:public|private|protected|static|async|\s)*(?:async\s+)?(\w+)\s*(?:<[^>]*>)?\s*\([^)]*\)\s*(?::\s*\w+[\w<>\[\]|&]*)?\s*\{', line)
                if match and match.group(1) not in ('if', 'for', 'while', 'switch', 'catch', 'class', 'constructor'):
                    functions.append({
                        'name': match.group(1),
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'private' not in line,
                        'is_async': 'async ' in line
                    })
        
        elif extension == '.rb':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                def_match = re.search(r'^def\s+(self\.)?(\w+[?!]?)\s*(?:\(.*\))?$', stripped)
                if def_match:
                    method_name = def_match.group(2)
                    is_class_method = bool(def_match.group(1))
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('#'):
                        doc = lines[i-1].strip()[1:].strip()
                    functions.append({
                        'name': method_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': True,
                        'is_class_method': is_class_method
                    })
        
        elif extension == '.php':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                func_match = re.search(
                    r'(public|private|protected)?\s*(?:static\s+)?function\s+(\w+)\s*\(', stripped
                )
                if func_match:
                    access = func_match.group(1) or 'public'
                    func_name = func_match.group(2)
                    doc = "No documentation"
                    # Collect PHPDoc above
                    j = i - 1
                    while j >= 0 and lines[j].strip().startswith('*'):
                        j -= 1
                    if j >= 0 and lines[j].strip().startswith('/**'):
                        block = ' '.join(lines[j+1:i])
                        doc = re.sub(r'[/*@]\w*', '', block).strip()[:120]
                    elif i > 0 and lines[i-1].strip().startswith('//'):
                        doc = lines[i-1].strip()[2:].strip()
                    functions.append({
                        'name': func_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': access != 'private'
                    })
        
        elif extension == '.go':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Function declarations
                func_match = re.search(r'func\s+(\w*)\s*(\w+)\s*\(', line)
                if func_match:
                    receiver = func_match.group(1) or ""
                    func_name = func_match.group(2)
                    doc = "No documentation"
                    # Look for comment above function
                    if i > 0 and lines[i-1].strip().startswith('//'):
                        doc = lines[i-1].strip()[2:].strip()
                    functions.append({
                        'name': func_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': func_name[0].isupper(),
                        'receiver': receiver
                    })
        
        elif extension == '.rs':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Function declarations
                func_match = re.search(r'(?:pub\s+)?fn\s+(\w+)\s*\(', line)
                if func_match:
                    func_name = func_match.group(1)
                    doc = "No documentation"
                    # Look for doc comment above function
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    functions.append({
                        'name': func_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'pub ' in line
                    })
        
        elif extension in {'.c', '.cpp', '.cxx', '.cc', '.h', '.hpp', '.hxx'}:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Function declarations/definitions
                func_match = re.search(r'\b(\w+)\s+(\w+)\s*\([^)]*\)\s*[{;]', line)
                if func_match and not line.strip().startswith('//'):
                    return_type = func_match.group(1)
                    func_name = func_match.group(2)
                    # Skip common C++ keywords
                    if return_type not in ['if', 'for', 'while', 'switch', 'class', 'struct']:
                        doc = "No documentation"
                        # Look for comment above function
                        if i > 0 and ('//' in lines[i-1] or '/*' in lines[i-1]):
                            doc = re.sub(r'[/*]+', '', lines[i-1]).strip()
                        functions.append({
                            'name': func_name,
                            'line': i + 1,
                            'doc': doc,
                            'is_public': not line.strip().startswith('static'),
                            'return_type': return_type
                        })
        
        elif extension == '.cs':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Method declarations
                method_match = re.search(r'(public|private|protected|internal)?\s+\w+\s+(\w+)\s*\(', line)
                if method_match and 'class ' not in line:
                    access_modifier = method_match.group(1) or 'private'
                    method_name = method_match.group(2)
                    doc = "No documentation"
                    # Look for XML doc comment
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    functions.append({
                        'name': method_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': access_modifier == 'public'
                    })
        
        return functions
    
    def extract_classes(self, content: str, extension: str) -> List[Dict[str, str]]:
        """Extract class definitions with documentation"""
        classes = []
        
        if extension == '.py':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_doc = ast.get_docstring(node) or "No documentation"
                        # Extract base classes
                        bases = []
                        for base in node.bases:
                            if isinstance(base, ast.Name):
                                bases.append(base.id)
                            elif isinstance(base, ast.Attribute):
                                bases.append(f'{base.value.id}.{base.attr}' if isinstance(base.value, ast.Name) else base.attr)
                        # Extract decorators
                        decorators = []
                        for d in node.decorator_list:
                            if isinstance(d, ast.Name):
                                decorators.append(d.id)
                            elif isinstance(d, ast.Attribute):
                                decorators.append(d.attr)
                        classes.append({
                            'name': node.name,
                            'line': node.lineno,
                            'doc': class_doc,
                            'is_public': not node.name.startswith('_'),
                            'bases': bases,
                            'decorators': decorators
                        })
            except:
                pass
        
        elif extension == '.java':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('*'):
                    continue
                class_match = re.search(
                    r'(public|private|protected)?\s*(?:abstract\s+|final\s+)?(?:class|interface|enum|record)\s+(\w+)\s*(?:<[^>]*>)?\s*(?:extends\s+(\w+))?\s*(?:implements\s+([^{]+))?',
                    stripped
                )
                if class_match:
                    access = class_match.group(1) or 'package'
                    class_name = class_match.group(2)
                    extends = class_match.group(3)
                    implements_raw = class_match.group(4)
                    implements = [x.strip() for x in implements_raw.split(',')] if implements_raw else []
                    doc = "No documentation"
                    # Look for Javadoc block above
                    j = i - 1
                    while j >= 0 and lines[j].strip().startswith('*'):
                        j -= 1
                    if j >= 0 and lines[j].strip().startswith('/**'):
                        block = ' '.join(lines[j+1:i])
                        doc = re.sub(r'[/*@]\w*', '', block).strip()[:200]
                    # Extract annotations
                    annotations = []
                    k = i - 1
                    while k >= 0 and lines[k].strip().startswith('@'):
                        annotations.append(lines[k].strip()[1:])
                        k -= 1
                    classes.append({
                        'name': class_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': access == 'public',
                        'extends': extends,
                        'implements': implements,
                        'annotations': annotations
                    })
        
        elif extension in {'.js', '.jsx', '.ts', '.tsx'}:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # class declarations and TypeScript interfaces/types
                class_match = re.search(r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?', line)
                if class_match and not line.strip().startswith('//'):
                    doc = "No documentation"
                    if i > 0:
                        prev = lines[i-1].strip()
                        if prev.endswith('*/'):
                            j = i - 1
                            while j >= 0 and not lines[j].strip().startswith('/**'):
                                j -= 1
                            block = ' '.join(lines[j+1:i])
                            doc = re.sub(r'[/*@]\w*', '', block).strip()[:200]
                        elif prev.startswith('//'):
                            doc = prev[2:].strip()
                    classes.append({
                        'name': class_match.group(1),
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'export' in line,
                        'extends': class_match.group(2),
                        'implements': [x.strip() for x in class_match.group(3).split(',')] if class_match.group(3) else []
                    })
                # TypeScript interface declarations
                iface_match = re.search(r'(?:export\s+)?interface\s+(\w+)', line)
                if iface_match and not line.strip().startswith('//'):
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('//'):
                        doc = lines[i-1].strip()[2:].strip()
                    classes.append({
                        'name': iface_match.group(1),
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'export' in line,
                        'kind': 'interface'
                    })
                # TypeScript type alias
                type_match = re.search(r'(?:export\s+)?type\s+(\w+)\s*(?:<[^>]*>)?\s*=', line)
                if type_match and not line.strip().startswith('//'):
                    classes.append({
                        'name': type_match.group(1),
                        'line': i + 1,
                        'doc': "No documentation",
                        'is_public': 'export' in line,
                        'kind': 'type_alias'
                    })
        
        elif extension == '.rb':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                mod_match = re.search(r'^(class|module)\s+([A-Z][\w:]*)\s*(?:<\s*(\w[\w:]*))?', stripped)
                if mod_match:
                    kind = mod_match.group(1)
                    name = mod_match.group(2)
                    parent = mod_match.group(3)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('#'):
                        doc = lines[i-1].strip()[1:].strip()
                    classes.append({
                        'name': name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': True,
                        'kind': kind,
                        'extends': parent
                    })
        
        elif extension == '.php':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('*'):
                    continue
                class_match = re.search(
                    r'(?:abstract\s+|final\s+)?(?:class|interface|trait|enum)\s+(\w+)\s*(?:extends\s+(\w+))?\s*(?:implements\s+([^{]+))?',
                    stripped
                )
                if class_match:
                    class_name = class_match.group(1)
                    extends = class_match.group(2)
                    implements_raw = class_match.group(3)
                    implements = [x.strip() for x in implements_raw.split(',')] if implements_raw else []
                    doc = "No documentation"
                    j = i - 1
                    while j >= 0 and lines[j].strip().startswith('*'):
                        j -= 1
                    if j >= 0 and lines[j].strip().startswith('/**'):
                        block = ' '.join(lines[j+1:i])
                        doc = re.sub(r'[/*@]\w*', '', block).strip()[:200]
                    # Extract PHP attributes (#[...])
                    attrs = []
                    k = i - 1
                    while k >= 0 and lines[k].strip().startswith('#['):
                        attrs.append(lines[k].strip())
                        k -= 1
                    classes.append({
                        'name': class_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': True,
                        'extends': extends,
                        'implements': implements,
                        'attributes': attrs
                    })
        
        elif extension == '.go':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Struct declarations
                struct_match = re.search(r'type\s+(\w+)\s+struct', line)
                if struct_match:
                    struct_name = struct_match.group(1)
                    doc = "No documentation"
                    # Look for comment above struct
                    if i > 0 and lines[i-1].strip().startswith('//'):
                        doc = lines[i-1].strip()[2:].strip()
                    classes.append({
                        'name': struct_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': struct_name[0].isupper()
                    })
                # Interface declarations
                interface_match = re.search(r'type\s+(\w+)\s+interface', line)
                if interface_match:
                    interface_name = interface_match.group(1)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('//'):
                        doc = lines[i-1].strip()[2:].strip()
                    classes.append({
                        'name': interface_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': interface_name[0].isupper()
                    })
        
        elif extension == '.rs':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Struct declarations
                struct_match = re.search(r'(?:pub\s+)?struct\s+(\w+)', line)
                if struct_match:
                    struct_name = struct_match.group(1)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    classes.append({
                        'name': struct_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'pub ' in line
                    })
                # Enum declarations
                enum_match = re.search(r'(?:pub\s+)?enum\s+(\w+)', line)
                if enum_match:
                    enum_name = enum_match.group(1)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    classes.append({
                        'name': enum_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'pub ' in line
                    })
                # Trait declarations
                trait_match = re.search(r'(?:pub\s+)?trait\s+(\w+)', line)
                if trait_match:
                    trait_name = trait_match.group(1)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    classes.append({
                        'name': trait_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': 'pub ' in line
                    })
        
        elif extension in {'.cpp', '.cxx', '.cc', '.hpp', '.hxx'}:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Class declarations
                class_match = re.search(r'class\s+(\w+)', line)
                if class_match and not line.strip().startswith('//'):
                    class_name = class_match.group(1)
                    doc = "No documentation"
                    if i > 0 and ('//' in lines[i-1] or '/*' in lines[i-1]):
                        doc = re.sub(r'[/*]+', '', lines[i-1]).strip()
                    classes.append({
                        'name': class_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': True
                    })
                # Struct declarations
                struct_match = re.search(r'struct\s+(\w+)', line)
                if struct_match and not line.strip().startswith('//'):
                    struct_name = struct_match.group(1)
                    doc = "No documentation"
                    if i > 0 and ('//' in lines[i-1] or '/*' in lines[i-1]):
                        doc = re.sub(r'[/*]+', '', lines[i-1]).strip()
                    classes.append({
                        'name': struct_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': True
                    })
        
        elif extension == '.cs':
            lines = content.splitlines()
            for i, line in enumerate(lines):
                # Class declarations
                class_match = re.search(r'(public|private|protected|internal)?\s+class\s+(\w+)', line)
                if class_match:
                    access_modifier = class_match.group(1) or 'internal'
                    class_name = class_match.group(2)
                    doc = "No documentation"
                    # Look for XML doc comment
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    classes.append({
                        'name': class_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': access_modifier == 'public'
                    })
                # Interface declarations
                interface_match = re.search(r'(public|private|protected|internal)?\s+interface\s+(\w+)', line)
                if interface_match:
                    access_modifier = interface_match.group(1) or 'internal'
                    interface_name = interface_match.group(2)
                    doc = "No documentation"
                    if i > 0 and lines[i-1].strip().startswith('///'):
                        doc = lines[i-1].strip()[3:].strip()
                    classes.append({
                        'name': interface_name,
                        'line': i + 1,
                        'doc': doc,
                        'is_public': access_modifier == 'public'
                    })
        
        return classes
    
    def calculate_complexity(self, content: str) -> int:
        """Calculate a simple complexity score for the file"""
        lines = content.splitlines()
        
        complexity_indicators = [
            'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except:', 
            'switch', 'case:', 'catch', '? ' # ternary
        ]
        
        score = 0
        for line in lines:
            line_lower = line.lower()
            for indicator in complexity_indicators:
                if indicator in line_lower:
                    score += 1
        
        return score
    
    def analyze_responsibility(self, content: str, relative_path: Path) -> Dict[str, Any]:
        """Analyze the single responsibility and cohesion of the file"""
        
        # Count different types of definitions
        function_count = content.count('def ') + content.count('function ')
        class_count = content.count('class ')
        
        responsibility = {
            'single_responsibility_score': 1.0,
            'cohesion_indicators': [],
            'concerns': []
        }
        
        # Check for multiple responsibilities
        if function_count > 20:
            responsibility['single_responsibility_score'] *= 0.7
            responsibility['concerns'].append('High function count may indicate multiple responsibilities')
        
        if class_count > 5:
            responsibility['single_responsibility_score'] *= 0.8
            responsibility['concerns'].append('Multiple classes may indicate mixed concerns')
        
        # Look for mixed concerns in content
        content_lower = content.lower()
        concern_patterns = {
            'database': ['sql', 'query', 'database', 'db.', 'select ', 'insert ', 'update ', 'delete '],
            'ui': ['render', 'component', 'jsx', 'html', 'css', 'style'],
            'api': ['request', 'response', 'http', 'api', 'endpoint', 'route'],
            'business_logic': ['calculate', 'process', 'validate', 'transform'],
            'auth': ['login', 'logout', 'auth', 'permission', 'password', 'token'],
            'logging': ['log', 'debug', 'info', 'warn', 'error'],
        }
        
        detected_concerns = []
        for concern, patterns in concern_patterns.items():
            if any(pattern in content_lower for pattern in patterns):
                detected_concerns.append(concern)
        
        responsibility['detected_concerns'] = detected_concerns
        
        if len(detected_concerns) > 2:
            responsibility['single_responsibility_score'] *= 0.6
            responsibility['concerns'].append('Multiple concerns detected: ' + ', '.join(detected_concerns))
        elif len(detected_concerns) <= 1:
            responsibility['cohesion_indicators'].append('Single concern detected' if detected_concerns else 'Minimal mixed concerns')
        
        return responsibility


@click.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='Output directory for analysis results')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(project_path, output, verbose):
    """Analyze all source files in a project for deep understanding"""
    
    if verbose:
        logging.basicConfig(level=logging.INFO)
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    analyzer = SourceFileAnalyzer()
    
    print(f"🔍 Analyzing source files in: {project_path}")
    results = analyzer.analyze_all_files(project_path)
    
    # Save file inventory
    inventory_file = output_path / 'file-inventory.json'
    with open(inventory_file, 'w') as f:
        json.dump(results['file_inventory'], f, indent=2)
    print(f"📋 File inventory saved to: {inventory_file}")
    
    # Save documentation map
    docs_file = output_path / 'documentation-map.json'
    with open(docs_file, 'w') as f:
        json.dump(results['documentation_map'], f, indent=2)
    print(f"📚 Documentation map saved to: {docs_file}")
    
    # Save function catalog
    functions_file = output_path / 'function-catalog.json'
    with open(functions_file, 'w') as f:
        json.dump(results['function_catalog'], f, indent=2)
    print(f"🔧 Function catalog saved to: {functions_file}")
    
    # Create individual file analysis directory
    file_analysis_dir = output_path / 'file-analysis'
    file_analysis_dir.mkdir(exist_ok=True)
    
    for file_path, analysis in results['file_inventory'].items():
        safe_filename = file_path.replace('/', '_').replace('\\', '_').replace('.', '_') + '.json'
        analysis_file = file_analysis_dir / safe_filename
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
    
    print(f"📁 Individual file analyses saved to: {file_analysis_dir}")
    print(f"✅ Analyzed {results['total_files']} source files successfully")


if __name__ == '__main__':
    main()
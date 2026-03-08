#!/usr/bin/env python3
"""
Pattern Detection Script for Codebase Architecture Analyst

This script analyzes a codebase to detect common architectural patterns,
design patterns, and code organization structures.
"""

import os
import re
import json
import itertools
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter

class PatternDetector:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.patterns_found = defaultdict(list)
        self.architecture_style = None
        self.framework_info = {}
        
    def detect_patterns(self) -> Dict:
        """Detect all patterns in the codebase."""
        self._detect_project_structure()
        self._detect_frameworks()
        self._detect_architectural_patterns()
        self._detect_security_patterns()
        self._detect_performance_patterns()
        
        return {
            'architecture_style': self.architecture_style,
            'framework_info': self.framework_info,
            'patterns': dict(self.patterns_found)
        }
    
    def _detect_project_structure(self):
        """Analyze project structure to infer architecture style."""
        directories = set()
        files = []
        
        for item in self.project_root.rglob('*'):
            if item.is_dir():
                directories.add(item.name.lower())
            else:
                files.append(item)
        
        # Detect microservices architecture
        if any('docker-compose' in f.name for f in files) or len([d for d in directories if d in ['services', 'microservices']]) > 0:
            self.architecture_style = 'microservices'
            self.patterns_found['architectural'].append({
                'type': 'Microservices Architecture',
                'confidence': 'high',
                'evidence': 'Docker compose files and/or services directory structure'
            })
        
        # Detect layered architecture
        layer_indicators = {'controllers', 'services', 'models', 'repositories', 'views'}
        if len(directories.intersection(layer_indicators)) >= 3:
            if not self.architecture_style:
                self.architecture_style = 'layered'
            self.patterns_found['architectural'].append({
                'type': 'Layered Architecture',
                'confidence': 'high',
                'evidence': f'Layer directories found: {directories.intersection(layer_indicators)}'
            })
        
        # Detect MVC pattern
        mvc_indicators = {'models', 'views', 'controllers'}
        if mvc_indicators.issubset(directories):
            self.patterns_found['architectural'].append({
                'type': 'Model-View-Controller (MVC)',
                'confidence': 'high',
                'evidence': 'MVC directory structure present'
            })
    
    def _detect_frameworks(self):
        """Detect frameworks and technologies used."""
        # Check package files
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            self._analyze_package_json(package_json)
        
        requirements_txt = self.project_root / 'requirements.txt'
        if requirements_txt.exists():
            self._analyze_python_requirements(requirements_txt)
        
        pom_xml = self.project_root / 'pom.xml'
        if pom_xml.exists():
            self._analyze_maven_pom(pom_xml)
            
        # Detect by file extensions and patterns
        self._detect_by_file_patterns()
    
    def _analyze_package_json(self, package_json_path: Path):
        """Analyze package.json for JavaScript frameworks."""
        try:
            with open(package_json_path, 'r') as f:
                data = json.load(f)
            
            dependencies = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            
            # Frontend frameworks
            if 'react' in dependencies:
                self.framework_info['frontend'] = 'React'
                self.patterns_found['framework'].append({
                    'type': 'React Framework',
                    'version': dependencies.get('react'),
                    'confidence': 'high'
                })
                
                # React-specific patterns
                if '@reduxjs/toolkit' in dependencies or 'redux' in dependencies:
                    self.patterns_found['state_management'].append({
                        'type': 'Redux State Management',
                        'confidence': 'high'
                    })
                    
                if 'react-router' in dependencies or 'react-router-dom' in dependencies:
                    self.patterns_found['routing'].append({
                        'type': 'React Router',
                        'confidence': 'high'
                    })
            
            if 'vue' in dependencies:
                self.framework_info['frontend'] = 'Vue.js'
                self.patterns_found['framework'].append({
                    'type': 'Vue.js Framework',
                    'version': dependencies.get('vue'),
                    'confidence': 'high'
                })
            
            if '@angular/core' in dependencies:
                self.framework_info['frontend'] = 'Angular'
                self.patterns_found['framework'].append({
                    'type': 'Angular Framework',
                    'version': dependencies.get('@angular/core'),
                    'confidence': 'high'
                })
            
            # Backend frameworks
            if 'express' in dependencies:
                self.framework_info['backend'] = 'Express.js'
                self.patterns_found['framework'].append({
                    'type': 'Express.js Backend',
                    'version': dependencies.get('express'),
                    'confidence': 'high'
                })
            
            if 'next' in dependencies:
                self.framework_info['fullstack'] = 'Next.js'
                self.patterns_found['framework'].append({
                    'type': 'Next.js Full-stack',
                    'version': dependencies.get('next'),
                    'confidence': 'high'
                })
                
        except Exception as e:
            print(f"Error analyzing package.json: {e}")
    
    def _analyze_python_requirements(self, requirements_path: Path):
        """Analyze Python requirements for frameworks."""
        try:
            with open(requirements_path, 'r') as f:
                content = f.read()
            
            # Extract package names
            packages = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    package = re.split(r'[>=<!\s]', line)[0]
                    if package:
                        packages.append(package.lower())
            
            # Detect frameworks
            if 'django' in packages:
                self.framework_info['backend'] = 'Django'
                self.patterns_found['framework'].append({
                    'type': 'Django Framework',
                    'confidence': 'high'
                })
            
            if 'flask' in packages:
                self.framework_info['backend'] = 'Flask'
                self.patterns_found['framework'].append({
                    'type': 'Flask Framework',
                    'confidence': 'high'
                })
            
            if 'fastapi' in packages:
                self.framework_info['backend'] = 'FastAPI'
                self.patterns_found['framework'].append({
                    'type': 'FastAPI Framework',
                    'confidence': 'high'
                })
                
        except Exception as e:
            print(f"Error analyzing requirements.txt: {e}")
    
    def _analyze_maven_pom(self, pom_path: Path):
        """Analyze Maven pom.xml for Java frameworks."""
        try:
            with open(pom_path, 'r') as f:
                content = f.read()
            
            if 'spring-boot' in content:
                self.framework_info['backend'] = 'Spring Boot'
                self.patterns_found['framework'].append({
                    'type': 'Spring Boot Framework',
                    'confidence': 'high'
                })
                
        except Exception as e:
            print(f"Error analyzing pom.xml: {e}")
    
    def _detect_by_file_patterns(self):
        """Detect patterns by analyzing file names and extensions."""
        files = list(self.project_root.rglob('*'))
        
        # Count file types
        extensions = Counter([f.suffix.lower() for f in files if f.is_file()])
        
        # Detect primary languages
        if extensions.get('.py', 0) > 0:
            self.framework_info['language'] = 'Python'
        elif extensions.get('.js', 0) + extensions.get('.ts', 0) > 0:
            self.framework_info['language'] = 'JavaScript/TypeScript'
        elif extensions.get('.java', 0) > 0:
            self.framework_info['language'] = 'Java'
        elif extensions.get('.cs', 0) > 0:
            self.framework_info['language'] = 'C#'
        
        # Detect containerization
        docker_files = [f for f in files if 'dockerfile' in f.name.lower() or f.name == 'docker-compose.yml']
        if docker_files:
            self.patterns_found['deployment'].append({
                'type': 'Containerization (Docker)',
                'confidence': 'high',
                'evidence': f'Docker files found: {[f.name for f in docker_files]}'
            })
        
        # Detect Kubernetes
        k8s_files = [f for f in files if f.suffix in ['.yaml', '.yml'] and 'k8s' in str(f) or 'kubernetes' in str(f)]
        if k8s_files:
            self.patterns_found['deployment'].append({
                'type': 'Kubernetes Orchestration',
                'confidence': 'medium',
                'evidence': f'K8s YAML files found'
            })
    
    def _detect_architectural_patterns(self):
        """Detect specific architectural patterns in code."""
        for file_path in self.project_root.rglob('*.py'):
            self._analyze_python_patterns(file_path)
        
        for file_path in self.project_root.rglob('*.js'):
            self._analyze_javascript_patterns(file_path)
    
    def _analyze_python_patterns(self, file_path: Path):
        """Analyze Python files for patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Repository pattern
            if re.search(r'class\s+\w*Repository', content):
                self.patterns_found['design'].append({
                    'type': 'Repository Pattern',
                    'file': str(file_path.relative_to(self.project_root)),
                    'confidence': 'high'
                })
            
            # Factory pattern
            if re.search(r'def\s+create_\w+|class\s+\w*Factory', content):
                self.patterns_found['design'].append({
                    'type': 'Factory Pattern',
                    'file': str(file_path.relative_to(self.project_root)),
                    'confidence': 'medium'
                })
            
            # Singleton pattern
            if re.search(r'__new__.*singleton|_instance.*None', content):
                self.patterns_found['design'].append({
                    'type': 'Singleton Pattern',
                    'file': str(file_path.relative_to(self.project_root)),
                    'confidence': 'medium'
                })
                
        except Exception as e:
            print(f"Error analyzing Python file {file_path}: {e}")
    
    def _analyze_javascript_patterns(self, file_path: Path):
        """Analyze JavaScript files for patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Module pattern
            if re.search(r'export\s+default|module\.exports', content):
                self.patterns_found['design'].append({
                    'type': 'Module Pattern',
                    'file': str(file_path.relative_to(self.project_root)),
                    'confidence': 'high'
                })
            
            # Observer pattern (EventEmitter)
            if re.search(r'addEventListener|on\(|emit\(', content):
                self.patterns_found['design'].append({
                    'type': 'Observer Pattern',
                    'file': str(file_path.relative_to(self.project_root)),
                    'confidence': 'medium'
                })
                
        except Exception as e:
            print(f"Error analyzing JavaScript file {file_path}: {e}")
    
    def _detect_security_patterns(self):
        """Detect security-related patterns."""
        auth_keywords = ['jwt', 'oauth', 'passport', 'auth', 'login', 'session']
        security_files = []
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                filename_lower = file_path.name.lower()
                if any(keyword in filename_lower for keyword in auth_keywords):
                    security_files.append(file_path)
        
        if security_files:
            self.patterns_found['security'].append({
                'type': 'Authentication System',
                'confidence': 'medium',
                'evidence': f'Auth-related files found: {[f.name for f in security_files[:3]]}'
            })
        
        # Check for HTTPS/SSL configuration
        config_files = list(self.project_root.rglob('*.conf')) + list(self.project_root.rglob('*.config'))
        for config_file in config_files:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if 'ssl' in content or 'https' in content:
                        self.patterns_found['security'].append({
                            'type': 'SSL/HTTPS Configuration',
                            'confidence': 'medium',
                            'file': str(config_file.relative_to(self.project_root))
                        })
                        break
            except:
                continue
    
    def _detect_performance_patterns(self):
        """Detect performance-related patterns."""
        cache_keywords = ['cache', 'redis', 'memcached']
        
        # Check for caching in dependency files
        for dep_file in ['package.json', 'requirements.txt', 'pom.xml']:
            dep_path = self.project_root / dep_file
            if dep_path.exists():
                try:
                    with open(dep_path, 'r') as f:
                        content = f.read().lower()
                        for cache_keyword in cache_keywords:
                            if cache_keyword in content:
                                self.patterns_found['performance'].append({
                                    'type': f'Caching ({cache_keyword})',
                                    'confidence': 'high',
                                    'evidence': f'Found in {dep_file}'
                                })
                except:
                    continue
        
        # Check for async patterns
        async_files = []
        for file_path in itertools.chain(
            self.project_root.rglob('*.py'), 
            self.project_root.rglob('*.js'),
            self.project_root.rglob('*.ts')
        ):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(r'async\s+def|async\s+function|await\s+', content):
                        async_files.append(file_path)
            except:
                continue
        
        if async_files:
            self.patterns_found['performance'].append({
                'type': 'Asynchronous Processing',
                'confidence': 'high',
                'evidence': f'Async patterns found in {len(async_files)} files'
            })

def main():
    """Main entry point for the script."""
    import argparse
    import itertools
    
    parser = argparse.ArgumentParser(description='Detect architectural and design patterns')
    parser.add_argument('project_path', help='Path to the project root')
    parser.add_argument('--output', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    detector = PatternDetector(args.project_path)
    results = detector.detect_patterns()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Security Analyzer Script for Codebase Architecture Analyst

This script analyzes a codebase for security patterns, vulnerabilities,
and security best practices implementation.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict

class SecurityAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.security_findings = defaultdict(list)
        
    def analyze_security(self) -> Dict:
        """Analyze security patterns and potential issues."""
        self._check_authentication_patterns()
        self._check_input_validation()
        self._check_data_protection()
        self._check_configuration_security()
        self._check_dependency_security()
        
        return dict(self.security_findings)
    
    def _check_authentication_patterns(self):
        """Check for authentication and authorization patterns."""
        auth_patterns = {
            'jwt': r'jwt|jsonwebtoken',
            'oauth': r'oauth|passport',
            'session': r'session|cookie',
            'bcrypt': r'bcrypt|scrypt|argon2',
            'auth_middleware': r'authenticate|authorize|verify.*token'
        }
        
        for file_path in self._get_code_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                for pattern_name, pattern in auth_patterns.items():
                    if re.search(pattern, content):
                        self.security_findings['authentication'].append({
                            'type': pattern_name.upper(),
                            'file': str(file_path.relative_to(self.project_root)),
                            'pattern': 'Authentication mechanism detected'
                        })
                        
            except Exception:
                continue
    
    def _check_input_validation(self):
        """Check for input validation patterns."""
        validation_patterns = {
            'sanitization': r'sanitize|escape|clean',
            'validation': r'validate|check.*input|filter',
            'parameterized_queries': r'prepared.*statement|parameterized|placeholder',
            'xss_protection': r'xss|cross.*site|htmlspecialchars',
            'csrf_protection': r'csrf|cross.*site.*request'
        }
        
        for file_path in self._get_code_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                for pattern_name, pattern in validation_patterns.items():
                    if re.search(pattern, content):
                        self.security_findings['input_validation'].append({
                            'type': pattern_name.replace('_', ' ').title(),
                            'file': str(file_path.relative_to(self.project_root)),
                            'pattern': 'Input validation detected'
                        })
                        
            except Exception:
                continue
    
    def _check_data_protection(self):
        """Check for data protection patterns."""
        protection_patterns = {
            'encryption': r'encrypt|aes|rsa|cipher',
            'hashing': r'hash|sha|md5|pbkdf2',
            'ssl_tls': r'ssl|tls|https',
            'secrets_management': r'env|dotenv|vault|secrets'
        }
        
        for file_path in self._get_code_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                for pattern_name, pattern in protection_patterns.items():
                    if re.search(pattern, content):
                        self.security_findings['data_protection'].append({
                            'type': pattern_name.replace('_', ' ').title(),
                            'file': str(file_path.relative_to(self.project_root)),
                            'pattern': 'Data protection mechanism detected'
                        })
                        
            except Exception:
                continue
    
    def _check_configuration_security(self):
        """Check for secure configuration patterns."""
        config_files = [
            '.env', '.env.example', 'config.json', 'settings.py',
            'application.properties', 'web.config', 'nginx.conf'
        ]
        
        for config_name in config_files:
            config_files_found = list(self.project_root.rglob(config_name))
            
            for config_file in config_files_found:
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for hardcoded secrets (potential risk)
                    secret_patterns = [
                        r'password\s*=\s*["\'][^"\']{4,}["\']',
                        r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']',
                        r'secret\s*=\s*["\'][^"\']{10,}["\']'
                    ]
                    
                    for pattern in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            self.security_findings['configuration_risks'].append({
                                'type': 'Potential Hardcoded Secret',
                                'file': str(config_file.relative_to(self.project_root)),
                                'risk': 'HIGH',
                                'pattern': 'Hardcoded credentials detected'
                            })
                    
                    # Check for security headers
                    security_headers = [
                        r'x-frame-options',
                        r'content-security-policy',
                        r'x-content-type-options',
                        r'strict-transport-security'
                    ]
                    
                    for header in security_headers:
                        if re.search(header, content, re.IGNORECASE):
                            self.security_findings['security_headers'].append({
                                'type': header.title(),
                                'file': str(config_file.relative_to(self.project_root)),
                                'pattern': 'Security header configuration found'
                            })
                            
                except Exception:
                    continue
    
    def _check_dependency_security(self):
        """Check for known vulnerable dependencies."""
        # Check package.json for Node.js projects
        package_json = self.project_root / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                
                # Check for security-related packages
                security_packages = ['helmet', 'cors', 'express-rate-limit', 'express-validator']
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                
                found_security_packages = [pkg for pkg in security_packages if pkg in deps]
                if found_security_packages:
                    self.security_findings['security_packages'].append({
                        'type': 'Security Packages Detected',
                        'packages': found_security_packages,
                        'file': 'package.json'
                    })
                    
            except Exception:
                pass
        
        # Check requirements.txt for Python projects
        requirements_txt = self.project_root / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r') as f:
                    content = f.read()
                
                # Check for security-related packages
                security_packages = ['cryptography', 'bcrypt', 'pycryptodome', 'django-cors-headers']
                
                found_packages = [pkg for pkg in security_packages if pkg in content.lower()]
                if found_packages:
                    self.security_findings['security_packages'].append({
                        'type': 'Security Packages Detected',
                        'packages': found_packages,
                        'file': 'requirements.txt'
                    })
                    
            except Exception:
                pass
    
    def _get_code_files(self) -> List[Path]:
        """Get all code files to analyze."""
        code_extensions = {'.py', '.js', '.ts', '.java', '.cs', '.php', '.rb', '.go'}
        code_files = []
        
        for file_path in self.project_root.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix in code_extensions and
                not self._should_skip_file(file_path)):
                code_files.append(file_path)
        
        return code_files
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'venv', 'env'}
        return any(skip_dir in file_path.parts for skip_dir in skip_dirs)

def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze codebase security patterns')
    parser.add_argument('project_path', help='Path to the project root')
    parser.add_argument('--output', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    analyzer = SecurityAnalyzer(args.project_path)
    results = analyzer.analyze_security()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))

if __name__ == '__main__':
    main()
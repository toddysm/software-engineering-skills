#!/usr/bin/env python3
"""
Human-Readable Reports Generator - Plain English analysis of codebase
Creates security overviews, architecture summaries, and component guides
"""

import json
import click
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict, Counter
import re


class HumanReadableReportsGenerator:
    """Generates human-readable analysis reports in plain English"""
    
    @staticmethod
    def _normalize_purpose(raw_purpose) -> Dict[str, Any]:
        """Normalize purpose field to a dict with at least a 'primary_role' key.
        
        The source file analyzer may store purpose as either a dict
        (e.g. {'primary_role': 'api', 'indicators': [...]}) or a plain
        string (e.g. 'Configuration file').  This helper guarantees a
        consistent dict so callers can safely use .get().
        """
        if isinstance(raw_purpose, dict):
            return raw_purpose
        if isinstance(raw_purpose, str) and raw_purpose:
            return {'primary_role': raw_purpose, 'indicators': []}
        return {'primary_role': 'unknown', 'indicators': []}
    
    def __init__(self):
        self.file_inventory = {}
        self.dependency_graph = {}
        self.function_dependencies = {}
        self.impact_analysis = {}
        self.circular_dependencies = []
        
    def load_analysis_data(self, analysis_dir: str):
        """Load all analysis data"""
        analysis_path = Path(analysis_dir)
        
        # Load file inventory
        inventory_file = analysis_path / 'source-files' / 'file-inventory.json'
        if inventory_file.exists():
            with open(inventory_file, 'r') as f:
                self.file_inventory = json.load(f)
        
        # Load dependency data
        dep_file = analysis_path / 'dependencies' / 'dependency-graph.json'
        if dep_file.exists():
            with open(dep_file, 'r') as f:
                self.dependency_graph = json.load(f)
        
        func_file = analysis_path / 'dependencies' / 'function-dependencies.json'
        if func_file.exists():
            with open(func_file, 'r') as f:
                self.function_dependencies = json.load(f)
        
        impact_file = analysis_path / 'dependencies' / 'impact-analysis.json'
        if impact_file.exists():
            with open(impact_file, 'r') as f:
                self.impact_analysis = json.load(f)
        
        circular_file = analysis_path / 'dependencies' / 'circular-dependencies.json'
        if circular_file.exists():
            with open(circular_file, 'r') as f:
                self.circular_dependencies = json.load(f)
        
        print(f"📊 Loaded analysis data for {len(self.file_inventory)} files")
    
    def generate_security_overview(self) -> str:
        """Generate plain English security analysis"""
        security_issues = []
        security_strengths = []
        recommendations = []
        
        # Analyze authentication patterns
        auth_files = self._find_files_by_purpose(['auth', 'login', 'password', 'token', 'session'])
        if auth_files:
            auth_analysis = self._analyze_authentication_security(auth_files)
            security_issues.extend(auth_analysis['issues'])
            security_strengths.extend(auth_analysis['strengths'])
            recommendations.extend(auth_analysis['recommendations'])
        
        # Analyze input validation
        validation_analysis = self._analyze_input_validation()
        security_issues.extend(validation_analysis['issues'])
        security_strengths.extend(validation_analysis['strengths'])
        
        # Analyze secret management
        secrets_analysis = self._analyze_secret_management()
        security_issues.extend(secrets_analysis['issues'])
        security_strengths.extend(secrets_analysis['strengths'])
        
        # Analyze API security
        api_analysis = self._analyze_api_security()
        security_issues.extend(api_analysis['issues'])
        security_strengths.extend(api_analysis['strengths'])
        
        # Generate human-readable report
        report = "# Security Overview\\n\\n"
        
        if security_strengths:
            report += "## Security Strengths\\n\\n"
            for strength in security_strengths:
                report += f"✅ {strength}\\n\\n"
        
        if security_issues:
            report += "## Security Concerns\\n\\n"
            for i, issue in enumerate(security_issues, 1):
                severity = issue.get('severity', 'Medium')
                report += f"⚠️ **{severity} Priority**: {issue['description']}\\n"
                if 'files' in issue:
                    report += f"   *Affected files: {', '.join(issue['files'][:3])}"
                    if len(issue['files']) > 3:
                        report += f" (and {len(issue['files'])-3} others)"
                    report += "*\\n\\n"
                else:
                    report += "\\n"
        
        if recommendations:
            report += "## Security Recommendations\\n\\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\\n\\n"
        
        if not security_issues and not security_strengths:
            report += "No significant security patterns detected. This could mean either good security practices or limited security analysis coverage.\\n\\n"
        
        return report
    
    def generate_architecture_overview(self) -> str:
        """Generate plain English architecture explanation"""
        
        # Detect architecture type
        arch_type = self._detect_architecture_type()
        
        # Analyze technology stack
        tech_stack = self._analyze_technology_stack()
        
        # Analyze component organization
        component_analysis = self._analyze_component_organization()
        
        # Analyze data flow
        data_flow = self._analyze_data_flow_patterns()
        
        # Generate report
        report = "# Architecture Overview\\n\\n"
        
        # Architecture type
        report += f"## System Type\\n\\n"
        report += f"This is a **{arch_type['type']}** with {arch_type['description']}.\\n\\n"
        if arch_type['indicators']:
            report += f"*Architecture indicators: {', '.join(arch_type['indicators'])}*\\n\\n"
        
        # Technology stack
        if tech_stack:
            report += "## Technology Stack\\n\\n"
            for category, technologies in tech_stack.items():
                if technologies:
                    report += f"**{category.title()}**: {', '.join(technologies)}\\n\\n"
        
        # Component organization
        report += "## Component Organization\\n\\n"
        report += f"The system is organized into {component_analysis['total_components']} main components "
        report += f"across {component_analysis['directory_depth']} directory levels. "
        report += f"The code is {component_analysis['organization_quality']} organized.\\n\\n"
        
        if component_analysis['main_directories']:
            report += f"**Main directories**: {', '.join(component_analysis['main_directories'])}\\n\\n"
        
        # Data flow
        if data_flow:
            report += "## Data Flow & Patterns\\n\\n"
            report += f"{data_flow['description']}\\n\\n"
            if data_flow['patterns']:
                report += f"**Key patterns**: {', '.join(data_flow['patterns'])}\\n\\n"
        
        # Dependencies and coupling
        coupling_analysis = self._analyze_coupling()
        report += "## System Coupling\\n\\n"
        report += f"The system has {coupling_analysis['level']} coupling. "
        report += f"{coupling_analysis['explanation']}\\n\\n"
        
        # Architectural strengths and concerns
        arch_assessment = self._assess_architecture_quality()
        
        if arch_assessment['strengths']:
            report += "## Architectural Strengths\\n\\n"
            for strength in arch_assessment['strengths']:
                report += f"✅ {strength}\\n\\n"
        
        if arch_assessment['concerns']:
            report += "## Architectural Concerns\\n\\n"
            for concern in arch_assessment['concerns']:
                report += f"⚠️ {concern}\\n\\n"
        
        return report
    
    def generate_components_guide(self) -> str:
        """Generate component relationship and interaction guide"""
        
        # Find central components (high impact)
        central_components = self._find_central_components()
        
        # Analyze component categories
        component_categories = self._categorize_components()
        
        # Generate interaction patterns
        interaction_patterns = self._analyze_component_interactions()
        
        # Generate report
        report = "# Component Guide\\n\\n"
        
        # Central components
        if central_components:
            report += "## Central Components\\n\\n"
            report += "These components are heavily used throughout the system. Changes here have wide impact:\\n\\n"
            
            for component in central_components[:5]:  # Top 5
                report += f"### {Path(component['file']).stem}\\n\\n"
                report += f"**File**: `{component['file']}`\\n\\n"
                report += f"**Used by**: {component['dependents']} other components\\n\\n"
                
                # Get file purpose
                file_info = self.file_inventory.get(component['file'], {})
                purpose = self._normalize_purpose(file_info.get('purpose', {}))
                if purpose.get('primary_role') and purpose.get('primary_role') != 'unknown':
                    report += f"**Purpose**: {purpose['primary_role'].replace('_', ' ').title()}"
                    if purpose.get('indicators'):
                        report += f" - {purpose['indicators'][0]}"
                    report += "\\n\\n"
                
                # Show key dependents
                if component['key_dependents']:
                    report += f"**Key dependent files**: {', '.join(component['key_dependents'][:3])}"
                    if len(component['key_dependents']) > 3:
                        report += f" (and {len(component['key_dependents'])-3} others)"
                    report += "\\n\\n"
        
        # Component categories
        if component_categories:
            report += "## Component Categories\\n\\n"
            
            for category, files in component_categories.items():
                if files:
                    report += f"### {category.replace('_', ' ').title()} ({len(files)} files)\\n\\n"
                    
                    # Show representative files
                    for file_path in files[:3]:
                        filename = Path(file_path).stem
                        report += f"- **{filename}**: `{file_path}`"
                        
                        # Add brief description
                        file_info = self.file_inventory.get(file_path, {})
                        doc = file_info.get('documentation', {})
                        if doc.get('file_docstring'):
                            desc = doc['file_docstring'][:100] + "..." if len(doc['file_docstring']) > 100 else doc['file_docstring']
                            report += f" - {desc}"
                        report += "\\n"
                    
                    if len(files) > 3:
                        report += f"... and {len(files)-3} other files\\n"
                    
                    report += "\\n"
        
        # Interaction patterns
        if interaction_patterns:
            report += "## Common Interaction Patterns\\n\\n"
            
            for pattern in interaction_patterns:
                report += f"### {pattern['name']}\\n\\n"
                report += f"{pattern['description']}\\n\\n"
                
                if pattern.get('example_files'):
                    report += f"**Example**: {' → '.join(pattern['example_files'])}\\n\\n"
        
        # Modification guidance
        report += "## Modification Guidance\\n\\n"
        
        modification_guide = self._generate_modification_guidance()
        for guidance in modification_guide:
            report += f"**{guidance['scenario']}**: {guidance['advice']}\\n\\n"
        
        return report
    
    def generate_technology_decisions(self) -> str:
        """Analyze and explain technology decisions"""
        
        tech_choices = self._analyze_technology_choices()
        
        report = "# Technology Decisions Analysis\\n\\n"
        
        if tech_choices['framework_choices']:
            report += "## Framework Choices\\n\\n"
            for choice in tech_choices['framework_choices']:
                report += f"**{choice['technology']}**: {choice['reasoning']}\\n\\n"
                if choice.get('alternatives'):
                    report += f"*Alternative options: {', '.join(choice['alternatives'])}*\\n\\n"
        
        if tech_choices['architectural_decisions']:
            report += "## Architectural Decisions\\n\\n"
            for decision in tech_choices['architectural_decisions']:
                report += f"**{decision['decision']}**: {decision['rationale']}\\n\\n"
        
        if tech_choices['recommendations']:
            report += "## Recommendations\\n\\n"
            for i, rec in enumerate(tech_choices['recommendations'], 1):
                report += f"{i}. {rec}\\n\\n"
        
        return report
    
    def _find_files_by_purpose(self, keywords: List[str]) -> List[str]:
        """Find files related to specific purpose keywords"""
        matching_files = []
        
        for file_path, file_info in self.file_inventory.items():
            file_content_lower = str(file_info).lower()
            path_lower = file_path.lower()
            
            for keyword in keywords:
                if keyword in path_lower or keyword in file_content_lower:
                    matching_files.append(file_path)
                    break
        
        return matching_files
    
    def _analyze_authentication_security(self, auth_files: List[str]) -> Dict[str, List]:
        """Analyze authentication security patterns"""
        issues = []
        strengths = []
        recommendations = []
        
        # Look for security patterns in auth files
        for file_path in auth_files:
            file_info = self.file_inventory.get(file_path, {})
            
            # Check for password handling
            if any('password' in str(file_info).lower() for _ in [1]):
                if 'bcrypt' in str(file_info).lower() or 'hash' in str(file_info).lower():
                    strengths.append("Password hashing detected with secure algorithms")
                else:
                    issues.append({
                        'description': "Password handling found but no secure hashing detected",
                        'severity': 'High',
                        'files': [file_path]
                    })
            
            # Check for JWT/token handling
            if 'jwt' in str(file_info).lower() or 'token' in str(file_info).lower():
                strengths.append("Token-based authentication system in use")
                
                if 'secret' in str(file_info).lower():
                    recommendations.append("Ensure JWT secrets are stored securely and rotated regularly")
        
        return {
            'issues': issues,
            'strengths': strengths,
            'recommendations': recommendations
        }
    
    def _analyze_input_validation(self) -> Dict[str, List]:
        """Analyze input validation patterns"""
        issues = []
        strengths = []
        
        validation_files = []
        unvalidated_files = []
        
        for file_path, file_info in self.file_inventory.items():
            purpose = self._normalize_purpose(file_info.get('purpose', {}))
            
            # Check API/controller files
            if purpose.get('primary_role') in ['api', 'controller']:
                file_content = str(file_info).lower()
                
                if any(pattern in file_content for pattern in ['validate', 'sanitize', 'escape', 'clean']):
                    validation_files.append(file_path)
                else:
                    unvalidated_files.append(file_path)
        
        if validation_files:
            strengths.append(f"Input validation detected in {len(validation_files)} files")
        
        if unvalidated_files:
            issues.append({
                'description': f"API/controller files without apparent input validation",
                'severity': 'Medium',
                'files': unvalidated_files[:5]  # Limit to 5 examples
            })
        
        return {'issues': issues, 'strengths': strengths}
    
    def _analyze_secret_management(self) -> Dict[str, List]:
        """Analyze how secrets and credentials are managed"""
        issues = []
        strengths = []
        
        # Look for environment variable usage
        env_files = self._find_files_by_purpose(['env', 'config', 'settings'])
        
        if env_files:
            strengths.append("Configuration files detected - good for secret management")
        
        # Look for hardcoded secrets (simplified detection)
        for file_path, file_info in self.file_inventory.items():
            file_content = str(file_info).lower()
            
            if any(pattern in file_content for pattern in ['password = ', 'secret = ', 'key = ']):
                issues.append({
                    'description': "Potential hardcoded secrets detected",
                    'severity': 'High',
                    'files': [file_path]
                })
        
        return {'issues': issues, 'strengths': strengths}
    
    def _analyze_api_security(self) -> Dict[str, List]:
        """Analyze API security patterns"""
        issues = []
        strengths = []
        
        api_files = self._find_files_by_purpose(['api', 'route', 'endpoint'])
        
        for file_path in api_files:
            file_info = self.file_inventory.get(file_path, {})
            file_content = str(file_info).lower()
            
            # Check for rate limiting
            if any(pattern in file_content for pattern in ['rate', 'limit', 'throttle']):
                strengths.append("Rate limiting detected in API endpoints")
            
            # Check for CORS
            if 'cors' in file_content:
                strengths.append("CORS configuration detected")
            
            # Check for authentication middleware
            if any(pattern in file_content for pattern in ['auth', 'authenticate', 'authorize']):
                strengths.append("Authentication middleware detected in API routes")
        
        if api_files and not any('rate' in str(self.file_inventory.get(f, {})).lower() for f in api_files):
            issues.append({
                'description': "API endpoints detected without apparent rate limiting",
                'severity': 'Medium',
                'files': api_files
            })
        
        return {'issues': issues, 'strengths': strengths}
    
    def _detect_architecture_type(self) -> Dict[str, Any]:
        """Detect the overall architecture pattern"""
        
        indicators = []
        
        # Check for web application patterns
        if self._find_files_by_purpose(['server', 'app', 'express']):
            indicators.append('web server detected')
        
        if self._find_files_by_purpose(['react', 'component', 'jsx']):
            indicators.append('React frontend detected')
        
        if self._find_files_by_purpose(['api', 'route', 'endpoint']):
            indicators.append('REST API structure')
        
        # Check for microservices patterns 
        service_files = self._find_files_by_purpose(['service'])
        if len(service_files) > 3:
            indicators.append('multiple services (possible microservices)')
        
        # Check for monolithic patterns
        if len(self.file_inventory) > 50 and len(service_files) < 3:
            indicators.append('monolithic structure')
        
        # Determine architecture type
        if 'React' in str(indicators) and 'web server' in str(indicators):
            return {
                'type': 'Full-Stack Web Application',
                'description': 'a React frontend with backend API services',
                'indicators': indicators
            }
        elif 'microservices' in str(indicators):
            return {
                'type': 'Microservices Architecture',
                'description': 'multiple independent services',
                'indicators': indicators
            }
        elif 'monolithic' in str(indicators):
            return {
                'type': 'Monolithic Application',
                'description': 'a single unified codebase',
                'indicators': indicators
            }
        elif 'web server' in str(indicators):
            return {
                'type': 'Backend Service',
                'description': 'server-side application with API endpoints',
                'indicators': indicators
            }
        else:
            return {
                'type': 'Software System',
                'description': 'a structured codebase',
                'indicators': indicators
            }
    
    def _analyze_technology_stack(self) -> Dict[str, List]:
        """Analyze the technology stack used"""
        
        stack = {
            'frontend': [],
            'backend': [],
            'database': [],
            'build_tools': [],
            'testing': []
        }
        
        # Analyze file extensions and imports
        for file_path, file_info in self.file_inventory.items():
            extension = file_info.get('extension', '')
            imports = file_info.get('imports', {})
            
            if extension in ['.jsx', '.tsx']:
                stack['frontend'].append('React/JSX')
            elif extension in ['.js', '.ts']:
                imports_str = str(imports).lower()
                if 'react' in imports_str:
                    stack['frontend'].append('React')
                elif 'vue' in imports_str:
                    stack['frontend'].append('Vue.js')
                elif 'angular' in imports_str or '@angular' in imports_str:
                    stack['frontend'].append('Angular')
                elif 'svelte' in imports_str:
                    stack['frontend'].append('Svelte')
                else:
                    stack['backend'].append('JavaScript/TypeScript')
                external_imports = imports.get('external', [])
                if any('express' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Express.js')
                if any('nest' in imp.lower() or '@nestjs' in imp.lower() for imp in external_imports):
                    stack['backend'].append('NestJS')
                if any('next' in imp.lower() for imp in external_imports):
                    stack['frontend'].append('Next.js')
                if any('nuxt' in imp.lower() for imp in external_imports):
                    stack['frontend'].append('Nuxt.js')
                if any('jest' in imp.lower() or 'mocha' in imp.lower() or 'vitest' in imp.lower() for imp in external_imports):
                    stack['testing'].append('JavaScript Testing Framework')
            elif extension == '.py':
                stack['backend'].append('Python')
                
                # Check for specific Python frameworks
                external_imports = imports.get('external', [])
                if any('flask' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Flask')
                if any('django' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Django')
                if any('fastapi' in imp.lower() for imp in external_imports):
                    stack['backend'].append('FastAPI')
                if any(imp.lower() in ('sqlalchemy', 'databases', 'tortoise') for imp in external_imports):
                    stack['database'].append('SQLAlchemy ORM')
                if any('celery' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Celery')
                if any('pytest' in imp.lower() or 'unittest' in imp.lower() for imp in external_imports):
                    stack['testing'].append('Python Test Framework')
                if any('numpy' in imp.lower() or 'pandas' in imp.lower() or 'tensorflow' in imp.lower() or 'torch' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Python Data/ML')
            
            elif extension == '.java':
                stack['backend'].append('Java')
                external_imports = imports.get('external', [])
                if any('springframework' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Spring Framework')
                if any('springboot' in imp.lower() or 'spring.boot' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Spring Boot')
                if any('jakarta.ee' in imp.lower() or 'javax.enterprise' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Jakarta EE')
                if any('hibernate' in imp.lower() for imp in external_imports):
                    stack['database'].append('Hibernate ORM')
                if any('junit' in imp.lower() or 'testng' in imp.lower() for imp in external_imports):
                    stack['testing'].append('JUnit/TestNG')
                if any('quarkus' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Quarkus')
                if any('micronaut' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Micronaut')
            
            elif extension == '.rb':
                stack['backend'].append('Ruby')
                external_imports = imports.get('external', [])
                if any('rails' in imp.lower() or 'actioncontroller' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Ruby on Rails')
                if any('sinatra' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Sinatra')
                if any('rspec' in imp.lower() or 'minitest' in imp.lower() for imp in external_imports):
                    stack['testing'].append('RSpec/Minitest')
                if any('activerecord' in imp.lower() for imp in external_imports):
                    stack['database'].append('ActiveRecord ORM')
                if any('sidekiq' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Sidekiq')
            
            elif extension == '.php':
                stack['backend'].append('PHP')
                external_imports = imports.get('external', [])
                if any('illuminate' in imp.lower() or 'laravel' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Laravel')
                if any('symfony' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Symfony')
                if any('wordpress' in imp.lower() or 'woocommerce' in imp.lower() for imp in external_imports):
                    stack['backend'].append('WordPress')
                if any('doctrine' in imp.lower() for imp in external_imports):
                    stack['database'].append('Doctrine ORM')
                if any('phpunit' in imp.lower() or 'pest' in imp.lower() for imp in external_imports):
                    stack['testing'].append('PHPUnit/Pest')
            
            elif extension == '.go':
                stack['backend'].append('Go')
                
                # Check for specific Go frameworks
                external_imports = imports.get('external', [])
                if any('gin' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Gin')
                if any('echo' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Echo')
                if any('fiber' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Fiber')
            
            elif extension == '.rs':
                stack['backend'].append('Rust')
                
                # Check for specific Rust frameworks
                external_imports = imports.get('external', [])
                if any('actix' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Actix Web')
                if any('rocket' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Rocket')
                if any('axum' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Axum')
            
            elif extension == '.cs':
                stack['backend'].append('C#')
                
                # Check for specific .NET frameworks
                external_imports = imports.get('external', [])
                if any('aspnetcore' in imp.lower() or 'asp.net' in imp.lower() for imp in external_imports):
                    stack['backend'].append('ASP.NET Core')
                if any('blazor' in imp.lower() for imp in external_imports):
                    stack['frontend'].append('Blazor')
            
            elif extension in ['.c', '.cpp', '.cxx', '.cc']:
                stack['backend'].append('C/C++')
                
                # Check for specific C++ frameworks
                external_imports = imports.get('external', [])
                if any('boost' in imp.lower() for imp in external_imports):
                    stack['backend'].append('Boost')
                if any('qt' in imp.lower() for imp in external_imports):
                    stack['frontend'].append('Qt')
            
            elif extension in ['.h', '.hpp', '.hxx']:
                # Header files - analyze content for framework detection
                if 'qt' in str(imports).lower():
                    stack['frontend'].append('Qt')
                if 'boost' in str(imports).lower():
                    stack['backend'].append('Boost')
            
            # Check for database-related imports
            if any(db in str(imports).lower() for db in ['sqlite', 'postgres', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra']):
                for db in ['sqlite', 'postgres', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra']:
                    if db in str(imports).lower():
                        stack['database'].append(db.title())
        
        # Check for build tools based on file presence
        if 'Cargo.toml' in self.file_inventory:
            stack['build_tools'].append('Cargo (Rust)')
        if 'go.mod' in self.file_inventory:
            stack['build_tools'].append('Go Modules')
        if any('.csproj' in path or '.sln' in path for path in self.file_inventory):
            stack['build_tools'].append('MSBuild (.NET)')
        if 'CMakeLists.txt' in self.file_inventory:
            stack['build_tools'].append('CMake')
        if 'Makefile' in self.file_inventory:
            stack['build_tools'].append('Make')
        if 'Gemfile' in self.file_inventory or 'Gemfile.lock' in self.file_inventory:
            stack['build_tools'].append('Bundler (Ruby)')
        if 'composer.json' in self.file_inventory:
            stack['build_tools'].append('Composer (PHP)')
        if 'pom.xml' in self.file_inventory:
            stack['build_tools'].append('Maven (Java)')
        if 'build.gradle' in self.file_inventory or 'build.gradle.kts' in self.file_inventory:
            stack['build_tools'].append('Gradle (Java/Kotlin)')
        if 'package.json' in self.file_inventory:
            stack['build_tools'].append('npm/yarn/pnpm')
        
        # Remove duplicates
        for category in stack:
            stack[category] = list(set(stack[category]))
        
        return stack
    
    def _analyze_component_organization(self) -> Dict[str, Any]:
        """Analyze how components are organized"""
        
        # Count directory levels
        max_depth = 0
        directories = set()
        
        for file_path in self.file_inventory.keys():
            path_parts = Path(file_path).parts
            max_depth = max(max_depth, len(path_parts))
            
            if len(path_parts) > 1:
                directories.add(path_parts[0])
        
        # Assess organization quality
        if max_depth <= 2:
            organization_quality = "simply"
        elif max_depth <= 4:
            organization_quality = "well"
        else:
            organization_quality = "complexly"
        
        return {
            'total_components': len(self.file_inventory),
            'directory_depth': max_depth,
            'main_directories': list(directories)[:5],  # Top 5
            'organization_quality': organization_quality
        }
    
    def _analyze_data_flow_patterns(self) -> Dict[str, Any]:
        """Analyze data flow patterns in the system"""
        
        patterns = []
        
        # Look for MVC pattern
        mvc_indicators = {
            'model': self._find_files_by_purpose(['model', 'schema']),
            'view': self._find_files_by_purpose(['view', 'component', 'template']),
            'controller': self._find_files_by_purpose(['controller', 'handler', 'route'])
        }
        
        if all(mvc_indicators.values()):
            patterns.append('MVC (Model-View-Controller)')
        
        # Look for layered architecture
        layer_indicators = {
            'data': self._find_files_by_purpose(['model', 'database', 'repo']),
            'service': self._find_files_by_purpose(['service', 'business']),
            'api': self._find_files_by_purpose(['api', 'controller'])
        }
        
        if all(layer_indicators.values()):
            patterns.append('Layered Architecture')
        
        # Generate description
        if patterns:
            description = f"The system follows {' and '.join(patterns)} patterns for clear separation of concerns."
        else:
            description = "The system uses a custom organization pattern."
        
        return {
            'description': description,
            'patterns': patterns
        }
    
    def _analyze_coupling(self) -> Dict[str, str]:
        """Analyze system coupling level"""
        
        total_files = len(self.dependency_graph)
        if total_files == 0:
            return {'level': 'unknown', 'explanation': 'No dependency data available.'}
        
        total_dependencies = sum(len(deps.get('imports_from', [])) for deps in self.dependency_graph.values())
        avg_dependencies = total_dependencies / total_files
        
        # Calculate coupling level
        if avg_dependencies < 2:
            level = "low"
            explanation = "Most files have few dependencies, indicating good separation of concerns."
        elif avg_dependencies < 5:
            level = "moderate"
            explanation = "Files have reasonable dependencies, showing balanced coupling."
        else:
            level = "high"
            explanation = "Files have many dependencies, which may make the system harder to maintain."
        
        return {
            'level': level,
            'explanation': explanation
        }
    
    def _assess_architecture_quality(self) -> Dict[str, List]:
        """Assess overall architecture quality"""
        
        strengths = []
        concerns = []
        
        # Check for circular dependencies
        if not self.circular_dependencies:
            strengths.append("No circular dependencies detected")
        else:
            concerns.append(f"{len(self.circular_dependencies)} circular dependencies found")
        
        # Check for single responsibility
        high_complexity_files = [
            file_path for file_path, file_info in self.file_inventory.items()
            if file_info.get('complexity_score', 0) > 20
        ]
        
        if len(high_complexity_files) < len(self.file_inventory) * 0.1:
            strengths.append("Most files have manageable complexity")
        else:
            concerns.append(f"{len(high_complexity_files)} files have high complexity")
        
        # Check documentation
        documented_files = [
            file_path for file_path, file_info in self.file_inventory.items()
            if file_info.get('documentation', {}).get('file_docstring') or 
               file_info.get('documentation', {}).get('header_comments')
        ]
        
        doc_percentage = len(documented_files) / len(self.file_inventory) * 100
        
        if doc_percentage > 70:
            strengths.append(f"Good documentation coverage ({doc_percentage:.0f}% of files)")
        elif doc_percentage > 30:
            strengths.append(f"Partial documentation coverage ({doc_percentage:.0f}% of files)")
        else:
            concerns.append(f"Low documentation coverage ({doc_percentage:.0f}% of files)")
        
        return {
            'strengths': strengths,
            'concerns': concerns
        }
    
    def _find_central_components(self) -> List[Dict[str, Any]]:
        """Find components that are central to the system"""
        
        component_impact = []
        
        for file_path, impact_files in self.impact_analysis.items():
            if len(impact_files) > 0:  # Has dependents
                dependents = self.dependency_graph.get(file_path, {}).get('imported_by', [])
                
                component_impact.append({
                    'file': file_path,
                    'dependents': len(dependents),
                    'total_impact': len(impact_files),
                    'key_dependents': dependents[:3]
                })
        
        # Sort by impact
        component_impact.sort(key=lambda x: x['total_impact'], reverse=True)
        
        return component_impact
    
    def _categorize_components(self) -> Dict[str, List[str]]:
        """Categorize components by their purpose"""
        
        categories = defaultdict(list)
        
        for file_path, file_info in self.file_inventory.items():
            purpose = self._normalize_purpose(file_info.get('purpose', {}))
            primary_role = purpose.get('primary_role', 'utility')
            
            categories[primary_role].append(file_path)
        
        return dict(categories)
    
    def _analyze_component_interactions(self) -> List[Dict[str, Any]]:
        """Analyze common interaction patterns between components"""
        
        patterns = []
        
        # API to Service pattern
        api_files = self._find_files_by_purpose(['api', 'controller'])
        service_files = self._find_files_by_purpose(['service'])
        
        if api_files and service_files:
            patterns.append({
                'name': 'API-Service Pattern',
                'description': 'API controllers delegate business logic to service components',
                'example_files': [api_files[0], service_files[0]] if api_files and service_files else []
            })
        
        # Service to Data pattern
        data_files = self._find_files_by_purpose(['model', 'database', 'repo'])
        
        if service_files and data_files:
            patterns.append({
                'name': 'Service-Data Pattern',
                'description': 'Services access data through model or repository components',
                'example_files': [service_files[0], data_files[0]] if service_files and data_files else []
            })
        
        return patterns
    
    def _generate_modification_guidance(self) -> List[Dict[str, str]]:
        """Generate guidance for common modification scenarios"""
        
        guidance = []
        
        # Central components
        central_files = [comp['file'] for comp in self._find_central_components()[:3]]
        
        if central_files:
            guidance.append({
                'scenario': 'Modifying core components',
                'advice': f"When changing {', '.join([Path(f).stem for f in central_files])}, "
                         f"test thoroughly as these components affect many other parts of the system."
            })
        
        # API changes
        api_files = self._find_files_by_purpose(['api', 'controller'])
        if api_files:
            guidance.append({
                'scenario': 'API changes',
                'advice': "When modifying API endpoints, update documentation and consider backward compatibility for existing clients."
            })
        
        # Database changes
        data_files = self._find_files_by_purpose(['model', 'schema'])
        if data_files:
            guidance.append({
                'scenario': 'Database schema changes',
                'advice': "When changing data models, create migration scripts and update all dependent services."
            })
        
        return guidance
    
    def _analyze_technology_choices(self) -> Dict[str, List]:
        """Analyze technology choices and their reasoning"""
        
        tech_stack = self._analyze_technology_stack()
        
        framework_choices = []
        architectural_decisions = []
        recommendations = []
        
        # Analyze framework choices
        if 'React' in tech_stack.get('frontend', []):
            framework_choices.append({
                'technology': 'React',
                'reasoning': 'Component-based frontend architecture for maintainable UI development',
                'alternatives': ['Vue.js', 'Angular']
            })
        
        if 'Flask' in tech_stack.get('backend', []):
            framework_choices.append({
                'technology': 'Flask',
                'reasoning': 'Lightweight Python web framework for flexible API development',
                'alternatives': ['Django', 'FastAPI']
            })
        
        # Architectural decisions
        if len(self._find_files_by_purpose(['service'])) > 3:
            architectural_decisions.append({
                'decision': 'Service-oriented architecture',
                'rationale': 'Separation of concerns through dedicated service components'
            })
        
        # Recommendations based on analysis
        if self.circular_dependencies:
            recommendations.append("Consider refactoring to eliminate circular dependencies for better maintainability")
        
        if not tech_stack.get('testing', []):
            recommendations.append("Consider adding a testing framework to improve code quality and reliability")
        
        return {
            'framework_choices': framework_choices,
            'architectural_decisions': architectural_decisions,
            'recommendations': recommendations
        }


@click.command()
@click.argument('analysis_dir', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='Output directory for human-readable reports')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(analysis_dir, output, verbose):
    """Generate human-readable analysis reports"""
    
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    generator = HumanReadableReportsGenerator()
    generator.load_analysis_data(analysis_dir)
    
    print("📝 Generating human-readable reports...")
    
    # Generate security overview
    security_report = generator.generate_security_overview()
    security_file = output_path / 'security-overview.md'
    with open(security_file, 'w') as f:
        f.write(security_report)
    print(f"🔒 Security overview saved to: {security_file}")
    
    # Generate architecture overview
    architecture_report = generator.generate_architecture_overview()
    architecture_file = output_path / 'architecture-overview.md'
    with open(architecture_file, 'w') as f:
        f.write(architecture_report)
    print(f"🏗️ Architecture overview saved to: {architecture_file}")
    
    # Generate components guide
    components_report = generator.generate_components_guide()
    components_file = output_path / 'components-guide.md'
    with open(components_file, 'w') as f:
        f.write(components_report)
    print(f"🧩 Components guide saved to: {components_file}")
    
    # Generate technology decisions
    tech_report = generator.generate_technology_decisions()
    tech_file = output_path / 'technology-decisions.md'
    with open(tech_file, 'w') as f:
        f.write(tech_report)
    print(f"⚙️ Technology decisions saved to: {tech_file}")
    
    print("✅ All human-readable reports generated successfully")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Mermaid Diagram Generator for Codebase Architecture Analyst

This script generates Mermaid diagrams based on analysis data from
the codebase architecture analysis.
"""

import json
from typing import Dict, List, Set, Optional
from pathlib import Path

class MermaidDiagramGenerator:
    def __init__(self):
        self.components = {}
        self.connections = []
        self.external_services = {}
        
    def generate_diagram(self, analysis_data: Dict) -> str:
        """Generate appropriate Mermaid diagram based on analysis data."""
        architecture_style = analysis_data.get('architecture_style', 'layered')
        
        if architecture_style == 'microservices':
            return self._generate_microservices_diagram(analysis_data)
        elif architecture_style == 'layered':
            return self._generate_layered_diagram(analysis_data)
        else:
            return self._generate_generic_diagram(analysis_data)
    
    def _generate_microservices_diagram(self, data: Dict) -> str:
        """Generate microservices architecture diagram."""
        mermaid = ["graph TB"]
        
        # User/Client
        mermaid.append('    User[👤 User/Client] --> Gateway[🌐 API Gateway]')
        
        # Services (infer from directory structure or patterns)
        services = self._extract_services(data)
        
        for i, service in enumerate(services):
            service_id = f"Service{i+1}"
            mermaid.append(f'    Gateway --> {service_id}[🔧 {service}]')
            
            # Add database for each service
            db_id = f"DB{i+1}"
            mermaid.append(f'    {service_id} --> {db_id}[(🗄️ {service} DB)]')
        
        # Message bus if event-driven patterns detected
        if self._has_messaging_patterns(data):
            mermaid.append('    subgraph "Message Bus"')
            mermaid.append('        EventBus[📨 Event Bus]')
            mermaid.append('    end')
            
            for i in range(len(services)):
                mermaid.append(f'    Service{i+1} --> EventBus')
        
        # External services
        external_services = self._extract_external_services(data)
        for ext_service in external_services:
            mermaid.append(f'    Gateway --> Ext{ext_service}[🌐 {ext_service}]')
        
        return '\n'.join(mermaid)
    
    def _generate_layered_diagram(self, data: Dict) -> str:
        """Generate layered architecture diagram."""
        mermaid = ["graph TB"]
        
        # Standard layers
        layers = [
            ("UI", "🖥️ User Interface"),
            ("Controllers", "🎛️ Controllers"),
            ("Services", "⚙️ Business Services"),
            ("Repository", "📦 Data Access Layer"),
            ("Database", "🗄️ Database")
        ]
        
        # Add layer connections
        for i in range(len(layers) - 1):
            current_layer, current_label = layers[i]
            next_layer, next_label = layers[i + 1]
            mermaid.append(f'    {current_layer}[{current_label}] --> {next_layer}[{next_label}]')
        
        # Add external integrations
        external_services = self._extract_external_services(data)
        if external_services:
            for ext_service in external_services:
                mermaid.append(f'    Services --> Ext{ext_service}[🌐 {ext_service}]')
        
        # Add caching layer if detected
        if self._has_caching_patterns(data):
            mermaid.append('    Services --> Cache[⚡ Cache Layer]')
        
        return '\n'.join(mermaid)
    
    def _generate_generic_diagram(self, data: Dict) -> str:
        """Generate generic component diagram."""
        mermaid = ["graph TB"]
        
        # Extract main components
        components = self._extract_main_components(data)
        
        if not components:
            # Fallback to basic structure
            mermaid.append('    User[👤 User] --> Frontend[🖥️ Frontend]')
            mermaid.append('    Frontend --> Backend[⚙️ Backend]')
            mermaid.append('    Backend --> Database[🗄️ Database]')
        else:
            # Build diagram based on detected components
            for i, component in enumerate(components):
                comp_id = f"Comp{i}"
                icon = self._get_component_icon(component)
                mermaid.append(f'    {comp_id}[{icon} {component}]')
            
            # Add basic connections
            if len(components) > 1:
                for i in range(len(components) - 1):
                    mermaid.append(f'    Comp{i} --> Comp{i+1}')
        
        # Add external dependencies
        external_deps = self._extract_external_dependencies(data)
        for dep in external_deps[:3]:  # Limit to top 3
            clean_dep = dep.replace('-', '').replace('.', '')
            mermaid.append(f'    Backend --> {clean_dep}[🌐 {dep}]')
        
        return '\n'.join(mermaid)
    
    def _extract_services(self, data: Dict) -> List[str]:
        """Extract service names from analysis data."""
        services = []
        
        # Look for microservices indicators
        patterns = data.get('patterns', {})
        framework_patterns = patterns.get('framework', [])
        
        # Check for common service names in directories
        common_services = ['user', 'order', 'payment', 'notification', 'auth', 'api']
        
        # Look for Docker compose services
        docker_patterns = [p for p in framework_patterns if 'docker' in p.get('type', '').lower()]
        if docker_patterns:
            services.extend(['User Service', 'Order Service', 'Payment Service'])
        
        # Fallback to generic services
        if not services:
            services = ['User Service', 'Business Service', 'Data Service']
        
        return services[:4]  # Limit to 4 services for clarity
    
    def _extract_external_services(self, data: Dict) -> List[str]:
        """Extract external service names."""
        external_services = []
        
        # Look for common external dependencies
        external_deps = data.get('external_dependencies', {})
        
        common_externals = {
            'express': 'REST API',
            'axios': 'HTTP Client',
            'mongoose': 'MongoDB',
            'redis': 'Redis Cache',
            'aws': 'AWS Services',
            'stripe': 'Payment Service',
            'sendgrid': 'Email Service'
        }
        
        for file_deps in external_deps.values():
            for dep in file_deps:
                dep_lower = str(dep).lower()
                for key, service_name in common_externals.items():
                    if key in dep_lower and service_name not in external_services:
                        external_services.append(service_name)
        
        return external_services[:3]  # Limit for clarity
    
    def _extract_main_components(self, data: Dict) -> List[str]:
        """Extract main component names."""
        components = []
        
        # Look at framework information
        framework_info = data.get('framework_info', {})
        
        if framework_info.get('frontend'):
            components.append(f"Frontend ({framework_info['frontend']})")
        
        if framework_info.get('backend'):
            components.append(f"Backend ({framework_info['backend']})")
        
        # Add database if detected
        db_patterns = data.get('patterns', {}).get('database', [])
        if db_patterns or any('db' in str(dep).lower() for deps in data.get('external_dependencies', {}).values() for dep in deps):
            components.append('Database')
        
        return components
    
    def _extract_external_dependencies(self, data: Dict) -> List[str]:
        """Extract external dependencies for diagram."""
        external_deps = set()
        
        deps_data = data.get('external_dependencies', {})
        for file_deps in deps_data.values():
            for dep in file_deps:
                # Filter out common but diagram-irrelevant deps
                dep_str = str(dep).lower()
                if not any(skip in dep_str for skip in ['util', 'test', 'dev', 'build', 'babel']):
                    external_deps.add(str(dep))
        
        return list(external_deps)
    
    def _has_messaging_patterns(self, data: Dict) -> bool:
        """Check if messaging/event patterns exist."""
        patterns = data.get('patterns', {})
        
        # Check for event-driven indicators
        event_indicators = ['event', 'message', 'queue', 'bus', 'kafka', 'rabbitmq']
        
        for pattern_category in patterns.values():
            for pattern in pattern_category:
                pattern_text = str(pattern).lower()
                if any(indicator in pattern_text for indicator in event_indicators):
                    return True
        
        return False
    
    def _has_caching_patterns(self, data: Dict) -> bool:
        """Check if caching patterns exist."""
        patterns = data.get('patterns', {})
        
        cache_indicators = ['cache', 'redis', 'memcached']
        
        for pattern_category in patterns.values():
            for pattern in pattern_category:
                pattern_text = str(pattern).lower()
                if any(indicator in pattern_text for indicator in cache_indicators):
                    return True
        
        return False
    
    def _get_component_icon(self, component: str) -> str:
        """Get appropriate icon for component."""
        component_lower = component.lower()
        
        if 'frontend' in component_lower or 'ui' in component_lower:
            return '🖥️'
        elif 'backend' in component_lower or 'api' in component_lower:
            return '⚙️'
        elif 'database' in component_lower or 'db' in component_lower:
            return '🗄️'
        elif 'auth' in component_lower:
            return '🔐'
        elif 'cache' in component_lower:
            return '⚡'
        else:
            return '📦'

def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Mermaid diagrams from analysis data')
    parser.add_argument('analysis_file', help='JSON file with analysis data')
    parser.add_argument('--output', help='Output file for Mermaid diagram')
    parser.add_argument('--style', choices=['microservices', 'layered', 'generic'], 
                       help='Force specific diagram style')
    
    args = parser.parse_args()
    
    # Load analysis data
    with open(args.analysis_file, 'r') as f:
        analysis_data = json.load(f)
    
    # Override architecture style if specified
    if args.style:
        analysis_data['architecture_style'] = args.style
    
    # Generate diagram
    generator = MermaidDiagramGenerator()
    mermaid_diagram = generator.generate_diagram(analysis_data)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(mermaid_diagram)
        print(f"Mermaid diagram saved to {args.output}")
    else:
        print(mermaid_diagram)

if __name__ == '__main__':
    main()
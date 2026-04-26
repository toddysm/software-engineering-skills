#!/usr/bin/env python3
"""
Enhanced Diagram Generator - Detailed architecture visualization
Creates comprehensive Mermaid diagrams showing file relationships, security model, and component interactions
"""

import json
import re
import click
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict, Counter


class EnhancedDiagramGenerator:
    """Generates detailed architectural diagrams from analysis data"""

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

        print(f"📊 Loaded analysis data for diagram generation")

    def generate_detailed_architecture_diagram(self) -> str:
        """Generate comprehensive architecture diagram with component relationships"""

        # Categorize components by purpose
        components = self._categorize_components_for_diagram()

        # Build the diagram
        diagram = "```mermaid\ngraph TD\n"

        # Define component nodes with shapes and colors
        for category, files in components.items():
            if files:
                diagram += f"\n    %% {category.title()} Components\n"

                for file_path in files[:10]:  # Limit to avoid clutter
                    node_id = self._sanitize_node_id(file_path)
                    display_name = Path(file_path).stem

                    # Choose shape and style based on component type
                    if category == 'entry_point':
                        diagram += f'    {node_id}["{display_name}"]:::entry\n'
                    elif category == 'api':
                        diagram += f'    {node_id}{{"{display_name}"}}:::api\n'
                    elif category == 'service':
                        diagram += f'    {node_id}["{display_name}"]:::service\n'
                    elif category == 'data_model':
                        diagram += f'    {node_id}[("{display_name}")]:::data\n'
                    elif category == 'ui_component':
                        diagram += f'    {node_id}("{display_name}"):::ui\n'
                    elif category == 'configuration':
                        diagram += f'    {node_id}[/"{display_name}"/]:::config\n'
                    else:
                        diagram += f'    {node_id}["{display_name}"]:::default\n'

        # Add relationships
        diagram += "\n    %% Dependencies\n"

        # Show key dependencies to avoid clutter
        important_deps = self._get_important_dependencies()

        for source_file, target_file, relationship_type in important_deps:
            source_id = self._sanitize_node_id(source_file)
            target_id = self._sanitize_node_id(target_file)

            if relationship_type == 'critical':
                diagram += f"    {source_id} ==> {target_id}\n"
            elif relationship_type == 'important':
                diagram += f"    {source_id} --> {target_id}\n"
            else:
                diagram += f"    {source_id} -.-> {target_id}\n"

        # Add circular dependency warnings
        if self.circular_dependencies:
            diagram += "\n    %% Circular Dependencies (Warning)\n"
            for i, cycle in enumerate(self.circular_dependencies[:3], 1):  # Show first 3
                for j in range(len(cycle) - 1):
                    source_id = self._sanitize_node_id(cycle[j])
                    target_id = self._sanitize_node_id(cycle[j + 1])
                    diagram += f"    {source_id} -.-> {target_id}\n"

        # Add styling
        diagram += self._get_component_styles()

        diagram += "```\n"

        return diagram

    def generate_dependency_graph_diagram(self) -> str:
        """Generate focused dependency relationship diagrams"""

        # Find most connected components
        central_components = self._find_central_components(limit=8)

        diagram = "```mermaid\nflowchart LR\n"

        # Create subgraphs for different layers
        layers = self._organize_components_by_layer(central_components)

        for layer_name, components in layers.items():
            if components:
                diagram += f"\n    subgraph {layer_name}\n"

                for comp in components:
                    node_id = self._sanitize_node_id(comp['file'])
                    display_name = Path(comp['file']).stem
                    dependents = comp['dependents']

                    # Size node based on connection count
                    if dependents > 5:
                        diagram += f'        {node_id}["{display_name}<br/>({dependents} deps)"]:::high\n'
                    elif dependents > 2:
                        diagram += f'        {node_id}["{display_name}<br/>({dependents} deps)"]:::medium\n'
                    else:
                        diagram += f'        {node_id}["{display_name}"]:::low\n'

                diagram += "    end\n"

        # Add cross-layer dependencies
        diagram += "\n    %% Layer Interactions\n"

        layer_deps = self._get_cross_layer_dependencies(layers)
        for source_id, target_id, dep_type in layer_deps:
            if dep_type == 'heavy':
                diagram += f"    {source_id} ===> {target_id}\n"
            else:
                diagram += f"    {source_id} --> {target_id}\n"

        # Add dependency styling
        diagram += """
    classDef high fill:#ff6b6b,stroke:#d63031,stroke-width:3px,color:#fff
    classDef medium fill:#74b9ff,stroke:#0984e3,stroke-width:2px,color:#fff
    classDef low fill:#55a3ff,stroke:#2d3436,stroke-width:1px,color:#fff
"""

        diagram += "```\n"

        return diagram

    def generate_security_model_diagram(self) -> str:
        """Generate security architecture visualization"""

        # Find security-related components
        security_components = self._find_security_components()

        if not security_components:
            return "```mermaid\ngraph TD\n    A[No Security Components Detected]\n```\n"

        diagram = "```mermaid\nflowchart TD\n"

        # Define security zones
        diagram += "\n    %% Security Zones\n"
        diagram += '    subgraph Public["Public Zone"]\n'
        diagram += "        Client[Client/Browser]:::client\n"
        diagram += "    end\n\n"

        diagram += '    subgraph DMZ["DMZ"]\n'

        # Add API gateway/entry points
        entry_points = security_components.get('entry_points', [])
        for entry in entry_points:
            node_id = self._sanitize_node_id(entry)
            display_name = Path(entry).stem
            diagram += f'        {node_id}["{display_name}"]:::api\n'

        diagram += "    end\n\n"

        diagram += '    subgraph Internal["Internal Zone"]\n'

        # Add authentication components
        auth_components = security_components.get('authentication', [])
        for auth in auth_components:
            node_id = self._sanitize_node_id(auth)
            display_name = Path(auth).stem
            diagram += f'        {node_id}["{display_name}"]:::auth\n'

        # Add business logic components
        business_components = security_components.get('business_logic', [])
        for biz in business_components:
            node_id = self._sanitize_node_id(biz)
            display_name = Path(biz).stem
            diagram += f'        {node_id}["{display_name}"]:::service\n'

        diagram += "    end\n\n"

        diagram += '    subgraph Data["Data Zone"]\n'

        # Add data components
        data_components = security_components.get('data', [])
        for data in data_components:
            node_id = self._sanitize_node_id(data)
            display_name = Path(data).stem
            diagram += f'        {node_id}[("{display_name}")]:::data\n'

        diagram += "    end\n\n"

        # Add security flows
        diagram += "    %% Security Flow\n"
        diagram += "    Client --> |HTTPS| "
        if entry_points:
            diagram += f"{self._sanitize_node_id(entry_points[0])}\n"

            if auth_components:
                diagram += f"    {self._sanitize_node_id(entry_points[0])} --> |Auth Check| {self._sanitize_node_id(auth_components[0])}\n"

                if business_components:
                    diagram += f"    {self._sanitize_node_id(auth_components[0])} --> |Authorized| {self._sanitize_node_id(business_components[0])}\n"

                    if data_components:
                        diagram += f"    {self._sanitize_node_id(business_components[0])} --> |Data Access| {self._sanitize_node_id(data_components[0])}\n"

        # Add security styling
        diagram += """
    classDef client fill:#e17055,stroke:#d63031,stroke-width:2px,color:#fff
    classDef api fill:#fd79a8,stroke:#e84393,stroke-width:2px,color:#fff
    classDef auth fill:#fdcb6e,stroke:#e17055,stroke-width:3px,color:#fff
    classDef service fill:#6c5ce7,stroke:#5f3dc4,stroke-width:2px,color:#fff
    classDef data fill:#00b894,stroke:#00a085,stroke-width:3px,color:#fff
"""

        diagram += "```\n"

        return diagram

    def generate_component_interaction_diagram(self) -> str:
        """Generate diagram showing how components interact"""

        # Find interaction patterns
        interaction_patterns = self._analyze_interaction_patterns()

        diagram = "```mermaid\nsequenceDiagram\n"

        # Define participants
        participants = set()
        for pattern in interaction_patterns:
            participants.update(pattern['participants'])

        diagram += "    participant User\n"
        for participant in sorted(participants)[:8]:  # Limit participants
            display_name = Path(participant).stem
            diagram += f"    participant {self._sanitize_node_id(participant)} as {display_name}\n"

        # Add interaction sequences
        diagram += "\n    %% Common Interaction Flows\n"

        for pattern in interaction_patterns[:3]:  # Show top 3 patterns
            diagram += f"\n    Note over User, {self._sanitize_node_id(pattern['participants'][-1])}: {pattern['name']}\n"

            current_actor = "User"
            for step in pattern['steps']:
                target = self._sanitize_node_id(step['target'])
                action = step['action']
                diagram += f"    {current_actor} ->> {target}: {action}\n"

                if step.get('return'):
                    diagram += f"    {target} -->> {current_actor}: {step['return']}\n"

                current_actor = target

        diagram += "```\n"

        return diagram

    def _categorize_components_for_diagram(self) -> Dict[str, List[str]]:
        """Categorize components for visual organization"""

        categories = defaultdict(list)

        for file_path, file_info in self.file_inventory.items():
            purpose = file_info.get('purpose', {})
            primary_role = purpose.get('primary_role', 'utility')

            # Map roles to diagram categories
            if primary_role in ['entry_point', 'application']:
                categories['entry_point'].append(file_path)
            elif primary_role in ['api', 'controller', 'web_server']:
                categories['api'].append(file_path)
            elif primary_role in ['service']:
                categories['service'].append(file_path)
            elif primary_role in ['data_model']:
                categories['data_model'].append(file_path)
            elif primary_role in ['ui_component', 'react_component']:
                categories['ui_component'].append(file_path)
            elif primary_role in ['configuration']:
                categories['configuration'].append(file_path)
            elif primary_role in ['test']:
                categories['test'].append(file_path)
            else:
                categories['utility'].append(file_path)

        return dict(categories)

    def _get_important_dependencies(self) -> List[tuple]:
        """Get important dependencies to avoid diagram clutter"""

        dependencies = []

        # Get central components
        central_files = [comp['file'] for comp in self._find_central_components(limit=15)]
        central_set = set(central_files)

        for source_file, deps in self.dependency_graph.items():
            if source_file not in central_set:
                continue

            imports = deps.get('imports_from', [])
            imported_by = deps.get('imported_by', [])

            # Prioritize relationships involving central components
            for target_file in imports:
                if target_file in central_set:
                    # Both are central - critical relationship
                    dependencies.append((source_file, target_file, 'critical'))
                elif len(self.dependency_graph.get(target_file, {}).get('imported_by', [])) > 3:
                    # Target is important
                    dependencies.append((source_file, target_file, 'important'))
                else:
                    dependencies.append((source_file, target_file, 'normal'))

        # Deduplicate and limit
        return list(set(dependencies))[:30]

    def _find_central_components(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Find most connected components"""

        component_scores = []

        for file_path, deps in self.dependency_graph.items():
            imported_by_count = len(deps.get('imported_by', []))
            imports_count = len(deps.get('imports_from', []))

            # Score based on connections (weighted toward being imported)
            score = imported_by_count * 2 + imports_count

            component_scores.append({
                'file': file_path,
                'dependents': imported_by_count,
                'dependencies': imports_count,
                'score': score
            })

        # Sort by score and return top components
        component_scores.sort(key=lambda x: x['score'], reverse=True)
        return component_scores[:limit]

    def _organize_components_by_layer(self, components: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize components into architectural layers"""

        layers = {
            'Presentation': [],
            'API': [],
            'Business': [],
            'Data': []
        }

        for comp in components:
            file_path = comp['file']
            file_info = self.file_inventory.get(file_path, {})
            purpose = file_info.get('purpose', {})
            primary_role = purpose.get('primary_role', 'utility')

            if primary_role in ['ui_component', 'react_component']:
                layers['Presentation'].append(comp)
            elif primary_role in ['api', 'controller', 'web_server']:
                layers['API'].append(comp)
            elif primary_role in ['service']:
                layers['Business'].append(comp)
            elif primary_role in ['data_model']:
                layers['Data'].append(comp)
            else:
                # Assign to closest layer based on dependencies
                imports = self.dependency_graph.get(file_path, {}).get('imports_from', [])

                # Simple heuristic based on what it imports
                if any('model' in imp.lower() or 'data' in imp.lower() for imp in imports):
                    layers['Business'].append(comp)
                else:
                    layers['API'].append(comp)

        return layers

    def _get_cross_layer_dependencies(self, layers: Dict[str, List[Dict]]) -> List[tuple]:
        """Get dependencies between architectural layers"""

        layer_components = {}
        for layer_name, components in layers.items():
            layer_components[layer_name] = [comp['file'] for comp in components]

        cross_layer_deps = []

        for layer_name, components in layer_components.items():
            for comp_file in components:
                comp_id = self._sanitize_node_id(comp_file)
                deps = self.dependency_graph.get(comp_file, {})

                for target_file in deps.get('imports_from', []):
                    # Find which layer the target is in
                    for target_layer, target_components in layer_components.items():
                        if target_file in target_components and target_layer != layer_name:
                            target_id = self._sanitize_node_id(target_file)

                            # Determine dependency weight
                            function_usage = deps.get('functions_used', {}).get(target_file, [])
                            dep_type = 'heavy' if len(function_usage) > 3 else 'normal'

                            cross_layer_deps.append((comp_id, target_id, dep_type))

        return cross_layer_deps

    def _find_security_components(self) -> Dict[str, List[str]]:
        """Categorize components by security function"""

        security_components = {
            'entry_points': [],
            'authentication': [],
            'business_logic': [],
            'data': []
        }

        for file_path, file_info in self.file_inventory.items():
            path_lower = file_path.lower()
            file_content = str(file_info).lower()

            # Entry points
            if any(pattern in path_lower for pattern in ['main', 'app', 'server', 'index']):
                security_components['entry_points'].append(file_path)

            # Authentication
            elif any(pattern in path_lower or pattern in file_content
                    for pattern in ['auth', 'login', 'session', 'token', 'passport']):
                security_components['authentication'].append(file_path)

            # Data layer
            elif any(pattern in path_lower or pattern in file_content
                    for pattern in ['model', 'database', 'schema', 'repo']):
                security_components['data'].append(file_path)

            # Business logic (services, controllers)
            else:
                purpose = file_info.get('purpose', {})
                if purpose.get('primary_role') in ['service', 'controller']:
                    security_components['business_logic'].append(file_path)

        return security_components

    def _analyze_interaction_patterns(self) -> List[Dict[str, Any]]:
        """Analyze common interaction patterns for sequence diagram"""

        patterns = []

        # Find API request patterns
        api_files = [f for f, info in self.file_inventory.items()
                    if info.get('purpose', {}).get('primary_role') in ['api', 'controller']]

        if api_files:
            # Trace typical API flow
            api_file = api_files[0]
            api_deps = self.dependency_graph.get(api_file, {})

            participants = [api_file]
            steps = [{'target': api_file, 'action': 'HTTP Request', 'return': 'Response'}]

            # Find service layer
            for dep_file in api_deps.get('imports_from', []):
                dep_info = self.file_inventory.get(dep_file, {})
                if dep_info.get('purpose', {}).get('primary_role') == 'service':
                    participants.append(dep_file)
                    steps.append({
                        'target': dep_file,
                        'action': 'Process Business Logic',
                        'return': 'Result'
                    })

                    # Find data layer
                    service_deps = self.dependency_graph.get(dep_file, {})
                    for data_file in service_deps.get('imports_from', []):
                        data_info = self.file_inventory.get(data_file, {})
                        if data_info.get('purpose', {}).get('primary_role') == 'data_model':
                            participants.append(data_file)
                            steps.append({
                                'target': data_file,
                                'action': 'Data Operation',
                                'return': 'Data'
                            })
                            break
                    break

            patterns.append({
                'name': 'API Request Flow',
                'participants': participants,
                'steps': steps
            })

        return patterns

    def _sanitize_node_id(self, file_path: str) -> str:
        """Convert file path to valid Mermaid node ID"""
        # Remove path separators and special characters
        node_id = file_path.replace('/', '_').replace('\\\\', '_').replace('.', '_')
        node_id = re.sub(r'[^a-zA-Z0-9_]', '_', node_id)

        # Ensure it starts with a letter
        if node_id and not node_id[0].isalpha():
            node_id = 'N_' + node_id

        return node_id or 'unknown'

    def _get_component_styles(self) -> str:
        """Get CSS styling for component types"""

        return """
    classDef entry fill:#ff6b6b,stroke:#d63031,stroke-width:3px,color:#fff
    classDef api fill:#fd79a8,stroke:#e84393,stroke-width:2px,color:#fff
    classDef service fill:#6c5ce7,stroke:#5f3dc4,stroke-width:2px,color:#fff
    classDef data fill:#00b894,stroke:#00a085,stroke-width:2px,color:#fff
    classDef ui fill:#74b9ff,stroke:#0984e3,stroke-width:2px,color:#fff
    classDef config fill:#fdcb6e,stroke:#e17055,stroke-width:1px,color:#fff
    classDef default fill:#b2bec3,stroke:#636e72,stroke-width:1px,color:#2d3436
"""


@click.command()
@click.argument('analysis_dir', type=click.Path(exists=True))
@click.option('--output', '-o', required=True, help='Output directory for visual diagrams')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(analysis_dir, output, verbose):
    """Generate enhanced architectural diagrams"""

    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    generator = EnhancedDiagramGenerator()
    generator.load_analysis_data(analysis_dir)

    print("🎨 Generating enhanced architectural diagrams...")

    # Generate detailed architecture diagram
    arch_diagram = generator.generate_detailed_architecture_diagram()
    arch_file = output_path / 'detailed-architecture.md'
    with open(arch_file, 'w') as f:
        f.write("# Detailed Architecture Diagram\n\n")
        f.write(arch_diagram)
    print(f"🏗️ Architecture diagram saved to: {arch_file}")

    # Generate dependency graph diagram
    dep_diagram = generator.generate_dependency_graph_diagram()
    dep_file = output_path / 'dependency-graphs.md'
    with open(dep_file, 'w') as f:
        f.write("# Dependency Relationship Diagrams\n\n")
        f.write(dep_diagram)
    print(f"📊 Dependency diagram saved to: {dep_file}")

    # Generate security model diagram
    security_diagram = generator.generate_security_model_diagram()
    security_file = output_path / 'security-model.md'
    with open(security_file, 'w') as f:
        f.write("# Security Architecture Model\n\n")
        f.write(security_diagram)
    print(f"🔒 Security diagram saved to: {security_file}")

    # Generate component interaction diagram
    interaction_diagram = generator.generate_component_interaction_diagram()
    interaction_file = output_path / 'component-interactions.md'
    with open(interaction_file, 'w') as f:
        f.write("# Component Interaction Sequences\n\n")
        f.write(interaction_diagram)
    print(f"🔄 Interaction diagram saved to: {interaction_file}")

    print("✅ All enhanced diagrams generated successfully")


if __name__ == '__main__':
    main()

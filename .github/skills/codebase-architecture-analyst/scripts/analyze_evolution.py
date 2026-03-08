#!/usr/bin/env python3
"""
Evolution Analysis Script for Codebase Architecture Analyst

This script analyzes architectural evolution by comparing analysis results
across different timestamps for the same project.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict

class ArchitecturalEvolutionAnalyzer:
    def __init__(self, project_name: str, base_path: str = "code-analysis-results"):
        self.project_name = project_name
        self.base_path = Path(base_path)
        self.project_path = self.base_path / project_name
        self.versions = []
        self.evolution_data = {}
        
    def analyze_evolution(self) -> Dict:
        """Analyze architectural evolution across all versions."""
        self._discover_versions()
        
        if len(self.versions) < 2:
            return {
                'message': 'Insufficient data for evolution analysis',
                'versions_found': len(self.versions),
                'requires_minimum': 2
            }
        
        self._load_version_data()
        evolution_analysis = {
            'project_name': self.project_name,
            'analysis_period': {
                'start': self.versions[0],
                'end': self.versions[-1],
                'total_versions': len(self.versions)
            },
            'architectural_changes': self._analyze_architectural_changes(),
            'dependency_evolution': self._analyze_dependency_evolution(),
            'pattern_evolution': self._analyze_pattern_evolution(),
            'security_evolution': self._analyze_security_evolution(),
            'complexity_trends': self._analyze_complexity_trends(),
            'summary': self._generate_evolution_summary()
        }
        
        return evolution_analysis
    
    def _discover_versions(self):
        """Discover all analysis versions for the project."""
        if not self.project_path.exists():
            return
        
        version_dirs = []
        for item in self.project_path.iterdir():
            if item.is_dir() and item.name != 'latest':
                # Check if it's a timestamp format (YYYY-MM-DD-HH-MM-SS)
                try:
                    datetime.strptime(item.name, "%Y-%m-%d-%H-%M-%S")
                    version_dirs.append(item.name)
                except ValueError:
                    continue
        
        self.versions = sorted(version_dirs)
    
    def _load_version_data(self):
        """Load analysis data for all versions."""
        for version in self.versions:
            version_path = self.project_path / version
            version_data = {}
            
            # Load JSON files
            for json_file in ['dependencies.json', 'patterns.json', 'security.json']:
                file_path = version_path / json_file
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            version_data[json_file.replace('.json', '')] = json.load(f)
                    except Exception as e:
                        version_data[json_file.replace('.json', '')] = {'error': str(e)}
            
            self.evolution_data[version] = version_data
    
    def _analyze_architectural_changes(self) -> Dict:
        """Analyze changes in architectural patterns over time."""
        architectural_changes = {
            'style_changes': [],
            'pattern_adoption': [],
            'pattern_removal': [],
            'framework_changes': []
        }
        
        prev_version = None
        for version in self.versions:
            if prev_version is None:
                prev_version = version
                continue
            
            prev_patterns = self.evolution_data.get(prev_version, {}).get('patterns', {})
            curr_patterns = self.evolution_data.get(version, {}).get('patterns', {})
            
            # Compare architecture styles
            prev_style = prev_patterns.get('architecture_style')
            curr_style = curr_patterns.get('architecture_style')
            
            if prev_style != curr_style:
                architectural_changes['style_changes'].append({
                    'from_version': prev_version,
                    'to_version': version,
                    'from_style': prev_style,
                    'to_style': curr_style
                })
            
            # Compare framework adoption
            prev_frameworks = prev_patterns.get('framework_info', {})
            curr_frameworks = curr_patterns.get('framework_info', {})
            
            framework_diff = self._compare_frameworks(prev_frameworks, curr_frameworks)
            if framework_diff:
                architectural_changes['framework_changes'].append({
                    'version': version,
                    'changes': framework_diff
                })
            
            prev_version = version
        
        return architectural_changes
    
    def _analyze_dependency_evolution(self) -> Dict:
        """Analyze how dependencies evolved over time."""
        dependency_evolution = {
            'external_deps_added': [],
            'external_deps_removed': [],
            'internal_structure_changes': [],
            'dependency_growth': []
        }
        
        prev_version = None
        for version in self.versions:
            if prev_version is None:
                prev_version = version
                continue
            
            prev_deps = self.evolution_data.get(prev_version, {}).get('dependencies', {})
            curr_deps = self.evolution_data.get(version, {}).get('dependencies', {})
            
            # Analyze external dependencies
            prev_external = set()
            curr_external = set()
            
            for file_deps in prev_deps.get('external_dependencies', {}).values():
                prev_external.update(file_deps)
            
            for file_deps in curr_deps.get('external_dependencies', {}).values():
                curr_external.update(file_deps)
            
            added_deps = curr_external - prev_external
            removed_deps = prev_external - curr_external
            
            if added_deps:
                dependency_evolution['external_deps_added'].append({
                    'version': version,
                    'dependencies': list(added_deps)
                })
            
            if removed_deps:
                dependency_evolution['external_deps_removed'].append({
                    'version': version,
                    'dependencies': list(removed_deps)
                })
            
            # Track dependency growth
            dependency_evolution['dependency_growth'].append({
                'version': version,
                'external_count': len(curr_external),
                'internal_files': len(curr_deps.get('internal_dependencies', {})),
                'total_files': len(curr_deps.get('file_types', {}))
            })
            
            prev_version = version
        
        return dependency_evolution
    
    def _analyze_pattern_evolution(self) -> Dict:
        """Analyze how design and architectural patterns evolved."""
        pattern_evolution = {
            'patterns_introduced': [],
            'patterns_deprecated': [],
            'pattern_confidence_changes': []
        }
        
        prev_version = None
        for version in self.versions:
            if prev_version is None:
                prev_version = version
                continue
            
            prev_patterns = self.evolution_data.get(prev_version, {}).get('patterns', {}).get('patterns', {})
            curr_patterns = self.evolution_data.get(version, {}).get('patterns', {}).get('patterns', {})
            
            # Extract pattern types from each version
            prev_pattern_types = set()
            curr_pattern_types = set()
            
            for category in prev_patterns.values():
                for pattern in category:
                    if isinstance(pattern, dict) and 'type' in pattern:
                        prev_pattern_types.add(pattern['type'])
            
            for category in curr_patterns.values():
                for pattern in category:
                    if isinstance(pattern, dict) and 'type' in pattern:
                        curr_pattern_types.add(pattern['type'])
            
            introduced = curr_pattern_types - prev_pattern_types
            deprecated = prev_pattern_types - curr_pattern_types
            
            if introduced:
                pattern_evolution['patterns_introduced'].append({
                    'version': version,
                    'patterns': list(introduced)
                })
            
            if deprecated:
                pattern_evolution['patterns_deprecated'].append({
                    'version': version,
                    'patterns': list(deprecated)
                })
            
            prev_version = version
        
        return pattern_evolution
    
    def _analyze_security_evolution(self) -> Dict:
        """Analyze security pattern evolution over time."""
        security_evolution = {
            'security_improvements': [],
            'new_security_patterns': [],
            'security_degradations': []
        }
        
        prev_version = None
        for version in self.versions:
            if prev_version is None:
                prev_version = version
                continue
            
            prev_security = self.evolution_data.get(prev_version, {}).get('security', {})
            curr_security = self.evolution_data.get(version, {}).get('security', {})
            
            # Count security patterns by type
            prev_counts = self._count_security_patterns(prev_security)
            curr_counts = self._count_security_patterns(curr_security)
            
            improvements = []
            degradations = []
            
            for pattern_type in set(list(prev_counts.keys()) + list(curr_counts.keys())):
                prev_count = prev_counts.get(pattern_type, 0)
                curr_count = curr_counts.get(pattern_type, 0)
                
                if curr_count > prev_count:
                    improvements.append({
                        'pattern': pattern_type,
                        'increase': curr_count - prev_count
                    })
                elif curr_count < prev_count:
                    degradations.append({
                        'pattern': pattern_type,
                        'decrease': prev_count - curr_count
                    })
            
            if improvements:
                security_evolution['security_improvements'].append({
                    'version': version,
                    'improvements': improvements
                })
            
            if degradations:
                security_evolution['security_degradations'].append({
                    'version': version,
                    'degradations': degradations
                })
            
            prev_version = version
        
        return security_evolution
    
    def _analyze_complexity_trends(self) -> Dict:
        """Analyze complexity and size trends over time."""
        complexity_trends = {
            'file_count_trend': [],
            'dependency_complexity_trend': [],
            'pattern_complexity_trend': []
        }
        
        for version in self.versions:
            version_data = self.evolution_data.get(version, {})
            
            # File count trend
            file_types = version_data.get('dependencies', {}).get('file_types', {})
            total_files = sum(file_types.values())
            
            complexity_trends['file_count_trend'].append({
                'version': version,
                'total_files': total_files,
                'file_types': len(file_types)
            })
            
            # Dependency complexity
            external_deps = version_data.get('dependencies', {}).get('external_dependencies', {})
            internal_deps = version_data.get('dependencies', {}).get('internal_dependencies', {})
            
            total_external = sum(len(deps) for deps in external_deps.values())
            total_internal = sum(len(deps) for deps in internal_deps.values())
            
            complexity_trends['dependency_complexity_trend'].append({
                'version': version,
                'external_dependencies': total_external,
                'internal_dependencies': total_internal,
                'dependency_ratio': total_external / max(total_internal, 1)
            })
            
            # Pattern complexity
            patterns = version_data.get('patterns', {}).get('patterns', {})
            pattern_count = sum(len(pattern_list) for pattern_list in patterns.values())
            
            complexity_trends['pattern_complexity_trend'].append({
                'version': version,
                'total_patterns': pattern_count,
                'pattern_categories': len(patterns)
            })
        
        return complexity_trends
    
    def _compare_frameworks(self, prev_frameworks: Dict, curr_frameworks: Dict) -> List[Dict]:
        """Compare framework information between versions."""
        changes = []
        
        all_keys = set(prev_frameworks.keys()) | set(curr_frameworks.keys())
        for key in all_keys:
            prev_val = prev_frameworks.get(key)
            curr_val = curr_frameworks.get(key)
            
            if prev_val != curr_val:
                changes.append({
                    'type': key,
                    'from': prev_val,
                    'to': curr_val,
                    'change_type': 'added' if prev_val is None else 'removed' if curr_val is None else 'changed'
                })
        
        return changes
    
    def _count_security_patterns(self, security_data: Dict) -> Dict[str, int]:
        """Count security patterns by type."""
        counts = defaultdict(int)
        
        for category, patterns in security_data.items():
            for pattern in patterns:
                if isinstance(pattern, dict) and 'type' in pattern:
                    counts[pattern['type']] += 1
        
        return dict(counts)
    
    def _generate_evolution_summary(self) -> Dict:
        """Generate high-level evolution summary."""
        if len(self.versions) < 2:
            return {'message': 'Insufficient data for summary'}
        
        first_version = self.versions[0]
        latest_version = self.versions[-1]
        
        first_data = self.evolution_data.get(first_version, {})
        latest_data = self.evolution_data.get(latest_version, {})
        
        # Calculate growth metrics
        first_deps = first_data.get('dependencies', {})
        latest_deps = latest_data.get('dependencies', {})
        
        first_external = sum(len(deps) for deps in first_deps.get('external_dependencies', {}).values())
        latest_external = sum(len(deps) for deps in latest_deps.get('external_dependencies', {}).values())
        
        first_files = sum(first_deps.get('file_types', {}).values())
        latest_files = sum(latest_deps.get('file_types', {}).values())
        
        return {
            'analysis_span': {
                'start_date': first_version,
                'end_date': latest_version,
                'total_analyses': len(self.versions)
            },
            'growth_metrics': {
                'file_growth': {
                    'start': first_files,
                    'end': latest_files,
                    'change': latest_files - first_files,
                    'growth_rate': ((latest_files - first_files) / max(first_files, 1)) * 100
                },
                'dependency_growth': {
                    'start': first_external,
                    'end': latest_external,
                    'change': latest_external - first_external,
                    'growth_rate': ((latest_external - first_external) / max(first_external, 1)) * 100
                }
            },
            'architectural_stability': {
                'architecture_style_changes': len([c for c in self.evolution_data if 'architecture_style' in str(c)]),
                'framework_changes': len([c for c in self.evolution_data if 'framework' in str(c)])
            }
        }

def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze architectural evolution across versions')
    parser.add_argument('project_name', help='Name of the project to analyze')
    parser.add_argument('--base-path', default='code-analysis-results', 
                       help='Base path for analysis results')
    parser.add_argument('--output', help='Output file for evolution analysis (JSON)')
    
    args = parser.parse_args()
    
    analyzer = ArchitecturalEvolutionAnalyzer(args.project_name, args.base_path)
    results = analyzer.analyze_evolution()
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Evolution analysis saved to {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))

if __name__ == '__main__':
    main()
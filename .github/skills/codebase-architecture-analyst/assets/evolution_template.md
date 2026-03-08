# {{PROJECT_NAME}} - Architectural Evolution Analysis

*Evolution analysis generated on {{DATE}} covering {{TOTAL_VERSIONS}} versions from {{START_DATE}} to {{END_DATE}}*

## Executive Summary

{{PROJECT_NAME}} has evolved through {{TOTAL_VERSIONS}} analyzed versions, showing {{GROWTH_TREND}} in system complexity and {{ARCHITECTURAL_STABILITY}} architectural stability. Key changes include {{KEY_CHANGES_SUMMARY}}.

**Analysis Period**: {{START_DATE}} → {{END_DATE}}  
**Total Versions Analyzed**: {{TOTAL_VERSIONS}}  
**Overall Growth**: {{OVERALL_GROWTH_PERCENTAGE}}%

## Evolution Timeline

```mermaid
gantt
    title Architectural Evolution Timeline
    dateFormat  YYYY-MM-DD
    section Analysis Versions
    {{#VERSIONS}}
    Version {{VERSION_NUMBER}} : {{VERSION_DATE}}, 1d
    {{/VERSIONS}}
```

## Architectural Changes Over Time

### Architecture Style Evolution
{{#STYLE_CHANGES}}
- **{{FROM_VERSION}} → {{TO_VERSION}}**: Changed from {{FROM_STYLE}} to {{TO_STYLE}}
{{/STYLE_CHANGES}}

{{#NO_STYLE_CHANGES}}
✅ **Architectural Style Stable**: No architectural pattern changes detected across versions
{{/NO_STYLE_CHANGES}}

### Framework and Technology Evolution
{{#FRAMEWORK_CHANGES}}
**{{VERSION}}**: 
{{#CHANGES}}
- {{CHANGE_TYPE}}: {{TYPE}} changed from {{FROM}} to {{TO}}
{{/CHANGES}}
{{/FRAMEWORK_CHANGES}}

{{#NO_FRAMEWORK_CHANGES}}
✅ **Technology Stack Stable**: No framework changes detected across versions
{{/NO_FRAMEWORK_CHANGES}}

## Dependency Evolution

### External Dependencies Trend
{{#EXTERNAL_DEPS_ADDED}}
**{{VERSION}}** - Added Dependencies:
{{#DEPENDENCIES}}
- `{{DEPENDENCY}}`
{{/DEPENDENCIES}}
{{/EXTERNAL_DEPS_ADDED}}

{{#EXTERNAL_DEPS_REMOVED}}
**{{VERSION}}** - Removed Dependencies:
{{#DEPENDENCIES}}
- `{{DEPENDENCY}}`
{{/DEPENDENCIES}}
{{/EXTERNAL_DEPS_REMOVED}}

### Dependency Growth Metrics
```mermaid
graph LR
    subgraph "Dependency Growth"
        A[{{FIRST_VERSION}}<br/>{{FIRST_DEPS}} deps] --> B[{{LATEST_VERSION}}<br/>{{LATEST_DEPS}} deps]
    end
    
    C[Growth Rate<br/>{{DEPENDENCY_GROWTH_RATE}}%] --> B
```

| Version | External Deps | Internal Files | Total Files |
|---------|---------------|----------------|-------------|
{{#DEPENDENCY_GROWTH}}
| {{VERSION}} | {{EXTERNAL_COUNT}} | {{INTERNAL_FILES}} | {{TOTAL_FILES}} |
{{/DEPENDENCY_GROWTH}}

## Pattern Evolution Analysis

### Pattern Adoption Over Time
{{#PATTERNS_INTRODUCED}}
**{{VERSION}}** - New Patterns Detected:
{{#PATTERNS}}
- {{PATTERN}}
{{/PATTERNS}}
{{/PATTERNS_INTRODUCED}}

{{#PATTERNS_DEPRECATED}}
**{{VERSION}}** - Patterns No Longer Detected:
{{#PATTERNS}}
- {{PATTERN}}
{{/PATTERNS}}
{{/PATTERNS_DEPRECATED}}

### Pattern Maturity Progression
The system shows {{PATTERN_MATURITY_TREND}} in architectural pattern adoption, indicating {{PATTERN_ANALYSIS_SUMMARY}}.

## Security Evolution

### Security Improvements
{{#SECURITY_IMPROVEMENTS}}
**{{VERSION}}** - Security Enhancements:
{{#IMPROVEMENTS}}
- {{PATTERN}}: {{INCREASE}} additional instances detected
{{/IMPROVEMENTS}}
{{/SECURITY_IMPROVEMENTS}}

### Security Trend Analysis
{{#SECURITY_DEGRADATIONS}}
⚠️ **{{VERSION}}** - Potential Security Concerns:
{{#DEGRADATIONS}}
- {{PATTERN}}: {{DECREASE}} fewer instances detected
{{/DEGRADATIONS}}
{{/SECURITY_DEGRADATIONS}}

{{#NO_SECURITY_CHANGES}}
✅ **Security Patterns Stable**: No significant changes in security pattern detection
{{/NO_SECURITY_CHANGES}}

## Complexity and Growth Trends  

### System Size Evolution
```mermaid
graph LR
    subgraph "System Growth"
        A[{{FIRST_VERSION}}<br/>{{FIRST_FILES}} files] --> B[{{LATEST_VERSION}}<br/>{{LATEST_FILES}} files]
    end
    
    C[Growth Rate<br/>{{FILE_GROWTH_RATE}}%] --> B
```

### Complexity Metrics Over Time

| Metric | First Version | Latest Version | Change | Trend |
|--------|---------------|----------------|---------|-------|
| **Total Files** | {{FIRST_FILES}} | {{LATEST_FILES}} | {{FILE_CHANGE}} | {{FILE_TREND}} |
| **External Dependencies** | {{FIRST_EXTERNAL_DEPS}} | {{LATEST_EXTERNAL_DEPS}} | {{EXTERNAL_DEPS_CHANGE}} | {{EXTERNAL_DEPS_TREND}} |
| **Pattern Complexity** | {{FIRST_PATTERNS}} | {{LATEST_PATTERNS}} | {{PATTERN_CHANGE}} | {{PATTERN_TREND}} |
| **Dependency Ratio** | {{FIRST_RATIO}} | {{LATEST_RATIO}} | {{RATIO_CHANGE}} | {{RATIO_TREND}} |

## Evolution Insights and Recommendations

### System Maturity Assessment
{{SYSTEM_MATURITY_ASSESSMENT}}

### Architectural Health Trends
{{#POSITIVE_TRENDS}}
✅ **Positive Trends**:
{{#TRENDS}}
- {{TREND_DESCRIPTION}}
{{/TRENDS}}
{{/POSITIVE_TRENDS}}

{{#AREAS_OF_CONCERN}}
⚠️ **Areas of Concern**:
{{#CONCERNS}}
- {{CONCERN_DESCRIPTION}}
{{/CONCERNS}}
{{/AREAS_OF_CONCERN}}

### Future Evolution Recommendations
{{#RECOMMENDATIONS}}
1. **{{RECOMMENDATION_CATEGORY}}**: {{RECOMMENDATION_DESCRIPTION}}
{{/RECOMMENDATIONS}}

## Technical Evolution Summary

### Architecture Stability Score
**{{STABILITY_SCORE}}/10** - {{STABILITY_ASSESSMENT}}

### Growth Sustainability Rating  
**{{SUSTAINABILITY_SCORE}}/10** - {{SUSTAINABILITY_ASSESSMENT}}

### Evolution Velocity
**{{EVOLUTION_VELOCITY}}** - {{VELOCITY_DESCRIPTION}}

## Detailed Analysis Files

- **[dependencies.json](latest/dependencies.json)** - Latest dependency analysis
- **[patterns.json](latest/patterns.json)** - Current architectural patterns
- **[security.json](latest/security.json)** - Security analysis findings
- **[architecture.md](latest/architecture.md)** - Current architecture diagram
- **[documentation.md](latest/documentation.md)** - Latest comprehensive documentation

### Historical Versions
{{#HISTORICAL_VERSIONS}}
- **[{{VERSION_DATE}}]({{VERSION_DATE}}/)** - Analysis from {{FORMATTED_DATE}}
{{/HISTORICAL_VERSIONS}}

---

## Analysis Metadata

**Evolution Analysis Tool**: Architectural Evolution Analyzer  
**Analysis Date**: {{ANALYSIS_DATE}}  
**Project**: {{PROJECT_NAME}}  
**Versions Analyzed**: {{TOTAL_VERSIONS}}  
**Analysis Span**: {{ANALYSIS_SPAN_DAYS}} days  
**Data Sources**: Dependencies, Patterns, Security, Complexity metrics

**Generated by**: Codebase Architecture Analyst - Evolution Analysis Module
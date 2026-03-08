# Dependency Query Guide

This reference provides comprehensive guidance for interactive dependency exploration and querying.

## Query Types and Patterns

### Direct Dependency Queries

#### "What depends on X?"
**Purpose**: Find all files that import or use a specific file
**Example Queries**:
- "What files depend on UserService.py?"
- "What depends on auth.js?"
- "Show me what imports database.py"

**Response Format**:
```json
{
  "target_file": "src/services/UserService.py",
  "imported_by": ["src/api/users.py", "src/controllers/auth.py"],
  "functions_used_by": {
    "src/api/users.py": ["get_user", "create_user"],
    "src/controllers/auth.py": ["authenticate_user"]
  },
  "impact_scope": ["src/api/users.py", "src/controllers/auth.py", "src/tests/test_auth.py"]
}
```

#### "What does X depend on?"
**Purpose**: Find all dependencies of a specific file
**Example Queries**:
- "What does main.py depend on?"
- "Show dependencies of UserController"
- "What imports does auth.js have?"

**Response Format**:
```json
{
  "source_file": "src/controllers/UserController.py",
  "imports_from": ["src/services/UserService.py", "src/models/User.py"],
  "functions_used_from": {
    "src/services/UserService.py": ["get_user", "create_user", "update_user"],
    "src/models/User.py": ["User"]
  },
  "classes_used_from": {
    "src/models/User.py": ["User", "UserRole"]
  }
}
```

### Hierarchical Dependency Queries

#### "Show dependency tree for X"
**Purpose**: Display hierarchical view of dependencies
**Example Queries**:
- "dependency tree for authentication system"
- "Show me the dependency tree for main.py"
- "Hierarchical dependencies of UserService"

**Response Structure**:
```json
{
  "root_file": "src/auth/authentication.py",
  "dependency_tree": {
    "file": "src/auth/authentication.py",
    "dependencies": [
      {
        "file": "src/models/User.py",
        "dependencies": [
          {"file": "src/database/connection.py", "dependencies": []}
        ]
      },
      {
        "file": "src/utils/encryption.py",
        "dependencies": []
      }
    ]
  }
}
```

### Impact Analysis Queries

#### "If I change X, what else is affected?"
**Purpose**: Analyze the impact radius of modifying a file
**Example Queries**:
- "If I modify DatabaseService, what is affected?"
- "Impact analysis for changing User.py"
- "What breaks if I update authentication.js?"

**Response Structure**:
```json
{
  "target_file": "src/models/User.py",
  "direct_impact": ["src/services/UserService.py", "src/api/users.py"],
  "transitive_impact": ["src/controllers/AuthController.py", "src/tests/test_users.py"],
  "total_affected_files": 4,
  "risk_assessment": "Medium - Moderate dependencies"
}
```

### Function-Level Queries

#### "What functions from X are used by Y?"
**Purpose**: Examine specific function usage between files
**Example Queries**:
- "What functions from utils.py are used by main.py?"
- "Which UserService functions does AuthController use?"
- "Show function usage between database.py and models.py"

**Response Structure**:
```json
{
  "source_file": "src/utils/helpers.py",
  "target_file": "src/services/UserService.py",
  "functions_used": ["validate_email", "hash_password", "generate_token"],
  "function_count": 3,
  "relationship": "Direct dependency"
}
```

### System-Wide Queries

#### "Show circular dependencies"
**Purpose**: Identify dependency cycles in the codebase
**Example Queries**:
- "Find circular dependencies"
- "Show dependency cycles"
- "Are there any circular imports?"

**Response Structure**:
```json
{
  "circular_dependencies": [
    ["src/models/User.py", "src/services/UserService.py", "src/models/User.py"],
    ["src/auth/session.py", "src/auth/middleware.py", "src/auth/session.py"]
  ],
  "count": 2,
  "affected_files": ["src/models/User.py", "src/services/UserService.py", "src/auth/session.py", "src/auth/middleware.py"]
}
```

#### "What are the entry points?"
**Purpose**: Find main files and system entry points
**Example Queries**:
- "Show entry points"
- "What are the main files?"
- "Find application entry points"

**Response Structure**:
```json
{
  "entry_points": [
    {"file": "src/main.py", "reason": "Main file pattern: main.py"},
    {"file": "src/app.py", "reason": "No internal dependencies"},
    {"file": "server.js", "reason": "Main file pattern: server.js"}
  ],
  "count": 3
}
```

## Natural Language Processing Patterns

### Query Pattern Recognition

**Dependency Pattern**: `what.*depend.*on.*(\S+)`
- Matches: "what depends on UserService?"
- Matches: "what files depend on authentication.py?"

**Reverse Dependency Pattern**: `what.*does.*(\S+).*depend`
- Matches: "what does main.py depend on?"
- Matches: "what does UserController depend on?"

**Tree Pattern**: `dependency tree|dep tree.*for.*(\S+)`
- Matches: "dependency tree for authentication"
- Matches: "show dep tree for main.py"

**Impact Pattern**: `impact.*chang.*(\S+)|chang.*(\S+).*impact`
- Matches: "impact of changing UserService"
- Matches: "if I change database.py what is impacted?"

### Fuzzy File Matching

**Exact Match Priority**:
1. Full path match: `src/services/UserService.py`
2. Filename match: `UserService.py`
3. Partial path match: `services/UserService`

**Partial Matching Strategies**:
- Case-insensitive substring matching
- Word boundary matching for compound names
- Extension-agnostic matching (`UserService` matches `UserService.py`)

## Query Response Guidelines

### Success Response Structure
```json
{
  "query_type": "dependency_analysis",
  "target": "UserService.py",
  "result": { /* query-specific data */ },
  "suggestions": ["Try: 'impact of changing UserService'", "Related: 'what uses UserService functions'"]
}
```

### Error Response Structure
```json
{
  "error": "File 'UserService' not found",
  "candidates": ["src/services/UserService.py", "tests/UserServiceTest.py"],
  "suggestion": "Please be more specific or choose from candidates"
}
```

### Ambiguity Resolution
```json
{
  "error": "Multiple files match 'config'",
  "candidates": ["src/config.py", "tests/config.json", "config/settings.py"],
  "suggestion": "Please specify the full path or be more specific"
}
```

## Advanced Query Capabilities

### Filtered Dependency Analysis

**By File Type**:
- "Show Python dependencies for UserService"
- "JavaScript imports for main.js"

**By Layer/Category**:
- "API dependencies for authentication"
- "Database dependencies for user management"

**By Relationship Strength**:
- "Heavy dependencies of UserService" (many functions used)
- "Light dependencies of utils.py" (few functions used)

### Temporal Query Patterns

**Change Impact Over Time**:
- "What would break if we remove deprecated functions from UserService?"
- "Dependencies that would be affected by UserService refactoring"

**Evolution Queries**:
- "How have UserService dependencies changed?"
- "New dependencies since last analysis"

## Query Optimization Strategies

### Caching Frequently Requested Data
- Central component lists
- Impact analysis for critical files
- Common dependency paths

### Result Limiting for Large Codebases
- Top N most important dependencies
- Hierarchical truncation at depth limits
- Sampling for very large result sets

### Performance Considerations
- Pre-compute common query results
- Index files by multiple attributes (name, path, type)
- Cache dependency graph traversals

## Interactive Query Session Flow

### Session Initialization
1. Load all analysis data (dependency graph, file inventory, etc.)
2. Build reverse lookup indices for fast searching
3. Validate data completeness and report any gaps

### Query Processing Pipeline
1. **Parse** natural language query using regex patterns
2. **Resolve** file/component references using fuzzy matching
3. **Execute** appropriate query against dependency database
4. **Format** results in human-readable structure
5. **Suggest** related or follow-up queries

### Error Handling and Recovery
- Graceful handling of ambiguous queries
- Helpful error messages with suggestions
- Multiple resolution options for unclear references
- Context-aware query interpretation
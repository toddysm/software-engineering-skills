# Source File Analysis Patterns

This reference document provides patterns and guidelines for analyzing individual source files in depth.

## File Purpose Detection Patterns

### Path-Based Indicators

**Test Files**:
- Path contains: `test/`, `tests/`, `__tests__/`, `spec/`
- Filename patterns: `test_*.py`, `*.test.js`, `*.spec.ts`
- Confidence: High (0.9)

**Configuration Files**:
- Path contains: `config/`, `settings/`, `conf/`
- Filename patterns: `config.py`, `settings.json`, `.env`
- Purpose: System configuration and environment setup
- Confidence: High (0.8)

**Utility/Helper Files**:
- Path contains: `util/`, `utils/`, `helper/`, `helpers/`
- Common patterns: `utils.py`, `helpers.js`, `common.ts`
- Purpose: Shared functionality and utilities
- Confidence: High (0.8)

**Data Model Files**:
- Path contains: `model/`, `models/`, `schema/`, `entities/`
- Filename patterns: `*Model.py`, `*Schema.js`, `*.model.ts`
- Purpose: Data structure definitions
- Confidence: High (0.8)

**API/Controller Files**:
- Path contains: `api/`, `controller/`, `controllers/`, `handler/`, `routes/`
- Filename patterns: `*Controller.py`, `*Handler.js`, `routes.ts`
- Purpose: HTTP request handling and API endpoints
- Confidence: High (0.8)

### Content-Based Indicators

**Web Server Files**:
- Keywords: `express(`, `app.get(`, `@app.route`, `Flask(__name__)`
- Purpose: Web server and application entry points
- Confidence: Very High (0.9)

**React Components**:
- Keywords: `import React`, `from 'react'`, `JSX.Element`, `useState`
- Purpose: UI component development
- Confidence: Very High (0.85)

**Database Models**:
- Keywords: `class.*Model`, `SQLAlchemy`, `mongoose.Schema`, `@Entity`
- Purpose: Database entity definitions
- Confidence: High (0.85)

**Authentication Files**:
- Keywords: `login`, `authenticate`, `passport`, `jwt`, `auth`, `session`
- Purpose: Authentication and authorization logic
- Confidence: High (0.8)

## Documentation Extraction Patterns

### Python Documentation

**Module-Level Docstrings**:
```python
"""
This module handles user authentication and session management.
Provides login, logout, and session validation functionality.
"""
```

**Function Docstrings**:
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user with username and password.
    
    Args:
        username: The user's username
        password: The user's password
        
    Returns:
        True if authentication successful, False otherwise
    """
```

**Header Comments**:
```python
# User Authentication Module
# Author: John Doe
# Created: 2023-01-01
# Purpose: Handle all user authentication logic
```

### JavaScript/TypeScript Documentation

**JSDoc Comments**:
```javascript
/**
 * Handles user authentication and session management
 * @param {string} username - The user's username
 * @param {string} password - The user's password
 * @returns {Promise<boolean>} Authentication result
 */
```

**Header Comments**:
```javascript
// User Authentication Service
// Manages login/logout and session validation
// Dependencies: jwt, bcrypt, express-session
```

### README-Style Headers

Files with extensive header comments (3+ lines) often contain:
- File purpose and overview
- Author and creation information
- Dependencies and requirements
- Usage examples
- Change history

## Complexity Analysis

### Cyclomatic Complexity Indicators

**Control Flow Keywords**:
- Conditionals: `if`, `elif`, `else`, `switch`, `case`
- Loops: `for`, `while`, `do`
- Exception Handling: `try`, `catch`, `except`, `finally`
- Ternary Operators: `? :` (JavaScript), `if-else` expressions (Python)

**Complexity Scoring**:
- Simple (0-10): Basic linear code with minimal branching
- Moderate (11-20): Some conditional logic and loops
- Complex (21-30): Multiple nested conditions and loops
- Very Complex (30+): Highly branched logic requiring refactoring

### Function and Class Analysis

**Function Extraction**:
- Extract function signatures, parameters, return types
- Identify public vs private functions (naming conventions)
- Map function relationships (calls, callbacks, inheritance)

**Class Analysis**:
- Identify inheritance relationships
- Extract public/private methods and properties
- Analyze class responsibility and cohesion

## Single Responsibility Assessment

### Responsibility Indicators

**Mixed Concerns Detection**:
- Database + UI logic in same file
- Authentication + Business logic mixing
- Configuration + Processing logic together

**Cohesion Patterns**:
- Single domain focus (all user-related functions)
- Consistent abstraction level (all high-level or low-level)
- Clear interface boundaries

### File Responsibility Categories

**High Cohesion Indicators**:
- Single primary purpose (auth, data, UI, etc.)
- Related functions that work together
- Clear, focused file naming
- Consistent dependency patterns

**Low Cohesion Warnings**:
- Multiple unrelated responsibilities
- High function count (>20 functions)
- Mixed abstraction levels
- Scattered dependency patterns

## Import and Export Analysis

### Internal vs External Dependencies

**Internal Dependencies** (Project Files):
- Relative imports: `./`, `../`
- Project package imports
- Local module references

**External Dependencies** (Third-Party):
- NPM packages: `react`, `express`, `lodash`
- Python packages: `flask`, `requests`, `pandas`
- Standard library: `os`, `sys`, `fs`, `path`

**Framework Detection**:
- React: `react`, `react-dom`, JSX usage
- Flask: `flask`, `@app.route` decorators
- Express: `express`, `app.get/post` methods
- Django: `django`, model inheritance patterns

## Export Analysis

### Public Interface Detection

**Python Exports**:
- Functions/classes without leading underscore
- `__all__` variable contents
- Module-level definitions

**JavaScript Exports**:
- `export function/class/const`
- `module.exports = `
- `export default`
- `exports.functionName`

### API Surface Analysis

**Function Categorization**:
- Public API functions (exported, documented)
- Internal helper functions (not exported)
- Legacy functions (deprecated, unused)

**Interface Completeness**:
- Well-documented public functions
- Clear parameter and return types
- Consistent naming conventions
- Adequate error handling
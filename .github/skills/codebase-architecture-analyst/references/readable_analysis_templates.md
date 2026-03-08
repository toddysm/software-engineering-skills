# Human-Readable Analysis Templates

This reference provides templates and guidelines for generating plain English analysis reports.

## Security Analysis Templates

### Security Overview Structure

```markdown
# Security Overview

## Security Strengths

✅ **Authentication Implementation**: JWT tokens with HTTP-only cookies provide secure session management
✅ **Password Security**: Bcrypt hashing detected with appropriate salt rounds
✅ **Input Validation**: Validation middleware found in 8 API endpoint files
✅ **Environment Configuration**: Secrets properly externalized using environment variables

## Security Concerns

⚠️ **High Priority**: SQL injection vulnerability in user search functionality
   *Affected files: src/api/search.py, src/database/queries.py*

⚠️ **Medium Priority**: API endpoints lack rate limiting protection
   *Affected files: src/api/users.py, src/api/orders.py (and 3 others)*

⚠️ **Medium Priority**: Cross-site scripting (XSS) risk in comment rendering
   *Affected files: src/components/CommentDisplay.jsx*

## Security Recommendations

1. **Implement parameterized queries** to prevent SQL injection in search functionality
2. **Add rate limiting middleware** to all public API endpoints using express-rate-limit or similar
3. **Sanitize user input** before rendering in UI components, especially user-generated content
4. **Enable CSRF protection** for state-changing operations
5. **Add security headers** (HSTS, CSP, X-Frame-Options) to all HTTP responses
```

### Security Analysis Language Patterns

**Strength Descriptions**:
- "implements secure X using Y methodology"
- "properly configured Z with appropriate settings"
- "follows security best practices for X"
- "adequately protected against Y vulnerabilities"

**Concern Descriptions**:
- "lacks protection against X attacks"
- "vulnerable to Y due to Z implementation"
- "exposes sensitive data through X"
- "insufficient validation of Y inputs"

**Recommendation Language**:
- "Implement X to prevent Y vulnerabilities"
- "Consider adding Z to improve X security"
- "Replace Y with more secure Z approach"
- "Enable X protection for Y functionality"

## Architecture Analysis Templates

### Architecture Overview Structure

```markdown
# Architecture Overview

## System Type

This is a **Full-Stack Web Application** with a React frontend, Express.js backend, and PostgreSQL database.

*Architecture indicators: React components detected, REST API structure, web server patterns, database models*

## Technology Stack

**Frontend**: React, TypeScript, Material-UI
**Backend**: Node.js, Express.js, TypeScript  
**Database**: PostgreSQL, Sequelize ORM
**Build Tools**: Webpack, Babel, npm
**Testing**: Jest, React Testing Library

## Component Organization

The system is organized into 47 main components across 4 directory levels. The code is well organized.

**Main directories**: src, components, services, api, models

## Data Flow & Patterns

The system follows MVC (Model-View-Controller) and Layered Architecture patterns for clear separation of concerns. 

**Key patterns**: REST API design, Component-based UI, Service layer abstraction

## System Coupling

The system has moderate coupling. Files have reasonable dependencies, showing balanced coupling.

## Architectural Strengths

✅ Clear separation between frontend and backend concerns
✅ Consistent API design with RESTful endpoints  
✅ Good documentation coverage (78% of files)
✅ No circular dependencies detected
✅ Well-structured component hierarchy in React frontend

## Architectural Concerns

⚠️ High complexity in user management module (UserService.py has 25+ dependencies)
⚠️ Some API endpoints lack proper error handling middleware
⚠️ Database query logic mixed with business logic in 3 service files
```

### Architecture Language Patterns

**System Type Descriptions**:
- "a monolithic application with X, Y, and Z components"
- "a microservices architecture with N independent services"
- "a full-stack web application with X frontend and Y backend"
- "a serverless system using X cloud functions"

**Organization Quality Indicators**:
- "simply organized" (≤2 directory levels)
- "well organized" (3-4 directory levels)
- "complexly organized" (5+ directory levels)

**Coupling Descriptions**:
- "low coupling - good separation of concerns"
- "moderate coupling - balanced dependencies"  
- "high coupling - may impact maintainability"

## Component Guide Templates

### Component Relationship Structure

```markdown
# Component Guide

## Central Components

These components are heavily used throughout the system. Changes here have wide impact:

### UserService

**File**: `src/services/UserService.py`

**Used by**: 8 other components

**Purpose**: Service - Handles user authentication, profile management, and user data operations

**Key dependent files**: UserController.py, AuthMiddleware.py, ProfileAPI.py (and 5 others)

### DatabaseConnection

**File**: `src/database/connection.py`  

**Used by**: 12 other components

**Purpose**: Data Model - Manages database connections and query execution

**Key dependent files**: UserModel.py, OrderModel.py, SessionStore.py (and 9 others)

## Component Categories

### API Components (8 files)

- **UserController**: `src/api/UserController.py` - Handles HTTP requests for user operations
- **OrderController**: `src/api/OrderController.py` - Manages order-related API endpoints  
- **AuthController**: `src/api/AuthController.py` - Authentication and authorization endpoints
... and 5 other files

### Service Components (5 files)

- **UserService**: `src/services/UserService.py` - Core user business logic and data operations
- **EmailService**: `src/services/EmailService.py` - Email sending and template management
- **PaymentService**: `src/services/PaymentService.py` - Payment processing and validation logic

## Common Interaction Patterns

### API Request Flow

HTTP requests flow from controllers to services to data models for clean separation of concerns.

**Example**: UserController → UserService → UserModel → Database

### Service Integration Pattern  

Services communicate through well-defined interfaces for loose coupling.

**Example**: OrderService → PaymentService → EmailService

## Modification Guidance

**Modifying core components**: When changing UserService, DatabaseConnection, test thoroughly as these components affect many other parts of the system.

**API changes**: When modifying API endpoints, update documentation and consider backward compatibility for existing clients.

**Database schema changes**: When changing data models, create migration scripts and update all dependent services.
```

### Component Description Patterns

**Central Component Language**:
- "heavily used throughout the system"
- "central to X functionality"  
- "critical component affecting Y operations"
- "core infrastructure used by Z other files"

**Category Descriptions**:
- "handles HTTP requests and API endpoints"
- "manages business logic and data operations" 
- "provides shared utilities and helper functions"
- "defines data structures and database models"

**Interaction Descriptions**:
- "flow from X through Y to Z for clean separation"
- "communicate through well-defined interfaces"
- "delegate responsibilities to appropriate layers"

## Technology Decisions Templates

### Technology Analysis Structure

```markdown
# Technology Decisions Analysis

## Framework Choices

**React**: Component-based frontend architecture for maintainable UI development
*Alternative options: Vue.js, Angular, Svelte*

**Express.js**: Lightweight Node.js framework for flexible API development  
*Alternative options: Koa.js, Fastify, NestJS*

**PostgreSQL**: Relational database for complex data relationships and ACID compliance
*Alternative options: MySQL, MongoDB, SQLite*

## Architectural Decisions

**Service-oriented architecture**: Separation of concerns through dedicated service components improves maintainability and testability

**RESTful API design**: Standard HTTP methods and resource-based URLs provide clear, predictable interfaces

**Component-based frontend**: React components enable reusable UI elements and improved development workflow

## Recommendations

1. **Consider adding TypeScript** to improve code quality and developer experience
2. **Implement comprehensive logging** using structured logging framework like Winston
3. **Add API documentation** using OpenAPI/Swagger for better developer experience  
4. **Consider containerization** with Docker for consistent deployment environments
5. **Add monitoring and observability** tools for production system health tracking
```

### Technology Decision Language

**Choice Rationales**:
- "provides X benefit for Y use case"
- "enables Z capability while maintaining A constraint"  
- "industry standard for X type of applications"
- "balances performance, maintainability, and developer experience"

**Alternative Presentations**:
- "Alternative options: A, B, C with different tradeoffs"
- "Could also use X for Y benefits, but Z was chosen for A reasons"

## Report Generation Guidelines

### Language Style Guidelines

**Use Active Voice**:
- ✅ "The system implements authentication using JWT tokens"
- ❌ "JWT tokens are implemented by the system for authentication"

**Be Specific and Concrete**:
- ✅ "3 API endpoints lack input validation"  
- ❌ "Some endpoints have validation issues"

**Provide Context and Impact**:
- ✅ "High coupling in UserService (15 dependencies) may impact maintainability"
- ❌ "UserService has high coupling"

**Use Plain English but Stay Technical**:
- ✅ "The React frontend components are well-organized by feature"
- ❌ "Frontend employs component-based architectural paradigm with feature-driven modularization"

### Severity and Priority Language

**Security Priorities**:
- "Critical Priority: Immediate security risk requiring urgent attention"
- "High Priority: Significant security concern needing prompt resolution"  
- "Medium Priority: Important security improvement opportunity"
- "Low Priority: Minor security enhancement suggestion"

**Architecture Concerns**:
- "Critical Issue: System stability or performance risk"
- "Major Concern: Maintainability or scalability impact"
- "Minor Issue: Code quality or convention deviation"

### Recommendation Formatting

**Actionable Recommendations**:
- Start with action verb: "Implement", "Add", "Replace", "Consider"
- Include specific technology/approach when possible  
- Explain the benefit: "to improve X", "to prevent Y", "to enable Z"
- Provide context: "in the authentication module", "for API endpoints"

**Progressive Disclosure**:
- Start with high-level overview
- Provide specific details for interested readers
- Include examples and code snippets when helpful
- Link to relevant files and line numbers
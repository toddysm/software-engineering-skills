# Language and Framework Analysis

This reference provides framework-specific analysis approaches and patterns to look for in different technology stacks.

## Frontend Frameworks

### React Applications
**Key Files to Analyze:**
- `package.json` - Dependencies and scripts
- `src/App.js` - Main component and routing
- `src/components/` - Component structure
- `src/hooks/` - Custom hooks and state management
- `src/context/` or `src/store/` - Global state management

**Patterns to Look For:**
- Component composition and prop drilling
- State management (useState, useReducer, Redux, Zustand)
- Routing patterns (React Router)
- API integration (fetch, axios, React Query)
- Authentication flows
- Performance optimizations (useMemo, useCallback, lazy loading)

**Architecture Analysis:**
- Component hierarchy and reusability
- State management strategy
- Code splitting and lazy loading
- Testing approach (Jest, React Testing Library)

### Vue.js Applications
**Key Files to Analyze:**
- `src/main.js` - App initialization
- `src/router/` - Vue Router configuration
- `src/store/` - Vuex/Pinia store
- `src/components/` - Vue components
- `src/views/` - Page components

**Patterns to Look For:**
- Single File Components (.vue)
- Composition API vs Options API
- State management (Vuex, Pinia)
- Plugin usage and configuration

### Angular Applications
**Key Files to Analyze:**
- `src/main.ts` - Bootstrap configuration
- `src/app/` - Application modules and components
- `src/app/app-routing.module.ts` - Routing configuration
- `src/app/services/` - Injectable services
- `angular.json` - Project configuration

**Patterns to Look For:**
- Module organization and lazy loading
- Dependency injection patterns
- RxJS usage for async operations
- NgRx for state management
- Guard implementations for route protection

## Backend Frameworks

### Node.js/Express Applications
**Key Files to Analyze:**
- `package.json` - Dependencies and scripts
- `server.js` or `app.js` - Server configuration
- `routes/` - Route definitions
- `controllers/` - Request handlers
- `middleware/` - Custom middleware
- `models/` - Data models

**Patterns to Look For:**
- Middleware stack organization
- Route organization and versioning
- Database integration (Mongoose, Sequelize, Prisma)
- Authentication middleware (Passport, JWT)
- Error handling patterns
- API documentation (Swagger)

### Django Applications
**Key Files to Analyze:**
- `settings.py` - Django configuration
- `urls.py` - URL routing
- `models.py` - Database models
- `views.py` - Request handlers
- `serializers.py` - API serialization (DRF)
- `forms.py` - Form handling

**Patterns to Look For:**
- App organization and Django apps
- Model relationships and migrations
- Class-based vs function-based views
- Django REST Framework usage
- Custom middleware and decorators
- Admin interface customization

### Spring Boot Applications
**Key Files to Analyze:**
- `src/main/java/` - Java source code
- `application.properties` or `application.yml` - Configuration
- `@Controller` and `@RestController` classes
- `@Service` and `@Repository` classes
- `@Entity` classes - JPA entities

**Patterns to Look For:**
- Dependency injection with `@Autowired`
- Spring Security configuration
- Data access patterns (JPA, JDBC)
- Transaction management
- Exception handling with `@ControllerAdvice`
- Configuration classes with `@Configuration`

### .NET Applications
**Key Files to Analyze:**
- `Program.cs` - Application entry point
- `Startup.cs` - Service configuration (older versions)
- `Controllers/` - API controllers
- `Models/` - Data models
- `Services/` - Business logic services
- `appsettings.json` - Configuration

**Patterns to Look For:**
- Dependency injection container setup
- Middleware pipeline configuration
- Entity Framework usage
- Authentication and authorization
- API versioning strategies
- Background services

## Databases and Data Storage

### SQL Databases
**Files to Analyze:**
- Migration files
- Schema definitions
- Query optimization logs
- Connection string configurations

**Patterns to Look For:**
- Normalization strategies
- Indexing approaches
- Foreign key relationships
- Stored procedures vs application logic

### NoSQL Databases
**Files to Analyze:**
- Collection schemas
- Index definitions
- Query patterns in code

**Patterns to Look For:**
- Document structure design
- Aggregation pipelines
- Sharding strategies
- Consistency models

## Mobile Applications

### React Native
**Key Files to Analyze:**
- `App.js` - Main component
- `src/screens/` - Screen components
- `src/navigation/` - Navigation configuration
- `package.json` - Dependencies including native modules

**Patterns to Look For:**
- Navigation patterns (React Navigation)
- State management across screens
- Native module usage
- Platform-specific code

### Flutter
**Key Files to Analyze:**
- `lib/main.dart` - App entry point
- `lib/screens/` - Screen widgets
- `lib/widgets/` - Custom widgets
- `pubspec.yaml` - Dependencies

**Patterns to Look For:**
- Widget composition patterns
- State management (Provider, Bloc, Riverpod)
- Navigation and routing
- Platform channels for native code

## DevOps and Infrastructure

### Docker Configurations
**Files to Analyze:**
- `Dockerfile` - Container build instructions
- `docker-compose.yml` - Multi-service orchestration
- `.dockerignore` - Build context exclusions

### Kubernetes
**Files to Analyze:**
- `*.yaml` deployment files
- Service and ingress configurations
- ConfigMaps and Secrets

### CI/CD Pipelines
**Files to Analyze:**
- `.github/workflows/` - GitHub Actions
- `.gitlab-ci.yml` - GitLab CI
- `Jenkinsfile` - Jenkins pipelines
- `azure-pipelines.yml` - Azure DevOps
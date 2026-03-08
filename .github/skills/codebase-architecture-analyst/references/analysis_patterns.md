# Analysis Patterns

This reference contains common architectural patterns, design patterns, and code structures to look for during codebase analysis.

## Architectural Patterns

### Layered Architecture
**Indicators:**
- Clear separation of presentation, business, and data layers
- Folders like `controllers/`, `services/`, `models/`, `repositories/`
- Dependencies flow downward through layers

**Analysis Focus:**
- Layer boundaries and responsibilities
- Cross-cutting concerns (logging, auth, validation)
- Violation of layer separation

### Microservices Architecture
**Indicators:**
- Multiple deployable services/applications
- Service discovery mechanisms
- API gateways or load balancers
- Container orchestration files (docker-compose, k8s)

**Analysis Focus:**
- Service boundaries and responsibilities
- Inter-service communication patterns
- Data consistency strategies
- Deployment and monitoring setup

### Model-View-Controller (MVC)
**Indicators:**
- Folders: `models/`, `views/`, `controllers/`
- Clear separation of concern between data, presentation, and logic
- Framework conventions (Rails, Django, ASP.NET MVC)

**Analysis Focus:**
- Controller responsibilities and routing
- Model relationships and business logic
- View composition and templating

### Event-Driven Architecture
**Indicators:**
- Message queues (RabbitMQ, Apache Kafka)
- Event brokers and publishers/subscribers
- Async processing patterns
- Event sourcing implementations

**Analysis Focus:**
- Event flow and message schemas
- Processing pipelines
- Error handling and resilience

## Design Patterns

### Repository Pattern
**Indicators:**
- Interfaces defining data access methods
- Implementations for different data sources
- Dependency injection of repositories

### Factory Pattern
**Indicators:**
- Factory classes or methods
- Object creation abstraction
- Multiple implementations of interfaces

### Observer Pattern
**Indicators:**
- Event listeners and subscribers
- Notification systems
- State change propagation

### Strategy Pattern
**Indicators:**
- Interchangeable algorithms
- Policy objects
- Behavior parameterization

## Security Patterns

### Authentication & Authorization
**Look for:**
- JWT token handling
- OAuth implementations
- Role-based access control (RBAC)
- API key management
- Session management

### Input Validation
**Look for:**
- Input sanitization
- Parameter validation
- SQL injection prevention
- XSS protection
- CSRF protection

### Data Protection
**Look for:**
- Encryption at rest and in transit
- Secure configuration management
- Secrets management
- Data masking/anonymization

## Performance Patterns

### Caching Strategies
**Look for:**
- In-memory caches (Redis, Memcached)
- HTTP caching headers
- Database query caching
- CDN usage

### Asynchronous Processing
**Look for:**
- Background job queues
- Async/await patterns
- Non-blocking I/O
- Reactive programming

### Database Optimization
**Look for:**
- Connection pooling
- Query optimization
- Database indexing strategies
- Read replicas and sharding

## Integration Patterns

### API Design
**Look for:**
- REST API conventions
- GraphQL schemas
- API versioning strategies
- Rate limiting and throttling

### Message Queuing
**Look for:**
- Producer-consumer patterns
- Request-response messaging
- Publish-subscribe patterns
- Dead letter queues

## Common Anti-Patterns

### God Objects
- Classes with too many responsibilities
- Large files with mixed concerns
- Tight coupling between components

### Big Ball of Mud
- Lack of clear structure
- Mixed architectural styles
- High cyclomatic complexity

### Golden Hammer
- Over-reliance on single technology
- Inappropriate pattern usage
- One-size-fits-all solutions

## Language-Specific Patterns

### Go Patterns
**Concurrency Patterns:**
- Goroutines and channels
- Worker pools
- Pipeline patterns
- Fan-in/fan-out patterns

**Error Handling:**
- Error interface implementations
- Panic/recover mechanisms
- Explicit error returns

**Project Structure:**
- Package-based organization
- Internal packages for private APIs
- Standard project layout (cmd/, pkg/, internal/)

**Key Indicators:**
- `go.mod` and `go.sum` files
- Interface definitions ending in `-er` suffix
- Context propagation patterns

### Rust Patterns
**Memory Safety:**
- Ownership and borrowing patterns
- RAII (Resource Acquisition Is Initialization)
- Zero-cost abstractions

**Error Handling:**
- Result<T, E> types
- Option<T> for nullability
- Custom error types

**Project Structure:**
- Cargo.toml configuration
- Module system with mod.rs
- Crate organization (lib.rs, main.rs)

**Key Indicators:**
- Trait implementations
- Macro usage
- Lifetime annotations

### C# Patterns
**Framework Patterns:**
- ASP.NET Core middleware pipeline
- Dependency injection containers
- Entity Framework patterns
- LINQ expressions

**Async Patterns:**
- Task-based asynchronous programming
- ConfigureAwait usage
- CancellationToken propagation

**Project Structure:**
- Solution (.sln) and project (.csproj) files
- Namespace organization
- Package references (NuGet)

**Key Indicators:**
- Attribute-based programming
- Extension methods
- Properties and indexers

### C/C++ Patterns
**Memory Management:**
- RAII in C++
- Smart pointers (unique_ptr, shared_ptr)
- Manual memory management in C

**Build Patterns:**
- Header/source file separation
- Include guards or #pragma once
- Makefiles or CMake configuration

**Project Structure:**
- Header files (.h, .hpp)
- Source files (.c, .cpp)
- Library organization (static/dynamic)

**Key Indicators:**
- Template usage (C++)
- Function pointer patterns (C)
- Namespace organization (C++)

## Framework-Specific Indicators

### Web Frameworks
**Go:**
- Gin: `gin.Default()`, route handlers
- Echo: `echo.New()`, middleware chains
- Fiber: Fast HTTP framework patterns

**Rust:**
- Actix Web: Actor-based patterns
- Rocket: Attribute-based routing
- Axum: Handler functions with extractors

**C#:**
- ASP.NET Core: Controller/action patterns
- Minimal APIs: app.MapGet() patterns
- Blazor: Component-based UI

### ORM/Database Patterns
**Go:**
- GORM: Model definitions and migrations
- sqlx: Raw SQL with struct scanning

**Rust:**
- Diesel: Schema definitions and migrations
- SeaORM: Entity definitions

**C#:**
- Entity Framework: DbContext patterns
- Dapper: Micro-ORM patterns

## Language-Specific Patterns

### Python Patterns
**Code Organization:**
- Package structure with `__init__.py` files
- Module system with `__all__` exports
- Virtual environments (venv, conda, poetry)
- Configuration via `settings.py`, `.env`, or `pyproject.toml`

**Class & Function Patterns:**
- Dataclasses and NamedTuples for data containers
- Abstract base classes (ABC) for interfaces
- Property decorators (`@property`, `@cached_property`)
- Class/static methods (`@classmethod`, `@staticmethod`)
- Async functions and coroutines (`async def`, `await`)
- Decorator factories for cross-cutting concerns

**Framework Indicators:**
- Django: `models.Model`, `views.View`, `urls.py`, `migrations/`
- Flask: `@app.route`, `Blueprint`, `Flask(__name__)`
- FastAPI: `@router.get`, `Depends()`, Pydantic models
- SQLAlchemy: `Base.metadata`, `Column`, session management
- Celery: `@app.task`, `shared_task`, broker config
- Pytest: `def test_`, `@pytest.fixture`, conftest.py

**Quality Indicators:**
- Type annotations (PEP 484, Python 3.5+)
- Docstrings following Google/NumPy/Sphinx format
- `__repr__` and `__str__` implementations
- Context managers (`__enter__`/`__exit__`)
- `requirements.txt`, `Pipfile`, or `pyproject.toml` for dependencies

### Java Patterns
**Project Structure:**
- Maven/Gradle build files (`pom.xml`, `build.gradle`)
- Standard layout: `src/main/java`, `src/test/java`
- Package hierarchy mirroring domain (e.g., `com.company.feature`)
- Resource files in `src/main/resources`

**Design Patterns:**
- Annotation-based configuration (`@Component`, `@Service`, `@Repository`)
- Dependency injection with Spring or CDI
- Builder pattern (common for immutable objects)
- Factory and Strategy patterns
- Interface-based design for testability

**Framework Indicators:**
- Spring Boot: `@SpringBootApplication`, `@RestController`, `application.properties`
- Spring MVC: `@Controller`, `@RequestMapping`, `ModelAndView`
- JPA/Hibernate: `@Entity`, `@Table`, `EntityManager`, `@Repository`
- JUnit 5: `@Test`, `@ExtendWith`, `@BeforeEach`
- Lombok: `@Data`, `@Builder`, `@AllArgsConstructor`
- Quarkus: `@QuarkusTest`, `@Inject`, `@ConfigProperty`

**Quality Indicators:**
- Javadoc on public APIs
- Checked vs unchecked exceptions
- Immutable value objects
- Use of `Optional<T>` for null safety
- Interface segregation (many focused interfaces)

### JavaScript & TypeScript Patterns
**Module Systems:**
- ESM: `import`/`export` with `.mjs` or `"type": "module"` in package.json
- CommonJS: `require()`/`module.exports`
- TypeScript path aliases in `tsconfig.json`
- Barrel files (`index.ts`) re-exporting module contents

**React Patterns:**
- Functional components with hooks (`useState`, `useEffect`, `useContext`)
- Custom hooks (`use` prefix) for reusable stateful logic
- Context providers for global state
- React Query / SWR for server state management
- Component composition over inheritance
- Prop drilling vs state lifting

**TypeScript Specific:**
- Strict mode (`"strict": true` in tsconfig)
- Generic types and utility types (`Partial<T>`, `Record<K,V>`)
- Discriminated unions for type-safe variants
- Type guards (`is` predicates)
- Interface vs type alias trade-offs

**Node.js/Backend Patterns:**
- Express middleware chains
- NestJS modules, controllers, providers
- Event-driven patterns with EventEmitter
- Stream processing
- `async`/`await` with proper error handling

**Quality Indicators:**
- ESLint/Prettier configuration
- Jest/Vitest test coverage
- TSConfig strict flags
- Dependency injection (InversifyJS, tsyringe)
- OpenAPI/Swagger decorators

### Ruby Patterns
**Code Organization:**
- Convention over configuration (Rails way)
- Gems for dependency management (`Gemfile`, `Gemfile.lock`)
- Module namespacing with `::` (e.g., `Admin::User`)
- Monkey-patching and open classes (use sparingly)
- Mixins via `include`, `extend`, `prepend`

**Rails Specific:**
- MVC with Active Record, Action Controller, Action View
- Concerns for cross-cutting behavior (`app/concerns/`)
- Callbacks (`before_action`, `after_create`)
- Active Job for background jobs
- Hotwire/Turbo for modern UIs without heavy JS
- Database migrations in `db/migrate/`

**Ruby Idioms:**
- Blocks, procs, and lambdas
- Enumerable and Comparable modules
- Symbol to proc (`.map(&:method)`)
- Method missing for metaprogramming
- `attr_accessor`, `attr_reader`, `attr_writer`
- Single return value (implicit last expression)

**Framework Indicators:**
- Rails: `ApplicationController`, `ApplicationRecord`, `routes.rb`
- Sinatra: `get '/'`, `post '/'` route blocks
- Hanami: `Hanami::Action`, highly decoupled
- RSpec: `describe`, `context`, `it`, `let`, `subject`
- Devise: authentication scaffolding
- Sidekiq: `include Sidekiq::Worker`, `perform_async`

**Quality Indicators:**
- RuboCop compliance
- Comprehensive RSpec test suite
- YARD documentation
- Brakeman security scanning
- Service objects for complex business logic

### PHP Patterns
**Code Organization:**
- PSR-4 autoloading with Composer
- Namespace declarations at top of file
- `composer.json` for dependency management
- Separation of public web root and application code

**Laravel Specific:**
- Eloquent ORM (`Model`, `hasMany`, `belongsTo`)
- Artisan CLI commands
- Blade templating (`@foreach`, `@if`, `@yield`)
- Service containers (IoC) and facades
- Policies and gates for authorization
- Queues and jobs (`implements ShouldQueue`)
- Event listeners and observers

**Symfony Specific:**
- Services and dependency injection containers
- Twig templating engine
- Doctrine ORM integration
- Security voters and firewalls
- Console commands (`Console\Command`)

**PHP Idioms:**
- PHP 8 attributes (`#[Route('/')]`)
- Named arguments and match expressions
- Null safe operator (`$user?->getProfile()`)
- Union types and intersection types
- Fibers for coroutines (PHP 8.1+)
- Enums (PHP 8.1+)

**Quality Indicators:**
- PHPStan/Psalm static analysis
- PHPUnit or Pest test coverage
- PHPDoc blocks on classes and methods
- Type declarations on function signatures
- `declare(strict_types=1)` at file top

## Framework-Specific Detection Signatures

### Python Framework Detection
- **Django**: `INSTALLED_APPS`, `DATABASES`, `MIDDLEWARE` in settings; `urlpatterns` in urls.py
- **Flask**: `Flask(__name__)`, `@app.route`, `app.run()`
- **FastAPI**: `FastAPI()`, `@router.get`, `response_model=`
- **Celery**: `Celery(broker=)`, `@celery.task`

### Java Framework Detection
- **Spring Boot**: `@SpringBootApplication`, `application.yml`, `spring.datasource`
- **Quarkus**: `application.properties` with `quarkus.` prefix, `@QuarkusTest`
- **Micronaut**: `@MicronautTest`, `micronaut.application.yml`

### JavaScript/Node Framework Detection
- **Express**: `const app = express()`, `app.use()`, `app.listen()`
- **NestJS**: `@Module`, `@Controller`, `@Injectable`, `@Get`
- **Next.js**: `pages/` or `app/` router, `getServerSideProps`, `generateStaticParams`

### Ruby Framework Detection
- **Rails**: `config/routes.rb`, `app/` directory structure, `Gemfile` with `rails` gem
- **Sinatra**: `require 'sinatra'`, `get '/'`, `post '/'`

### PHP Framework Detection
- **Laravel**: `artisan`, `app/Http/Controllers/`, `routes/web.php`, `Illuminate\`
- **Symfony**: `symfony.lock`, `config/services.yaml`, `Symfony\Component\`
- **WordPress**: `wp-config.php`, `functions.php`, `wp_enqueue_script`
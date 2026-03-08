# Diagram Templates

This reference provides Mermaid diagram patterns and templates for visualizing different types of system architectures.

## Architecture Diagram Types

### System Context Diagrams
Use for showing high-level system boundaries and external interactions:

```mermaid
graph TB
    User[👤 User] --> WebApp[Web Application]
    Admin[👤 Admin] --> AdminPanel[Admin Panel]
    
    WebApp --> API[REST API]
    AdminPanel --> API
    
    API --> Database[(🗄️ Database)]
    API --> Cache[(⚡ Cache)]
    API --> EmailService[📧 Email Service]
    
    ExternalAPI[🌐 External API] --> API
```

### Layered Architecture
Use for traditional n-tier applications:

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[User Interface]
        Controllers[Controllers]
    end
    
    subgraph "Business Logic Layer"
        Services[Business Services]
        Validation[Validation]
    end
    
    subgraph "Data Access Layer"
        Repository[Repository]
        ORM[ORM/Data Mapper]
    end
    
    subgraph "Database Layer"
        DB[(Database)]
    end
    
    UI --> Controllers
    Controllers --> Services
    Services --> Validation
    Services --> Repository
    Repository --> ORM
    ORM --> DB
```

### Microservices Architecture
Use for distributed service architectures:

```mermaid
graph TB
    Client[👤 Client] --> Gateway[API Gateway]
    
    Gateway --> UserService[👤 User Service]
    Gateway --> OrderService[📦 Order Service]
    Gateway --> PaymentService[💳 Payment Service]
    Gateway --> NotificationService[📬 Notification Service]
    
    UserService --> UserDB[(👤 User DB)]
    OrderService --> OrderDB[(📦 Order DB)]
    PaymentService --> PaymentDB[(💳 Payment DB)]
    
    OrderService --> PaymentService
    OrderService --> NotificationService
    PaymentService --> NotificationService
    
    subgraph "Message Bus"
        EventBus[📨 Event Bus]
    end
    
    OrderService --> EventBus
    PaymentService --> EventBus
    NotificationService --> EventBus
```

### Component Architecture
Use for showing internal component relationships:

```mermaid
graph LR
    subgraph "Frontend Components"
        App[App Component]
        Header[Header]
        Sidebar[Sidebar]
        MainContent[Main Content]
        Footer[Footer]
    end
    
    subgraph "State Management"
        Store[Global Store]
        UserState[User State]
        AppState[App State]
    end
    
    subgraph "Services"
        APIService[API Service]
        AuthService[Auth Service]
        RouterService[Router Service]
    end
    
    App --> Header
    App --> Sidebar
    App --> MainContent
    App --> Footer
    
    MainContent --> Store
    Store --> UserState
    Store --> AppState
    
    APIService --> AuthService
    AuthService --> Store
    RouterService --> App
```

## Data Flow Diagrams

### Request-Response Flow
Use for showing how requests flow through the system:

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant Service
    participant Database
    
    Client->>Gateway: HTTP Request
    Gateway->>Auth: Validate Token
    Auth-->>Gateway: Token Valid
    Gateway->>Service: Forward Request
    Service->>Database: Query Data
    Database-->>Service: Return Data
    Service-->>Gateway: Response
    Gateway-->>Client: HTTP Response
```

### Event-Driven Flow
Use for asynchronous, event-based architectures:

```mermaid
graph LR
    Producer1[Producer 1] --> EventBus[Event Bus]
    Producer2[Producer 2] --> EventBus
    
    EventBus --> Consumer1[Consumer 1]
    EventBus --> Consumer2[Consumer 2]
    EventBus --> Consumer3[Consumer 3]
    
    Consumer1 --> Database1[(DB 1)]
    Consumer2 --> Database2[(DB 2)]
    Consumer3 --> ExternalAPI[External API]
```

## Database Architecture

### Relational Database Schema
Use for showing table relationships:

```mermaid
erDiagram
    Users ||--o{ Orders : places
    Users {
        int user_id PK
        string username
        string email
        datetime created_at
    }
    
    Orders ||--o{ OrderItems : contains
    Orders {
        int order_id PK
        int user_id FK
        decimal total_amount
        datetime order_date
    }
    
    Products ||--o{ OrderItems : included_in
    Products {
        int product_id PK
        string name
        decimal price
        int stock_quantity
    }
    
    OrderItems {
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
```

### NoSQL Database Structure
Use for showing document relationships:

```mermaid
graph TB
    UserCollection[👤 Users Collection]
    PostCollection[📝 Posts Collection]
    CommentCollection[💬 Comments Collection]
    
    UserDoc[User Document<br/>- id<br/>- username<br/>- profile]
    PostDoc[Post Document<br/>- id<br/>- user_id<br/>- content<br/>- timestamp]
    CommentDoc[Comment Document<br/>- id<br/>- post_id<br/>- user_id<br/>- content]
    
    UserCollection --> UserDoc
    PostCollection --> PostDoc
    CommentCollection --> CommentDoc
    
    PostDoc -.-> UserDoc
    CommentDoc -.-> PostDoc
    CommentDoc -.-> UserDoc
```

## Deployment Architecture

### Cloud Infrastructure
Use for showing cloud deployment structure:

```mermaid
graph TB
    subgraph "CDN"
        CloudFront[CloudFront CDN]
    end
    
    subgraph "Load Balancer"
        ALB[Application Load Balancer]
    end
    
    subgraph "Auto Scaling Group"
        EC2_1[EC2 Instance 1]
        EC2_2[EC2 Instance 2]
        EC2_3[EC2 Instance 3]
    end
    
    subgraph "Database"
        RDS_Primary[(RDS Primary)]
        RDS_Replica[(RDS Read Replica)]
    end
    
    subgraph "Cache"
        ElastiCache[(ElastiCache)]
    end
    
    subgraph "Storage"
        S3[S3 Bucket]
    end
    
    Users[👥 Users] --> CloudFront
    CloudFront --> ALB
    ALB --> EC2_1
    ALB --> EC2_2
    ALB --> EC2_3
    
    EC2_1 --> RDS_Primary
    EC2_2 --> RDS_Primary
    EC2_3 --> RDS_Primary
    
    EC2_1 --> RDS_Replica
    EC2_2 --> RDS_Replica
    EC2_3 --> RDS_Replica
    
    EC2_1 --> ElastiCache
    EC2_2 --> ElastiCache
    EC2_3 --> ElastiCache
    
    EC2_1 --> S3
    EC2_2 --> S3
    EC2_3 --> S3
```

### Container Orchestration
Use for Docker/Kubernetes deployments:

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Namespace: Production"
            subgraph "Frontend Pods"
                FE1[Frontend Pod 1]
                FE2[Frontend Pod 2]
            end
            
            subgraph "Backend Pods"
                BE1[Backend Pod 1]
                BE2[Backend Pod 2]
                BE3[Backend Pod 3]
            end
            
            subgraph "Database"
                DB[Database Pod]
                DBVolume[(Persistent Volume)]
            end
        end
        
        Ingress[Ingress Controller]
        Service1[Frontend Service]
        Service2[Backend Service]
    end
    
    Users[👥 Users] --> Ingress
    Ingress --> Service1
    Service1 --> FE1
    Service1 --> FE2
    
    FE1 --> Service2
    FE2 --> Service2
    Service2 --> BE1
    Service2 --> BE2
    Service2 --> BE3
    
    BE1 --> DB
    BE2 --> DB
    BE3 --> DB
    DB --> DBVolume
```

## Security Architecture

### Authentication Flow
Use for showing authentication and authorization:

```mermaid
graph TB
    User[👤 User] --> Login[Login Page]
    Login --> AuthService[Auth Service]
    AuthService --> OAuth[OAuth Provider]
    OAuth --> AuthService
    AuthService --> JWT[JWT Token]
    
    JWT --> APIGateway[API Gateway]
    APIGateway --> AuthMiddleware[Auth Middleware]
    AuthMiddleware --> Protected[Protected Resources]
    
    AuthService --> UserDB[(User Database)]
    AuthMiddleware --> TokenCache[(Token Cache)]
```

## Performance Architecture

### Caching Strategy
Use for showing caching layers:

```mermaid
graph TB
    Client[👤 Client] --> CDN[CDN Cache]
    CDN --> LoadBalancer[Load Balancer]
    
    LoadBalancer --> App1[App Server 1]
    LoadBalancer --> App2[App Server 2]
    
    App1 --> AppCache[Application Cache]
    App2 --> AppCache
    
    AppCache --> Database[(Database)]
    
    subgraph "Cache Layers"
        Browser[Browser Cache]
        CDN
        AppCache
        DBCache[Database Cache]
    end
    
    Database --> DBCache
```

## Template Selection Guide

**Choose diagram type based on analysis focus:**

- **System Context**: High-level overview, external dependencies
- **Layered Architecture**: Traditional applications with clear layers
- **Microservices**: Distributed systems with multiple services
- **Component**: Frontend applications, modular systems
- **Request-Response Flow**: API interactions, synchronous processing
- **Event-Driven Flow**: Asynchronous systems, message queues
- **Database Schema**: Data relationships, data architecture
- **Deployment**: Infrastructure, hosting, scalability
- **Security**: Authentication, authorization, security controls
- **Performance**: Caching, optimization, bottlenecks
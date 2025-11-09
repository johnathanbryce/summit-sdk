# Architecture Overview

## High-Level Concept

Summit SDK is an AI-powered content querying service that transforms web pages and text into interactive, queryable assets using a proprietary LLM.

## Core Components

### 1. SDK Packages (Frontend)

**@summit/core** - Core TypeScript SDK
- Framework-agnostic
- Handles API communication
- Query processing and caching
- TypeScript-first with full type safety

**@summit/ui** - React UI Components
- Optional headless components
- Unstyled and customizable
- Built with Mantine (headless mode)
- Framework: React 19

**@summit/types** - Shared Type Definitions
- TypeScript interfaces and types
- Shared across all packages
- Single source of truth for data structures

### 2. Backend Services (Python)

**API Gateway** (FastAPI)
- Authentication and rate limiting
- Request routing
- REST API endpoints
- Session management (Redis)

**Worker Service** (Python)
- LLM calls (Anthropic Claude)
- Web scraping and content extraction
- Background processing
- Queue management

**Ingestion Pipeline** (Premium Feature)
- Website crawling
- Content embedding generation
- Vector database management (Pinecone)
- Cross-document semantic search

### 3. Data Layer

**PostgreSQL**
- User accounts
- Billing metadata
- API usage metrics
- **Note:** Customer content is NOT stored here

**Redis**
- Session caching
- Rate limiting
- Temporary query results
- TTL-based data expiration

**Pinecone (Premium)**
- Vector embeddings for RAG
- Cross-website semantic search
- Customer-provided content only
- Clear TTL policies

**S3 (Optional)**
- File uploads (if needed)
- Backup storage

### 4. Applications

**Demo App** (Vite + React)
- Interactive SDK demonstration
- Testing and development
- Simple UI: input + submit + results

**Marketing Site** (Next.js)
- Landing page
- Pricing information
- Documentation portal
- Public-facing content

## Architecture Principles

### 1. Minimal Data Storage
- No website content stored unless explicitly required for premium features
- Clear TTLs on all cached data
- Privacy-first approach

### 2. Developer-First
- SDK over controlled UI (prevents styling conflicts)
- Framework-agnostic core
- Optional framework-specific accelerators
- Comprehensive TypeScript types

### 3. Monorepo Structure
- Unified version control
- Shared tooling and standards
- Efficient dependency management (pnpm workspaces)
- Clear separation of concerns

### 4. Scalability
- Stateless API services
- Horizontal scaling via App Runner
- Managed services (RDS, ElastiCache)
- CDN for static assets (CloudFront)

## Technology Stack

**Frontend:**
- TypeScript
- React 19
- Vite (bundler)
- Mantine (UI framework)

**Backend:**
- Python
- FastAPI (API gateway)
- Background workers

**AI & Data:**
- Anthropic Claude (LLM)
- Pinecone (vector database)
- Redis (cache)
- PostgreSQL (metadata)

**Infrastructure:**
- AWS App Runner (services)
- RDS PostgreSQL (database)
- ElastiCache Redis (cache)
- S3 (storage)
- CloudFront (CDN)

**Development:**
- pnpm workspaces (monorepo)
- Docker Compose (local dev)
- GitHub Actions (CI/CD)
- Vitest (testing - SDK)
- pytest (testing - backend)

## Data Flow

### Basic Query Flow

```
User App
  ↓ (uses @summit/core)
SDK Client
  ↓ (HTTPS request)
API Gateway (FastAPI)
  ↓ (enqueues job)
Worker Service
  ↓ (calls LLM)
Anthropic Claude
  ↓ (returns result)
Worker Service
  ↓ (caches in Redis)
API Gateway
  ↓ (JSON response)
SDK Client
  ↓
User App (displays result)
```

### Premium RAG Flow

```
Customer provides website URLs
  ↓
Ingestion Pipeline
  ↓ (crawls & extracts content)
Content Processing
  ↓ (generates embeddings)
Pinecone (stores vectors)
  ↓
User Query
  ↓
Worker retrieves relevant context from Pinecone
  ↓
LLM generates answer with full context
  ↓
Response to user
```

## Deployment Architecture

**Development:**
- Local Docker Compose (PostgreSQL, Redis)
- Local pnpm dev servers
- Mock API responses

**Staging:**
- AWS App Runner (API + Worker)
- RDS PostgreSQL
- ElastiCache Redis
- Separate from production

**Production:**
- AWS App Runner (auto-scaling)
- Multi-AZ RDS
- Multi-AZ ElastiCache
- CloudFront CDN
- Route 53 DNS

## Security

- All API communication over HTTPS
- API key authentication
- Rate limiting per user/key
- Secrets managed via AWS Secrets Manager
- No customer data in logs
- Regular security audits via Dependabot

## Future Considerations

- GraphQL API (alternative to REST)
- WebSocket support for real-time queries
- On-premise deployment option
- Additional LLM providers
- Multi-region support

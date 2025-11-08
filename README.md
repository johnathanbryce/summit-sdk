# Summit SDK

An SDK service that uses AI to turn any web page or text into an interactive, queryable asset.

## Project Structure

```
summit-sdk/
├── packages/          # TypeScript packages
│   ├── core/         # Pure TypeScript SDK
│   ├── react/        # React UI components
│   └── types/        # Shared TypeScript definitions
├── services/         # Backend services
│   ├── api/          # FastAPI gateway
│   └── worker/       # Background processing
├── apps/             # Applications
│   ├── marketing/    # Next.js landing site
│   └── demo/         # Demo application
├── infrastructure/   # Infrastructure as code
└── scripts/          # Build and deploy scripts
```

## Tech Stack

**Frontend / SDK**
- TypeScript, React 18, Mantine, Vite

**Backend Services**
- Python, FastAPI, Background workers

**AI & Data**
- Anthropic Claude, Pinecone, Redis, PostgreSQL

**Infrastructure**
- AWS (App Runner, RDS, ElastiCache), S3, CloudFront

## Getting Started

Documentation coming soon.

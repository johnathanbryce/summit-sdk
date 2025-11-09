# Summit SDK

> An SDK service that uses AI to turn any web page or text into an interactive, queryable asset.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pnpm](https://img.shields.io/badge/maintained%20with-pnpm-cc00ff.svg)](https://pnpm.io/)

## Overview

Summit SDK provides developers with a powerful, type-safe interface to transform web content and text into AI-queryable assets. Built with TypeScript and powered by Anthropic Claude, it offers both a framework-agnostic core SDK and optional UI components for rapid integration.

**Key Features:**

- 🤖 AI-powered content querying
- 📦 Framework-agnostic core SDK
- ⚛️ Optional headless React components
- 🔒 Type-safe with full TypeScript support
- 🎨 Fully customizable (no forced styling)
- 🚀 Premium RAG features for cross-document search

## Quick Start

### Installation

```bash
npm install @summit/core
# or
yarn add @summit/core
# or
pnpm add @summit/core
```

### Basic Usage

```typescript
import { SummitSDK } from '@summit/core'

const sdk = new SummitSDK({ apiKey: 'your-api-key' })

const result = await sdk.query('https://example.com', 'What is this page about?')

console.log(result.answer)
```

### With React Components

```bash
npm install @summit/core @summit/ui
```

```tsx
import { SummitSDK } from '@summit/core'
import { QueryInput } from '@summit/ui'

const sdk = new SummitSDK({ apiKey: 'your-api-key' })

function App() {
  const handleQuery = async (url: string, question: string) => {
    const result = await sdk.query(url, question)
    console.log(result)
  }

  return <QueryInput onSubmit={handleQuery} />
}
```

## Documentation

- 📖 [Documentation](docs/README.md)
- 🏗️ [Architecture Overview](docs/architecture/overview.md)
- 🚀 [Development Guide](docs/contributing/development.md)

## Project Structure

This is a monorepo managed with pnpm workspaces:

```
summit-sdk/
├── packages/          # Published SDK packages
│   ├── core/         # @summit/core - Core SDK (framework-agnostic)
│   ├── ui/           # @summit/ui - React UI components
│   └── types/        # @summit/types - Shared TypeScript types
├── apps/             # Applications
│   ├── demo/         # Demo app (Vite + React)
│   └── marketing/    # Marketing site (Next.js)
├── services/         # Backend services (Python)
│   ├── api/          # FastAPI gateway
│   └── worker/       # Background worker
├── docs/             # Documentation
└── infrastructure/   # Infrastructure as code
```

## Packages

| Package                         | Version     | Description                 |
| ------------------------------- | ----------- | --------------------------- |
| [@summit/core](packages/core)   | Coming soon | Core SDK functionality      |
| [@summit/ui](packages/ui)       | Coming soon | Optional React components   |
| [@summit/types](packages/types) | Coming soon | TypeScript type definitions |

## Tech Stack

**SDK & Frontend:**

- TypeScript
- React 19
- Vite (bundler)
- Mantine (UI components)

**Backend:**

- Python
- FastAPI (API gateway)
- Background workers

**AI & Data:**

- Anthropic Claude (LLM)
- Pinecone (vector database)
- Redis (caching)
- PostgreSQL (metadata)

**Infrastructure:**

- AWS App Runner
- RDS PostgreSQL
- ElastiCache Redis
- S3 & CloudFront

## Development

### Prerequisites

- Node.js >= 18
- pnpm >= 8
- Python >= 3.11 (for backend services)

### Setup

```bash
# Clone repository
git clone https://github.com/johnathanbryce/summit-sdk.git
cd summit-sdk

# Install dependencies
pnpm install

# Run demo app
pnpm dev

# Build all packages
pnpm build
```

See the [Development Guide](docs/contributing/development.md) for detailed instructions.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## Security

Please report security vulnerabilities to the email specified in [SECURITY.md](SECURITY.md). Do not open public issues for security concerns.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Documentation](docs/README.md)
- [Issues](https://github.com/johnathanbryce/summit-sdk/issues)
- [Changelog](CHANGELOG.md) - Coming soon

---

Built with ❤️ by [@johnathanbryce](https://github.com/johnathanbryce)

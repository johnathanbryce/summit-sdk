# Development Guide

Complete guide for setting up Summit SDK for local development.

## Prerequisites

### Required Software

- **Node.js** >= 18.0.0 ([Download](https://nodejs.org/))
- **pnpm** >= 8.0.0 (Package manager)
- **Git** (Version control)
- **Python** >= 3.11 (for backend services - coming soon)

### Check Versions

```bash
node --version   # Should be >= 18
pnpm --version   # Should be >= 8
git --version
python --version # Should be >= 3.11
```

### Install pnpm

If you don't have pnpm installed:

```bash
npm install -g pnpm
```

Or via Homebrew (macOS):

```bash
brew install pnpm
```

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/johnathanbryce/summit-sdk.git
cd summit-sdk
```

### 2. Install Dependencies

```bash
pnpm install
```

This will:

- Install all Node.js dependencies
- Create `node_modules/` folders
- Symlink workspace packages together
- Generate `pnpm-lock.yaml` (if not exists)

### 3. Verify Installation

```bash
# Check that packages are linked
ls -la node_modules/@summit

# Should see symlinks to local packages:
# @summit/core -> ../../packages/core
# @summit/ui -> ../../packages/ui
# @summit/types -> ../../packages/types
```

## Project Structure

```
summit-sdk/
├── packages/          # SDK packages (what we publish)
│   ├── core/         # Core SDK (@summit/core)
│   ├── ui/           # React components (@summit/ui)
│   └── types/        # Type definitions (@summit/types)
├── apps/             # Applications
│   ├── demo/         # Demo app (Vite + React)
│   └── marketing/    # Marketing site (Next.js)
├── services/         # Backend services (Python)
│   ├── api/          # FastAPI gateway
│   └── worker/       # Background worker
├── docs/             # Documentation
└── infrastructure/   # Infrastructure as code
```

## Development Workflow

### Building Packages

**Build all SDK packages:**

```bash
pnpm build
```

**Build specific package:**

```bash
pnpm --filter @summit/core build
```

**Build in watch mode:**

```bash
pnpm --filter @summit/core dev
```

### Running Applications

**Demo app (recommended for development):**

```bash
pnpm dev
# Opens at http://localhost:3000
```

**Marketing site:**

```bash
pnpm dev:marketing
# Opens at http://localhost:3000
```

### Making Changes

**Workflow for SDK changes:**

1. **Edit source code:**

   ```bash
   # Example: Edit core SDK
   code packages/core/src/index.ts
   ```

2. **Changes auto-available in demo app** (via workspace symlink)

3. **Test in demo app:**

   ```bash
   pnpm dev
   ```

4. **Build packages when ready:**
   ```bash
   pnpm build
   ```

## Common Commands

### Package Management

```bash
# Add dependency to specific package
pnpm --filter @summit/core add axios

# Add devDependency
pnpm --filter @summit/core add -D vitest

# Add shared devDependency (root level)
pnpm add -D -w eslint

# Update all dependencies
pnpm update

# Remove dependency
pnpm --filter @summit/core remove axios
```

### Building

```bash
# Build SDK packages only
pnpm build

# Build demo app
pnpm build:demo

# Build marketing site
pnpm build:marketing

# Build everything
pnpm build:all
```

### Cleaning

```bash
# Clean all build artifacts and node_modules
pnpm clean

# Clean specific package
pnpm --filter @summit/core exec rm -rf dist
```

## Working with Packages

### Package: @summit/core

**Location:** `packages/core/`

**Purpose:** Core SDK functionality (framework-agnostic)

**Development:**

```bash
cd packages/core

# Build once
pnpm build

# Build and watch for changes
pnpm dev
```

**Testing changes:**

1. Make changes in `src/`
2. Demo app auto-picks up changes (via symlink)
3. Refresh browser to see results

### Package: @summit/ui

**Location:** `packages/ui/`

**Purpose:** Optional React UI components

**Development:**

```bash
cd packages/ui
pnpm dev  # Watch mode
```

**Adding new component:**

```bash
# 1. Create component file
touch packages/ui/src/NewComponent.tsx

# 2. Export from index
echo "export { NewComponent } from './NewComponent'" >> packages/ui/src/index.ts

# 3. Use in demo app
# Edit apps/demo/src/App.tsx to import and use
```

### Package: @summit/types

**Location:** `packages/types/`

**Purpose:** Shared TypeScript type definitions

**Development:**

```bash
cd packages/types
pnpm build  # Generates .d.ts files
```

**Adding new types:**

```typescript
// packages/types/src/index.ts
export interface NewType {
  id: string
  name: string
}
```

## Git Workflow

### Creating a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feat/your-feature-name
```

### Committing Changes

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: add query caching to SDK"
git commit -m "fix: resolve memory leak in worker"
git commit -m "docs: update installation guide"
```

**Commit types:**

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance
- `perf:` - Performance improvement

### Pushing and Creating PR

```bash
# Push branch
git push origin feat/your-feature-name

# Open pull request on GitHub
# Fill out PR template with description of changes
```

### Branch Protection

The `main` branch is protected:

- Cannot push directly (must use PR)
- Must resolve all conversations
- Must maintain linear history

## Troubleshooting

### Issue: pnpm command not found

**Solution:**

```bash
npm install -g pnpm
```

### Issue: Changes not reflected in demo app

**Solution:**

```bash
# Re-link workspace packages
pnpm install

# Or restart dev server
# Ctrl+C to stop, then:
pnpm dev
```

### Issue: TypeScript errors in editor

**Solution:**

```bash
# Build packages first
pnpm build

# Restart TypeScript server in your editor
# VS Code: Cmd+Shift+P → "TypeScript: Restart TS Server"
```

### Issue: Build fails with "Cannot find module"

**Solution:**

```bash
# Ensure all packages are built
pnpm build

# Check dependencies are installed
pnpm install
```

### Issue: Port 3000 already in use

**Solution:**

```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill

# Or use different port
PORT=3001 pnpm dev
```

## Editor Setup

### VS Code (Recommended)

**Recommended extensions:**

- ESLint
- Prettier
- TypeScript and JavaScript Language Features (built-in)
- GitLens

**Workspace settings:**

Create `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

### Other Editors

- **WebStorm:** Built-in support for monorepos and pnpm
- **Vim/Neovim:** Use CoC or LSP with TypeScript language server
- **Sublime Text:** Install TypeScript plugin

## Testing (Coming Soon)

Testing infrastructure will be added in future PRs:

- **Vitest** for SDK packages
- **React Testing Library** for UI components
- **pytest** for Python services

Example workflow:

```bash
# Run all tests
pnpm test

# Run tests for specific package
pnpm --filter @summit/core test

# Run tests in watch mode
pnpm --filter @summit/core test:watch
```

## CI/CD (Coming Soon)

GitHub Actions will run on every PR:

- Lint checks
- Type checking
- Tests
- Build verification

## Backend Services (Coming Soon)

Python services setup instructions will be added when backend is implemented.

Expected workflow:

```bash
cd services/api
pip install -r requirements.txt
python main.py
```

## Environment Variables

When backend is added, you'll need `.env` files:

```bash
# .env.local (not committed)
ANTHROPIC_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

**Never commit `.env` files** - they're in `.gitignore`.

## Getting Help

- **Documentation:** Check `/docs` folder
- **Issues:** Open GitHub issue
- **Questions:** Ask in PR comments
- **Contact:** [@johnathanbryce](https://github.com/johnathanbryce)

## Next Steps

After setup:

1. Read [Architecture Overview](../architecture/overview.md)
2. Review [Monorepo Structure](../architecture/monorepo.md)
3. Check [Architecture Decisions](../architecture/decisions.md)
4. Run demo app and explore code
5. Make your first contribution!

# Contributing to Summit SDK

Thank you for your interest in contributing to Summit SDK!

## Development Setup

See our [Development Guide](docs/contributing/development.md) for detailed setup instructions.

Quick start:
```bash
# Prerequisites: Node.js >= 18, pnpm >= 8

# Clone and install
git clone https://github.com/johnathanbryce/summit-sdk.git
cd summit-sdk
pnpm install
```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   pnpm build        # Build packages
   pnpm lint         # Lint code (when available)
   pnpm test         # Run tests (when available)
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feat/your-feature-name
   ```

5. **Open a Pull Request**
   - Describe what changed and why
   - Link any related issues
   - Wait for review

## Project Structure

- `/packages` - SDK packages (core, ui, types)
- `/apps` - Demo and marketing applications
- `/services` - Backend services (API, worker)
- `/docs` - Documentation
- `/infrastructure` - Infrastructure as code

## Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add query caching to SDK
fix: resolve memory leak in worker service
docs: update installation guide
```

## Code of Conduct

Be respectful, collaborative, and constructive. We're building something great together.

## Questions?

Open an issue or reach out to [@johnathanbryce](https://github.com/johnathanbryce).

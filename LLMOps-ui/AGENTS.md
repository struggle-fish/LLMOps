# Repository Guidelines

## Project Structure & Module Organization

This repository is a Vue 3 + TypeScript application built with Vite.

- `src/views/` contains route-level pages such as `HomeView.vue` and `AboutView.vue`.
- `src/components/` contains reusable UI components; component tests live in nearby `__tests__/` directories.
- `src/router/` defines Vue Router routes, while `src/stores/` contains Pinia stores.
- `src/services/` contains API-facing service modules, and `src/config/` contains application configuration.
- `src/assets/` holds styles and bundled assets; `public/` holds files copied directly to the build output.

## Build, Test, and Development Commands

Install dependencies with `yarn`, then use:

- `yarn dev` — start the Vite development server with hot reload.
- `yarn build` — run TypeScript checking and create a production build.
- `yarn test:unit` — run Vitest unit tests in the JSDOM environment.
- `yarn lint` — run ESLint and Oxlint; review the resulting diff because configured checks may fix files.
- `yarn format` — format files under `src/` with Prettier.

## Coding Style & Naming Conventions

Use `<script setup lang="ts">` and the Composition API. Follow the existing two-space indentation, single quotes, and no-semicolon style. Name Vue components and interfaces in PascalCase; name variables, functions, and services in camelCase. Keep page-specific code in views and move reusable behavior into components, composables, stores, or services.

## Testing Guidelines

Use Vitest with `@vue/test-utils`. Name tests `*.spec.ts` and place them in `__tests__/` directories, for example `src/components/__tests__/HelloWorld.spec.ts`. Add focused tests for changed behavior and run `yarn test:unit` before submitting a change.

## Commit & Pull Request Guidelines

Keep commit subjects short and action-oriented, matching the existing Chinese history (for example, `初始化UI文件夹`); `feat:`, `fix:`, `refactor:`, and `test:` prefixes are also appropriate. Pull requests should explain the user-visible change, link a related issue when available, list validation commands, and include screenshots or recordings for UI changes.

## Security & Configuration Tips

Do not commit secrets or local environment files. Treat `import.meta.env` values and external API data as untrusted, and never log tokens, passwords, or private user data.

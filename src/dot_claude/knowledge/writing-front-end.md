---
slug: writing-front-end
categories: [languages]
priority: 1
description: Next.js 15+ / React 19+ / TypeScript 5+ style — Server Components, hooks, type design, error boundaries, testing.
applies_when:
  - writing React components
  - building Next.js apps
  - designing TypeScript types
  - writing frontend tests
related: [coding-style, writing-tests]
---

# Front-End (Next.js / React / TypeScript / JavaScript)

Applies to any front-end work using React 19+, Next.js 15+ (App Router), and TypeScript 5+. Default to TypeScript -- never start new files in plain JavaScript.

## Modern Language Features

Use modern ES2023+ and TypeScript 5+ as the baseline. Legacy patterns are not optional to avoid -- they are outright wrong in a new codebase.

### JavaScript

- Use `const` by default, `let` only when reassignment is genuinely needed, never `var`
- Use array-by-copy methods (`toSorted`, `toReversed`, `toSpliced`, `with`) over mutating counterparts
- Use optional chaining (`?.`) and nullish coalescing (`??`) over manual null checks and `||`
- Use `structuredClone()` for deep copies, not `JSON.parse(JSON.stringify(x))`
- Use `async`/`await` over raw `.then()` chains
- Use `Temporal` (or `date-fns`/`luxon`) over the legacy `Date` object for anything beyond a timestamp

### TypeScript

- Enable `strict: true` in `tsconfig.json`. Also enable `noUncheckedIndexedAccess`, `noImplicitOverride`, and `exactOptionalPropertyTypes`
- Never use `any`. Use `unknown` at boundaries and narrow with type guards
- Never use non-null assertions (`!`) -- narrow the type instead
- Prefer `type` aliases for unions, shapes, and function signatures; use `interface` only when declaration merging or `extends` provides real value
- Use `as const` for literal-typed constants and config objects
- Use `satisfies` to validate a value matches a type without widening it:

```typescript
// WRONG: loses literal types
const config: Record<string, string> = { theme: "dark", locale: "en" };

// CORRECT: retains literal types AND type-checks the shape
const config = { theme: "dark", locale: "en" } satisfies Record<string, string>;
```

## Type Design

### Make Invalid States Unrepresentable

Use discriminated unions so only valid states can exist:

```typescript
// WRONG: invalid states are representable
type UserData = {
  status: "loading" | "success" | "error";
  data?: User;
  error?: Error;
};

// CORRECT: each state carries exactly its own data
type UserData =
  | { status: "loading" }
  | { status: "success"; data: User }
  | { status: "error"; error: Error };
```

Use exhaustive `switch` with a `never` check to force compile errors when a new variant is added:

```typescript
function render(state: UserData): ReactNode {
  switch (state.status) {
    case "loading": return <Spinner />;
    case "success": return <Profile user={state.data} />;
    case "error":   return <ErrorView error={state.error} />;
    default: {
      const _exhaustive: never = state;
      return _exhaustive;
    }
  }
}
```

### Branded Types Over Raw Primitives

```typescript
// WRONG: nothing stops you passing an OrderId where a UserId is expected
type UserId = string;
type OrderId = string;

// CORRECT: compile-time distinction at zero runtime cost
type UserId = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };
```

### Enums and Booleans

- Never use TypeScript `enum` -- use `as const` object literals or union string types instead. Enums produce runtime code and have inconsistent semantics
- Replace boolean parameters with discriminated string unions when the boolean's meaning isn't obvious from the call site

```typescript
// WRONG: what does `true` mean at the call site?
function send(msg: string, urgent: boolean): void {}

// CORRECT: semantic meaning
function send(msg: string, priority: "normal" | "urgent"): void {}
```

### Rules

- Parse external data (API responses, form input, env vars) through Zod/Valibot schemas -- never cast with `as`
- Use `readonly` on arrays, object fields, and tuples by default
- Prefer narrow types at function parameters (`Pick`, `Omit`, sub-types) and wide types at return positions

## React Components

### Server Components First (App Router)

Default to Server Components. Only add `"use client"` when you need interactivity, state, effects, browser APIs, or event handlers.

```tsx
// Server Component: no "use client", zero JS to the browser
export default async function UserProfile({ id }: { id: UserId }) {
  const user = await fetchUser(id);
  return <Profile user={user} />;
}
```

Rules:
- Keep `"use client"` boundaries as small as possible -- lift data-fetching to a Server Component parent and pass results as props
- Server Components can render Client Components; Client Components can receive Server Components as `children` or props but cannot import them
- Never pass non-serializable values (functions, Dates in some contexts, class instances) from Server to Client Components
- Co-locate Suspense boundaries with slow data fetches so fast content streams first

### Component Structure

```tsx
// WRONG: mutable, untyped, unclear inputs
export default function Card(props) {
  const [open, setOpen] = useState(false);
  props.onToggle && props.onToggle(open);
  return <div>{props.children}</div>;
}

// CORRECT: typed props, explicit contract, stable callback usage
type CardProps = {
  title: string;
  children: ReactNode;
  onToggle?: (open: boolean) => void;
};

export function Card({ title, children, onToggle }: CardProps): ReactNode {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    onToggle?.(open);
  }, [open, onToggle]);

  return (
    <section aria-labelledby="card-title">
      <h2 id="card-title">{title}</h2>
      {children}
    </section>
  );
}
```

Rules:
- One component per file. File name matches the component name in PascalCase
- Use named exports. Avoid default exports except where required by Next.js (`page.tsx`, `layout.tsx`, `route.ts`)
- Always type props explicitly with a `type` alias above the component
- Return type is `ReactNode` (or `JSX.Element` when you mean exactly one element). Never annotate as `FC` / `FunctionComponent` -- it implicitly adds `children` and hurts inference
- Destructure props in the signature, not inside the body
- Never spread unknown props (`{...props}`) onto DOM elements without narrowing first

### Hooks

- Call hooks only at the top level of a component or custom hook -- never conditionally, never in loops (exception: React 19's `use()` hook)
- Custom hooks start with `use` and return either a value, a tuple, or a stable object. Be consistent within a codebase
- Never put non-serializable values in state if the component may hydrate
- Derive state during render -- do not mirror props into state with `useEffect`
- `useEffect` is for synchronizing with external systems (subscriptions, DOM APIs, non-React code). If you're reaching for it for data fetching, reach for a Server Component or a data library (`@tanstack/react-query`, SWR) instead
- Specify complete dependency arrays. Never disable `react-hooks/exhaustive-deps` -- fix the underlying issue

### React 19 Features

- Use `use()` to unwrap promises and context, including inside conditionals
- Use Actions (`action` prop on `<form>`) with `useActionState` and `useFormStatus` for form handling -- they work without JS and integrate with Suspense
- Use `useOptimistic` for instant UI feedback on pending mutations
- Rely on the React Compiler for memoization -- do not reach for `useMemo`/`useCallback`/`memo` unless profiling shows a real problem

## Next.js (App Router)

### Data Fetching

- Fetch in Server Components using `async`/`await` with the native `fetch` API -- React deduplicates identical requests within a render
- Control caching with route segment config (`export const dynamic`, `export const revalidate`) and fetch options (`{ cache: "force-cache" | "no-store", next: { revalidate, tags } }`)
- Use `revalidateTag`/`revalidatePath` from Server Actions to invalidate specific cache entries, not the whole cache
- Use `unstable_cache` only for non-`fetch` data sources (e.g., direct DB calls)

### Server Actions

- Mark server-only modules with `"use server"` at the top of the file (not per-function for shared modules)
- Validate all Server Action inputs with Zod/Valibot -- never trust the client
- Return typed results (`{ ok: true, data } | { ok: false, error }`) rather than throwing across the client/server boundary
- Use `redirect()` and `notFound()` from `next/navigation` for control flow in Server Components and Actions

### Routing

- Use Route Groups `(group)` to organize routes without affecting URLs
- Use Parallel Routes (`@slot`) for independent loading states and Intercepting Routes (`(..)path`) for modal UX
- Always add `loading.tsx` and `error.tsx` at appropriate segment boundaries
- Use `generateMetadata` for dynamic `<head>` metadata; never manipulate `document.title` manually

### Rules

- Never import server-only modules (DB clients, secrets, Node APIs) into Client Components. Use `server-only` as an import guard in shared modules
- Environment variables: prefix client-exposed vars with `NEXT_PUBLIC_`. Everything else stays server-side. Validate all env vars on boot through a Zod schema
- Use `next/image`, `next/link`, and `next/font` -- never raw `<img>`, `<a>` for internal navigation, or `<link>` for fonts
- Use `dynamic()` with `{ ssr: false }` only for components that genuinely cannot render on the server (e.g., those using `window` in module scope)

## Immutability

Never mutate state, props, or external data. React relies on reference equality for rerender detection.

```tsx
// WRONG: mutation
function addItem(items: Item[], item: Item): Item[] {
  items.push(item);
  return items;
}

// CORRECT: new array
function addItem(items: Item[], item: Item): Item[] {
  return [...items, item];
}
```

Rules:
- Use spread syntax or array-by-copy methods for simple updates
- Use Immer (via `useImmer` or `produce`) for deeply nested state updates
- Never mutate props -- copy first, then modify

## Error Handling

- Use Error Boundaries (class components or `react-error-boundary`) at route and feature boundaries -- not around every component
- In the App Router, implement `error.tsx` and `global-error.tsx` for route-level fallbacks
- Throw typed domain errors in Server Components and Server Actions; catch them at the boundary and return structured results
- Never swallow errors in `catch` blocks. Either handle, rethrow with context, or log with a logger (`pino`, `winston`) -- never just `console.error` in production code paths
- For async side effects in Client Components, always handle the rejected case

```tsx
useEffect(() => {
  let cancelled = false;
  fetchData()
    .then(data => { if (!cancelled) setState(data); })
    .catch(err => { if (!cancelled) setError(err); });
  return () => { cancelled = true; };
}, []);
```

## Naming Conventions

| Item | Convention | Example |
|---|---|---|
| Component files | PascalCase | `UserProfile.tsx` |
| Hook files | camelCase, `use` prefix | `useUser.ts` |
| Utility files | kebab-case | `format-date.ts` |
| Next.js special files | lowercase | `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx` |
| Components, types | PascalCase | `UserProfile`, `OrderStatus` |
| Functions, variables, hooks | camelCase | `parseConfig`, `useAuth` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_RETRIES` |
| Boolean variables | `is`/`has`/`should` prefix | `isLoading`, `hasError` |
| Event handlers (props) | `on` prefix | `onClick`, `onSubmit` |
| Event handlers (internal) | `handle` prefix | `handleClick`, `handleSubmit` |
| CSS Modules | kebab-case in file, camelCase in import | `styles.userCard` |

## Testing

Use **Vitest** + **React Testing Library** + **MSW** for component and integration tests. Use **Playwright** for a small suite of critical end-to-end flows. Do not use Jest or Enzyme in new projects.

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";

describe("LoginForm", () => {
  it("shows a validation error when email is missing", async () => {
    render(<LoginForm onSubmit={() => {}} />);
    await userEvent.click(screen.getByRole("button", { name: /sign in/i }));
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });
});
```

Rules:
- Query by accessible role, label, or text -- never by `data-testid` unless nothing else works, and never by CSS class or DOM structure
- Use `userEvent` over `fireEvent` -- it simulates real user interactions including focus, keyboard, and pointer events
- Mock network at the HTTP boundary with MSW, not by mocking fetch or hand-rolled service stubs
- Never mock React itself, your own hooks, or your own components. If a component is hard to test, refactor it -- don't mock around it
- Use `await screen.findBy*` for async appearances; never add arbitrary timeouts
- Test the public contract (props in, rendered output and events out). Do not assert on internal state, refs, or hook call order
- Snapshot tests only for small, stable, presentational components. Never snapshot large trees

## Project Organization

Organize by feature/domain, not by type. "Screens → hooks/, components/, utils/, types/" flat splits don't scale.

```
src/
  app/                           -- Next.js App Router (routes only)
    (marketing)/
      page.tsx
      layout.tsx
    dashboard/
      page.tsx
      loading.tsx
      error.tsx
    api/
      webhooks/
        route.ts
  components/
    ui/                          -- reusable primitives (Button, Input, Dialog)
    layout/                      -- shared layout pieces (Header, Footer)
  features/
    auth/
      components/
      hooks/
      actions.ts                 -- Server Actions
      schema.ts                  -- Zod schemas
      types.ts
    billing/
      components/
      hooks/
      actions.ts
  lib/                           -- cross-feature utilities
    db.ts
    env.ts
    http.ts
  styles/
  types/                         -- truly global types only
```

Rules:
- Co-locate components, hooks, tests, and styles within the feature that owns them. A component used in only one place belongs in that feature's folder
- Never nest more than 3-4 directories deep -- if you have to, split by sub-domain
- Use path aliases (`@/components`, `@/features/auth`) configured in `tsconfig.json` -- never relative imports that cross feature boundaries (`../../../features/auth`)
- `lib/` is for cross-cutting utilities with no domain coupling. Feature-specific code never lives in `lib/`
- Place `page.tsx`, `layout.tsx`, and `route.ts` under `app/`; keep them thin -- they import and compose from `features/` and `components/`

## Performance

- Rely on Server Components to eliminate JS shipped to the client by default
- Use `next/image` with explicit `width`/`height` and `priority` on LCP images
- Use `next/font` for font loading -- it auto-hosts and prevents layout shift
- Use `next/dynamic` to code-split heavy Client Components below the fold
- Use Suspense streaming for slow data so fast content isn't blocked
- Trust the React Compiler -- do not preemptively add `useMemo`/`useCallback`. Measure with React DevTools Profiler before optimizing
- Use `@tanstack/react-query` or SWR for client-side data with caching, deduplication, and background revalidation -- never hand-roll fetch-in-`useEffect`
- Keep bundles lean: audit with `@next/bundle-analyzer`. Tree-shake by importing specific members (`import { debounce } from "lodash-es"`, not `import _ from "lodash"`)
- Measure Core Web Vitals (LCP, INP, CLS) in production via the `useReportWebVitals` hook and a real analytics provider

## Accessibility

Accessibility is a correctness concern, not a polish step.

- Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<article>`) over generic `<div>`s with ARIA
- Every interactive element must be reachable by keyboard and have a visible focus style
- Every form input must have an associated `<label>` (via `htmlFor` or wrapping)
- Every image must have meaningful `alt` text (or `alt=""` if decorative)
- Use `aria-*` attributes only when semantic HTML cannot express the relationship. ARIA is a last resort
- Run `eslint-plugin-jsx-a11y` in CI. Run axe-core in integration tests for critical flows

## Linting & Formatting

- Use **ESLint** with `@next/eslint-config-next`, `@typescript-eslint`, `eslint-plugin-react-hooks`, and `eslint-plugin-jsx-a11y`
- Use **Prettier** for formatting -- never debate style in review
- Use **Biome** as an alternative to ESLint+Prettier when starting fresh -- it is faster and has a unified config
- Run `tsc --noEmit` in CI with zero tolerance for errors
- Never disable lint rules inline without a comment explaining why
- Suppress with the narrowest possible scope: `// eslint-disable-next-line specific-rule`, never file-level disables without justification

## Anti-Patterns to Avoid

- `any`, non-null assertions (`!`), and `as` casts outside of parsing boundaries
- TypeScript `enum` -- use `as const` unions
- `useEffect` for data fetching, derived state, or synchronizing with React itself
- Mirroring props into state with `useEffect`
- Mutating props, state, or function arguments
- Spreading unknown props onto DOM elements (`<div {...props} />`)
- Index as React `key` when the list can reorder or items have stable IDs
- Default exports for components (except in Next.js special files)
- `FC` / `FunctionComponent` type annotations
- Throwing strings or plain objects as errors -- always throw `Error` (or subclass)
- Catching errors just to `console.log` and rethrow
- Client-side data fetching when a Server Component could do it
- Importing server-only code into Client Components
- `dangerouslySetInnerHTML` without sanitization
- Storing secrets or API keys in `NEXT_PUBLIC_*` env vars
- Hand-rolled global state when `useState` + props, React Context, or a purpose-built library (Zustand, Jotai) would do
- Large `useReducer` state machines -- reach for XState when the logic genuinely warrants it
- `document.getElementById` / direct DOM manipulation when a ref would do
- Inline styles for anything beyond a single dynamic value -- use CSS Modules, Tailwind, or a styling system

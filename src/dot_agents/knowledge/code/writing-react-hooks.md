---
slug: writing-react-hooks
categories: [languages]
priority: 1
description: React 19+ hooks — rules of hooks, state, Effects, useEffectEvent, useSyncExternalStore, refs, concurrency, custom hook design.
applies_when:
  - writing React hooks
  - writing a custom hook
  - reaching for useEffect
  - debugging stale closures or re-render loops
  - fixing an exhaustive-deps warning
related: [writing-front-end, coding-style, writing-tests]
---

# React Hooks (React 19+)

Applies to any hook usage in React 19+. Most hook bugs are not hook bugs -- they are an Effect doing a job that belonged in a handler, a derivation, or a store. Reach for the smallest tool that works, in this order: **render → event handler → Effect**.

## Rules of Hooks

- Call hooks only at the top level of a Client Component or another custom hook. Never inside conditions, loops, `try`/`catch`, event handlers, callbacks, class components, or plain functions
- `use()` is the only exception: it may be called in conditions and loops. It still may not be called inside `try`/`catch`
- Hooks do not exist in Server Components. A component that needs one needs `"use client"`
- A function is a hook only if it calls another hook. A `useSorted(items)` that just sorts is a plain function -- name it `getSorted` so callers can call it conditionally
- Never suppress `react-hooks/exhaustive-deps`. Every legitimate reason to suppress it has a real fix: `useEffectEvent` for a non-reactive read, a functional update for stale state, hoisting a constant out of the component, or deleting the Effect

## State

- Initialize expensively with the lazy form: `useState(() => parse(raw))`, not `useState(parse(raw))` -- the latter re-runs `parse` on every render and throws the result away
- Update from previous state with the functional form: `setCount(c => c + 1)`. Reading `count` directly is stale inside batched updates, timers, and async callbacks
- The `useState` initializer runs on the first render only. To reset a component's state when an input changes, remount it with `key` -- never sync it with an Effect

```tsx
// WRONG: renders once with the stale comment, then again to clear it
useEffect(() => { setComment(""); }, [userId]);

// CORRECT: React discards the old state and mounts a fresh component
<Profile userId={userId} key={userId} />
```

- Reach for `useReducer` when several state fields change together or the next state is a function of the current one. Reach for XState only when the transitions are a genuine state machine with guards and side effects
- Never put non-serializable values in state if the component may hydrate

## You Probably Don't Need an Effect

| Instead of an Effect that... | Do this |
|---|---|
| Computes state from props/state | Compute it during render |
| Caches an expensive computation | `useMemo` (only if profiling proves it's expensive) |
| Resets state when a prop changes | Remount with `key` |
| Adjusts some state when a prop changes | Compare against a previous-value state during render, or derive it |
| Runs logic after a user interaction | Put the logic in the event handler |
| Triggers another Effect (a chain) | Compute everything in the one event handler |
| Notifies the parent after state changes | Call the parent's callback in the same handler that sets state |
| Runs one-time app initialization | Run it at module scope |
| Subscribes to an external store | `useSyncExternalStore` |
| Fetches data | Server Component, or `@tanstack/react-query`/SWR |

Effects are for synchronizing with systems that live outside React -- a WebSocket, a media player, a browser API, a third-party widget. If the "external system" is React itself, delete the Effect.

```tsx
// WRONG: an Effect to tell the parent what just happened
const [open, setOpen] = useState(false);
useEffect(() => { onToggle?.(open); }, [open, onToggle]);

// CORRECT: one handler, one pass -- React batches both updates
function handleToggle() {
  const next = !open;
  setOpen(next);
  onToggle?.(next);
}
```

## Effects

- Every Effect that creates something must destroy it in the cleanup: subscriptions, timers, listeners, connections, observers
- In development, StrictMode mounts, cleans up, and remounts every Effect. That is a test, not a bug -- an Effect that breaks on setup → cleanup → setup is broken in production too
- Never call `setState` synchronously in an Effect body to derive a value. It renders twice and cascades (`react-hooks/set-state-in-effect`)
- Keep dependencies primitive. Objects, arrays, and functions created during render are new on every render -- declare them inside the Effect or hoist them out of the component rather than memoizing them into submission
- Any async work in an Effect must be cancellable, or a slow response for the previous input will land after a fast one for the current input and overwrite it

```tsx
useEffect(() => {
  const controller = new AbortController();
  connectToRoom(roomId, { signal: controller.signal });
  return () => controller.abort();
}, [roomId]);
```

For a promise you cannot abort, guard the write instead:

```tsx
useEffect(() => {
  let cancelled = false;
  subscribeToFeed(feedId)
    .then(data => { if (!cancelled) setState(data); })
    .catch(err => { if (!cancelled) setError(err); });
  return () => { cancelled = true; };
}, [feedId]);
```

## useEffectEvent (React 19.2+)

The escape hatch for an Effect that must *read* a value without *reacting* to it. This is the fix for the dependency you were tempted to suppress.

```tsx
// WRONG: reconnects the socket every time the theme changes
useEffect(() => {
  const conn = createConnection(roomId);
  conn.on("connected", () => showToast("Connected!", theme));
  conn.connect();
  return () => conn.disconnect();
}, [roomId, theme]);

// CORRECT: theme is read at call time, not depended on
const onConnected = useEffectEvent(() => {
  showToast("Connected!", theme);
});

useEffect(() => {
  const conn = createConnection(roomId);
  conn.on("connected", onConnected);
  conn.connect();
  return () => conn.disconnect();
}, [roomId]);
```

Rules:
- Declare it at the top level of a component or custom hook; call it only from inside that component's Effects
- Never list it in a dependency array, and never pass it to another component or hook
- It is not a general-purpose "stabilize this function" tool. If the Effect genuinely should re-run when the value changes, it is a dependency -- leave it in

## External Stores and Browser APIs

Subscribe with `useSyncExternalStore`, not an Effect plus state. It reads the value during render (no torn UI under concurrent rendering) and takes a server snapshot for SSR.

```tsx
function useOnlineStatus(): boolean {
  return useSyncExternalStore(
    (onChange) => {
      window.addEventListener("online", onChange);
      window.addEventListener("offline", onChange);
      return () => {
        window.removeEventListener("online", onChange);
        window.removeEventListener("offline", onChange);
      };
    },
    () => navigator.onLine,
    () => true,
  );
}
```

The third argument is the server snapshot. Omit it and the component crashes during SSR; return the wrong thing and you get a hydration mismatch.

## Refs

- `useRef` holds a mutable value that is *not* rendered. If rendering it should update the screen, it belongs in state
- Never read or write `ref.current` during render -- only in Effects and event handlers (`react-hooks/refs`)
- `ref` is an ordinary prop in React 19. Do not write `forwardRef` in new code; it is deprecated
- Ref callbacks may return a cleanup function -- use it instead of the legacy `null` call

```tsx
<video ref={(node) => {
  const observer = observeVisibility(node);
  return () => observer.disconnect();
}} />
```

- `useImperativeHandle` is a last resort for exposing imperative methods (`focus`, `play`). Prefer props

## Concurrency and Identity

- `useTransition` marks an update non-urgent so typing and clicking stay responsive; its `isPending` flag drives the busy state. In React 19 the action may be `async`, which keeps `isPending` true across the `await`
- `useDeferredValue` lets expensive derived UI lag behind an urgent input. Pass an `initialValue` to avoid blocking the first paint
- Both are the front line for a bad INP score -- reach for them before hand-memoizing
- `useId` generates ids that are stable across server and client. Use it for every `htmlFor`/`aria-labelledby`/`aria-describedby` link. Never hand-write a literal id in a reusable component, and never use `useId` as a list `key`
- `useLayoutEffect` only for measuring the DOM before paint. It blocks paint and does not run on the server

## Context

- Prefer `use(Context)` over `useContext` in React 19 -- same semantics, plus conditional reads
- Every consumer re-renders when a provider's value changes. Split context by update frequency (a stable dispatch context separate from a volatile value context), and keep fast-changing values out of context entirely -- that is what Zustand and Jotai are for

## React 19 Hook APIs

- `use()` unwraps promises and context, including inside conditionals. The promise must come from a Server Component, a cached function, or a data library -- **never create it during a client render** (`use(fetch(url))` refetches forever). Pair every `use(promise)` with a `<Suspense>` boundary and an error boundary, since it cannot be wrapped in `try`/`catch`
- `useActionState` returns `[state, formAction, isPending]` and is the default for form submission -- wired to a `<form action>` it works without JS
- `useFormStatus` reads the pending state of the nearest parent `<form>`. It only works in a *child* of that form, not in the component that renders it -- which is what makes it right for design-system buttons
- `useOptimistic` gives instant feedback on pending mutations. The optimistic value only holds while an action or transition is in flight; it reverts automatically when the action settles
- Rely on the React Compiler for memoization -- do not reach for `useMemo`/`useCallback`/`memo` unless profiling shows a real problem. They remain valid escape hatches when you need a guaranteed stable identity (a value feeding an Effect's dependency array, or an object handed to a non-React consumer)

## Custom Hooks

- Name the hook for the concrete use case, not the mechanism: `useChatRoom`, `useOnlineStatus`, `useFormInput` -- never `useData`, `useEffectWrapper`, `useStateWrapper`
- Never build lifecycle wrappers (`useMount`, `useEffectOnce`, `useUpdateEffect`). They hide dependencies from the linter, which is the only thing standing between you and a stale closure
- Pass reactive values in as arguments so the hook re-synchronizes when they change. Wrap callback arguments in `useEffectEvent` so a new function identity on every render doesn't re-trigger the Effect
- Custom hooks share *logic*, not *state*. Two components calling `useCounter()` get two independent counters. To share state, lift it up or use a store
- Return a value, a tuple, or an object -- consistently across the codebase. Tuples for two-slot returns you expect callers to rename, objects for three or more

```tsx
export function useChatRoom({ roomId, onMessage }: ChatRoomOptions): void {
  const onReceive = useEffectEvent(onMessage);

  useEffect(() => {
    const conn = createConnection(roomId);
    conn.on("message", onReceive);
    conn.connect();
    return () => conn.disconnect();
  }, [roomId]);
}
```

## Linting

Run `eslint-plugin-react-hooks` v6+ in flat config, and turn the React Compiler on (`reactCompiler: true` in `next.config.ts`). Beyond `rules-of-hooks` and `exhaustive-deps`, the compiler-powered rules catch what the compiler cannot compile around: `set-state-in-render`, `set-state-in-effect`, `purity`, `immutability`, `refs`, `static-components`, `preserve-manual-memoization`. Opt into the bleeding-edge set with the `recommended-latest` config.

## Testing

- Test a custom hook through a component that uses it -- the hook's contract is what the component can observe
- Reach for `renderHook` only when the hook is itself the public API (a published package, a shared primitive). Assert on `result.current` and wrap out-of-band updates in `act`
- Never mock your own hooks to make a component testable. If a component is hard to test, the hook boundary is wrong

## Anti-Patterns to Avoid

- `useEffect` for data fetching, derived state, or synchronizing with React itself
- Mirroring props into state with `useEffect`
- Resetting state with an Effect when `key` would remount the component
- Calling `setState` in an Effect body to derive a value, or chaining Effects that trigger each other
- Notifying a parent from an Effect instead of from the handler that changed the state
- Suppressing `react-hooks/exhaustive-deps` instead of reaching for `useEffectEvent`
- Lifecycle wrapper hooks (`useMount`, `useEffectOnce`, `useUpdateEffect`) -- they blind the linter
- Subscribing to an external store with `useEffect` + `useState` instead of `useSyncExternalStore`
- Creating a promise during render and passing it to `use()`
- Reading or writing `ref.current` during render
- `forwardRef` in new code -- `ref` is a plain prop in React 19
- Hard-coded DOM ids in reusable components -- use `useId`
- An Effect with no cleanup that opened a subscription, timer, or listener

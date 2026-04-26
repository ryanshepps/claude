---
slug: writing-react-native
categories: [languages]
priority: 2
description: React Native 0.84+ / Expo SDK 53+ style — New Architecture, Expo Router, Hermes V1, Reanimated worklets, FlashList, EAS.
applies_when:
  - writing React Native components
  - building Expo apps
  - shipping mobile apps for iOS/Android
  - choosing mobile libraries or navigation
related: [writing-front-end, coding-style, writing-tests]
---

# React Native / Expo

Applies to mobile work using React Native 0.84+, Expo SDK 53+, and TypeScript 5+. Default to **Expo's managed workflow with Expo Router** for new apps -- bare React Native or non-file-based navigation should be a deliberate, justified choice.

Most rules from [[writing-front-end]] (TypeScript strictness, hooks discipline, immutability, error handling, naming, testing philosophy) carry over verbatim. This file covers what's mobile-specific.

## Baseline Stack

- **React Native 0.84+** with the **New Architecture** (Fabric + TurboModules) enabled. The old bridge was removed in 0.82 -- there is no opt-out path on a current SDK
- **Hermes V1** as the JS engine (default since 0.84). Never ship JSC
- **Expo SDK 53+** managed workflow. Use `npx create-expo-app` with the TypeScript template
- **Expo Router v4+** for navigation (file-based, typed routes, deep links by default)
- **EAS Build / Update / Submit** for CI, OTA updates, and store submission. Never hand-build IPAs/APKs
- **TanStack Query** for server state; **Zustand** or **Jotai** for client state. Never Redux in new apps unless an existing codebase demands it
- **NativeWind 5** or restyle for styling; raw `StyleSheet.create` is fine for primitives
- **Reanimated 4** + **react-native-gesture-handler** for animations and gestures -- never the legacy `Animated` API
- **@shopify/flash-list** for any list longer than a screen. `FlatList` is acceptable only for short, fixed lists; never `ScrollView` with `.map()` for long data
- **react-native-mmkv** for key/value storage -- never `AsyncStorage` (slow, JSON-only, async even for tiny reads)
- **expo-image** over `react-native/Image` -- caching, blurhash placeholders, better memory behavior

## Project Structure (Expo Router)

```
app/                              -- routes only, file-based
  (tabs)/
    _layout.tsx
    index.tsx
    profile.tsx
  (auth)/
    sign-in.tsx
  [...not-found].tsx
  _layout.tsx                     -- root layout, providers mount here
src/
  features/
    auth/
      components/
      hooks/
      api.ts
      schema.ts
    feed/
  components/
    ui/                           -- Button, Text, Pressable primitives
  lib/
    mmkv.ts
    query-client.ts
    env.ts                        -- Zod-validated process.env
  theme/
assets/
app.json                          -- or app.config.ts for dynamic config
eas.json
```

Rules:
- Keep `app/` thin -- routes import and compose from `src/features/`
- Use Route Groups `(group)` to share layouts without affecting URLs; use `_layout.tsx` for stack/tabs configuration
- Co-locate by feature, not by type. Same rule as web

## Components

Same component rules as [[writing-front-end]] (typed props, named exports, no `FC`, `ReactNode` return). Mobile-specific additions:

- Use `Pressable` over `TouchableOpacity`/`TouchableHighlight` -- it's the modern, accessible primitive
- Wrap text in `<Text>` always. Bare strings inside `<View>` crash on native
- Use `SafeAreaView` from `react-native-safe-area-context` (not the built-in one) at screen roots
- Use `KeyboardAvoidingView` or `react-native-keyboard-controller` for inputs near the bottom of the screen
- For platform-specific files, use the `.ios.tsx` / `.android.tsx` / `.web.tsx` extensions before reaching for `Platform.select`. Use `Platform.select` only for one-off branches inside otherwise shared components

## Navigation (Expo Router)

- Use **typed routes** (`experiments.typedRoutes` in `app.json`) so `<Link href="...">` is type-checked
- Navigate with `<Link>` and `useRouter()` from `expo-router`. Never use the underlying `@react-navigation/*` APIs directly unless you need an escape hatch
- Define route params via the file name (`[id].tsx`) and read with `useLocalSearchParams<{ id: string }>()`. Validate params with Zod -- they arrive as untyped strings
- Configure deep links and universal links in `app.json` (`scheme`, `ios.associatedDomains`, `android.intentFilters`). Test both
- Use `<Stack.Screen options={...} />` inside the screen, not in `_layout.tsx`, when options depend on screen-local state

## State & Data

- **Server state**: TanStack Query. Same rules as web -- never store server data in Zustand/Redux just to "have it everywhere"
- **Client state**: Zustand for global state, `useState`/`useReducer` for local. Jotai if you have many small atoms with cross-cutting derivations
- **Forms**: `react-hook-form` + Zod resolver. Never hand-roll controlled-input arrays for non-trivial forms
- **Persistence**: MMKV for sync key/value, SQLite (`expo-sqlite`) for relational, **WatermelonDB** or **op-sqlite** + Drizzle for offline-first apps with sync
- Never persist secrets in MMKV or AsyncStorage. Use `expo-secure-store` (Keychain / Keystore-backed)

## Performance

The mobile bar is higher than web because users feel jank on a 60/120Hz UI thread.

- **Lists**: FlashList with a stable `estimatedItemSize`. Provide `keyExtractor` returning a stable string. Never compute keys from index for reorderable data
- **Images**: `expo-image` with `cachePolicy="memory-disk"`. Provide explicit `style` width/height -- never rely on intrinsic sizing for off-screen images
- **Animations**: Run on the UI thread via Reanimated worklets (`useSharedValue`, `useAnimatedStyle`, `withTiming`/`withSpring`). Never animate layout props with `setState` in a render loop
- **Gestures**: `react-native-gesture-handler`, composed with Reanimated. Never use `PanResponder`
- **Re-renders**: Trust the React Compiler (Expo SDK 52+ ships it on by default). Don't preemptively reach for `memo`/`useMemo`/`useCallback` -- profile with the React DevTools Profiler and Flipper / React Native DevTools first
- **Startup**: Lazy-load heavy screens by importing from `app/` only when navigated. Use `expo-splash-screen` and call `SplashScreen.hideAsync()` after critical fonts/auth resolve, not after every fetch
- **Bundle**: Hermes bytecode + Metro tree-shaking. Avoid moment.js, full lodash, and any library shipping a CommonJS-only build

## Native Modules

- Prefer existing **Expo SDK** modules (`expo-camera`, `expo-location`, `expo-notifications`, `expo-file-system`) -- they're maintained against current RN versions and work with EAS Build
- For custom native code, use the **Expo Modules API** (Swift / Kotlin), not the legacy `NativeModule` / TurboModule C++ paths directly
- A custom native module forces a "development build" (no Expo Go). Document this in the README -- contributors will hit it
- Never patch native code via `patch-package` against Pods/Gradle long-term. Fork or write a config plugin

## Configuration & Environment

- Use `app.config.ts` (not static `app.json`) when any value depends on environment. Read env via `process.env.EXPO_PUBLIC_*` for client-exposed, plain `process.env.*` for build-time-only
- **Public env vars** must be prefixed `EXPO_PUBLIC_`. Treat anything else as build-time secrets injected via EAS Secrets
- Validate all env at module load through a Zod schema in `src/lib/env.ts`. Crash fast on missing config
- Never commit `.env*` files. Use EAS Secrets and `eas env` for shared values
- Lock SDK and native dependency versions. Run `npx expo install --check` before every release to flag mismatched native deps

## EAS & Releases

- One `eas.json` profile per environment: `development` (dev client), `preview` (internal distribution), `production` (store)
- Use **EAS Update** for OTA JS/asset updates. Pin updates to a runtime version that matches the native build -- never push an OTA across an SDK upgrade
- Use **EAS Build** with managed credentials. Don't commit signing keys
- Submit via **EAS Submit**. Automate with GitHub Actions on a release tag

## Accessibility

iOS VoiceOver and Android TalkBack are first-class -- not optional.

- Use `accessibilityRole` (`"button"`, `"header"`, `"link"`) on every interactive element
- Provide `accessibilityLabel` for any control whose visible text isn't sufficient (icon buttons, decorative wrappers around touch targets)
- Use `accessibilityState` (`{ disabled, selected, checked }`) instead of styling-only state
- Test with the screen reader on a real device for any new screen. Simulators lie about gesture nav
- Respect `useReducedMotion()` -- gate non-essential animations behind it
- Honor system text scaling. Set `allowFontScaling` thoughtfully; never hard-clamp font sizes for layout convenience

## Testing

- **Unit / component**: Jest + `@testing-library/react-native`. Same query and `userEvent` rules as the web RTL setup. RN doesn't yet have first-class Vitest support
- **E2E**: **Maestro** for most flows (YAML, fast, no native code knowledge required). **Detox** when you need fine-grained control or are already invested
- Run E2E on EAS Build artifacts in CI via Maestro Cloud or a self-hosted simulator farm. Never test only the JS bundle in isolation
- Mock the network with MSW (works in Jest with the native fetch polyfill). Never mock React Native modules wholesale -- use `jest-expo`'s preset and `jest.mock` only at the module boundary

## Anti-Patterns to Avoid

- Bare React Native CLI for new apps without a strong reason -- Expo's managed workflow + dev clients now covers virtually every native need
- `AsyncStorage` for anything beyond legacy compatibility -- use MMKV
- `FlatList` / `ScrollView` for long or heterogeneous lists -- use FlashList
- Legacy `Animated` API or `LayoutAnimation` -- use Reanimated worklets
- `TouchableOpacity` -- use `Pressable`
- `PanResponder` -- use Gesture Handler
- Storing tokens or secrets in MMKV/AsyncStorage -- use `expo-secure-store`
- `EXPO_PUBLIC_*` for anything sensitive -- it ships in the JS bundle
- OTA updates that cross a native dependency change -- runtime version mismatch will crash on launch
- `console.log` left in production paths -- it slows Hermes and clutters native logs. Use a logger gated by `__DEV__`
- Inline anonymous functions in hot list rows when the React Compiler isn't on yet -- profile first, then memoize
- Manipulating navigation state by reaching into `@react-navigation/native` while using Expo Router -- pick one
- Synchronous expensive work in `useEffect` on screen mount -- defer with `InteractionManager.runAfterInteractions` or move off the JS thread
- Hard-coded insets (`paddingTop: 44`) -- use `useSafeAreaInsets()`
- Per-screen API clients -- one `queryClient` and one `fetch` wrapper, mounted at the root layout

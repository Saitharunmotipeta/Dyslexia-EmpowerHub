Frontend comes here ...
design flow and plan must be started after containerisation ...
frontend/
│
├── public/
│   ├── images/
│   ├── audio/
│   ├── icons/
│   └── static/
│
├── src/
│
│   ├── app/                               # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │
│   │   ├── (public)/
│   │   │   ├── page.tsx
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │
│   │   ├── (private)/
│   │   │   ├── layout.tsx                 # Auth Guard wrapper
│   │   │   ├── home/page.tsx
│   │   │
│   │   │   ├── learning/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── level/[levelId]/page.tsx
│   │   │   │   └── dynamic/page.tsx
│   │   │
│   │   │   ├── practice/
│   │   │   │   ├── upload/page.tsx
│   │   │   │   ├── evaluate/page.tsx
│   │   │   │   └── phoneme/page.tsx
│   │   │
│   │   │   ├── mock/
│   │   │   │   ├── start/page.tsx
│   │   │   │   ├── word/page.tsx
│   │   │   │   ├── result/page.tsx
│   │   │   │   └── report/page.tsx
│   │   │
│   │   │   └── feedback/
│   │   │       ├── trend/page.tsx
│   │   │       ├── pattern/page.tsx
│   │   │       └── recommendation/page.tsx
│   │
│   │   └── chatbot/page.tsx
│
│   ├── components/                        # GLOBAL reusable components
│   │
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Loader.tsx
│   │   │   ├── ProgressBar.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   │
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   │
│   │   ├── charts/
│   │   │   ├── TrendChart.tsx
│   │   │   └── PatternChart.tsx
│   │   │
│   │   ├── media/
│   │   │   ├── AudioPlayer.tsx
│   │   │   └── LazyImage.tsx
│   │   │
│   │   └── chatbot/
│   │       └── ChatBox.tsx
│
│   ├── hooks/                             # GLOBAL reusable hooks
│   │   ├── useAuth.ts
│   │   ├── useDebounce.ts
│   │   ├── useThrottle.ts
│   │   ├── useInfiniteScroll.ts
│   │   ├── useLazyLoad.ts
│   │   ├── useRequestCancel.ts
│   │   └── useLocalStorage.ts
│
│   ├── features/                          # Domain-driven business logic
│   │
│   │   ├── auth/
│   │   │   ├── api.ts
│   │   │   ├── types.ts
│   │   │   └── service.ts
│   │   │
│   │   ├── learning/
│   │   │   ├── api.ts
│   │   │   ├── types.ts
│   │   │   └── service.ts
│   │   │
│   │   ├── practice/
│   │   ├── feedback/
│   │   ├── mock/
│   │   └── dynamic/
│
│   ├── lib/                               # Core Infrastructure Layer
│   │
│   │   ├── api/
│   │   │   ├── axios.ts                   # ENTRY POINT
│   │   │   ├── interceptors.ts
│   │   │   └── config.ts
│   │   │
│   │   ├── auth/
│   │   │   ├── token-storage.ts
│   │   │   └── auth-guard.tsx
│   │   │
│   │   ├── react-query/
│   │   │   ├── queryClient.ts
│   │   │   └── provider.tsx
│   │   │
│   │   └── performance/
│   │       ├── debounce.ts
│   │       ├── throttle.ts
│   │       ├── lazy-loader.ts
│   │       └── request-cancel.ts
│
│   ├── utils/
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── helpers.ts
│
│   ├── constants/
│   │   ├── routes.ts
│   │   └── config.ts
│
│   ├── types/
│   │   ├── api.ts
│   │   └── global.ts
│
│   └── styles/
│       ├── globals.css
│       └── variables.css
│
├── .env.local
├── next.config.js
├── tsconfig.json
├── package.json
└── README.md

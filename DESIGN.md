# Student Assignment Management System (SAMS)
## Visual Design Specification & Design Tokens (`DESIGN.md`)

*Derived directly from visual reference: `reference/design_v2.mp4` (10.04s, 24fps, 1912x1080) and frame captures in `reference/frames_v2/`.*

---

### 1. Visual Overview & Scene Architecture
The visual reference presents a tranquil, serene, Nordic misty lake aesthetic that radiates focus, clarity, and elegance:
- **Atmospheric Misty Horizon:** A cool pearlescent overcast dawn sky blending seamlessly into soft morning lake fog.
- **Dense Evergreen Pine Forest:** Towering, lush conifer trees along symmetrical lake shorelines that convey stability, structure, and depth.
- **Glass-Like Reflective Water:** Still, mirrored lake waters duplicating the evergreen silhouettes and mist with deep slate-teal depth.
- **Central Wooden Rowboat:** A solitary, handcrafted pale birch and midnight-navy rowboat resting serenely at the visual center, symbolizing personal agency, focus, and purposeful progress.
- **Concentric Water Ripple Motion:** Expanding, glassy concentric water rings pulsing smoothly outward from the boat across the mirrored lake surface.

---

### 2. Color Palette & Exact Hex Tokens

| Category | Token Name | Hex Value | Usage / Meaning |
| :--- | :--- | :--- | :--- |
| **Abyssal Lake** | `--color-nordic-deep` | `#0b171a` | Darkest background foundation & body canvas |
| **Slate Pine Dark** | `--color-nordic-dark` | `#122428` | Deep container & sidebar background |
| **Nordic Surface** | `--color-nordic-surface` | `#183035` | Card surfaces & elevated table rows |
| **Dense Pine 900** | `--color-pine-900` | `#0e1d19` | Deepest evergreen foliage shadow |
| **Conifer Pine 700**| `--color-pine-700` | `#1b3b32` | Container borders & primary dark contrast |
| **Forest Pine 500** | `--color-pine-500` | `#2d6354` | Primary brand accent & active states |
| **Serene Lake Teal**| `--color-mist-teal` | `#3d7a6f` | Primary button gradient & highlighted tabs |
| **Water Slate** | `--color-water-slate` | `#2b444c` | Water reflection shadows & card headers |
| **Atmospheric Mist**| `--color-mist-fog` | `#a9b8c6` | Horizon haze & muted meta text |
| **Ripple Glow** | `--color-ripple-glow` | `#bcc8d4` | Concentric ripple ring highlight |
| **Mist Sky Light** | `--color-mist-sky` | `#e3e7ed` | Primary headline text & luminous accents |
| **Pale Birch Wood** | `--color-boat-wood` | `#ebd9d4` | Warm driftwood trim & card highlight glow |
| **Warm Driftwood** | `--color-boat-wood-dark`| `#c4ac9e` | Secondary warm contrast & pending badges |
| **Midnight Hull** | `--color-boat-hull` | `#101e28` | Boat keel shadow & deep button text |
| **Frost Cyan** | `--color-frost-cyan` | `#64b5b0` | Interactive focus rings & active links |
| **Glass Surface** | `--color-glass-card` | `rgba(18, 36, 40, 0.72)` | Frosted glass cards with backdrop blur |
| **Glass Border** | `--color-glass-border` | `rgba(188, 200, 212, 0.16)` | Luminous misty glass borders |

#### Semantic Status Tokens (Badge System)
- **Pending:** `--color-status-pending: #d4a373` (bg: `rgba(212, 163, 115, 0.16)`, border: `rgba(212, 163, 115, 0.35)`)
- **Submitted:** `--color-status-submitted: #4a9ea8` (bg: `rgba(74, 158, 168, 0.16)`, border: `rgba(74, 158, 168, 0.35)`)
- **Late:** `--color-status-late: #d96b6b` (bg: `rgba(217, 107, 107, 0.16)`, border: `rgba(217, 107, 107, 0.35)`)
- **Evaluated:** `--color-status-evaluated: #38a37a` (bg: `rgba(56, 163, 122, 0.16)`, border: `rgba(56, 163, 122, 0.35)`)
- **Returned:** `--color-status-returned: #6a8eae` (bg: `rgba(106, 142, 174, 0.16)`, border: `rgba(106, 142, 174, 0.35)`)

---

### 3. Typography Hierarchy
- **Primary Body & Display Font:** `Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `sans-serif` (self-hosted in `static/fonts/Inter.woff2`).
- Clean, balanced grotesque sans-serif with geometric precision and serene letter-spacing.

| Hierarchy | Weight | Size (Desktop) | Size (Mobile) | Letter Spacing | Line Height |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Kicker** | 700 | 0.875rem (14px) | 0.75rem (12px) | `0.22em` (uppercase) | 1.2 |
| **Hero Headline** | 800 | 4.0rem (64px) | 2.25rem (36px) | `-0.035em` (uppercase)| 1.1 |
| **Hero Subline** | 400 | 1.25rem (20px) | 1.0rem (16px) | `-0.01em` | 1.65 |
| **Section Title**| 700 | 2.25rem (36px) | 1.75rem (28px) | `-0.025em` | 1.25 |
| **Card Heading** | 600 | 1.25rem (20px) | 1.125rem (18px)| `-0.015em` | 1.35 |
| **Body Text** | 400 | 1.0rem (16px) | 0.9375rem (15px)| `normal` | 1.6 |
| **Badges / Meta**| 600 | 0.8125rem (13px)| 0.75rem (12px) | `0.06em` | 1.0 |

---

### 4. Nav, Button, Card & Form Shapes
- **Navigation Bar:**
  - Floating pill dock shape: `border-radius: 9999px` (or `20px` on mobile), margin-top `16px`.
  - Backdrop blur: `backdrop-filter: blur(20px)`, background: `rgba(11, 23, 26, 0.82)`.
  - Misty border highlight: `border: 1px solid rgba(188, 200, 212, 0.18)`, `box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45)`.
- **Buttons:**
  - **Primary Button:** Gradient from Forest Pine (`#2d6354`) to Serene Lake Teal (`#3d7a6f`), pill radius `9999px`, padding `14px 28px`, box-shadow `0 4px 20px rgba(45, 99, 84, 0.35)`.
  - **Secondary Glass Button:** Translucent mist glass `rgba(227, 231, 237, 0.08)`, border `1.5px solid rgba(188, 200, 212, 0.28)`, hover bg `rgba(227, 231, 237, 0.16)`, color `#e3e7ed`.
  - **Action / Icon Buttons:** Rounded square `10px` or pill `9999px`.
- **Cards & Containers:**
  - Glassmorphic panels with `backdrop-filter: blur(16px)`.
  - Radii: `--radius-lg: 16px`, `--radius-xl: 24px`.
  - Border: `1px solid rgba(188, 200, 212, 0.12)`.
- **Forms & Inputs:**
  - Surface: `rgba(18, 36, 40, 0.6)`.
  - Focus Ring: `0 0 0 3px rgba(100, 181, 176, 0.35)`, border-color `#64b5b0`.

---

### 5. Motion Choreography & Animations
- **Concentric Water Ripple Motion:**
  - Water ripple circles propagating outward around focal elements or hero background:
  - Duration: `4.5s`, loop infinite, easing `cubic-bezier(0.25, 0.8, 0.25, 1)`.
  - Scale: `0.8 -> 2.4`, opacity: `0.7 -> 0`.
- **Serene Floating Boat Motion:**
  - Gentle vertical drift: `translateY(0px) rotate(0deg) -> translateY(-6px) rotate(0.4deg) -> translateY(0px) rotate(0deg)`.
  - Duration: `6.0s`, infinite ease-in-out.
- **Scroll Entrance Motion:**
  - Cards slide in smoothly with `opacity: 0, transform: translateY(24px)` to `opacity: 1, transform: translateY(0)`.
  - Duration: `0.6s`, easing `cubic-bezier(0.16, 1, 0.3, 1)`.
- **Reduced Motion Support:**
  - `@media (prefers-reduced-motion: reduce)`: disables background video, ripple loops, and transitions immediately.

# 📘 PRD: Next.js Journaling App

## Overview

A minimal, fast, and intelligent journaling app built with **Next.js**. The app empowers users to log daily reflections, track emotional and productivity patterns, and optionally use AI features for summaries, insights, and coaching prompts. Designed for clarity, speed, and focus.

---

## Goals

- ✅ Allow users to create, edit, and delete daily journal entries  
- 🧠 Integrate optional AI features for summarization, mood analysis, and self-coaching  
- 📈 Provide visual insights (charts, tags, moods over time)  
- 🔒 Ensure privacy-first journaling (local-first or encrypted cloud storage)  
- 📱 Mobile-first responsive UI  

---

## Key Features

### 1. Journaling Core

- [ ] Create/edit/delete journal entries (rich text & markdown)
- [ ] Tag entries (custom tags, e.g., `#gratitude`, `#focus`)
- [ ] Mood slider or emoji selector
- [ ] Time-based view (calendar / timeline / list)
- [ ] Full-text search

### 2. AI-Powered Insights (optional)

- [ ] Summarize journal entries
- [ ] Extract patterns (e.g., “You feel most productive on Tuesdays”)
- [ ] Suggest reflection prompts based on recent entries
- [ ] Mood trend detection

### 3. Data Visualization

- [ ] Mood over time (chart)
- [ ] Tag frequency
- [ ] Word cloud / common themes

### 4. Authentication & Storage

- [ ] Sign in with email + magic link or social login
- [ ] Optional local-first journaling (e.g., IndexedDB)
- [ ] Cloud sync using Supabase, Firebase, or similar
- [ ] End-to-end encryption for sensitive content

### 5. UI/UX

- [ ] Dark/light mode
- [ ] Mobile responsive design
- [ ] Minimalist editor interface
- [ ] Keyboard-first UX (for fast entry)

---

## Tech Stack

| Layer              | Tech                                  |
|-------------------|---------------------------------------|
| Frontend           | Next.js, Tailwind CSS, TypeScript     |
| Auth               | NextAuth.js / Clerk / Supabase Auth   |
| Database           | Supabase / PostgreSQL                 |
| AI Integration     | OpenAI API / Local LLM Option         |
| Data Sync          | Supabase / Firebase                   |
| Storage (optional) | LocalForage or IndexedDB              |
| Charts             | Recharts / Chart.js                   |

---

## Pages

- `/` → Welcome / onboarding  
- `/journal` → Daily entries (list view + create entry)  
- `/entry/[id]` → Single entry (edit/view)  
- `/stats` → Visualizations and insights  
- `/settings` → Theme, storage, AI toggle, privacy  

---

## Milestones

### Phase 1: MVP (Core Journaling)

- [ ] Entry creation/editing
- [ ] Calendar view
- [ ] Tags + mood tracker
- [ ] Auth & local storage

### Phase 2: AI & Visuals

- [ ] Summary and insights
- [ ] Charts + word cloud
- [ ] Prompt suggestions

### Phase 3: Pro Mode

- [ ] Encrypted cloud storage
- [ ] Offline mode
- [ ] Daily reminder emails
- [ ] Export to PDF/Markdown

---

## Stretch Features

- Voice-to-text journaling
- Daily quote + prompt generator
- “Year in Review” smart journal export
- Gamification (streaks, XP, badges)

---

## Success Metrics

- 90% of users create entries at least 3 times/week
- Average session length > 5 min
- >70% opt-in to AI features after first use
- <1 sec load time on mobile
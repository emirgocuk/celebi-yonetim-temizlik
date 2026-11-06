# Cline's Memory Bank Protocol & Operational Rules

## 1. Core Operating Philosophy
I am Cline, an expert software engineer with a unique operational characteristic: my memory resets completely between sessions. This is not a limitation—it is the catalyst for maintaining pristine, authoritative, and up-to-date documentation.

After every session reset, I rely **ENTIRELY** on this Memory Bank to understand the project architecture, context, business goals, and current progress.
**Mandatory Rule:** I MUST read ALL memory bank files at the start of EVERY task. This is non-negotiable.

---

## 2. Memory Bank Hierarchy & File Structure

The Memory Bank resides inside `vault/memory-bank/` and follows a strict hierarchy where each file has a dedicated responsibility:

```
vault/
├── memory-bank/
│   ├── projectbrief.md      <-- Foundation, scope, non-negotiable goals
│   ├── productContext.md    <-- Purpose, problems solved, UX & business goals
│   ├── activeContext.md     <-- Current sprint/focus, active decisions, immediate next steps
│   ├── systemPatterns.md    <-- Architecture, component patterns, data flow, performance design
│   ├── techContext.md       <-- Tech stack (Astro + PocketBase), setup, constraints
│   └── progress.md          <-- Status tracker (Done / In Progress / Backlog / Known Issues)
└── rules/
    ├── design-principles.md     <-- pbakaus/impeccable standards, Apple aesthetic, airy white theme
    ├── copywriting-anti-slop.md <-- petergyang/no-ai-slop rules, authentic Turkish corporate copy
    ├── performance-and-seo.md   <-- 100/100 PageSpeed Insights criteria, Core Web Vitals, Schema.org
    ├── tech-standards.md        <-- Astro 5, PocketBase, TypeScript, CSS architecture
    └── memory-bank-rules.md     <-- (This file) Protocol for maintaining the vault
```

---

## 3. Core File Responsibilities

1. **`projectbrief.md`**:
   - The permanent single source of truth for scope and core requirements.
   - Outlines client profile ("Çelebi Yönetim ve Temizlik"), primary tech stack (Astro + PocketBase), target benchmarks (100 PageSpeed, 100 SEO).

2. **`productContext.md`**:
   - Explains *why* the website exists and *what* problems it solves for site managers and building residents.
   - Defines user personas, customer journey, trust factors, and conversion funnels.

3. **`activeContext.md`**:
   - Captures real-time work focus.
   - Records the most recent modifications, open questions, and active design decisions (e.g., color token placeholders, logo integration roadmap).

4. **`systemPatterns.md`**:
   - Architectural patterns: Astro Islands, PocketBase collection schemas, component modularity.
   - Animation patterns: GPU-accelerated non-blocking CSS animations, dynamic Apple-style frosted header.

5. **`techContext.md`**:
   - Environment configurations, dependencies, Node runtime, PocketBase instance connection.
   - Performance budgeting and Core Web Vitals constraints.

6. **`progress.md`**:
   - Living checklist of working features, pending features, test validations, and known bugs.

---

## 4. Documentation Update Triggers

The Memory Bank MUST be updated under the following circumstances:
1. **Discovering New Patterns**: When an architectural, styling, or performance pattern is finalized.
2. **Post-Implementation**: Immediately after completing a significant feature or milestone.
3. **User Command**: When the user requests **"update memory bank"**, ALL files must be systematically reviewed and synchronized.
4. **Context Drift / Clarification**: Whenever scope or technical decisions are refined.

---

## 5. Session Initialization Workflow
At the beginning of any work session:
1. Read `vault/memory-bank/projectbrief.md`
2. Read `vault/memory-bank/productContext.md`
3. Read `vault/memory-bank/activeContext.md`
4. Read `vault/memory-bank/systemPatterns.md`
5. Read `vault/memory-bank/techContext.md`
6. Read `vault/memory-bank/progress.md`
7. Check relevant files in `vault/rules/` before writing code or copy.


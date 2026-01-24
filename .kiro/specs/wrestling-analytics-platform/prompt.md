
# ✅ MASTER PROMPT — DubStat Wrestling Analytics Platform

You are a senior full-stack engineer helping me improve an existing Wrestling Analytics MVP.

The system already has:

* A deployed frontend (Next.js + Supabase).
* A working Supabase database.
* An initial scraper using BeautifulSoup.


Your job is to **refactor the scraper to include playwright, add automation, add a dashboard and dashboard functionality with live updates,.**

---

## 🎯 GOAL

Build a robust scraping + analytics system for Ohio high school wrestling using DubStat’s free results database (THIS IS NOT A START UP, JUST A SMALL PROJECT, IT DOES NOT NEED TO BE COMPLEX OR BE ABLE TO HANDLE A LOT OF USERS YET)

The scraper must:

* Loop through **Gender → School → Wrestler → Results**
* Extract all matches per wrestler
* Insert normalized data into Supabase
* Be triggered manually from the dashboard

The dashboard must:

* Display statistics and graphs once data exists
* Allow the user to click a button to run the scraper
* Refresh automatically when scraping finishes

* I will give you some free rein in the design aspect for the dashboard: 
🧭 Dashboard Layout Ideas

Think in sections, not pages.

🏠 1. Home Overview Page

This is your landing page.

At the top:

🔢 Stat Cards

Row of big numbers:

Total Matches

Total Wrestlers

Win %

Pins %

Avg Match Score

Tournaments Scraped

Each card:

Icon

Big number

Small subtitle

Example:

[ 324 Matches ]
[ 61 Wrestlers ]
[ 58% Win Rate ]
[ 34% Pins ]

📈 Performance Over Time

Big line chart:

X-axis → Date

Y-axis → Wins / Matches

Toggle:

Wins

Matches

Pins

This answers:

“Are we improving over time?”

🥇 Top Performers

Table or cards:

Wrestler

Team

Wins

Win %

Pins

Sortable.

🤼 2. Wrestlers Page

Search + filter heavy.

🔍 Controls

Search by name

Filter by team

Filter by weight class

Sort by:

Wins

Win %

Pins

📋 Wrestler Table

Columns:

Name

Team

Weight

Wins

Losses

Win %

Pins

Clickable rows → profile page.

🧑‍💼 3. Wrestler Profile Page

This is where it gets powerful.

Top section:

👤 Header Card

Name

Team

Weight class

Record (W-L)

Win %

📊 Charts
Win/Loss Pie

Wins vs Losses

Win Types Bar

Pins

Tech Falls

Majors

Decisions

Matches Timeline

Line chart:

Date vs Result

📜 Match History Table

Columns:

Date

Tournament

Opponent

Result

Score

Round

Filterable and sortable.

🏫 4. Teams Page

Think coach dashboard.

🏆 Team Rankings

Table:

Team Name

Wrestlers

Total Wins

Win %

Pins

📊 Team Comparison

Bar chart:

Teams vs Wins

Or radar chart:

Wins

Pins

Techs

Matches

🏟️ 5. Tournaments Page
🗂️ Tournament List

Name

Date

Matches

Wins

Click → details.

📋 Tournament Detail Page

Tournament stats

Team performance

Top wrestlers

Match list

🧠 Interaction Ideas

These make your dashboard feel professional.

🔄 Run Scraper Button

Top right:

[ Run Scraper ]


When clicked:

Spinner

Button disabled

Status text:

“Scraping schools…”

“Scraping wrestlers…”

“Saving matches…”

Then auto refresh.

🎚 Filters Everywhere

Add dropdowns:

Team

Weight class

Date range

Tournament

So coaches can ask:

“Show me 132 lb wrestlers at Liberty in January.”

🧠 Compare Mode

Select two wrestlers:

Side-by-side stats

Charts comparison

📱 Mobile Friendly

Cards stack vertically

Tables collapse

Charts resize

🎨 UI Style Ideas

Since it’s wrestling:

Dark theme

Strong contrast

Rounded cards

Shadowed components

Minimal clutter

Data-forward

Think:

ESPN meets analytics.

🧱 Page Structure Example
Navbar
 ├── Home
 ├── Wrestlers
 ├── Teams
 ├── Tournaments
 └── Settings

Main
 ├── Stat Cards
 ├── Charts
 ├── Tables
 └── Buttons


---

## 🧱 TECH STACK (DO NOT CHANGE)

Backend / Scraper:

* Python
* Playwright (sync API)
* BeautifulSoup
* Supabase Python client
* python-dotenv

Frontend:

* Next.js (App Router)
* TypeScript
* Tailwind CSS
* Supabase JS client
* Chart library (Recharts or Chart.js)

Database:

* Supabase (schema already exists)

---

## 🚫 CONSTRAINTS

* Do NOT change database schema
* Do NOT add tables
* Do NOT invent columns
* Do NOT scrape hidden APIs
* Use HTML scraping via Playwright + BS4 only
* Keep code simple and readable
* No over-engineering, this is not a start up idea that needs to be scalable
* No auth system
* No background queues yet

---

## 🧠 SCRAPER ARCHITECTURE

Target: DubStat free results database page.

User flow on site:

```
Gender → School → Wrestler → Get Results → Table
```

Your scraper must replicate this using Playwright.

---

### 🔁 LOOP LOGIC

1. Open browser once.
2. Load DubStat database page.
3. Select gender option.
4. Get all school options.
5. For each school:

   * Select school.
   * Wait for wrestler dropdown to populate.
6. For each wrestler:

   * Select wrestler.
   * Click “Get Results”.
   * Wait for results table.
   * Capture HTML.
   * Parse with BeautifulSoup.
   * Extract all rows.
   * Insert into Supabase.
7. Continue until all wrestlers are scraped.
8. Close browser.

---

### 🔍 DATA EXTRACTION

From each results table row extract:

* tournament name
* round
* weight class
* wrestler name
* wrestler school
* opponent name
* opponent school
* result (W/L)
* score / win type

Skip rows that are empty or incomplete.

---

### 🧩 SCRAPER FUNCTIONS

Organize scraper with functions:

* load_page()
* select_gender()
* get_schools()
* get_wrestlers()
* scrape_wrestler_results()
* normalize_data()
* insert_into_supabase()

Add simple logging:

```
Scraping: School → Wrestler
Matches found: X
```

Handle failures gracefully without crashing loops.

---

## 🗄️ SUPABASE LOGIC

* Use environment variables.
* Do not hardcode credentials.
* Use service role key.
* Prevent duplicate wrestler creation.
* Insert one row per match per wrestler.

Re-running scraper may insert duplicates (fine for now).

---

## 🌐 DASHBOARD FEATURES

### 📊 Stats

Display:

* Total matches
* Wins / losses
* Win percentage
* Pins / techs / decisions breakdown
* Matches over time
* Team leaderboard

Use charts:

* Line chart → matches over time
* Bar chart → win types
* Pie chart → W vs L

---

### 🔘 SCRAPER BUTTON

Add a **“Run Scraper”** button.

Behavior:

1. User clicks button.
2. Frontend sends POST request to backend route `/api/run-scraper`.
3. Backend runs Python scraper process.
4. Button disables while running.
5. Loading indicator shows.
6. On completion, frontend refetches Supabase data.
7. Charts refresh automatically.

Handle errors gracefully.

---

## 🔌 BACKEND API

Create an API route:

```
POST /api/run-scraper
```

Responsibilities:

* Launch Playwright scraper.
* Return JSON status.
* Do not block UI permanently.
* Log progress.

---

## 🧱 TASK LIST

### Phase 1 — Scraper Refactor

* [ ] Replace requests/BS4 scraping with Playwright + BS4 hybrid
* [ ] Implement Gender → School → Wrestler loop
* [ ] Implement Playwright interactions
* [ ] Add waits after every action
* [ ] Parse results table
* [ ] Normalize data
* [ ] Insert into Supabase
* [ ] Add logging + failure handling

---

### Phase 2 — API Trigger

* [ ] Create POST /api/run-scraper route
* [ ] Connect route to Python scraper
* [ ] Return status JSON
* [ ] Add basic error handling

---

### Phase 3 — Dashboard Functionality

* [ ] Add Run Scraper button
* [ ] Add loading + disabled states
* [ ] Add stat queries from Supabase
* [ ] Build charts for wins, losses, trends
* [ ] Auto refresh data after scrape

---

### Phase 4 — UX Polish

* [ ] Add skeleton loaders
* [ ] Improve mobile layout
* [ ] Handle empty data states
* [ ] Improve table readability

---

## ✅ OUTPUT EXPECTATION

* Scraper loops all schools and wrestlers.
* Dashboard can trigger scraping.
* Stats update dynamically.
* Code stays simple and readable.
* No schema changes.
* No fake data fields.

---

## 🧠 MINDSET

Ship functionality first.
Optimize later.
Avoid complexity.
Make it work, then make it clean.

-- Final Notes:
I want you to delete and/or replace any code or files that are not needed
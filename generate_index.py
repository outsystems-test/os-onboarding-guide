"""
generate_index.py
Scans all *-guide.html files in the repo root and regenerates index.html.
Filename convention: {first}-{last}-week-{n}-guide.html
  e.g. lexie-porter-week-one-guide.html  →  "Lexie Porter", Week 1
"""

import glob
import os
import re
import json

WEEK_MAP = {
    "one": 1, "two": 2, "three": 3, "four": 4,
    "1": 1,   "2": 2,   "3": 3,    "4": 4,
}
WEEK_LABEL = {1: "Week One", 2: "Week Two", 3: "Week Three", 4: "Week Four"}
WEEK_KEY   = {1: "week-one", 2: "week-two", 3: "week-three", 4: "week-four"}

def parse_guide(filename):
    """Return (display_name, week_int) or None if filename doesn't match."""
    base = os.path.basename(filename)
    m = re.match(r'^(.+?)-week-(\w+)-guide\.html$', base)
    if not m:
        return None
    slug, week_str = m.group(1), m.group(2).lower()
    week = WEEK_MAP.get(week_str)
    if week is None:
        return None
    name = " ".join(part.capitalize() for part in slug.split("-"))
    return {"file": base, "name": name, "week": week}

def build_guides():
    files = sorted(glob.glob("*-guide.html"))
    guides = [g for f in files if (g := parse_guide(f))]
    return guides

def render_index(guides):
    unique_people = len({g["name"] for g in guides})
    total = len(guides)

    cards_js = json.dumps(guides, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>OutSystems Onboarding Guides</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --red:    #E8272A;
      --dark:   #0E0E0E;
      --mid:    #1A1A1A;
      --border: #2A2A2A;
      --muted:  #666;
      --light:  #F5F4F0;
    }}
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--dark); color: var(--light);
      font-family: 'DM Sans', sans-serif; font-weight: 300;
      min-height: 100vh; overflow-x: hidden;
    }}
    header {{
      padding: 4rem 6vw 3rem; border-bottom: 1px solid var(--border);
      position: relative; overflow: hidden;
    }}
    header::before {{
      content: ''; position: absolute; top: -60px; right: -60px;
      width: 320px; height: 320px; border-radius: 50%;
      background: radial-gradient(circle, rgba(232,39,42,0.18) 0%, transparent 70%);
      pointer-events: none;
    }}
    .logo-row {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2.5rem; }}
    .logo-dot {{
      width: 10px; height: 10px; border-radius: 50%; background: var(--red);
      animation: pulse 2.4s ease-in-out infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50%       {{ opacity: 0.5; transform: scale(0.8); }}
    }}
    .logo-label {{
      font-family: 'DM Mono', monospace; font-size: 0.7rem;
      letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted);
    }}
    h1 {{
      font-family: 'DM Serif Display', serif;
      font-size: clamp(2.4rem, 6vw, 4.8rem);
      line-height: 1.05; letter-spacing: -0.02em; max-width: 700px;
    }}
    h1 em {{ font-style: italic; color: var(--red); }}
    .subtitle {{
      margin-top: 1.2rem; font-size: 0.95rem; color: var(--muted);
      letter-spacing: 0.01em; max-width: 480px; line-height: 1.7;
    }}
    .stats-bar {{
      display: flex; gap: 3rem; padding: 1.6rem 6vw;
      border-bottom: 1px solid var(--border);
    }}
    .stat {{ display: flex; flex-direction: column; gap: 0.2rem; }}
    .stat-value {{ font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: var(--light); }}
    .stat-label {{
      font-family: 'DM Mono', monospace; font-size: 0.62rem;
      letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted);
    }}
    .filter-row {{
      padding: 1.4rem 6vw; display: flex; align-items: center;
      gap: 0.6rem; border-bottom: 1px solid var(--border); flex-wrap: wrap;
    }}
    .filter-label {{
      font-family: 'DM Mono', monospace; font-size: 0.65rem;
      letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); margin-right: 0.4rem;
    }}
    .filter-btn {{
      background: transparent; border: 1px solid var(--border); color: var(--muted);
      font-family: 'DM Mono', monospace; font-size: 0.68rem;
      letter-spacing: 0.1em; text-transform: uppercase;
      padding: 0.35rem 0.8rem; border-radius: 2px; cursor: pointer; transition: all 0.18s;
    }}
    .filter-btn:hover, .filter-btn.active {{
      background: var(--red); border-color: var(--red); color: white;
    }}
    .grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 1px; background: var(--border); padding: 1px;
      margin: 2rem 6vw; border: 1px solid var(--border);
    }}
    .card {{
      background: var(--mid); padding: 1.8rem 1.6rem;
      display: flex; flex-direction: column; gap: 1rem;
      text-decoration: none; color: inherit;
      position: relative; overflow: hidden; transition: background 0.2s;
      opacity: 0; transform: translateY(16px);
      animation: fadeUp 0.4s ease forwards;
    }}
    .card:hover {{ background: #222; }}
    .card::after {{
      content: ''; position: absolute; top: 0; left: 0;
      width: 3px; height: 100%; background: var(--red);
      transform: scaleY(0); transform-origin: bottom; transition: transform 0.22s ease;
    }}
    .card:hover::after {{ transform: scaleY(1); }}
    @keyframes fadeUp {{ to {{ opacity: 1; transform: none; }} }}
    .card-week {{
      font-family: 'DM Mono', monospace; font-size: 0.62rem;
      letter-spacing: 0.16em; text-transform: uppercase; color: var(--red);
    }}
    .card-name {{ font-family: 'DM Serif Display', serif; font-size: 1.35rem; line-height: 1.2; color: var(--light); }}
    .card-filename {{
      font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--muted);
      letter-spacing: 0.04em; margin-top: auto; padding-top: 0.8rem;
      border-top: 1px solid var(--border); display: flex; align-items: center; gap: 0.4rem;
    }}
    .card-filename svg {{ flex-shrink: 0; opacity: 0.4; }}
    .arrow {{
      position: absolute; top: 1.6rem; right: 1.6rem;
      width: 24px; height: 24px; color: var(--border); transition: color 0.18s, transform 0.18s;
    }}
    .card:hover .arrow {{ color: var(--red); transform: translate(3px, -3px); }}
    footer {{
      margin-top: 4rem; padding: 2rem 6vw; border-top: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 1rem;
    }}
    .footer-text {{
      font-family: 'DM Mono', monospace; font-size: 0.65rem;
      letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted);
    }}
    .footer-link {{ color: var(--muted); text-decoration: none; transition: color 0.15s; }}
    .footer-link:hover {{ color: var(--light); }}
    .empty {{
      grid-column: 1/-1; padding: 3rem; text-align: center;
      font-family: 'DM Mono', monospace; font-size: 0.75rem;
      letter-spacing: 0.1em; color: var(--muted); text-transform: uppercase;
    }}
  </style>
</head>
<body>

<header>
  <div class="logo-row">
    <div class="logo-dot"></div>
    <span class="logo-label">OutSystems — Onboarding</span>
  </div>
  <h1>New Hire<br><em>Guides</em></h1>
  <p class="subtitle">Personalised week-by-week onboarding documents, generated for each new team member joining the Revenue organisation.</p>
</header>

<div class="stats-bar">
  <div class="stat">
    <span class="stat-value">{total}</span>
    <span class="stat-label">Guides published</span>
  </div>
  <div class="stat">
    <span class="stat-value">{unique_people}</span>
    <span class="stat-label">People onboarded</span>
  </div>
</div>

<div class="filter-row">
  <span class="filter-label">Filter</span>
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="week-one">Week 1</button>
  <button class="filter-btn" data-filter="week-two">Week 2</button>
  <button class="filter-btn" data-filter="week-three">Week 3</button>
  <button class="filter-btn" data-filter="week-four">Week 4</button>
</div>

<div class="grid" id="grid"></div>

<footer>
  <span class="footer-text">os-onboarding-guide · outsystems-test</span>
  <a class="footer-text footer-link" href="https://github.com/outsystems-test/os-onboarding-guide" target="_blank">View on GitHub ↗</a>
</footer>

<script>
  const guides = {cards_js};
  const weekLabel = {{1:"Week One",2:"Week Two",3:"Week Three",4:"Week Four"}};
  const weekKey   = {{1:"week-one",2:"week-two",3:"week-three",4:"week-four"}};
  const grid = document.getElementById("grid");

  function render(filter) {{
    grid.innerHTML = "";
    const filtered = filter === "all" ? guides : guides.filter(g => weekKey[g.week] === filter);
    if (!filtered.length) {{
      grid.innerHTML = '<div class="empty">No guides found</div>';
      return;
    }}
    filtered.forEach((g, i) => {{
      const a = document.createElement("a");
      a.className = "card";
      a.href = g.file;
      a.style.animationDelay = i * 55 + "ms";
      a.innerHTML = `
        <svg class="arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M7 17L17 7M17 7H7M17 7v10"/>
        </svg>
        <span class="card-week">${{weekLabel[g.week]}}</span>
        <span class="card-name">${{g.name}}</span>
        <span class="card-filename">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          ${{g.file}}
        </span>`;
      grid.appendChild(a);
    }});
  }}

  document.querySelectorAll(".filter-btn").forEach(btn => {{
    btn.addEventListener("click", () => {{
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      render(btn.dataset.filter);
    }});
  }});

  render("all");
</script>
</body>
</html>"""

if __name__ == "__main__":
    guides = build_guides()
    html = render_index(guides)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ index.html regenerated — {len(guides)} guide(s) found.")

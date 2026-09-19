"""Landing page served at GET / — what a visitor sees when they open the
API's URL in a browser. Everything dynamic (title, version, endpoint list)
is read from the app's own OpenAPI schema, so it can't drift out of date
when routes change. Self-contained: inline CSS/JS, no external assets."""

import html

from fastapi import FastAPI

TAG_ORDER = ["users", "projects", "tasks", "health"]
TAG_BLURB = {
    "users": "Accounts. Passwords are hashed and never returned.",
    "projects": "Owned by a user. Owner must exist.",
    "tasks": "Belong to a project. Status: todo, in-progress, done.",
    "health": "Liveness check.",
}


def public_base_url(host: str, scheme: str) -> str:
    """Behind Render's TLS-terminating proxy the app sees plain http, so
    build https links for any non-local host."""
    local = host.split(":")[0] in {"localhost", "127.0.0.1", "0.0.0.0"}
    return f"{scheme if local else 'https'}://{host}"


def _endpoint_groups(app: FastAPI) -> str:
    groups: dict[str, list[tuple[str, str, str]]] = {}
    for path, methods in app.openapi().get("paths", {}).items():
        for method, op in methods.items():
            tag = (op.get("tags") or ["other"])[0]
            groups.setdefault(tag, []).append((method.upper(), path, op.get("summary", "")))

    ordered = [t for t in TAG_ORDER if t in groups] + [t for t in groups if t not in TAG_ORDER]
    cards = []
    for tag in ordered:
        rows = "".join(
            f'<li><span class="m {html.escape(m.lower())}">{html.escape(m)}</span>'
            f'<code>{html.escape(p)}</code></li>'
            for m, p, _summary in groups[tag]
        )
        blurb = html.escape(TAG_BLURB.get(tag, ""))
        cards.append(
            f'<section class="card"><h3>{html.escape(tag.title())}</h3>'
            f'<p class="blurb">{blurb}</p><ul>{rows}</ul></section>'
        )
    return "".join(cards)


def render_landing(app: FastAPI, base_url: str, environment: str, repo_url: str, label: str) -> str:
    title = html.escape(app.title)
    b = html.escape(base_url)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(app.description)}">
<style>
:root {{
  --bg:#f6f7f9; --panel:#fff; --text:#14181f; --muted:#5b6472; --line:#e3e6eb;
  --accent:#2563eb; --accent-text:#fff; --code:#f0f2f5; --ok:#15803d; --warn:#b45309; --bad:#b91c1c;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#15181d; --panel:#1d2128; --text:#e8ebf0; --muted:#98a1af; --line:#2d333c;
    --accent:#6ea0ff; --accent-text:#0b1220; --code:#252b34; --ok:#4ade80; --warn:#fbbf24; --bad:#f87171; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
a {{ color:var(--accent); }}
code,pre {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:.9em; }}
.wrap {{ max-width:960px; margin:0 auto; padding:0 20px; }}
header {{ padding:48px 0 28px; }}
.eyebrow {{ color:var(--muted); font-size:.85rem; letter-spacing:.06em; text-transform:uppercase; }}
h1 {{ margin:.3rem 0 .5rem; font-size:clamp(1.7rem,4vw,2.4rem); line-height:1.15; }}
.lead {{ color:var(--muted); max-width:60ch; margin:0 0 20px; }}
.row {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; }}
.pill {{ display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border-radius:999px;
  border:1px solid var(--line); background:var(--panel); font-size:.9rem; }}
.dot {{ width:9px; height:9px; border-radius:50%; background:var(--muted); }}
.pill.ok .dot {{ background:var(--ok); }} .pill.warn .dot {{ background:var(--warn); }}
.pill.bad .dot {{ background:var(--bad); }}
.btn {{ display:inline-block; padding:9px 16px; border-radius:8px; border:1px solid var(--line);
  background:var(--panel); color:var(--text); text-decoration:none; font-weight:600; font-size:.95rem; cursor:pointer; }}
.btn.primary {{ background:var(--accent); color:var(--accent-text); border-color:var(--accent); }}
.btn:focus-visible,a:focus-visible,button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
h2 {{ font-size:1.15rem; margin:36px 0 12px; }}
.grid {{ display:grid; gap:14px; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:16px 18px; }}
.card h3 {{ margin:0 0 2px; font-size:1rem; }}
.blurb {{ margin:0 0 10px; color:var(--muted); font-size:.88rem; }}
ul {{ list-style:none; margin:0; padding:0; }}
li {{ display:flex; align-items:baseline; gap:8px; padding:5px 0; border-top:1px solid var(--line); flex-wrap:wrap; }}
li code {{ font-size:.82rem; }} .s {{ color:var(--muted); font-size:.82rem; margin-left:auto; }}
.m {{ font:700 .68rem ui-monospace,Menlo,monospace; padding:2px 6px; border-radius:4px; min-width:52px; text-align:center;
  color:#fff; background:#64748b; }}
.m.get {{ background:#2563eb; }} .m.post {{ background:#15803d; }} .m.patch {{ background:#b45309; }}
.m.delete {{ background:#b91c1c; }} .m.put {{ background:#7c3aed; }}
.links a {{ display:block; text-decoration:none; color:inherit; }}
.links .card:hover {{ border-color:var(--accent); }}
.links strong {{ display:block; color:var(--accent); }} .links span {{ color:var(--muted); font-size:.88rem; }}
.snip {{ position:relative; background:var(--code); border:1px solid var(--line); border-radius:10px; margin:10px 0; }}
.snip pre {{ margin:0; padding:14px 76px 14px 16px; overflow-x:auto; }}
.snip button {{ position:absolute; top:8px; right:8px; padding:3px 9px; font-size:.75rem; border-radius:6px;
  border:1px solid var(--line); background:var(--panel); color:var(--text); cursor:pointer; }}
#out {{ display:none; margin:12px 0 0; }}
.note {{ color:var(--muted); font-size:.88rem; }}
footer {{ margin:44px 0 40px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:.88rem; }}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="eyebrow">{html.escape(label)} · Innovation Hacks Full Stack Internship</div>
  <h1>{title}</h1>
  <p class="lead">A REST API for users, projects, and tasks — validated inputs, one consistent
  error format, and interactive documentation you can try right here.</p>
  <div class="row">
    <span id="status" class="pill"><span class="dot"></span><span id="status-text">Checking status…</span></span>
    <span class="pill">v{html.escape(app.version)}</span>
    <span class="pill">{html.escape(environment)}</span>
  </div>
  <div class="row" style="margin-top:18px">
    <a class="btn primary" href="/docs">Open interactive docs</a>
    <button class="btn" id="check" type="button">Check API health</button>
    <a class="btn" href="{html.escape(repo_url)}">Source on GitHub</a>
  </div>
  <div class="snip" id="out"><pre id="out-pre"></pre></div>
</header>

<h2>Explore</h2>
<div class="grid links">
  <section class="card"><a href="/docs"><strong>Swagger UI →</strong><span>Send real requests from your browser with “Try it out”.</span></a></section>
  <section class="card"><a href="/redoc"><strong>ReDoc →</strong><span>Clean, readable reference for every schema and response.</span></a></section>
  <section class="card"><a href="/openapi.json"><strong>OpenAPI JSON →</strong><span>Machine-readable spec for client generators and Postman.</span></a></section>
</div>

<h2>Endpoints</h2>
<div class="grid">{_endpoint_groups(app)}</div>

<h2>Try it from a terminal</h2>
<div class="snip"><button type="button" data-copy>Copy</button><pre>curl -X POST {b}/users \\
  -H "Content-Type: application/json" \\
  -d '{{"name":"Ada Lovelace","email":"ada@example.com","password":"supersecret1"}}'</pre></div>
<div class="snip"><button type="button" data-copy>Copy</button><pre>curl {b}/users</pre></div>
<p class="note">Every error, including unknown routes, uses one shape:
<code>{{"error": {{"code", "message", "details"}}}}</code>. This service runs on a free tier, so the first
request after a quiet period can take up to a minute while it wakes. Data is held in memory and resets on restart.</p>

<footer>{title} · <a href="{html.escape(repo_url)}">{html.escape(repo_url.removeprefix("https://"))}</a></footer>
</div>
<script>
(function () {{
  var pill = document.getElementById("status"), text = document.getElementById("status-text");
  var out = document.getElementById("out"), pre = document.getElementById("out-pre");
  function set(cls, msg) {{ pill.className = "pill " + cls; text.textContent = msg; }}
  function check(show) {{
    var t0 = performance.now(), slow = setTimeout(function () {{ set("warn", "Waking up (free tier)…"); }}, 3000);
    return fetch("/health", {{ cache: "no-store" }}).then(function (r) {{
      return r.json().then(function (body) {{ return {{ r: r, body: body }}; }});
    }}).then(function (x) {{
      clearTimeout(slow);
      var ms = Math.round(performance.now() - t0);
      set(x.r.ok ? "ok" : "bad", x.r.ok ? "Operational · " + ms + " ms" : "Unhealthy (HTTP " + x.r.status + ")");
      if (show) {{ out.style.display = "block"; pre.textContent = "GET /health → " + x.r.status + " (" + ms + " ms)\\n" + JSON.stringify(x.body, null, 2); }}
    }}).catch(function () {{
      clearTimeout(slow); set("bad", "Unreachable");
      if (show) {{ out.style.display = "block"; pre.textContent = "Request failed."; }}
    }});
  }}
  document.getElementById("check").addEventListener("click", function () {{ check(true); }});
  document.querySelectorAll("[data-copy]").forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      var code = btn.parentNode.querySelector("pre").textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(code) : Promise.reject()).then(function () {{
        btn.textContent = "Copied"; setTimeout(function () {{ btn.textContent = "Copy"; }}, 1500);
      }}).catch(function () {{ btn.textContent = "Press Ctrl+C"; }});
    }});
  }});
  check(false);
}})();
</script>
</body>
</html>"""

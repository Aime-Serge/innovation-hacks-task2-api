"""Landing page served at GET / — what a visitor sees when they open the
API's URL in a browser. Everything dynamic (title, version, endpoint list)
is read from the app's own OpenAPI schema, so it can't drift out of date
when routes change. Self-contained: inline CSS/JS, no external assets."""

import html

from fastapi import FastAPI

TAG_ORDER = ["users", "projects", "tasks", "health"]
TAG_BLURB = {
    "users": "Passwords are hashed, never returned",
    "projects": "Each belongs to an existing user",
    "tasks": "todo · in-progress · done",
    "health": "Liveness check",
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
            f'<section><h3>{html.escape(tag.title())}</h3>'
            f'<p>{blurb}</p><ul>{rows}</ul></section>'
        )
    return "".join(cards)


def render_landing(app: FastAPI, base_url: str, environment: str, repo_url: str, label: str) -> str:
    title = html.escape(app.title)
    b = html.escape(base_url)
    repo = html.escape(repo_url)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(app.description)}">
<style>
:root {{
  --bg:#fff; --text:#111827; --muted:#6b7280; --line:#e5e7eb; --accent:#2563eb; --accent-text:#fff;
  --code:#f3f4f6; --ok:#15803d; --warn:#b45309; --bad:#b91c1c;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#111418; --text:#e7eaee; --muted:#9aa3af; --line:#272c34; --accent:#6ea0ff;
    --accent-text:#0b1220; --code:#1a1f26; --ok:#4ade80; --warn:#fbbf24; --bad:#f87171; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text);
  font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; }}
a {{ color:var(--accent); }}
code,pre {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }}
.wrap {{ max-width:840px; margin:0 auto; padding:56px 20px 40px; }}
.eyebrow {{ color:var(--muted); font-size:.8rem; letter-spacing:.08em; text-transform:uppercase; }}
h1 {{ margin:.4rem 0 .6rem; font-size:clamp(1.6rem,4.5vw,2.2rem); line-height:1.2; letter-spacing:-.01em; }}
.lead {{ margin:0 0 18px; color:var(--muted); }}
.meta {{ display:flex; flex-wrap:wrap; gap:16px; align-items:center; margin:0 0 24px; font-size:.9rem; color:var(--muted); }}
.status {{ display:inline-flex; align-items:center; gap:8px; color:var(--text); }}
.dot {{ width:8px; height:8px; border-radius:50%; background:var(--muted); }}
.status.ok .dot {{ background:var(--ok); }} .status.warn .dot {{ background:var(--warn); }} .status.bad .dot {{ background:var(--bad); }}
.cta {{ display:flex; flex-wrap:wrap; gap:14px; align-items:center; }}
.btn {{ display:inline-block; padding:10px 18px; border-radius:8px; background:var(--accent); color:var(--accent-text);
  font-weight:600; text-decoration:none; }}
a:focus-visible,button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
h2 {{ margin:40px 0 10px; font-size:.8rem; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); font-weight:600; }}
.step {{ margin:0 0 10px; }}
.snip {{ background:var(--code); border-radius:8px; }}
.snip pre {{ margin:0; padding:2px 16px 14px; overflow-x:auto; font-size:.85rem; }}
.snip .bar {{ display:flex; justify-content:flex-end; padding:8px 8px 0; }}
.snip button {{ padding:3px 10px; font-size:.75rem; border-radius:6px;
  border:1px solid var(--line); background:var(--bg); color:var(--text); cursor:pointer; }}
.eps {{ display:grid; gap:24px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); }}
.eps h3 {{ margin:0; font-size:.95rem; }} .eps p {{ margin:0 0 8px; color:var(--muted); font-size:.8rem; }}
ul {{ list-style:none; margin:0; padding:0; }}
li {{ display:flex; align-items:baseline; gap:8px; padding:4px 0; }}
li code {{ font-size:.8rem; overflow-wrap:break-word; min-width:0; }}
.m {{ flex:none; font:700 .62rem ui-monospace,Menlo,monospace; padding:2px 0; border-radius:4px; width:48px; text-align:center;
  color:#fff; background:#64748b; }}
.m.get {{ background:#2563eb; }} .m.post {{ background:#15803d; }} .m.patch {{ background:#b45309; }}
.m.delete {{ background:#b91c1c; }} .m.put {{ background:#7c3aed; }}
footer {{ margin-top:48px; padding-top:16px; border-top:1px solid var(--line); color:var(--muted); font-size:.85rem; }}
footer p {{ margin:0 0 6px; }}
</style>
</head>
<body>
<main class="wrap">
  <div class="eyebrow">{html.escape(label)} · Innovation Hacks</div>
  <h1>{title}</h1>
  <p class="lead">REST API for users, projects and tasks, with validated inputs and one consistent error format.</p>
  <div class="meta">
    <span id="status" class="status" role="status"><span class="dot"></span><span id="status-text">Checking status…</span></span>
    <span>v{html.escape(app.version)} · {html.escape(environment)}</span>
  </div>
  <div class="cta">
    <a class="btn" href="/docs">Open API docs</a>
    <a href="/redoc">ReDoc</a>
    <a href="{repo}">GitHub</a>
  </div>

  <h2>Quick start</h2>
  <p class="step">Create a user, then use the returned <code>id</code> as <code>owner_id</code> in <code>POST /projects</code>, and the project's <code>id</code> in <code>POST /tasks</code>.</p>
  <div class="snip"><div class="bar"><button type="button" id="copy">Copy</button></div><pre id="cmd">curl -X POST {b}/users \\
  -H "Content-Type: application/json" \\
  -d '{{"name":"Ada Lovelace","email":"ada@example.com","password":"supersecret1"}}'</pre></div>

  <h2>Endpoints</h2>
  <div class="eps">{_endpoint_groups(app)}</div>

  <footer>
    <p>Errors always use <code>{{"error": {{"code", "message", "details"}}}}</code>. Interactive docs: <a href="/docs">/docs</a> · Spec: <a href="/openapi.json">/openapi.json</a></p>
    <p>Free tier: the first request after inactivity can take up to a minute. Data is in memory and resets on restart.</p>
  </footer>
</main>
<script>
(function () {{
  var box = document.getElementById("status"), text = document.getElementById("status-text");
  function set(cls, msg) {{ box.className = "status " + cls; text.textContent = msg; }}
  var t0 = performance.now(), slow = setTimeout(function () {{ set("warn", "Waking up…"); }}, 3000);
  fetch("/health", {{ cache: "no-store" }}).then(function (r) {{
    clearTimeout(slow);
    var ms = Math.round(performance.now() - t0);
    set(r.ok ? "ok" : "bad", r.ok ? "Operational · " + ms + " ms" : "Unhealthy (HTTP " + r.status + ")");
  }}).catch(function () {{ clearTimeout(slow); set("bad", "Unreachable"); }});
  var btn = document.getElementById("copy");
  btn.addEventListener("click", function () {{
    var code = document.getElementById("cmd").textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(code) : Promise.reject()).then(function () {{
      btn.textContent = "Copied"; setTimeout(function () {{ btn.textContent = "Copy"; }}, 1500);
    }}).catch(function () {{ btn.textContent = "Ctrl+C"; }});
  }});
}})();
</script>
</body>
</html>"""

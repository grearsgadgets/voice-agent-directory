#!/usr/bin/env python3
"""Generate static site into ./site from data/platforms.json. No dependencies."""
import json, os, html, shutil
BASE = os.environ.get("SITE_URL", "https://example.com").rstrip("/")
NAME = "VoiceAgentIndex"
R = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(R, "data/platforms.json")))
OUT = os.path.join(R, "site"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/platforms")
e = lambda s: html.escape(s or "")
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f172a;background:#f8fafc;line-height:1.6}
a{color:#4f46e5}header{background:#0f172a;color:#fff}nav{max-width:1100px;margin:auto;display:flex;gap:20px;align-items:center;padding:14px 20px;flex-wrap:wrap}
nav a{color:#cbd5e1;text-decoration:none;font-size:15px}nav .logo{color:#fff;font-weight:800;font-size:19px;margin-right:auto}
main{max-width:1100px;margin:auto;padding:28px 20px}.hero{background:linear-gradient(135deg,#4f46e5,#06b6d4);color:#fff;border-radius:18px;padding:40px;margin-bottom:28px}
.hero h1{margin:0 0 8px;font-size:34px}.card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:22px;margin-bottom:20px}
.controls{display:flex;gap:10px;margin-bottom:14px;flex-wrap:wrap}input,select{padding:10px 12px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #e2e8f0}th,td{padding:12px 14px;text-align:left;border-bottom:1px solid #f1f5f9;vertical-align:top;font-size:14px}
th{background:#f1f5f9;cursor:pointer;user-select:none}.tag{display:inline-block;background:#eef2ff;color:#4338ca;border-radius:999px;padding:2px 10px;font-size:12px}
.btn{display:inline-block;background:#4f46e5;color:#fff;padding:10px 18px;border-radius:10px;text-decoration:none;font-weight:600}.muted{color:#64748b;font-size:13px}
footer{text-align:center;color:#64748b;font-size:13px;padding:30px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}"""
open(OUT + "/style.css", "w").write(CSS)
def page(path, title, desc, body, depth=0):
    pre = "../" * depth
    nav = f'<a class="logo" href="{pre}index.html">🎙️ {NAME}</a><a href="{pre}compare.html">Compare</a><a href="{pre}guides/choose-ai-receptionist.html">Guides</a><a href="{pre}advertise.html">Get featured</a><a href="{pre}disclosure.html">Disclosure</a>'
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}/{path}"><link rel="stylesheet" href="{pre}style.css"></head>
<body><header><nav>{nav}</nav></header><main>{body}</main><footer>Independent directory of AI voice agent platforms. Some links may be affiliate links — see our <a href="{pre}disclosure.html">disclosure</a>. Prices are as published on vendor sites on the date shown; always confirm on the vendor's site.</footer></body></html>"""
    os.makedirs(os.path.dirname(os.path.join(OUT, path)) or OUT, exist_ok=True)
    open(os.path.join(OUT, path), "w").write(doc); PAGES.append(path)
PAGES = []
def link(p, label=None, pre=""):
    return f'<a href="{e(p["url"])}" data-affiliate="{p["slug"]}" rel="sponsored noopener" target="_blank">{e(label or "Visit " + p["name"])}</a>'
cats = sorted({p["category"] for p in P})
rows = "".join(f'<tr data-cat="{e(p["category"])}"><td><a href="platforms/{p["slug"]}.html"><b>{e(p["name"])}</b></a></td><td><span class="tag">{e(p["category"])}</span></td><td>{e(p["pricing_model"]) or "—"}</td><td>{e(p["starting_price"]) or "Not published"}</td><td>{e(p["free_tier"]) or "—"}</td><td>{e(p["best_for"])}</td></tr>' for p in P)
opts = "".join(f"<option>{e(c)}</option>" for c in cats)
home = f"""<section class="hero"><h1>Find the right AI voice agent</h1><p>An independent, regularly checked directory of AI phone agent and AI receptionist platforms — with published pricing, features and who each one is best for.</p></section>
<div class="controls"><input id="q" placeholder="Search platforms…" oninput="f()"><select id="c" onchange="f()"><option value="">All categories</option>{opts}</select></div>
<table id="t"><thead><tr><th onclick="s(0)">Platform ↕</th><th onclick="s(1)">Category ↕</th><th onclick="s(2)">Pricing model ↕</th><th onclick="s(3)">Starting price ↕</th><th>Free tier / trial</th><th>Best for</th></tr></thead><tbody>{rows}</tbody></table>
<p class="muted">{len(P)} platforms · pricing checked {max(p["checked"] for p in P)}</p>
<div class="grid"><div class="card"><h3>New to voice agents?</h3><p>Read <a href="guides/choose-ai-receptionist.html">How to choose an AI receptionist for a small business</a>.</p></div>
<div class="card"><h3>Comparing costs?</h3><p>See <a href="guides/voice-agent-pricing-explained.html">Voice agent pricing models explained</a>.</p></div>
<div class="card"><h3>Building one?</h3><p>See <a href="guides/developer-platform-checklist.html">Developer platform evaluation checklist</a>.</p></div></div>
<script>function f(){{const q=document.getElementById('q').value.toLowerCase(),c=document.getElementById('c').value;document.querySelectorAll('#t tbody tr').forEach(r=>{{r.style.display=(r.textContent.toLowerCase().includes(q)&&(!c||r.dataset.cat===c))?'':'none'}})}}
let d=1;function s(i){{const b=document.querySelector('#t tbody');[...b.rows].sort((a,x)=>a.cells[i].textContent.localeCompare(x.cells[i].textContent,undefined,{{numeric:true}})*d).forEach(r=>b.appendChild(r));d=-d}}</script>"""
page("index.html", f"{NAME} — AI Voice Agent & AI Receptionist Directory", "Compare AI voice agent platforms like Retell, Vapi, Bland and Synthflow: published pricing, features and best use cases.", home)
for p in P:
    feats = "".join(f"<li>{e(x)}</li>" for x in p["features"])
    pr = f'<a href="{e(p["pricing_url"])}" target="_blank" rel="noopener">official pricing page</a>' if p["pricing_url"] else "vendor site"
    b = f"""<p class="muted"><a href="../index.html">All platforms</a> / {e(p["name"])}</p><div class="card"><span class="tag">{e(p["category"])}</span><h1>{e(p["name"])}</h1><p><b>Best for:</b> {e(p["best_for"])}</p><p class="btn">{link(p)}</p></div>
<div class="grid"><div class="card"><h2>Pricing</h2><p><b>Model:</b> {e(p["pricing_model"]) or "—"}<br><b>Starting price:</b> {e(p["starting_price"]) or "Not published"}<br><b>Free tier / trial:</b> {e(p["free_tier"]) or "—"}</p><p>{e(p["pricing_notes"])}</p><p class="muted">Source: {pr}, checked {p["checked"]}.</p></div>
<div class="card"><h2>Key features</h2><ul>{feats}</ul><p class="muted">From the vendor's own site; not independently tested.</p></div></div>"""
    page(f"platforms/{p['slug']}.html", f"{p['name']} pricing & review — {NAME}", f"{p['name']}: {p['best_for']}. Published pricing and key features, checked {p['checked']}."[:155], b, 1)
crow = "".join(f'<tr><td><a href="platforms/{p["slug"]}.html">{e(p["name"])}</a></td><td>{e(p["category"])}</td><td>{e(p["pricing_model"]) or "—"}</td><td>{e(p["pricing_notes"])}</td><td>{e(p["free_tier"]) or "—"}</td><td>{link(p,"Site")}</td></tr>' for p in P)
page("compare.html", f"Compare AI voice agent platforms side by side — {NAME}", "Side-by-side comparison of AI voice agent pricing models, free tiers and plans.", f"<h1>Compare AI voice agent platforms</h1><p>Per-minute developer platforms and flat-rate receptionists are priced very differently — read the pricing notes, not just the headline.</p><table><thead><tr><th>Platform</th><th>Category</th><th>Model</th><th>Pricing details</th><th>Free tier</th><th>Link</th></tr></thead><tbody>{crow}</tbody></table>")
G = {
"choose-ai-receptionist": ("How to choose an AI receptionist for a small business", "A practical checklist for picking an AI receptionist: call volume, pricing model, booking, transfers and trials.", """<h1>How to choose an AI receptionist for a small business</h1>
<div class="card"><h2>1. Count your calls first</h2><p>Pull last month's call log. Note total calls, average length and how many were missed. Minute-based plans (e.g. <a href="../platforms/rosie.html">Rosie</a>) and per-customer plans (e.g. <a href="../platforms/goodcall.html">Goodcall</a>) reward different patterns: long calls favour per-customer billing; few short calls favour small minute bundles.</p>
<h2>2. List the jobs it must do</h2><p>Message taking, appointment booking into your calendar, live or warm transfers to you, texting links, bilingual support. Check which plan tier includes each — booking and transfers are often not on the cheapest tier.</p>
<h2>3. Keep your number</h2><p>Prefer services that let you forward your existing number so you can switch providers later.</p>
<h2>4. Test with real scenarios</h2><p>Use the free trial or demo agent. Call it 10 times with your real questions, an angry caller, a wrong number and a spam call. Read the transcripts.</p>
<h2>5. Know when you need a developer platform</h2><p>If you need custom integrations or outbound campaigns at volume, look at <a href="../platforms/retell.html">Retell</a>, <a href="../platforms/vapi.html">Vapi</a> or <a href="../platforms/bland.html">Bland</a> — or hire an agency that builds on them.</p></div>"""),
"voice-agent-pricing-explained": ("AI voice agent pricing models explained", "Per-minute, all-in, per-customer and annual-contract pricing for AI voice agents compared, with how to estimate real cost.", """<h1>AI voice agent pricing models explained</h1>
<div class="card"><h2>Component per-minute (Vapi, Retell)</h2><p>You pay a platform fee per minute plus the speech-to-text, LLM, voice and telephony costs. Headline rates look low; the real rate depends on the models you pick. Retell publishes a $0.07–$0.31/min range; Vapi lists $0.05/min hosting plus provider costs.</p>
<h2>All-in per-minute (Bland)</h2><p>One rate covers LLM, STT and TTS (Bland Start: $0.14/min, telephony separate). Easier to forecast.</p>
<h2>Bundled minutes (Rosie)</h2><p>A monthly fee with included minutes — simple for small businesses; check overage terms.</p>
<h2>Per unique customer (Goodcall)</h2><p>Billed by distinct callers per month, not minutes, so long calls cost no more.</p>
<h2>Annual contracts (Synthflow Enterprise)</h2><p>Scoped deals (Synthflow lists from $30,000/year) including implementation.</p>
<h2>Estimate your cost</h2><p>Monthly minutes × all-in per-minute rate + phone numbers + concurrency add-ons + platform fee. Run it for your busiest month, not an average one.</p></div>"""),
"developer-platform-checklist": ("Voice agent developer platform evaluation checklist", "What to test before building on Retell, Vapi, Bland or similar: latency, concurrency, telephony, compliance and cost.", """<h1>Voice agent developer platform evaluation checklist</h1>
<div class="card"><ul><li><b>Latency:</b> time-to-first-word on a real phone line, not the web demo.</li><li><b>Interruptions:</b> does the agent stop talking when the caller cuts in?</li><li><b>Concurrency:</b> included limits differ (e.g. Retell 20 free, Vapi 4 on the no-package tier, Bland 10 on Start) — check add-on prices.</li><li><b>Telephony:</b> bring-your-own Twilio/SIP support and number porting.</li><li><b>Model choice:</b> can you swap LLM and voice, and what does each cost per minute?</li><li><b>Testing:</b> built-in simulation/testing before going live.</li><li><b>Compliance:</b> SOC 2, HIPAA BAA availability and which plan includes it.</li><li><b>Observability:</b> transcripts, recordings, data retention period, webhooks.</li><li><b>Exit plan:</b> can you export prompts, flows and call data?</li></ul></div>""")}
for slug, (t, d, b) in G.items():
    page(f"guides/{slug}.html", f"{t} — {NAME}", d, b, 1)
page("advertise.html", f"Advertise / get featured — {NAME}", "Reach businesses and developers choosing AI voice agent platforms. Featured listings and sponsorships.", """<h1>Advertise & get featured</h1><div class="grid">
<div class="card"><h2>Featured listing</h2><p>Highlighted row at the top of the directory and your category, with a "Featured" label.</p><p class="muted">Price: [TBD]</p></div>
<div class="card"><h2>Sponsored guide placement</h2><p>A clearly labelled sponsor block on a relevant guide.</p><p class="muted">Price: [TBD]</p></div>
<div class="card"><h2>Agency listing</h2><p>Build voice agents for clients? Get listed as an implementation partner.</p><p class="muted">Price: [TBD]</p></div></div>
<div class="card"><h2>Our rules</h2><p>Paid placements are always labelled. Payment never changes the facts we publish about any platform, and we list platforms whether or not they pay.</p><p>Contact: <b>[contact email TBD]</b></p></div>""")
page("disclosure.html", f"Affiliate disclosure — {NAME}", "How this directory makes money: affiliate links, featured listings and sponsorships.", """<h1>Affiliate disclosure</h1><div class="card"><p>Some links to platforms on this site are, or may become, affiliate links. If you sign up through them we may earn a commission at no extra cost to you.</p><p>We also sell clearly labelled featured listings and sponsorships. These never change the pricing or feature data we publish, which comes from each vendor's public website on the date shown.</p><p>We have not independently tested every platform; feature lists are taken from vendor sites. Always confirm pricing on the vendor's site before buying.</p></div>""")
open(OUT + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(OUT + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{BASE}/{p}</loc></url>\n" for p in PAGES) + "</urlset>\n")
print(f"Built {len(PAGES)} pages for {len(P)} platforms into site/")

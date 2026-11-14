import html, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from articles import ARTICLES, LISTINGS

BASE = "https://jorgeangelmejia-ev.github.io"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/site"
FORM = "https://form.jotform.com/263176099225059"
WA = "https://wa.me/message/A6LXEFOC6VP3D1"
LI = "https://www.linkedin.com/in/jorge1mejia/"
NAME = "Jorge Ángel Mejía"
ROLE = "Sales Manager · Engel & Völkers Tulum"
ADDR = "LT B88, Itzama, Aldea Zamá Manzana 26, 77760 Tulum, Q.R., Mexico"
SECTIONS = ["Market Intelligence", "Global Capital", "Buying Well", "Tulum",
            "Wellness Real Estate", "Branded Residences", "For Sellers"]
e = html.escape

CSS = """
:root{--black:#303030;--red:#E60000;--g3:#666;--g5:#999;--g7:#ccc;--beige:#F8F5F0;--beige1:#E2D9D0}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:var(--black);font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:1.6}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px}
.narrow{max-width:720px;margin:0 auto;padding:0 24px}
header.site{border-bottom:1px solid var(--g7);background:#fff;position:sticky;top:0;z-index:5}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-top:14px;padding-bottom:14px}
.brand{text-decoration:none;line-height:1.25}
.brand b{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:20px;display:block}
.brand span{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g3)}
nav.top a{font-size:12px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;margin-left:20px}
nav.top a:hover{color:var(--red)}
.btn{display:inline-block;background:var(--black);color:#fff;text-decoration:none;padding:13px 22px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--black)}
.btn:hover{background:#000}
.btn-outline{display:inline-block;border:1px solid var(--black);text-decoration:none;padding:12px 20px;font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.btn-outline:hover{border-color:var(--red)}
.hero{background:var(--beige);padding:88px 0 80px;text-align:center}
.kicker{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--g3);margin:0 0 18px}
h1,h2,h3{font-family:Georgia,'Times New Roman',serif;font-weight:400;line-height:1.3;margin:0}
.hero h1{font-size:46px;max-width:820px;margin:0 auto 22px}
.hero p.lead{max-width:640px;margin:0 auto 32px;color:var(--g3)}
.redline{width:1px;height:56px;background:var(--red);margin:0 auto}
section.block{padding:72px 0}
.sec-title{text-align:center;margin-bottom:40px}
.sec-title h2{font-size:32px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.card{display:block;text-decoration:none;border-top:1px solid var(--g7);padding-top:18px}
.card .kicker{margin-bottom:8px}
.card h3{font-size:21px;margin-bottom:10px}
.card p{font-size:15px;color:var(--g3);margin:0}
.card:hover h3{text-decoration:underline;text-decoration-color:var(--red);text-underline-offset:4px}
.num{font-size:12px;color:var(--g5);letter-spacing:.1em}
.about{display:grid;grid-template-columns:1fr 1px 1fr;gap:48px;align-items:start}
.about .vline{background:var(--red);height:100%;min-height:160px}
.facts{list-style:none;padding:0;margin:0}
.facts li{border-bottom:1px solid var(--g7);padding:12px 0;font-size:15px}
.facts li span{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g5)}
.listing{background:var(--beige);padding:32px;display:grid;grid-template-columns:2fr 1fr;gap:24px;align-items:center}
.cta{background:var(--black);color:#fff;text-align:center;padding:72px 24px}
.cta h2{font-size:32px;margin-bottom:14px}
.cta p{color:var(--g7);max-width:560px;margin:0 auto 28px}
.cta .btn{background:#fff;color:var(--black);border-color:#fff}
.cta .btn-outline{color:#fff;border-color:#fff;margin-left:10px}
article{padding:56px 0 24px}
article h1{font-size:40px;margin-bottom:18px}
article .meta{font-size:13px;color:var(--g5);margin-bottom:32px}
article h2{font-size:25px;margin:40px 0 12px}
article p{margin:0 0 18px}
article ul{padding-left:20px;margin:0 0 18px}article li{margin-bottom:8px}
blockquote{margin:36px 0;padding:4px 0 4px 24px;border-left:1px solid var(--red);font-family:Georgia,serif;font-size:22px;line-height:1.45}
.faq{background:var(--beige);padding:28px 32px;margin:40px 0}
.faq h2{margin-top:0}
.faq dt{font-weight:bold;margin-top:14px}.faq dd{margin:6px 0 0}
.author{display:flex;gap:16px;align-items:center;border-top:1px solid var(--g7);border-bottom:1px solid var(--g7);padding:20px 0;margin:40px 0}
.author p{margin:0;font-size:14px;color:var(--g3)}
.nextprev{display:flex;justify-content:space-between;gap:24px;margin:24px 0 56px;font-size:14px}
.nextprev a{text-decoration:none;max-width:48%}
.nextprev small{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g5)}
footer.site{border-top:1px solid var(--g7);padding:40px 0;font-size:12px;color:var(--g3);line-height:1.6}
footer.site .wrap{display:grid;grid-template-columns:2fr 1fr;gap:32px}
.hero-img{position:relative;height:72vh;min-height:440px;background:#303030 center/cover no-repeat;display:flex;align-items:flex-end}
.hero-img .box{background:#fff;max-width:640px;margin:0 0 48px 48px;padding:40px 44px}
.hero-img h1{font-size:40px;margin:0 0 16px}
.hero-img p.lead{color:#666;margin:0 0 26px}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
.pcard{text-decoration:none;display:block}
.pcard img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;margin-bottom:14px}
.pcard h3{font-size:22px;margin:4px 0 6px}
.pcard .price{font-size:15px;margin:0}
.pcard:hover h3{text-decoration:underline;text-decoration-color:var(--red);text-underline-offset:4px}
.gallery{display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:8px;margin:0 0 40px}
.gallery img{width:100%;height:100%;object-fit:cover;display:block}
.gallery .main{grid-row:1 / span 2;aspect-ratio:4/3}
.gallery .sub{aspect-ratio:auto;min-height:0}
.gallery-extra img{width:100%;margin-top:8px;display:block}
.specs{display:flex;flex-wrap:wrap;border-top:1px solid var(--g7);border-bottom:1px solid var(--g7);margin:28px 0}
.specs div{flex:1;min-width:130px;padding:16px 16px 16px 0;border-right:1px solid var(--red);margin-right:16px}
.specs div:last-child{border-right:none}
.specs span{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--g5)}
.specs b{font-weight:400;font-size:18px}
.note{font-size:12px;color:var(--g5)}
@media(max-width:820px){.pgrid{grid-template-columns:1fr}.hero-img .box{margin:0 16px 24px;padding:28px}.hero-img h1{font-size:30px}.gallery{grid-template-columns:1fr;grid-template-rows:auto}.gallery .main{grid-row:auto}}
@media(max-width:820px){.grid{grid-template-columns:1fr}.about{grid-template-columns:1fr}.about .vline{display:none}
.hero h1{font-size:34px}article h1{font-size:31px}nav.top{display:none}.listing{grid-template-columns:1fr}
footer.site .wrap{grid-template-columns:1fr}.cta .btn-outline{margin:12px 0 0}}
"""

def md(body):
    out = []
    for block in body.strip().split("\n\n"):
        block = block.strip()
        if block.startswith("## "):
            out.append(f"<h2>{e(block[3:])}</h2>")
        elif block.startswith("> "):
            out.append(f"<blockquote>{e(block[2:].strip())}</blockquote>")
        elif block.startswith("- "):
            items = "".join(f"<li>{e(l[2:])}</li>" for l in block.split("\n"))
            out.append(f"<ul>{items}</ul>")
        else:
            out.append(f"<p>{e(block)}</p>")
    return "\n".join(out)

def head(title, desc, url, extra_ld=None, prefix=""):
    ld = extra_ld or []
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{prefix}styles.css">{lds}</head><body>
<header class="site"><div class="wrap"><a class="brand" href="{prefix}index.html"><b>{NAME}</b><span>{ROLE}</span></a>
<nav class="top"><a href="{prefix}index.html#insights">Insights</a><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#properties">Properties</a><a href="{FORM}" target="_blank" rel="noopener">Contact</a></nav></div></header>"""

def cta(title="Find your place in Tulum"):
    return f"""<section class="cta"><h2>{e(title)}</h2>
<p>Tell me what you are looking for and I will come back with a considered answer, not a list of listings.</p>
<a class="btn" href="{FORM}" target="_blank" rel="noopener">Start the conversation</a><a class="btn-outline" href="{WA}" target="_blank" rel="noopener">WhatsApp</a></section>"""

FOOT = f"""<footer class="site"><div class="wrap"><div><b>{NAME}</b> · {ROLE}<br>{ADDR}<br>
Each Engel &amp; Völkers shop is independently owned and operated. Content is market commentary for general information and is not legal, tax or financial advice. Figures are cited from public sources as of publication and may change.</div>
<div><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><br><a href="{WA}" target="_blank" rel="noopener">WhatsApp</a><br><a href="{FORM}" target="_blank" rel="noopener">Contact form</a></div></div></footer></body></html>"""

PERSON = {"@context":"https://schema.org","@type":"RealEstateAgent","name":NAME,"jobTitle":"Sales Manager",
  "worksFor":{"@type":"Organization","name":"Engel & Völkers Tulum"},"url":BASE+"/","sameAs":[LI],
  "address":{"@type":"PostalAddress","streetAddress":"LT B88, Itzama, Aldea Zamá Manzana 26","addressLocality":"Tulum","addressRegion":"Quintana Roo","postalCode":"77760","addressCountry":"MX"},
  "areaServed":["Tulum","Riviera Maya","Playa del Carmen","Cancún"],"knowsLanguage":["en","es"]}

def build_properties():
    for i,l in enumerate(LISTINGS):
        p="../../"; url=f"{BASE}/properties/{l['slug']}/"
        imgs=[f"{p}img/{l['slug']}-{k}.jpg" for k in range(1,5)]
        ld=[{"@context":"https://schema.org","@type":"RealEstateListing","name":f"{l['name']}, {l['place']}","description":l["text"],"url":url,
             "image":[f"{BASE}/img/{l['slug']}-{k}.jpg" for k in range(1,5)],
             "offers":{"@type":"Offer","price":l["price"].replace("USD","").replace(",","").strip(),"priceCurrency":"USD"},
             "contentLocation":{"@type":"Place","name":l["place"]},"provider":{"@type":"RealEstateAgent","name":NAME,"url":BASE+"/"}}]
        specs="".join(f"<div><span>{e(a)}</span><b>{e(b)}</b></div>" for a,b in l["specs"])+f"<div><span>Price</span><b>{e(l['price'])}</b></div>"
        feats="".join(f"<li>{e(f)}</li>" for f in l["feats"])
        co=f'<p class="note">{e(l["co"])}, Engel &amp; Völkers Tulum.</p>' if l.get("co") else ""
        others="".join(f'<a class="pcard" href="{p}properties/{o["slug"]}/index.html"><img src="{p}img/{o["slug"]}-1.jpg" alt="{e(o["name"])}" loading="lazy"><p class="kicker" style="margin:0">{e(o["place"])}</p><h3>{e(o["name"])}</h3><p class="price">{e(o["price"])}</p></a>' for o in [x for x in LISTINGS if x is not l][:3])
        desc=f"{l['name']} in {l['place']}: {l['tagline'].lower()}. {l['price']}. Presented by {NAME}, Engel & Völkers Tulum."
        page=head(f"{l['name']} · {l['place']} · {l['price']} | Engel & Völkers Tulum", desc, url, ld, p)+f"""
<main><div class="wrap" style="padding-top:40px"><p class="kicker">{e(l['place'])}</p><h1 style="font-size:40px;margin-bottom:8px">{e(l['name'])}</h1>
<p style="color:#666;margin:0 0 28px">{e(l['tagline'])}</p>
<div class="gallery"><img class="main" src="{imgs[0]}" alt="{e(l['name'])}"><img class="sub" src="{imgs[1]}" alt="{e(l['name'])} interior" loading="lazy"><img class="sub" src="{imgs[2]}" alt="{e(l['name'])} detail" loading="lazy"></div></div>
<div class="narrow"><div class="specs">{specs}</div><p>{e(l['text'])}</p><h2 style="font-size:25px;margin:32px 0 12px">Highlights</h2><ul>{feats}</ul>
<img src="{imgs[3]}" alt="{e(l['name'])}" loading="lazy" style="width:100%;margin:24px 0">
<p><a class="btn" href="{FORM}" target="_blank" rel="noopener">Request the brochure and a private viewing</a></p>{co}
<p class="note">Information deemed reliable but not guaranteed. Price and availability subject to change without notice. Prices in Mexican pesos are subject to the exchange rate agreed at signing. Measurements are approximate and must be verified against the relevant documentation.</p></div>
<section class="block"><div class="wrap"><div class="sec-title"><p class="kicker">Also available</p><h2>More residences</h2></div><div class="pgrid">{others}</div></div></section>
{cta('Find your place in Tulum')}</main>"""+FOOT
        d=os.path.join(OUT,"properties",l["slug"]); os.makedirs(d)
        open(os.path.join(d,"index.html"),"w").write(page)

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img"), os.path.join(OUT,"img"))
    ordered = [a for s in SECTIONS for a in ARTICLES if a["section"] == s]
    # article pages
    for i, a in enumerate(ordered):
        url = f"{BASE}/insights/{a['slug']}/"
        ld = [{"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["desc"],
               "datePublished":a["date"],"author":{"@type":"Person","name":NAME,"url":BASE+"/"},
               "publisher":{"@type":"Organization","name":"Engel & Völkers Tulum"},"mainEntityOfPage":url,"inLanguage":"en"}]
        faq = a.get("faq")
        if faq:
            ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in faq]})
        p = "../../"
        prev_ = ordered[i-1] if i > 0 else None
        next_ = ordered[i+1] if i < len(ordered)-1 else None
        nav = '<div class="nextprev">'
        nav += f'<a href="{p}insights/{prev_["slug"]}/index.html"><small>Previous</small>{e(prev_["title"])}</a>' if prev_ else "<span></span>"
        nav += f'<a style="text-align:right" href="{p}insights/{next_["slug"]}/index.html"><small>Next</small>{e(next_["title"])}</a>' if next_ else "<span></span>"
        nav += "</div>"
        faq_html = ""
        if faq:
            faq_html = '<div class="faq"><h2>Frequently asked</h2><dl>' + "".join(f"<dt>{e(q)}</dt><dd>{e(ans)}</dd>" for q,ans in faq) + "</dl></div>"
        series = f' · {e(a["series"])}' if a.get("series") else ""
        page = head(f'{a["title"]} | {NAME}, Engel & Völkers Tulum', a["desc"], url, ld, p) + f"""
<main><article class="narrow"><p class="kicker">{e(a['section'])}{series}</p><h1>{e(a['title'])}</h1>
<p class="meta">By {NAME} · {a['date']}</p>{md(a['body'])}{a.get('cta_extra','')}{faq_html}
<div class="author"><div><b>{NAME}</b><p>Sales Manager at Engel &amp; Völkers Tulum. Advising international buyers and sellers in Tulum and the Riviera Maya, in English and Spanish, after nearly 20 years living in Tulum.</p></div></div>
{nav}</article>{cta(a.get('cta_title','Find your place in Tulum'))}</main>""" + FOOT
        d = os.path.join(OUT, "insights", a["slug"]); os.makedirs(d)
        open(os.path.join(d, "index.html"), "w").write(page)
    # home
    cards = []
    n = 0
    for s in SECTIONS:
        items = [a for a in ordered if a["section"] == s]
        if not items: continue
        cs = ""
        for a in items:
            n += 1
            cs += f'<a class="card" href="insights/{a["slug"]}/index.html"><p class="kicker"><span class="num">{n:02d}</span> · {e(a["section"])}</p><h3>{e(a["title"])}</h3><p>{e(a["desc"])}</p></a>'
        cards.append(cs)
    grid = "".join(cards)
    lst = "".join(f'<a class="pcard" href="properties/{l["slug"]}/index.html"><img src="img/{l["slug"]}-1.jpg" alt="{e(l["name"])}, {e(l["place"])}" loading="lazy"><p class="kicker" style="margin:0">{e(l["place"])}</p><h3>{e(l["name"])}</h3><p class="price">{e(l["price"])}</p></a>' for l in LISTINGS)
    build_properties()
    desc = "Jorge Ángel Mejía, Sales Manager at Engel & Völkers Tulum: market intelligence, branded residences and advisory for buying and selling real estate in Tulum and the Riviera Maya."
    home = head(f"{NAME} | Tulum & Riviera Maya Real Estate Advisor · Engel & Völkers", desc, BASE+"/", [PERSON], "") + f"""
<main><section class="hero-img" style="background-image:url('img/villa-hunab-ku-1.jpg')" role="img" aria-label="Villa Hunab Ku courtyard, Aldea Zamá, Tulum"><div class="box"><p class="kicker">Tulum · Riviera Maya · Engel &amp; Völkers</p>
<h1>Real estate decisions in Tulum, made with evidence</h1>
<p class="lead">Market intelligence, branded residences and considered advice for international buyers and sellers, from someone who has lived in Tulum for nearly 20 years.</p>
<a class="btn" href="index.html#properties">View properties</a> <a class="btn-outline" href="{FORM}" target="_blank" rel="noopener" style="margin-left:6px">Find your place</a></div></section>
<div class="redline"></div>
<section class="block" id="insights"><div class="wrap"><div class="sec-title"><p class="kicker">Insights</p><h2>Read in order: from the market to the decision</h2></div>
<div class="grid">{grid}</div></div></section>
<section class="block" id="about" style="background:#F8F5F0"><div class="wrap about">
<div><p class="kicker">About</p><h2 style="font-size:32px;margin-bottom:18px">{NAME}</h2>
<p>Active in leisure and hospitality real estate since 2002, with consulting experience in the United States, Canada, Southeast Asia, Ireland, Uruguay and Mexico. I left Mexico City for Tulum almost 20 years ago, after a career in hospitality, leisure and marketing.</p>
<p>Today I lead sales at Engel &amp; Völkers Tulum, working with international buyers, sellers and family offices on residences, branded residences and investment property across the Riviera Maya.</p></div>
<div class="vline"></div>
<ul class="facts"><li><span>Focus</span>Tulum, Riviera Maya, Cancún</li><li><span>Specialties</span>Branded residences · Market analysis · CMAs</li><li><span>Languages</span>English · Español</li><li><span>Office</span>{ADDR}</li></ul></div></section>
<section class="block" id="properties"><div class="wrap"><div class="sec-title"><p class="kicker">Properties</p><h2>Selected residences in Tulum</h2></div><div class="pgrid">{lst}</div>
<p style="text-align:center;margin-top:36px"><a class="btn-outline" href="{FORM}" target="_blank" rel="noopener">Ask about off-market opportunities</a></p></div></section>
{cta()}</main>""" + FOOT
    open(os.path.join(OUT, "index.html"), "w").write(home)
    open(os.path.join(OUT, "styles.css"), "w").write(CSS)
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    urls = [BASE+"/"] + [f"{BASE}/insights/{a['slug']}/" for a in ordered] + [f"{BASE}/properties/{l['slug']}/" for l in LISTINGS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
    print(len(ordered), "articles built in", OUT)

build()

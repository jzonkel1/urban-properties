# -*- coding: utf-8 -*-
"""
Urban Properties site builder.
  src/home.html  = the master (CSS, nav, footer, scripts live here; edit design there)
  build.py       = generates index.html + every subpage folder from the shell in src/home.html
Run:  python build.py
Pages are one folder deep (e.g. /apply/index.html) so links use a {R} prefix:
  "" on the home page, "../" on subpages.
"""
import io, os, re, html
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
SRC = io.open("src/home.html", encoding="utf-8").read()

# ---------------------------------------------------------------- pieces
head_end = SRC.index("</head>")
HEAD = SRC[:head_end]
nav_a = SRC.index('<header class="nav">')
nav_b = SRC.index("<!-- ============ HERO ============ -->")
NAV = SRC[nav_a:nav_b]
# topbar sits between <body> and header
body_a = SRC.index("<body>") + len("<body>")
TOPBAR = SRC[body_a:nav_a]
foot_a = SRC.index("<footer")
script_a = SRC.index("<script>", foot_a)
FOOTER = SRC[foot_a:script_a]           # footer + callbar + demo tag
script_b = SRC.index("</script>", script_a)
SCRIPT = SRC[script_a + len("<script>"):script_b]
form_split = SCRIPT.index("/* ---- US phone")
SCRIPT_COMMON = SCRIPT[:form_split]
SCRIPT_FORM = SCRIPT[form_split:]
wiz_a = SRC.index('<form class="formwrap" id="wiz"')
wiz_b = SRC.index("</form>", wiz_a) + len("</form>")
WIZARD = SRC[wiz_a:wiz_b]

# ---------------------------------------------------------------- link map (label -> page)
LINKS = {
    "Full-Service Management": "full-service-management/",
    "Tenant Screening &amp; Placement": "tenant-screening-placement/",
    "Tenant Placement": "tenant-screening-placement/",
    "Rent Collection &amp; Owner Deposits": "rent-collection-owner-deposits/",
    "Rent Collection": "rent-collection-owner-deposits/",
    "Maintenance Coordination": "maintenance-coordination/",
    "Maintenance": "maintenance-coordination/",
    "Lease Renewals &amp; Enforcement": "lease-renewals-enforcement/",
    "Move-In / Move-Out Inspections": "move-in-move-out-inspections/",
    "Free Rental Market Analysis": "rent-analysis/",
    "Free Rent Analysis": "rent-analysis/",
    "What We Charge": "what-we-charge/",
    "How Onboarding Works": "how-onboarding-works/",
    "Investment Property Sales": "investment-property-sales/",
    "Commercial Leasing &amp; Multifamily": "commercial-leasing-multifamily/",
    "Commercial &amp; Multifamily": "commercial-leasing-multifamily/",
    "Residential Sales": "residential-sales/",
    "Residential &amp; Land Sales": "residential-sales/",
    "Lot &amp; Land Sales": "lot-land-sales/",
    "Build-to-Rent: From Dirt to Deposit": "build-to-rent/",
    "Build-to-Rent for Investors": "build-to-rent/",
    "Build-to-Rent": "build-to-rent/",
    "Available Rentals": "available-rentals/",
    "Apply for a Rental": "apply/",
    "Pay Rent": "pay-rent/",
    "Submit a Maintenance Request": "maintenance-request/",
    "Tenant FAQs": "tenant-faqs/",
    "Corpus Christi": "corpus-christi/",
    "Padre Island": "padre-island/",
    "Calallen": "calallen/",
    "Robstown": "robstown/",
    "Surrounding Areas": "service-areas/",
    "About Urban Properties": "about/",
    "About Us": "about/",
    "Our Companies": "our-companies/",
    "Urban Properties": "our-companies/",
    "Reviews": "reviews/",
    "Contact": "contact/",
}
TOP = {  # top-level nav anchors
    "#services": "property-management/", "#owners": "rent-analysis/", "#tenants": "tenants/",
    "#areas": "service-areas/", "#about": "about/", "#analysis": "rent-analysis/",
}

def relink(block):
    """Rewrite in-page anchors in nav/footer/callbar to real page paths with an {R} prefix."""
    def sub(m):
        href, label = m.group(1), m.group(2)
        if not href.startswith("#"):
            return m.group(0)
        if label.strip() in LINKS:
            return '<a href="{R}%s">%s</a>' % (LINKS[label.strip()], label)
        return '<a href="{R}%s">%s</a>' % (TOP.get(href, href), label)
    block = re.sub(r'<a href="([^"]+)">([^<]+)</a>', sub, block)
    # top-level items that contain a caret svg
    for anchor, page in TOP.items():
        block = block.replace('<a href="%s">' % anchor, '<a href="{R}%s">' % page)
        block = block.replace("<a href=\"%s\"\n" % anchor, "<a href=\"{R}%s\"\n" % page)
    block = block.replace('href="#" class="brand"', 'href="{R}" class="brand"')
    block = block.replace('<a class="btn btn-p" href="#analysis">', '<a class="btn btn-p" href="{R}rent-analysis/">')
    block = block.replace('<a class="btn btn-g" href="#analysis">', '<a class="btn btn-g" href="{R}rent-analysis/">')
    block = block.replace('<a class="c2" href="#analysis">', '<a class="c2" href="{R}rent-analysis/">')
    block = block.replace('class="dlink" href="#reviews"', 'class="dlink" href="{R}reviews/"')
    block = block.replace('class="dlink" href="#contact"', 'class="dlink" href="{R}contact/"')
    block = block.replace('src="img/', 'src="{R}img/')
    block = block.replace('<a href="#">Information About Brokerage Services</a>', '<a href="{R}docs/TREC-Information-About-Brokerage-Services.pdf" target="_blank" rel="noopener">TREC Information About Brokerage Services</a>')
    block = block.replace('<a href="#">Consumer Protection Notice</a>', '<a href="{R}docs/TREC-Consumer-Protection-Notice.pdf" target="_blank" rel="noopener">TREC Consumer Protection Notice</a>')
    block = block.replace('<a href="#">Privacy Policy</a>', '<a href="{R}privacy-policy/">Privacy Policy</a><a href="{R}terms-of-use/">Terms of Use</a><a href="{R}accessibility/">Accessibility</a><a href="{R}fair-housing/">Fair Housing</a>')
    return block

NAV = relink(NAV)
FOOTER = relink(FOOTER)

# ---------------------------------------------------------------- extra CSS (shared)
EXTRA_CSS = """
/* ---- page hero + photo bands (added by build.py) ---- */
.phero{position:relative;min-height:clamp(380px,48vh,540px);display:flex;align-items:flex-end;background:var(--ink);overflow:hidden}
.phero .hero-bg{position:absolute;inset:0}.phero .hero-bg img{width:100%;height:100%;object-fit:cover}
.phero .wrap{position:relative;z-index:2;width:100%;padding-top:110px;padding-bottom:58px}
.phero .eyebrow{color:#DCA8EA}.phero .eyebrow::after{background:rgba(255,255,255,.3)}
.phero h1{color:#fff;font-size:clamp(36px,4.8vw,64px);line-height:1.06;letter-spacing:-.018em;max-width:17ch}
.phero h1 em{font-style:normal;color:#E2B4EE}
.gal-cap figure{position:relative}.gal-cap figcaption{position:absolute;left:0;right:0;bottom:0;padding:26px 14px 11px;color:#fff;font-size:14px;font-weight:600;line-height:1.3;background:linear-gradient(transparent,rgba(23,20,27,.78))}
/* group photo: pin right, fade into ink on the left so the headline never sits on a face */
.phero-team .hero-bg img{position:absolute;right:0;top:0;width:60%;height:100%;object-position:50% 30%;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,rgba(0,0,0,.55) 7%,#000 15%);mask-image:linear-gradient(90deg,transparent 0,rgba(0,0,0,.55) 7%,#000 15%)}
.phero-team .hero-scrim{background:linear-gradient(94deg,rgba(18,14,22,.92) 0%,rgba(18,14,22,.82) 30%,rgba(18,14,22,.3) 45%,rgba(18,14,22,.12) 100%)}
@media(max-width:860px){.phero-team .hero-bg img{width:100%;object-position:60% 20%;-webkit-mask-image:none;mask-image:none}}
.phero p.hl{color:#DAD3E2;font-size:clamp(16.5px,1.3vw,19.5px);margin:18px 0 26px;max-width:54ch}
.crumb{font-size:13px;color:#A79FB2;margin-bottom:18px;display:flex;gap:8px;flex-wrap:wrap}.crumb a{color:#DCA8EA}
.phero .hero-trust{margin-top:26px}
/* phones: subpage heroes centred like the home hero, trust lines left-aligned inside a centred block */
@media(max-width:860px){
  .phero{align-items:center;min-height:auto}
  .phero .wrap{text-align:center;padding-top:80px;padding-bottom:54px}
  .phero .crumb{justify-content:center}
  .phero .eyebrow{justify-content:center;font-size:10.5px;letter-spacing:.13em;gap:9px;flex-wrap:nowrap}
  .phero .eyebrow::before{content:"";height:1px;flex:1;max-width:34px;background:rgba(255,255,255,.3)}
  .phero .eyebrow::after{max-width:34px}
  .phero h1{max-width:none}
  .phero p.hl{margin-left:auto;margin-right:auto}
  .phero .hero-btns{justify-content:center}.phero .hero-btns .btn{flex:1 1 260px}
  .phero .hero-trust{display:inline-grid;grid-template-columns:1fr;gap:11px;text-align:left;margin-top:26px}
  .phero .hero-scrim{background:linear-gradient(to bottom,rgba(18,14,22,.72) 0%,rgba(18,14,22,.68) 45%,rgba(18,14,22,.88) 100%)}
}
.photo-band{position:relative;overflow:hidden;background:var(--ink);color:#DAD3E2}
.photo-band .pb-bg{position:absolute;inset:0}.photo-band .pb-bg img{width:100%;height:100%;object-fit:cover}
.photo-band .pb-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(23,20,27,.95) 0%,rgba(23,20,27,.86) 45%,rgba(23,20,27,.66) 100%)}
.photo-band .wrap{position:relative;z-index:2}
.photo-band h2,.photo-band h3,.photo-band h4{color:#fff}.photo-band .lead{color:#DAD3E2}.photo-band p{color:#CFC8D8}
.photo-band .eyebrow{color:#DCA8EA}.photo-band .eyebrow::after,.photo-band .eyebrow::before{background:rgba(255,255,255,.25)}
.photo-band .idx{border-top-color:rgba(255,255,255,.2)}.photo-band .idx li{border-bottom-color:rgba(255,255,255,.2)}
.photo-band .idx a,.photo-band .idx .cur{color:#fff}.photo-band .idx a svg{color:#E2B4EE}.photo-band .idx a:hover{color:#E2B4EE}
.photo-band .team{border-top-color:rgba(255,255,255,.15)}.photo-band .team-h{color:#DCA8EA}
.photo-band .team li{border-bottom-color:rgba(255,255,255,.15)}.photo-band .team li b{color:#fff}.photo-band .team li span{color:#C9C2CF}
.photo-band .mapbox{border-color:rgba(255,255,255,.15)}
.cta-band .pb-bg::after{background:linear-gradient(180deg,rgba(23,20,27,.8),rgba(23,20,27,.92))}
.cta-band .wrap{text-align:center}.cta-band .lead{margin-left:auto;margin-right:auto}
.facts2{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:28px}
.fact{display:flex;gap:13px;align-items:flex-start;padding:16px;border-radius:14px;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12)}
.fact .fi{flex:none;width:40px;height:40px;border-radius:11px;display:grid;place-items:center;background:linear-gradient(180deg,#9140a5,#681f77);color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.25)}
.fact .fi svg{width:20px;height:20px}.fact b{display:block;color:#fff;font-size:17px;line-height:1.2}.fact p{margin:3px 0 0;font-size:14px;color:#C9C2CF;line-height:1.45}
.roster{margin-top:28px;padding:18px;border-radius:16px;background:var(--paper-2);border:1px solid var(--line)}
.roster-h{font-size:11.5px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--pur);margin-bottom:12px}
.av{flex:none;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-size:13px;font-weight:800;background:var(--pur-wash);color:var(--pur)}
.av-lg{width:48px;height:48px;font-size:16px;background:linear-gradient(180deg,#9140a5,#681f77);color:#fff}
.broker{display:flex;gap:13px;align-items:center;padding-bottom:14px;margin-bottom:12px;border-bottom:1px solid var(--line)}
.broker b,.agents b{display:block;color:var(--ink);font-size:16px;line-height:1.2}.broker span:not(.av),.agents span:not(.av){font-size:13px;color:var(--muted)}
.agents{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,1fr);gap:12px 16px}.agents li{display:flex;gap:10px;align-items:center}
.photo-band .roster{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.12)}.photo-band .roster-h{color:#DCA8EA}
.photo-band .broker{border-bottom-color:rgba(255,255,255,.14)}.photo-band .broker b,.photo-band .agents b{color:#fff}.photo-band .broker span:not(.av),.photo-band .agents span:not(.av){color:#C9C2CF}
.photo-band .av:not(.av-lg){background:rgba(226,180,238,.16);color:#E2B4EE}
@media(max-width:560px){.facts2,.agents{grid-template-columns:1fr}}
/* home about band: widened team photo (team-wide = real photo + extended office wing on the left), people on the right */
/* phones, tablets, small laptops: the whole team photo as a band on top, text below (below 1400 the
   text column is too wide for the group to fit beside it at full band height) */
@media(max-width:1399px){.about-band{padding-top:0}
  .about-band .pb-bg{position:relative;inset:auto;aspect-ratio:9/5;margin-bottom:34px}
  .about-band .pb-bg img{object-position:100% 45%}
  .about-band .pb-bg::after{background:linear-gradient(180deg,rgba(23,20,27,0) 60%,rgba(23,20,27,.55) 85%,var(--ink) 100%)}}
/* phones: zoom the band a touch so the people read clearly; origin low so nobody's feet leave the frame */
@media(max-width:860px){.about-band{padding-bottom:56px}.about-band+section{border-top:1px solid rgba(255,255,255,.12);padding-top:64px}.about-band .pb-bg{overflow:hidden}.about-band .pb-bg img{transform:scale(1.22);transform-origin:50% 80%}}
@media(max-width:1399px){.about-band .wrap.g2{grid-template-columns:1fr}.about-band .wrap.g2>div:empty{display:none}}
@media(min-width:981px) and (max-width:1399px){.about-band .facts2{grid-template-columns:repeat(4,1fr)}}
/* Where We Work: lighter scrim so the coast shows through */
#areas .pb-bg::after{background:linear-gradient(90deg,rgba(23,20,27,.88) 0%,rgba(23,20,27,.7) 42%,rgba(23,20,27,.34) 100%)}
@media(max-width:860px){#areas .pb-bg::after{background:linear-gradient(180deg,rgba(23,20,27,.8) 0%,rgba(23,20,27,.66) 45%,rgba(23,20,27,.5) 100%)}}
#areas .wrap{text-shadow:0 1px 14px rgba(0,0,0,.35)}
/* wide screens: photo at full band height, roofline to feet, no top fade. The group is pinned to the right
   edge: 466 of the photo's 1075px height is building to the right of the group, so right = -43.3cqh */
@media(min-width:1400px){.about-band{padding:76px 0}
  .about-band .pb-bg{background:var(--ink);container-type:size}
  .about-band .pb-bg img{position:absolute;top:0;bottom:auto;left:auto;right:calc(8px - 43.3cqh);height:100%;width:auto;max-width:none;
    -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 18%);mask-image:linear-gradient(90deg,transparent 0,#000 18%)}
  .about-band .pb-bg::after{background:linear-gradient(90deg,rgba(23,20,27,.96) 0%,rgba(23,20,27,.9) calc(50% - 300px),rgba(23,20,27,.5) calc(50% - 90px),rgba(23,20,27,.1) calc(50% + 80px),rgba(23,20,27,.05) 100%)}}
.facts{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:32px}
.facts div>div{font-family:var(--serif);font-weight:700;font-size:19px;color:#fff}.facts p{font-size:14.5px;color:#C9C2CF;margin:4px 0 0}
.prose p{font-size:17px;color:var(--body);max-width:68ch;margin:0 0 18px;line-height:1.7}
.prose h3{font-size:26px;margin:34px 0 10px}
.faq details{border-top:1px solid var(--line);padding:18px 0}.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font-family:var(--serif);font-weight:700;font-size:21px;color:var(--ink);list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--pur);font-size:26px;line-height:1;flex:none}.faq details[open] summary::after{content:"\\2013"}
.faq p{margin:12px 0 0;color:var(--body);max-width:70ch;font-size:16px}
.fee-row.big b{font-size:26px}
.form-plain{background:#fff;border:1px solid var(--line);border-radius:18px;box-shadow:var(--sh-l);padding:34px;max-width:680px;margin:0 auto}
.form-plain .btn{width:100%;margin-top:6px}
.note-box{background:var(--pur-wash);border:1px solid #E4CFEA;border-radius:14px;padding:18px 22px;font-size:15px;color:var(--body)}
.note-box b{color:var(--pur)}
"""
HEAD = HEAD.replace("</style>", EXTRA_CSS + "</style>", 1)

# ---------------------------------------------------------------- helpers
PHONE = '(361) 434-0040'; TEL = 'tel:+13614340040'
JON_TEL = 'tel:+13615102325'; JON_SMS = 'sms:+13615102325'
CALL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>'
CHECK = '<li><svg viewBox="0 0 24 24" style="stroke:var(--pur)"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg><span style="color:var(--body)">%s</span></li>'
CHECK_D = '<li><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>%s</li>'

def pic(img, alt, lazy=True):
    base = img.rsplit(".", 1)[0]
    return ('<picture><source srcset="{R}img/%s.webp" type="image/webp"><img src="{R}img/%s" alt="%s"%s></picture>'
            % (base, img, html.escape(alt), ' loading="lazy"' if lazy else ''))

ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

HERO_TRUST = SRC[SRC.index('<ul class="hero-trust">'):SRC.index('</ul>', SRC.index('<ul class="hero-trust">')) + 5]
TRUST_STRIP = SRC[SRC.index('<section class="trust">'):SRC.index('</section>', SRC.index('<section class="trust">')) + 10]

def hero(eyebrow, h1, hl, img, crumb, btn2=None):
    b2 = btn2 or ('<a class="btn btn-o btn-lg cta-quote" href="{R}rent-analysis/">Get a free rent analysis %s</a>' % ARR)
    return '''<section class="phero%s">
  <div class="hero-bg">%s</div>
  <div class="hero-scrim"></div><div class="hero-scrim2"></div>
  <div class="wrap">
    <div class="crumb"><a href="{R}">Home</a><span>/</span>%s</div>
    <div class="eyebrow">%s</div>
    <h1>%s</h1>
    <p class="hl">%s</p>
    <div class="hero-btns">
      <a class="btn btn-p btn-lg cta-call" href="%s">%s Call %s</a>
      %s
    </div>
    %s
  </div>
</section>''' % (" phero-team" if img.startswith("team") else "", pic(img, re.sub(r"<[^>]+>", "", h1), lazy=False), crumb, eyebrow, h1, hl, TEL, CALL_SVG, PHONE, b2, HERO_TRUST)

def cta(kind="owner"):
    if kind == "tenant":
        return '''<section class="sec photo-band cta-band">
  <div class="pb-bg">%s</div>
  <div class="wrap">
    <div class="eyebrow c">Questions?</div>
    <h2 class="big">Text the office. A real person answers.</h2>
    <p class="lead">Repairs, rent, applications, anything about your lease.</p>
    <div class="cta-row cta-c" style="margin-top:30px">
      <a class="btn btn-p" href="%s">Text (361) 510-2325</a>
      <a class="btn btn-o" href="%s">%s Call %s</a>
    </div>
  </div>
</section>''' % (pic("int-living.jpg", ""), JON_SMS, TEL, CALL_SVG, PHONE)
    return '''<section class="sec photo-band cta-band">
  <div class="pb-bg">%s</div>
  <div class="wrap">
    <div class="eyebrow c">Free, No Obligation</div>
    <h2 class="big">Let&rsquo;s find out what your property is worth.</h2>
    <p class="lead">A real number from a licensed local broker, and what we&rsquo;d fix first. Yours to keep whether or not you hire us.</p>
    <div class="cta-row cta-c" style="margin-top:30px">
      <a class="btn btn-p btn-lg" href="{R}rent-analysis/">Get your free rent analysis today <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      <a class="btn btn-o" href="%s">%s Call %s</a>
    </div>
  </div>
</section>''' % (pic("hero.jpg", ""), TEL, CALL_SVG, PHONE)

def intro(eyebrow, h2, paras, bullets, img, alt, imgfirst=False, extra=""):
    ps = "".join('<p class="lead">%s</p>' % p if i == 0 else '<p style="color:var(--muted);margin-top:14px">%s</p>' % p for i, p in enumerate(paras))
    ul = ('<ul class="checks" style="color:var(--body)">%s</ul>' % "".join(CHECK % b for b in bullets)) if bullets else ""
    txt = '<div><div class="eyebrow">%s</div><h2 class="big">%s</h2>%s%s%s</div>' % (eyebrow, h2, ps, ul, extra)
    im = '<div class="band-img" style="box-shadow:var(--sh-l)">%s</div>' % pic(img, alt)
    inner = (im + txt) if imgfirst else (txt + im)
    return '<section class="sec"><div class="wrap g2%s">%s</div></section>' % (" imgfirst" if imgfirst else "", inner)

def gallery(eyebrow, h2, lead, items, bg=False, more=None):
    """items: (img, caption, cls) - captioned photo grid, reuses .gal"""
    figs = "".join('<figure class="%s">%s<figcaption>%s</figcaption></figure>' % (c, pic(i, cap), cap) for i, cap, c in items)
    return ('<section class="sec"%s><div class="wrap"><div class="center" style="margin-bottom:40px"><div class="eyebrow c">%s</div>'
            '<h2 class="big">%s</h2><p class="lead">%s</p></div><div class="gal gal-cap">%s</div>%s</div></section>'
            % (' style="background:var(--paper-2);border-top:1px solid var(--line)"' if bg else "", eyebrow, h2, lead, figs,
               ('<div class="center cta-row cta-c" style="margin-top:34px"><a class="btn btn-g btn-lg" href="{R}gallery/#%s">See the full gallery %s</a></div>' % (more, ARR)) if more else ""))

def cards(eyebrow, h2, items, lead="", bg=True):
    cs = "".join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in items)
    style = ' style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"' if bg else ""
    return '''<section class="sec"%s><div class="wrap">
  <div class="center" style="margin-bottom:50px"><div class="eyebrow c">%s</div><h2 class="big">%s</h2>%s</div>
  <div class="g3">%s</div></div></section>''' % (style, eyebrow, h2, ('<p class="lead">%s</p>' % lead) if lead else "", cs)

def faq(eyebrow, h2, qs):
    ds = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in qs)
    return '''<section class="sec"><div class="wrap" style="max-width:860px">
  <div class="center" style="margin-bottom:40px"><div class="eyebrow c">%s</div><h2 class="big">%s</h2></div>
  <div class="faq">%s</div></div></section>''' % (eyebrow, h2, ds)

def steps4(eyebrow, h2, items):
    st = "".join('<div class="step">%s<h4>%s</h4><p>%s</p></div>' % ('<div class="bar"></div>' if i < len(items) - 1 else '', h, p) for i, (h, p) in enumerate(items))
    return '''<section class="sec"><div class="wrap"><div class="center" style="margin-bottom:58px"><div class="eyebrow c">%s</div><h2 class="big">%s</h2></div><div class="steps">%s</div></div></section>''' % (eyebrow, h2, st)

FEES = '''<div class="fee" id="fees" style="margin-top:0">
  <div class="fee-h">What we charge</div>
  <div class="fee-row big"><b>One month&rsquo;s rent</b><span>to find, screen and place your tenant. <strong>Collected out of their first month&rsquo;s rent, not from you.</strong></span></div>
  <div class="fee-row big"><b>10% of rent</b><span>each month for ongoing management. Rent comes in, your share is deposited, the rest is handled.</span></div>
  <div class="fee-row big"><b>Either one on its own</b><span>Already have a tenant? <strong>Just&nbsp;the&nbsp;management.</strong> Want to manage it yourself? <strong>Just&nbsp;the&nbsp;placement.</strong></span></div>
</div>'''

SERVICE_LIST = [
    ("full-service-management/", "Full-Service Management"),
    ("tenant-screening-placement/", "Tenant Screening &amp; Placement"),
    ("rent-collection-owner-deposits/", "Rent Collection &amp; Owner Deposits"),
    ("maintenance-coordination/", "Maintenance Coordination"),
    ("lease-renewals-enforcement/", "Lease Renewals &amp; Enforcement"),
    ("move-in-move-out-inspections/", "Move-In / Move-Out Inspections"),
    ("investment-property-sales/", "Investment Property Sales"),
    ("residential-sales/", "Residential Sales"),
    ("lot-land-sales/", "Lot &amp; Land Sales"),
    ("commercial-leasing-multifamily/", "Commercial Leasing &amp; Multifamily"),
]
def idx(items, current=None, cls=""):
    """editorial index list: items = [(href, label)]; the current page shows as a marked row"""
    return '<ul class="idx%s">%s</ul>' % (" " + cls if cls else "", "".join(
        '<li><span class="cur">%s <small>This page</small></span></li>' % l if p == current
        else '<li><a href="%s"%s>%s %s</a></li>' % (p, ' target="_blank" rel="noopener"' if p.startswith("http") else "", l, ARR)
        for p, l in items))
def service_links(current=None):
    return idx([("{R}" + p, l) for p, l in SERVICE_LIST], "{R}" + current if current else None)

LANDING = set()   # services, towns, hubs, owner pages -> trust strip under the hero
LANDING.update(p for p, _ in SERVICE_LIST)
LANDING.update(["property-management/", "service-areas/", "rent-analysis/", "what-we-charge/", "how-onboarding-works/", "build-to-rent/"])
TOWNS = [("corpus-christi/", "Corpus Christi"), ("padre-island/", "Padre Island"), ("calallen/", "Calallen"), ("robstown/", "Robstown")]
LANDING.update(p for p, _ in TOWNS)

# ---------------------------------------------------------------- pages
PAGES = []
def page(slug, title, desc, body, crumb_label=None, cta_kind="owner", has_form=False):
    if cta_kind == "tenant":
        body = body.replace(HERO_TRUST, "", 1)   # owner proof lines don't belong on tenant pages
    if slug in LANDING:
        i = body.index("</section>") + len("</section>")   # first section = the hero
        body = body[:i] + "\n" + TRUST_STRIP + body[i:]
    PAGES.append(dict(slug=slug, title=title, desc=desc, body=body, crumb=crumb_label or title, cta=cta_kind, form=has_form))

# ---- services --------------------------------------------------------
def service_page(slug, title, eyebrow, h1, hl, img, intro_h2, paras, bullets, card_items, qs, img2):
    body = (hero(eyebrow, h1, hl, img, '<a href="{R}property-management/">Property Management</a><span>/</span><span>%s</span>' % title)
            + intro("What&rsquo;s Included", intro_h2, paras, bullets, img2, title)
            + cards("The Details", "What that looks like in practice", card_items)
            + faq("Common Questions", "Owners usually ask", qs)
            + '<section class="sec-tight" style="border-top:1px solid var(--line)"><div class="wrap"><div class="eyebrow">Everything Else We Handle</div>%s</div></section>' % service_links(slug))
    page(slug, title, hl, body)

service_page("full-service-management/", "Full-Service Management", "Property Management", "The whole thing, <em>handled.</em>",
    "Marketing, leasing, rent, maintenance and renewals, run by a licensed Corpus Christi broker. You get the deposit. We get the phone calls.",
    "prop-blue-street.jpg", "Everything a rental needs, from one office.",
    ["Full-service management is the option most of our owners pick, because it turns a rental into something that behaves like an investment: money arrives, problems get solved, and you find out about the ones that matter.",
     "It starts with a free rent analysis and a walkthrough, and after that the tenant calls us, not you."],
    ["Listing, showings and screening through our sister firm CC Lease Locators", "Lease written, signed and enforced by a licensed Texas broker",
     "Rent collected and your share auto-deposited every month", "Maintenance dispatched to trades we already trust", "Renewals negotiated before the lease runs out",
     "Move-in and move-out inspections with photos"],
    [("One point of contact", "Jon and the office. Not a call center, not a ticket number."),
     ("No news is good news", "You hear from us when something needs a decision or costs more than $250. Otherwise the deposit is the update."),
     ("Ten percent, all in", "One fee for ongoing management. No markups on repairs, no surprise line items."),
     ("Your rules, enforced", "Late fees, pet policies, lease terms. We hold the line so you don&rsquo;t have to."),
     ("Owner of record stays you", "Your property, your deposit account, your decisions on anything big."),
     ("Sell when you&rsquo;re ready", "The broker managing the door can also list it. Same office, same file.")],
    [("How fast can you take over a property that already has a tenant?", "We collect the lease, the deposit records and the keys, introduce ourselves to the tenant, and rent comes to us from the next due date."),
     ("Do I approve the tenant?", "Yes. We screen and recommend; you say yes before anyone signs."),
     ("What if I only want part of this?", "Then you pay for that part. Placement only is one month&rsquo;s rent. Management only is 10%. See <a href=\"{R}what-we-charge/\">what we charge</a>.")],
    "int-kitchen-open.jpg")

service_page("tenant-screening-placement/", "Tenant Screening &amp; Placement", "Find The Right Tenant", "The decision that decides the next <em>two years.</em>",
    "Income and rental history verified, then a signed lease. One month&rsquo;s rent, paid out of the tenant&rsquo;s first month.",
    "int-kitchen-white.jpg", "A good tenant is the whole game.",
    ["Most rental headaches trace back to one bad placement. So we treat screening like the most important thing we do, because it is.",
     "Our sister firm, CC Lease Locators, places renters across Corpus Christi, which means your vacancy gets a steady stream of candidates who are already looking."],
    ["Listed on the MLS and syndicated to Zillow, Realtor.com, Trulia, Redfin and Homes.com", "Showings handled by our agents", "Income and rental history verified on every applicant",
     "$50 application fee paid by the applicant, not you", "You approve the tenant before anyone signs", "Lease prepared and executed by a licensed broker"],
    [("Priced right, from day one", "A vacancy that sits for six weeks costs more than a rent that&rsquo;s $50 too low. We price from real comps."),
     ("Screened, not guessed", "Stable income, verified history, a clean background. We don&rsquo;t rent to a good feeling."),
     ("Fast, because we have the flow", "CC Lease Locators already has renters looking. Your unit goes in front of them the day it&rsquo;s listed."),
     ("Move-in documented", "Photos and a condition report before the keys change hands, so the deposit conversation later is simple."),
     ("Placement only, if that&rsquo;s all you want", "Find the tenant, sign the lease, hand it back to you. One month&rsquo;s rent, done."),
     ("Or keep going", "Add management and the same office collects the rent and takes the calls.")],
    [("What do you charge to place a tenant?", "One month&rsquo;s rent, collected out of the tenant&rsquo;s first month. You don&rsquo;t write a check."),
     ("Who pays the application fee?", "The applicant. $50 per application."),
     ("What are the requirements?", "Stable, verifiable income and rental history preferred. Pets and other specifics are set with you, per property.")],
    "ext-duplex-front.jpg")

service_page("rent-collection-owner-deposits/", "Rent Collection &amp; Owner Deposits", "Get Paid On Time", "Rent comes in. Your share <em>goes out.</em> Automatically.",
    "Clear due dates, consistent follow-up, and your money deposited to your account every month without you chasing anyone.",
    "int-living.jpg", "You should never have to ask a tenant for money.",
    ["We set the due date, the grace period and the late fee in the lease, and then we enforce them the same way every month. Tenants pay us, by check, cash, Cash App or a scheduled transfer, and your share is deposited to you.",
     "No monthly paperwork lands in your inbox unless something happened. Anything over $250 gets itemized and sent to you."],
    ["Due dates and late fees written into the lease and enforced", "Tenants pay the office: check, cash, Cash App, Avail, Venmo or PayPal", "Your share auto-deposited every month",
     "Follow-up on late rent handled by us, in writing", "Itemized notice for any expense over $250", "Eviction filings coordinated if it ever comes to that"],
    [("Auto-deposit", "Rent clears, your portion is deposited. You see it in your bank, not in a spreadsheet you have to reconcile."),
     ("Late rent, handled", "Reminders, late fees, notices. The tenant hears from the office, never from you."),
     ("No news is good news", "We don&rsquo;t send reports for the sake of reports. When there&rsquo;s nothing to report, there&rsquo;s nothing in your inbox."),
     ("Over $250? You&rsquo;ll know", "Any repair or expense above $250 comes to you itemized before or as it happens."),
     ("Ten percent, all in", "Management is 10% of collected rent. That&rsquo;s the fee."),
     ("Tax time", "Ask and we&rsquo;ll pull the year&rsquo;s numbers for your accountant.")],
    [("When do I get paid?", "After rent clears each month, your share is deposited to the account you give us at onboarding."),
     ("What if the tenant pays late?", "The late fee kicks in per the lease and we follow up in writing. You&rsquo;re told if it becomes a pattern."),
     ("Do I get a statement every month?", "Only when something happened. An itemized notice goes out for any expense over $250; otherwise the deposit is the statement.")],
    "prop-grey-row.jpg")

service_page("maintenance-coordination/", "Maintenance Coordination", "Repairs Without The 2 A.M. Call", "Tenants call <em>us.</em> Trades we trust show up.",
    "Repair requests come to the office by text or call, we dispatch vetted local trades, and you hear about anything over $250 before it happens.",
    "stock-tools.jpg", "One call ends it. And it isn&rsquo;t to you.",
    ["A water heater doesn&rsquo;t care what time it is. Our tenants text or call the office, and the office decides what&rsquo;s urgent, who to send and what it should cost.",
     "We use plumbers, electricians and handymen we&rsquo;ve worked with for years, on our own buildings as well as yours."],
    ["Tenant requests by text or call to (361) 510-2325", "Vetted local trades, no markup on their invoice", "Your approval on anything over $250",
     "Emergencies go to the front of the line", "Photos before and after when it matters", "Preventive items caught at inspections"],
    [("Text or call", "Tenants text the office with the address and the problem. Photos help. Emergencies, they call."),
     ("Triage first", "Not every request is a repair. Some are a reset button or a filter. We sort that before anyone drives out."),
     ("Trades we already use", "The same people who service the eight-unit complex and the commercial building we own."),
     ("Your $250 line", "Under it, we handle it and note it. Over it, you approve it first."),
     ("No markup", "You pay what the trade charges. Coordination is part of the 10%."),
     ("Documented", "Every request, who went, what it cost. Ask any time.")],
    [("Do I have to approve every repair?", "Only over $250. Small items are handled so the tenant isn&rsquo;t waiting and you aren&rsquo;t getting a call about a faucet."),
     ("Can I use my own plumber?", "Yes. Tell us at onboarding and they go on the list for your property."),
     ("Who pays for tenant damage?", "The tenant, out of the deposit or by invoice, per the lease. Wear and tear is the owner&rsquo;s.")],
    "stock-maintenance.jpg")

service_page("lease-renewals-enforcement/", "Lease Renewals &amp; Enforcement", "Written By A Broker", "Leases that hold up, and get <em>renewed.</em>",
    "Texas leases prepared and enforced by a licensed broker, renewals negotiated before the term ends, and rules that actually get followed.",
    "prop-grey-row.jpg", "A lease is only as good as the person enforcing it.",
    ["We use current Texas lease forms, filled out for your property and your rules: pets, smoking, occupancy, late fees, maintenance responsibilities.",
     "Well before a lease ends we&rsquo;re already talking to the tenant about renewal and to you about the rent. Turnover is the most expensive thing that happens to a rental; we try not to let it happen by accident."],
    ["Texas lease forms, prepared by a licensed broker", "Your rules written in and enforced", "Renewal conversations start well before the lease ends",
     "Rent adjusted to market at renewal, with your approval", "Notices served properly and on time", "Eviction coordinated with counsel if it ever comes to it"],
    [("The right paperwork", "Lease, addenda, disclosures and the notices Texas requires. Done correctly the first time."),
     ("Renewals ahead of time", "Good tenants get asked to stay before they start looking. Rent moves with the market."),
     ("Enforcement without drama", "Late fees, unauthorized occupants, unapproved pets. Handled in writing, by the office."),
     ("Notices done right", "Timing and delivery matter in Texas. We follow the statute."),
     ("You decide the big things", "Renew, raise, or let it end. You get a recommendation and the final say."),
     ("If it goes wrong", "Rare, but if a tenancy has to end early we coordinate the process start to finish.")],
    [("Can I use my own lease?", "We&rsquo;ll review it. Most owners switch to the current Texas forms because they hold up better."),
     ("How much do you raise rent at renewal?", "To market, if the market moved, and only with your approval. Keeping a good tenant is usually worth more than the last $25."),
     ("What happens if a tenant stops paying?", "Notices per the lease and Texas law, then the eviction process if needed. You&rsquo;re told at every step.")],
    "int-living.jpg")

service_page("move-in-move-out-inspections/", "Move-In / Move-Out Inspections", "Documented Both Ways", "Photos in. Photos out. <em>No arguments.</em>",
    "A documented condition report with photos at move-in and move-out, so the deposit is settled on evidence instead of memory.",
    "int-kitchen-white.jpg", "The deposit conversation is easy when it&rsquo;s on paper.",
    ["Before a tenant gets the keys, we walk the property and document its condition with photos. When they leave, we do it again.",
     "That record is what makes a deposit deduction fair and defensible, and it&rsquo;s what tells you when a unit needs work before the next listing."],
    ["Room-by-room condition report with photos", "Condition documented before the keys change hands", "Move-out walkthrough within days of vacancy",
     "Deposit itemization per Texas rules and timelines", "Make-ready list so the unit relists fast", "Records kept for the life of the tenancy"],
    [("Move-in", "Documented and signed before the first night. The tenant knows exactly what they&rsquo;re responsible for."),
     ("During", "Maintenance visits are a chance to catch small problems before they grow."),
     ("Move-out", "Compared against the move-in report. Damage beyond wear and tear comes out of the deposit."),
     ("Deposit handled", "Itemized and returned within the timeline Texas requires. We do the paperwork."),
     ("Make-ready", "Paint, clean, repair. We line up the trades so the unit is back on the market quickly."),
     ("Fewer vacant days", "The whole point. Turnover handled fast is money you don&rsquo;t lose.")],
    [("Do I need to be there?", "No. You&rsquo;re welcome to, but the report and photos come to you either way."),
     ("How long does a turnover take?", "Depends on condition. A clean unit relists in days. We tell you the make-ready scope and cost up front."),
     ("Who decides deposit deductions?", "We recommend based on the reports and Texas rules; you approve.")],
    "stock-inspection.jpg")

service_page("investment-property-sales/", "Investment Property Sales", "Buy The Next Door", "The broker who manages it can help you <em>buy it.</em>",
    "Buying the next rental or selling the last one. A full Texas brokerage in the same office that manages your property.",
    "prop-blue-street.jpg", "We know what it will rent for before you make the offer.",
    ["Most investors buy with a guess about rent and a guess about expenses. We manage thirty doors in this market; we know what a duplex on that street rents for and what it costs to run.",
     "That&rsquo;s the advantage of buying through the office that will manage it: the numbers you underwrite are the numbers you&rsquo;ll actually see."],
    ["MLS opportunities across Corpus Christi, vetted by a manager", "Rent and expense estimates from a manager, not a listing", "Offer, inspection and closing handled by a licensed broker",
     "Tenant placement lined up before you close", "Management ready on day one", "Sell the same way when you&rsquo;re ready to trade up"],
    [("Real rent numbers", "From the office that collects rent on thirty doors. Not a website estimate."),
     ("Real expense numbers", "We know what repairs, turnover and vacancy actually cost here."),
     ("Duplex to apartment", "Single family, duplexes, fourplexes, small complexes, commercial. We own and manage all of them."),
     ("Closing to keys", "Under contract to placed tenant, one office, one file."),
     ("Build it instead", "If the deal is land, Manhattan Builders can put the building on it. See <a href=\"{R}build-to-rent/\">build-to-rent</a>."),
     ("Selling", "When it&rsquo;s time, we list it with the rent roll and the records that make it easy to sell.")],
    [("Do I have to use you for management if I buy through you?", "No. But most do, because the analysis we used to buy it is the plan we manage it with."),
     ("Do you help with financing?", "We&rsquo;ll connect you with local lenders who do investment loans and know these numbers."),
     ("What about 1031 exchanges?", "Talk to Jon early. Exchanges run on strict deadlines, and the timeline shapes the search.")],
    "prop-grey-row.jpg")

service_page("residential-sales/", "Residential Sales", "Buying &amp; Selling Homes", "A Corpus Christi brokerage with <em>five agents</em> and one broker.",
    "Buying or selling a home in Corpus Christi and the surrounding area, with agents who know what every block is worth because we manage rentals on them.",
    "mb-home.jpg", "Local agents, licensed broker, straight answers.",
    ["Urban Properties is a full Texas real estate brokerage. Our agents help families buy and sell homes across Corpus Christi, Padre Island, Calallen and Robstown.",
     "Because the same office manages rental property, we see what homes actually rent for, what they cost to maintain, and which streets are moving. That&rsquo;s useful whether you&rsquo;re buying your first house or selling one you&rsquo;ve had for twenty years."],
    ["Five licensed agents under broker Jon Roel", "Listings on the MLS and every major site", "Pricing from real local comps",
     "Showings, offers and negotiation handled", "Inspection and closing coordinated", "Investors and first-time buyers alike"],
    [("Selling", "Priced from comps we trust, photographed, listed everywhere, shown by our agents."),
     ("Buying", "Tell us the budget and the neighborhoods. We find it, show it, write the offer, and get you to closing."),
     ("Rent it instead?", "Sometimes the better move is to keep the house and rent it. We&rsquo;ll run both numbers for you honestly."),
     ("Relocating", "Coming to Corpus for work or the base? We can start the search before you get here."),
     ("Lots and land too", "Buying a lot to build on? See <a href=\"{R}lot-land-sales/\">lot and land sales</a>."),
     ("The team", "Laura Vasquez, Amy Soza, Danny Guerrero, Maria Cruz, Michael Benavidez. <a href=\"{R}about/\">Meet them</a>.")],
    [("Which areas do you cover for sales?", "Corpus Christi, Padre Island, Calallen, Robstown and the surrounding area."),
     ("Should I sell or rent my house out?", "Ask us. We&rsquo;ll give you the sale number and the rent number from the same office, and tell you which we&rsquo;d do."),
     ("Do you work with first-time buyers?", "Yes, and with the local lenders who make that easier.")],
    "mb-kitchen.jpg")

service_page("lot-land-sales/", "Lot &amp; Land Sales", "Lots, Acreage, Infill", "Buy the dirt. <em>Build the deposit.</em>",
    "Lots, acreage and infill parcels across the Coastal Bend, from a brokerage that shares an office with a home builder.",
    "aerial-lot.jpg", "Land is where the whole chain starts.",
    ["We help buyers find and close on residential lots, small acreage and infill parcels in and around Corpus Christi, and we list land for owners ready to sell.",
     "The difference here: Manhattan Builders is down the hall. If you&rsquo;re buying to build, the person who can tell you what fits on the lot and what it costs is in the same building."],
    ["Residential lots, acreage and infill parcels", "Zoning, utilities and setback questions answered before you offer", "Build feasibility from Manhattan Builders",
     "Listing and marketing for land owners", "Closing handled by a licensed broker", "Build-to-rent path if you&rsquo;re investing"],
    [("Find the lot", "MLS parcels, checked for utilities, zoning and access before you offer."),
     ("Check the build", "Manhattan Builders reviews the lot for what can go on it and what that costs. Before you close."),
     ("Sell your land", "Priced, listed and marketed to builders and investors, not just posted."),
     ("Infill", "Corpus Christi has empty lots in good neighborhoods. Duplexes on them rent well. We know that firsthand."),
     ("Acreage", "Outside the city limits, we&rsquo;ll walk it with you and pull the county records."),
     ("Then build to rent", "Dirt to deposit, one office. See <a href=\"{R}build-to-rent/\">how that works</a>.")],
    [("Can you tell me if a lot is buildable?", "Yes. The builder reviews it before you make an offer."),
     ("Do you sell commercial land?", "Yes. Small commercial parcels and pad sites in the Corpus Christi area."),
     ("What does it cost to list land with you?", "Standard listing commission, agreed in writing up front.")],
    "aerial-lot-2.jpg")

service_page("commercial-leasing-multifamily/", "Commercial Leasing &amp; Multifamily", "Bigger Buildings, Same Process", "Duplexes, complexes, HOAs and <em>commercial space.</em>",
    "Leased and managed with the same process, by an office that owns and runs an eight-tenant commercial building and an eight-unit townhome complex of its own.",
    "prop-grey-row.jpg", "We manage buildings like yours because we own buildings like yours.",
    ["Multifamily and commercial property need the same fundamentals as a single house, at scale: screening, leases, rent, maintenance, renewals. We run that process on our own eight-unit complex and our own commercial building with eight tenants.",
     "We also take on HOA and association management for small communities that want a local office instead of a national firm."],
    ["Duplexes, fourplexes and small apartment communities", "Commercial space: retail, office, flex", "HOA and association management",
     "Commercial leases negotiated and enforced", "Vendor and common-area management", "Rent roll and expense records kept clean for lenders and buyers"],
    [("Multifamily", "Unit turns, tenant mix, shared maintenance. We do it on our own complex every month."),
     ("Commercial leasing", "Retail, office and flex space. Tenant sourcing, lease terms, renewals."),
     ("HOA / association", "Dues, vendors, meetings, enforcement. A local office your board can actually call."),
     ("Owner deposits", "Same as residential: rent in, your share out, itemized notice on anything over $250."),
     ("Ready for the lender", "Clean records make refinancing and selling simple. We keep them that way."),
     ("Build one", "Manhattan Builders builds multifamily. Land to lease-up, one office. See <a href=\"{R}build-to-rent/\">build-to-rent</a>.")],
    [("What size buildings do you take?", "Duplexes up to small apartment communities, and small commercial properties. Call about anything larger."),
     ("Do you handle HOA finances?", "Tell Jon what your association needs. The scope is set in writing in the management agreement."),
     ("What do you charge on commercial?", "Depends on the property. Call for a quote; it&rsquo;s a percentage of collected rent like everything else we do.")],
    "int-kitchen-blue.jpg")

# ---- hub: property management ------------------------------------------
pm_cards = [(l, "") for _, l in SERVICE_LIST]
pm_body = (hero("Property Management", "Everything between &ldquo;I own a rental&rdquo; and <em>&ldquo;the money showed up.&rdquo;</em>",
                "Ten services, one office, one fee. Pick what you need or hand us the whole thing.", "hero.jpg", "<span>Property Management</span>")
    + '''<section class="sec"><div class="wrap">
  <div class="center" style="margin-bottom:50px"><div class="eyebrow c">What We Handle</div><h2 class="big">Every service, on its own page.</h2></div>
  <div class="g3">%s</div></div></section>''' % "".join(
        '<a class="card" href="{R}%s" style="text-decoration:none;display:block"><h3>%s</h3><p>%s</p></a>' % (p, l, d) for (p, l), d in zip(SERVICE_LIST, [
            "Marketing, leasing, rent, maintenance and renewals. The option most owners pick.",
            "Income and rental history verified. You approve the tenant before anyone signs.",
            "Clear due dates, consistent follow-up, your share auto-deposited monthly.",
            "Tenants text the office. Vetted trades show up. You approve anything over $250.",
            "Texas leases prepared and enforced by a licensed broker. Renewals started early.",
            "Photos and a signed condition report both ways. Deposits settled on evidence.",
            "Buy the next door through the office that already knows what it rents for.",
            "Five agents, one broker, real local comps. Buying or selling a home.",
            "Lots, acreage and infill, with a home builder down the hall.",
            "Duplexes, complexes, HOAs and commercial, run like our own buildings."]))
    + '<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap" style="max-width:900px">%s</div></section>' % FEES)
page("property-management/", "Property Management", "Corpus Christi property management services from a licensed Texas brokerage. Screening, rent collection, maintenance, leases, inspections and sales.", pm_body)

# ---- owners ------------------------------------------------------------
ra_body = (hero("Free, No Obligation", "What will your property <em>actually</em> rent for?",
                "Four quick questions. A real number from a licensed local broker, and what we&rsquo;d fix first. Yours to keep whether or not you hire us.",
                "int-kitchen-open.jpg", "<span>Free Rent Analysis</span>", btn2='<a class="btn btn-o" href="#wiz">Start below</a>')
    + '<section class="sec" id="analysis"><div class="wrap">' + WIZARD.replace('src="img/', 'src="{R}img/') + '</div></section>'
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap g2">
  <div><div class="eyebrow">What You Get</div><h2 class="big">A number you can plan around.</h2>
  <ul class="checks" style="color:var(--body)">%s</ul></div>
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div></div></section>''' % ("".join(CHECK % b for b in [
        "What comparable units nearby are actually leasing for right now",
        "Where your property should be priced to lease in weeks, not months",
        "The one or two things we&rsquo;d fix before listing, and roughly what they cost",
        "What you&rsquo;d net after our 10% if we managed it",
        "A call or text from Jon, not an automated report"]), pic("prop-blue-street.jpg", "Managed rental in Corpus Christi")))
page("rent-analysis/", "Free Rent Analysis", "Free rental market analysis for Corpus Christi property owners. Find out what your property should rent for, from a licensed local broker.", ra_body, has_form=True)

wwc_body = (hero("Pricing", "Two numbers. <em>No fine print.</em>",
                 "One month&rsquo;s rent to place a tenant. Ten percent of rent to manage. Either one on its own. That&rsquo;s the whole price list.",
                 "prop-grey-row.jpg", "<span>What We Charge</span>")
    + '<section class="sec"><div class="wrap" style="max-width:900px">%s</div></section>' % FEES
    + cards("What&rsquo;s Inside The 10%", "Management, all in", [
        ("Rent collection", "Due dates, late fees, follow-up. Your share deposited automatically."),
        ("Maintenance coordination", "Tenant requests to the office, vetted trades dispatched, no markup on invoices."),
        ("Lease enforcement", "Your rules held, notices served correctly, renewals started early."),
        ("Inspections", "Move-in and move-out condition reports with photos."),
        ("Owner communication", "You hear from us when something needs a decision or costs over $250."),
        ("One price list", "One month&rsquo;s rent to place. Ten percent of collected rent to manage. Nothing hidden.")])
    + faq("Fair Questions", "About the money", [
        ("Do I pay the placement fee?", "No. One month&rsquo;s rent is collected out of the tenant&rsquo;s first month. You don&rsquo;t write a check."),
        ("Is 10% charged on vacant months?", "No. It&rsquo;s a percentage of collected rent. If nothing came in, nothing is charged."),
        ("What if I already have a tenant?", "Then it&rsquo;s management only, 10%, starting from the next rent date."),
        ("What if I just want a tenant found?", "Placement only. One month&rsquo;s rent, and the property is handed back to you with a signed lease."),
        ("Are repairs marked up?", "No. You pay the trade&rsquo;s invoice. Coordinating it is part of management."),
        ("Is there a contract term?", "A standard Texas management agreement. Talk to Jon about terms; nothing here is designed to trap you.")]))
page("what-we-charge/", "What We Charge", "Urban Properties management fees: one month's rent to place a tenant, 10% of rent to manage. No markups, no setup fees.", wwc_body)

how_body = (hero("Getting Started", "Four steps, and you&rsquo;re <em>out of the day-to-day.</em>",
                 "From the first call to the first deposit, here&rsquo;s exactly what happens and what we need from you.",
                 "int-kitchen-island.jpg", "<span>How Onboarding Works</span>")
    + steps4("The Process", "What happens, in order", [
        ("Free rent analysis", "Tell us about the property. We come back with what it should rent for and what we&rsquo;d do first."),
        ("Sign &amp; onboard", "Management agreement, keys, a walkthrough. We photograph and document the condition."),
        ("We market and screen", "Listed on the MLS and everywhere it syndicates, shown, screened. You approve the tenant."),
        ("You get paid", "Rent lands in your account automatically. The phone calls come to us instead of you.")])
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap g2">
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div>
  <div><div class="eyebrow">What We Need From You</div><h2 class="big">About twenty minutes of your time.</h2>
  <ul class="checks" style="color:var(--body)">%s</ul></div></div></section>''' % (pic("int-living.jpg", "Managed rental interior"), "".join(CHECK % b for b in [
        "A signed management agreement",
        "Keys, garage remotes, gate codes",
        "The current lease and deposit records, if there&rsquo;s a tenant in place",
        "The bank account your rent should be deposited to",
        "Any rules you want enforced: pets, smoking, occupancy",
        "Your preferred trades, if you have them. Otherwise we use ours."]))
    + faq("Timing", "How long things take", [
        ("How fast can you start?", "If the property already has a tenant, we start from the next rent date. If it&rsquo;s vacant, we list it as soon as it&rsquo;s photographed and ready."),
        ("How long to find a tenant?", "Depends on price and condition. Priced right, most units in Corpus Christi lease within a few weeks, and CC Lease Locators has renters looking already."),
        ("When&rsquo;s the first deposit?", "After the first rent clears. Your share is deposited to the account you gave us.")]))
page("how-onboarding-works/", "How Onboarding Works", "How to hand your Corpus Christi rental to Urban Properties: rent analysis, agreement, marketing, first deposit. Four steps.", how_body)

btr_body = (hero("For Investors", "From dirt <em>to deposit.</em>",
                 "Manhattan Builders builds it. CC Lease Locators fills it. Urban Properties manages it and, when you&rsquo;re ready, sells it. One office, one team.",
                 "build-fourplex.jpg", "<span>Build-to-Rent</span>")
    + '''<section class="band sec"><div class="wrap">
  <div class="center" style="margin-bottom:46px"><div class="eyebrow c">One Office, Three Companies</div><h2 class="big">We build it, fill it, manage it, and sell it.</h2></div>
  <div class="cos">
    <a class="co brand" href="https://manhattanbuilders.cc" target="_blank" rel="noopener"><div class="co-step">Builds it</div><div class="co-logo"><img src="{R}img/logo-manhattan.png" alt="Manhattan Builders" loading="lazy"></div><p>Custom homes, multifamily and light commercial across the Coastal Bend since 2003.</p><span class="co-link">manhattanbuilders.cc &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co brand" href="https://ccleaselocators.com" target="_blank" rel="noopener"><div class="co-step">Fills it</div><div class="co-logo"><img src="{R}img/logo-cclease.png" alt="CC Lease Locators" loading="lazy"></div><p>Free apartment locating for renters across Corpus Christi. 4.9 stars from 150 Google reviews.</p><span class="co-link">ccleaselocators.com &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co you" href="{R}property-management/"><div class="co-step">Manages &amp; sells it</div><div class="co-logo"><img src="{R}img/logo-light.png" alt="Urban Properties" loading="lazy"></div><p>Property management and a full brokerage, for the day you&rsquo;re ready to buy the next one or sell the last.</p><span class="co-link">You&rsquo;re here</span></a>
  </div></div></section>'''
    + intro("On The Job Right Now", "This one is still going up.", [
        "The drawing is a real Manhattan Builders home under construction right now, sketched from a job-site photo. Every build-to-rent project starts the same way: a lot, a plan, and a crew we&rsquo;ve worked with for years.",
        "When it&rsquo;s finished, CC Lease Locators fills it and Urban Properties manages it. Same office, same file, from the slab to the first deposit."],
        [], "wip-drawing.jpg", "Sketch of a Manhattan Builders home currently under construction")
    + gallery("From The Job Site", "Builds in progress", "Straight from Jon&rsquo;s phone: Manhattan Builders homes on their way up across the Coastal Bend.", [
        ("wip-wrapped.jpg", "Framed, wrapped and ready for windows", "w2"),
        ("wip-raised-coastal.jpg", "Raised coastal home on pilings", "w2"),
        ("wip-framing-water.jpg", "Wall framing, bay-view lot", ""),
        ("wip-roofing.jpg", "Roof going on", ""),
        ("wip-rafters.jpg", "Vaulted rafters, before the roof deck", ""),
        ("wip-interior-framing.jpg", "Interior framing", ""),
        ("wip-porch-beams.jpg", "Porch beams and brackets", "w2"),
        ("wip-kitchen-rough.jpg", "Kitchen cabinets going in", "w2")], bg=True, more="progress")
    + steps4("How It Goes", "Land to lease-up", [
        ("The lot", "You have one, or we find one. Manhattan Builders confirms what fits and what it costs before you commit."),
        ("The build", "Duplex, fourplex or small multifamily, built by a Coastal Bend builder since 2003."),
        ("The tenants", "CC Lease Locators has renters looking before the paint is dry. Screened and placed by our office."),
        ("The deposit", "Urban Properties manages it. Rent in, your share out, one office for the life of the asset.")])
    + faq("Investors Ask", "Straight answers", [
        ("Why build instead of buy?", "New construction rents at the top of the market, needs almost no maintenance for years, and you know exactly what you paid for every part of it."),
        ("Do I have to use all three companies?", "No. But the numbers work best when the builder, the leasing office and the manager are the same people with the same file."),
        ("What does a duplex cost to build here?", "Depends on the lot and the finish. Call Jon. You&rsquo;ll get a real number, not a range from a website.")]))
page("build-to-rent/", "Build-to-Rent for Investors", "Build-to-rent in Corpus Christi: Manhattan Builders builds it, CC Lease Locators fills it, Urban Properties manages it. One office.", btr_body)

# ---- tenants -----------------------------------------------------------
ten_form = '''<form class="form-plain" name="tenant-request" method="POST" data-netlify="true" netlify-honeypot="company-website" id="treq">
  <input type="hidden" name="form-name" value="tenant-request">
  <p class="hp"><label>Leave this empty: <input name="company-website"></label></p>
  <div class="fld"><label>What&rsquo;s it about?</label><div class="tchips">
    <label><input type="radio" name="topic" value="Rent or payment" checked><span>Paying rent</span></label>
    <label><input type="radio" name="topic" value="Applying for a rental"><span>Applying</span></label>
    <label><input type="radio" name="topic" value="Lease, renewal or move-out"><span>My lease</span></label>
    <label><input type="radio" name="topic" value="Something else"><span>Something else</span></label></div></div>
  <div class="fld"><label for="t-name">Your name</label><input id="t-name" name="name" autocomplete="name" placeholder="First and last"></div>
  <div class="fld"><label for="t-phone">Phone</label><input id="t-phone" name="phone" inputmode="tel" autocomplete="tel" placeholder="(361) 555-0123"></div>
  <div class="fld"><label for="t-addr">Property address and unit, if you rent from us</label><input id="t-addr" name="property_address" placeholder="e.g. 1234 Example St, Unit B"></div>
  <div class="fld"><label for="t-msg">Your question</label><textarea id="t-msg" name="message" rows="4" placeholder="What do you need from the office?"></textarea></div>
  <div class="note-box" style="margin-bottom:18px"><b>Something broken?</b> Use the <a href="{R}maintenance-request/" style="color:var(--pur);font-weight:700">maintenance request</a> so it goes straight to repairs.</div>
  <button type="button" class="btn btn-p" id="t-send">Send to the office</button>
</form>'''
TEN_CSS = """<style>
.tchips{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.tchips label{margin:0;position:relative;display:flex}.tchips input{position:absolute;left:0;top:0;width:1px;height:1px;padding:0;margin:0;border:0;opacity:0;pointer-events:none}
.tchips span{flex:1;display:flex;align-items:center;justify-content:center;text-align:center;padding:12px 10px;border:1.5px solid var(--line);border-radius:11px;font-size:14.5px;font-weight:600;color:var(--ink-3);cursor:pointer;transition:.15s}
.tchips input:checked+span{border-color:var(--pur);background:var(--pur-wash);color:var(--pur)}
.tchips input:focus-visible+span{outline:3px solid var(--pur);outline-offset:2px}
</style>"""
ten_hub = (hero("For Tenants", "Renting from us is <em>simple.</em>",
                "Apply, pay rent or report a repair: pick what you need below. Anything else, send the office a message.",
                "int-living.jpg", "<span>Tenants</span>", btn2='<a class="btn btn-o" href="%s">Text (361) 510-2325</a>' % JON_SMS)
    + TEN_CSS
    + '''<section class="sec"><div class="wrap">
  <div class="center" style="margin-bottom:46px"><div class="eyebrow c">What Do You Need?</div><h2 class="big">Three things, one office.</h2></div>
  <div class="g3">%s%s%s</div></div></section>''' % (
      '<div class="card tc"><div class="ico"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 15h6"/><path d="M9 11h6"/></svg></div><h3>Apply for a Rental</h3><p>$50 application fee. Stable income and rental history preferred. Here&rsquo;s how to apply.</p><a class="btn btn-p" href="{R}apply/" style="margin-top:18px">How to apply <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></div>', '<div class="card tc"><div class="ico"><svg viewBox="0 0 24 24"><rect width="20" height="12" x="2" y="6" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 12h.01M18 12h.01"/></svg></div><h3>Pay Rent</h3><p>Drop off a check or cash at 5117 Williams Dr, Mon&ndash;Fri 9 to 5, or pay by Cash App, Avail, Venmo or PayPal.</p><a class="btn btn-p" href="{R}pay-rent/" style="margin-top:18px">How to pay rent <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></div>', '<div class="card tc"><div class="ico"><svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z"/></svg></div><h3>Report a Repair</h3><p>Text (361) 510-2325 with your address and a photo, or send the request online. Emergencies: call.</p><a class="btn btn-p" href="{R}maintenance-request/" style="margin-top:18px">Report a repair <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a></div>')
    + '''<section class="sec" id="message" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap g2" style="align-items:start">
  <div><div class="eyebrow">Everything Else</div><h2 class="big">Send the office a message.</h2>
  <p class="lead">Questions about rent, your lease, renewing or moving out. A real person at the office reads it and gets back to you.</p>
  <p style="color:var(--muted);margin-top:14px">Faster by phone? Call the office at <a href="%s" style="color:var(--pur);font-weight:700;white-space:nowrap">(361) 434-0040</a>, or text <a href="%s" style="color:var(--pur);font-weight:700;white-space:nowrap">(361) 510-2325</a>.</p>
  %s</div>
  %s</div></section>''' % (TEL, JON_SMS, idx([("{R}available-rentals/", "Available Rentals"), ("{R}tenant-faqs/", "Tenant FAQs"), ("{R}contact/", "Office hours &amp; address")]), ten_form))
page("tenants/", "For Tenants", "Urban Properties tenants: apply, pay rent, request maintenance and find available rentals in Corpus Christi.", ten_hub, cta_kind="tenant", has_form=True)

avail_body = (hero("Available Rentals", "Our listings are <em>everywhere</em> you already look.",
                   "Every Urban Properties rental goes on the MLS and syndicates to Zillow, Realtor.com, Trulia, Redfin and Homes.com.",
                   "prop-blue-street.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Available Rentals</span>', btn2='<a class="btn btn-o" href="{R}apply/">How to apply</a>')
    + '''<section class="sec"><div class="wrap g2">
  <div><div class="eyebrow">Where To Look</div><h2 class="big">Search &ldquo;Urban Properties&rdquo; on any of these.</h2>
  <p class="lead">We list through the MLS, so the same units show up on every major site at once. Search the address or filter by the Corpus Christi area and look for our name.</p>
  %s
  <p style="color:var(--muted);margin-top:26px">Looking for an apartment rather than a house? Our sister firm <a href="https://ccleaselocators.com" target="_blank" rel="noopener" style="color:var(--pur);font-weight:700">CC Lease Locators</a> finds apartments across Corpus Christi for free.</p>
  <div class="cta-row" style="margin-top:28px"><a class="btn btn-p" href="{R}apply/">Apply for a rental</a><a class="btn btn-g" href="%s">Text the office</a></div></div>
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div></div></section>''' % (idx([("https://www.zillow.com/", "Zillow"), ("https://www.realtor.com/", "Realtor.com"), ("https://www.trulia.com/", "Trulia"), ("https://www.redfin.com/", "Redfin"), ("https://www.homes.com/", "Homes.com")]), JON_SMS, pic("int-kitchen-white.jpg", "Rental unit kitchen")))
page("available-rentals/", "Available Rentals", "Urban Properties rentals in Corpus Christi are listed on the MLS, Zillow, Realtor.com, Trulia, Redfin and Homes.com.", avail_body, cta_kind="tenant")

apply_body = (hero("Apply", "Apply for a <em>rental.</em>",
                   "$50 application fee per adult. Stable, verifiable income and rental history preferred. Download the application, fill it out, and bring or send it to the office.",
                   "int-kitchen-white.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Apply</span>', btn2='<a class="btn btn-o" href="#">Download the application</a>')
    + '''<section class="sec"><div class="wrap g2">
  <div><div class="eyebrow">How It Works</div><h2 class="big">Three steps to the keys.</h2>
  <ul class="checks" style="color:var(--body)">%s</ul>
  <div class="note-box" style="margin-top:28px"><b>Application fee:</b> $50 per adult applicant, paid when you submit. <b>We look for:</b> stable, verifiable income and rental history. Pets and other specifics are set per property; ask before you apply.</div>
  <div class="cta-row" style="margin-top:28px"><a class="btn btn-p" href="#">Download the application (PDF)</a><a class="btn btn-g" href="%s">Text a question</a></div></div>
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div></div></section>''' % ("".join(CHECK % b for b in [
        "Download the application and fill it out for every adult who will live there",
        "Bring it to 5117 Williams Dr (Mon&ndash;Fri, 9 to 5) or send it back the way we sent it to you, with the $50 fee",
        "We verify income, rental history and background, then call you with the answer"]), JON_SMS, pic("door-entry.jpg", "Front door of a rental home"))
    + faq("Before You Apply", "Applicants usually ask", [
        ("What do I need to bring?", "Photo ID, proof of income (recent pay stubs or an offer letter), and your last two landlords&rsquo; contact info."),
        ("How long does approval take?", "As soon as income and rental history are verified. We call you with the answer."),
        ("Is the fee refundable?", "No. It covers the screening whether or not you&rsquo;re approved."),
        ("Do you accept pets?", "It depends on the property. Ask about the specific unit before applying.")]))
page("apply/", "Apply for a Rental", "Apply for an Urban Properties rental in Corpus Christi. $50 application fee, stable income and rental history preferred.", apply_body, cta_kind="tenant")

pay_body = (hero("Pay Rent", "Pay rent the way that <em>works for you.</em>",
                 "Drop off a check or cash at the office, or pay electronically with Cash App, Avail, Venmo or PayPal.",
                 "int-living.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Pay Rent</span>', btn2='<a class="btn btn-o" href="%s">Text the office</a>' % JON_SMS)
    + cards("Ways To Pay", "Pick one and stick with it", [
        ("In person", "Check or cash at <b>5117 Williams Dr, Corpus Christi, TX 78411</b>. Mon&ndash;Fri, 9:00am to 5:00pm."),
        ("Cash App", "Ask the office for the account name, then send it with your address in the note."),
        ("Avail", "If you were set up on Avail at move-in, pay there as usual."),
        ("Venmo", "Ask the office for the account name. Put your unit address in the note."),
        ("PayPal", "Same: office gives you the account, you put the address in the note."),
        ("Automatic", "Want it to just happen? Set up a scheduled transfer for the due date. Ask the office how.")], bg=False)
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap" style="max-width:860px">
  <div class="eyebrow">Good To Know</div><h2 class="big">Due dates and late fees</h2>
  <div class="prose"><p>Rent is due on the date in your lease. Your lease also states the grace period and the late fee, and the office applies them the same way every month. If something has come up and you know rent will be late, text the office <b>before</b> the due date. That conversation is always easier early.</p>
  <p>Always put your unit address in the note on an electronic payment, so it&rsquo;s credited to the right account the same day.</p></div></div></section>''')
page("pay-rent/", "Pay Rent", "How to pay rent to Urban Properties in Corpus Christi: in person at 5117 Williams Dr, or Cash App, Avail, Venmo and PayPal.", pay_body, cta_kind="tenant")

maint_form = '''<form class="form-plain" name="maintenance-request" method="POST" data-netlify="true" netlify-honeypot="company-website" id="mreq">
  <input type="hidden" name="form-name" value="maintenance-request">
  <p class="hp"><label>Leave this empty: <input name="company-website"></label></p>
  <div class="fld"><label for="m-name">Your name</label><input id="m-name" name="name" autocomplete="name" placeholder="First and last"></div>
  <div class="fld"><label for="m-phone">Phone</label><input id="m-phone" name="phone" inputmode="tel" autocomplete="tel" placeholder="(361) 555-0123"></div>
  <div class="fld"><label for="m-addr">Property address and unit</label><input id="m-addr" name="property_address" placeholder="e.g. 1234 Example St, Unit B"></div>
  <div class="fld"><label for="m-issue">What&rsquo;s wrong?</label><textarea id="m-issue" name="issue" rows="4" placeholder="Where it is, what it&rsquo;s doing, and since when."></textarea></div>
  <div class="fld"><label for="m-when">Is it OK to enter if you&rsquo;re not home?</label><input id="m-when" name="entry_permission" placeholder="Yes / No, call first / pets inside"></div>
  <div class="note-box" style="margin-bottom:18px"><b>Photos help.</b> Text them to <a href="%s" style="color:var(--pur);font-weight:700">(361) 510-2325</a> after you send this.</div>
  <button type="button" class="btn btn-p" id="m-send">Send the request</button>
</form>''' % JON_SMS
maint_body = (hero("Maintenance", "Something broke? <em>Tell us.</em>",
                   "Text or call the office with your address and what&rsquo;s wrong, or send it here. Emergencies: call.",
                   "int-kitchen-blue.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Maintenance Request</span>', btn2='<a class="btn btn-o" href="%s">Text (361) 510-2325</a>' % JON_SMS)
    + '''<section class="sec"><div class="wrap g2" style="align-items:start">
  <div><div class="eyebrow">Fastest</div><h2 class="big">Text it. Photos help.</h2>
  <p class="lead">Text <a href="%s" style="color:var(--pur);font-weight:700">(361) 510-2325</a> with your address, what&rsquo;s wrong, and a photo if you can. The office triages it and sends the right person.</p>
  <div class="note-box" style="margin-top:22px"><b>Emergencies</b> (no water, no power, flooding, gas smell, no A/C in summer heat): call, don&rsquo;t text. Gas smell: leave the property and call the gas company first.</div>
  <h3 style="margin-top:34px;font-size:24px">Or use the form</h3><p style="color:var(--muted)">Same thing, in writing. It goes straight to the office.</p></div>
  %s</div></section>''' % (JON_SMS, maint_form)
    + faq("What To Expect", "After you report it", [
        ("How fast will someone come?", "Emergencies come first. Everything else is scheduled with you as soon as the right trade is available."),
        ("Do I have to be home?", "Not if you tell us it&rsquo;s OK to enter. If you have pets or would rather be there, say so and we&rsquo;ll schedule around you."),
        ("Who pays for the repair?", "Normal wear and repairs are on the owner. Damage caused by the tenant is charged back per the lease."),
        ("What counts as an emergency?", "Anything that&rsquo;s a safety issue or is actively damaging the property: water where it shouldn&rsquo;t be, no power, no working toilet, no A/C in extreme heat.")]))
# repairs go to one number: Jon's onboarding form (9/24) says maintenance = text or call (361) 510-2325
maint_body = maint_body.replace('<a class="btn btn-p btn-lg cta-call" href="%s">%s Call %s</a>' % (TEL, CALL_SVG, PHONE),
                                '<a class="btn btn-p btn-lg cta-call" href="%s">%s Call (361) 510-2325</a>' % (JON_TEL, CALL_SVG), 1)
page("maintenance-request/", "Maintenance Request", "Report a repair to Urban Properties: text or call (361) 510-2325, or send a maintenance request online.", maint_body, cta_kind="tenant", has_form=True)

faq_body = (hero("Tenant FAQs", "The answers, <em>before you have to ask.</em>",
                 "Rent, deposits, repairs, moving out, pets. If it isn&rsquo;t here, text the office.",
                 "prop-tan-corner.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>FAQs</span>', btn2='<a class="btn btn-o" href="%s">Text (361) 510-2325</a>' % JON_SMS)
    + faq("Renting With Us", "Frequently asked", [
        ("When is rent due?", "On the date in your lease, usually the 1st. The grace period and late fee are in the lease too, and they&rsquo;re applied the same way every month."),
        ("How do I pay?", "In person at 5117 Williams Dr, or Cash App, Avail, Venmo or PayPal. Details on the <a href=\"{R}pay-rent/\">Pay Rent</a> page."),
        ("How do I report a repair?", "Text or call (361) 510-2325, or use the <a href=\"{R}maintenance-request/\">maintenance request form</a>. Emergencies: call."),
        ("Can I have a pet?", "Depends on the property and your lease. Ask before you bring one home; unauthorized pets are a lease violation."),
        ("What happens to my deposit?", "It&rsquo;s held per Texas law and returned, itemized, within the required timeline after move-out, less any damage beyond normal wear and tear and any unpaid balance."),
        ("How do I give notice?", "In writing, with the notice period your lease requires (usually 30 days). Text or email the office and we&rsquo;ll confirm the date."),
        ("Can I renew?", "We&rsquo;ll reach out well before your lease ends. If you want to stay, say so and we&rsquo;ll send the renewal."),
        ("Can I sublet or add a roommate?", "Not without written approval. Anyone living there has to be on the lease and screened."),
        ("Who do I call about a neighbor problem?", "The office. If it&rsquo;s a safety issue, call 911 first, then let us know."),
        ("What if I&rsquo;m going to be late on rent?", "Text the office before the due date. That conversation is always easier early.")]))
page("tenant-faqs/", "Tenant FAQs", "Answers for Urban Properties tenants in Corpus Christi: rent due dates, deposits, repairs, pets, notice and renewals.", faq_body, cta_kind="tenant")

# ---- areas ---------------------------------------------------------------
def town_page(slug, name, h1, hl, img, para1, para2, bullets, mapq):
    body = (hero("Property Management in " + name, h1, hl, img, '<a href="{R}service-areas/">Service Areas</a><span>/</span><span>%s</span>' % name)
        + intro("Managing In " + name, "Local, licensed, and already here.", [para1, para2], bullets, "int-kitchen-open.jpg", "Managed rental interior")
        + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap g2">
  <div><div class="eyebrow">Where We Work</div><h2 class="big">%s and the surrounding area.</h2><p class="lead">Our office is at 5117 Williams Drive in Corpus Christi. We manage across the city, the Island, Calallen, Robstown and beyond.</p>
  %s
  <div style="margin-top:30px">%s</div></div>
  <div class="mapbox"><iframe src="https://www.google.com/maps?q=%s&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of %s"></iframe></div></div></section>''' % (
            name, idx([("{R}" + p, t) for p, t in TOWNS + [("service-areas/", "Surrounding Areas")]], "{R}" + slug, "idx-towns"),
            FEES.replace('id="fees"', ''), mapq, name)
        + '<section class="sec-tight"><div class="wrap"><div class="eyebrow">What We Handle In %s</div>%s</div></section>' % (name, service_links()))
    page(slug, "Property Management in " + name, hl, body, crumb_label=name)

town_page("corpus-christi/", "Corpus Christi", "Corpus Christi rental property, <em>managed from Williams Drive.</em>",
    "Single-family homes, duplexes, small apartment communities and commercial space across Corpus Christi, managed by a licensed local brokerage.",
    "prop-blue-street.jpg",
    "Corpus Christi is home. Our office, our own rentals and most of the doors we manage are here, from the Southside to Calallen to the Island.",
    "That means when a tenant reports a leak on Everhart, someone who knows the property is across town, not across the country, and when you ask what a duplex near the base should rent for, the answer comes from units we already manage.",
    ["Southside, Westside, Flour Bluff, downtown and the Bay area", "Single family, duplex, fourplex, multifamily and commercial", "Tenants placed through CC Lease Locators", "Rent auto-deposited, one point of contact"],
    "Corpus+Christi,+TX")
town_page("padre-island/", "Padre Island", "Island rentals, <em>handled from the mainland.</em>",
    "Property management for homes, condos and townhomes on Padre Island, with tenant placement, rent collection and maintenance handled by our Corpus Christi office.",
    "ext-duplex-front.jpg",
    "Island properties have their own rhythm: salt air, seasonal demand, HOAs and a tenant pool that ranges from Navy families to long-term locals.",
    "We manage on the Island the same way we manage everywhere else, with one addition: we know which trades will actually drive over the causeway.",
    ["Single-family homes, condos and townhomes", "Long-term leases, not short-term rental turnover", "HOA rules written into the lease and enforced", "Island-familiar maintenance trades"],
    "Padre+Island,+Corpus+Christi,+TX")
town_page("calallen/", "Calallen", "Calallen and Annaville rentals, <em>managed locally.</em>",
    "Property management for houses and duplexes in Calallen and Annaville, from a Corpus Christi brokerage that manages units in the area already.",
    "prop-grey-row.jpg",
    "Calallen and Annaville draw families for the schools and the quiet, which makes them steady rental markets with long tenancies.",
    "We manage single-family homes and duplexes out here and price them from what nearby units actually lease for, not from a website estimate.",
    ["Single-family homes and duplexes", "Family tenants, long leases, low turnover", "Screening through CC Lease Locators", "Owners deposited automatically every month"],
    "Calallen,+Corpus+Christi,+TX")
town_page("robstown/", "Robstown", "Robstown rentals, with a <em>Corpus Christi office</em> behind them.",
    "Property management for homes and small multifamily in Robstown, handled by a licensed brokerage twenty minutes away.",
    "prop-tan-corner.jpg",
    "Robstown owners often manage from a distance, or have been doing it themselves for years. Either way, the calls stop coming to you the day we take over.",
    "We handle screening, rent, repairs and renewals for Robstown properties exactly as we do in the city, with the same trades and the same office.",
    ["Single-family homes and small multifamily", "Rent collection and auto-deposit", "Maintenance dispatched from our regular trades", "Placement-only or full management"],
    "Robstown,+TX")

areas_hub = (hero("Where We Work", "Managing across the <em>Coastal Bend.</em>",
                  "Based on Williams Drive in Corpus Christi. Managing across the city, Padre Island, Calallen, Robstown and the surrounding area.",
                  "hero.jpg", "<span>Service Areas</span>")
    + '''<section class="sec"><div class="wrap"><div class="center" style="margin-bottom:46px"><div class="eyebrow c">Areas</div><h2 class="big">One office. Every one of these.</h2></div>
  <div class="g3">%s
    <div class="card"><h3>Surrounding Areas</h3><p>Own something just outside the list? Call us anyway. If we can&rsquo;t take it, we&rsquo;ll tell you who should.</p></div>
  </div></div></section>''' % "".join('<a class="card" href="{R}%s" style="text-decoration:none;display:block"><h3>%s</h3><p>Property management, tenant placement and sales in %s.</p></a>' % (p, t, t) for p, t in TOWNS)
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap g2">
  <div><div class="eyebrow">The Office</div><h2 class="big">5117 Williams Drive, Corpus Christi.</h2><p class="lead">Mon&ndash;Fri, 9:00am to 5:00pm. Tenants drop rent here; owners are welcome to stop by.</p>
  <div class="cta-row" style="margin-top:28px"><a class="btn btn-p" href="%s">%s Call %s</a><a class="btn btn-g" href="{R}contact/">Contact</a></div></div>
  <div class="mapbox"><iframe src="https://www.google.com/maps?q=5117+Williams+Dr,+Corpus+Christi,+TX+78411&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Urban Properties office location"></iframe></div></div></section>''' % (TEL, CALL_SVG, PHONE))
page("service-areas/", "Service Areas", "Urban Properties manages rental property across Corpus Christi, Padre Island, Calallen, Robstown and the surrounding Coastal Bend.", areas_hub)

# ---- about / companies / reviews / contact -----------------------------
FACT_ICONS = {'chart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/></svg>', 'award': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15.477 12.89 1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/></svg>', 'heart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19.414 14.414C21 12.828 22 11.5 22 9.5a5.5 5.5 0 0 0-9.591-3.676.6.6 0 0 1-.818.001A5.5 5.5 0 0 0 2 9.5c0 2.3 1.5 4 3 5.5l5.535 5.362a2 2 0 0 0 2.879.052 2.12 2.12 0 0 0-.004-3 2.124 2.124 0 1 0 3-3 2.124 2.124 0 0 0 3.004 0 2 2 0 0 0 0-2.828l-1.881-1.882a2.41 2.41 0 0 0-3.409 0l-1.71 1.71a2 2 0 0 1-2.828 0 2 2 0 0 1 0-2.828l2.823-2.762"/></svg>', 'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2a9 9 0 0 1 9 9"/><path d="M13 6a5 5 0 0 1 5 5"/><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>'}
def facts_html(items):
    return '<div class="facts2">%s</div>' % "".join('<div class="fact"><span class="fi">%s</span><div><b>%s</b><p>%s</p></div></div>' % (FACT_ICONS[k], t, d) for k, t, d in items)

def roster():
    ini = lambda n: "".join(w[0] for w in n.split()[:2])
    broker, agents = TEAM[0], TEAM[1:]
    return ('<div class="roster"><div class="roster-h">The team</div>'
            '<div class="broker"><span class="av av-lg">%s</span><div><b>%s</b><span>Designated Broker &middot; TREC #0547401</span></div></div>'
            '<ul class="agents">%s</ul></div>') % (ini(broker[0]), broker[0],
            "".join('<li><span class="av">%s</span><div><b>%s</b><span>%s</span></div></li>' % (ini(n), n, r) for n, r in agents))

TEAM = [("Jon Roel", "Broker"), ("Laura Vasquez", "Realtor"), ("Amy Soza", "Realtor"), ("Danny Guerrero", "Realtor"), ("Maria Cruz", "Realtor"), ("Michael Benavidez", "Realtor")]
about_body = (hero("About Urban Properties", "A Corpus Christi brokerage that <em>actually answers the phone.</em>",
                   "Full-service real estate since 2009. Property management, tenant placement, sales, and a builder down the hall. All under one licensed roof, led by broker Jon Roel.",
                   "team.jpg", "<span>About</span>")
    + intro("Since 2009", "The same person who manages your rental can tell you what to buy next.", [
        "Urban Properties opened in 2009. Today we manage rental property, place tenants through our sister firm CC Lease Locators, and help people buy and sell, all from one office on Williams Drive.",
        "We own and manage our own buildings, an eight-unit townhome complex, an eight-tenant commercial building, a duplex and houses, and we run yours the same way. You&rsquo;re not handing your investment to a call center three states away."],
        [], "jon-roel.jpg", "Jon Roel, broker and owner of Urban Properties, with his son",
        extra=roster())
    + cards("What We Stand On", "Four things you can hold us to", [
        ("Results", "Occupied units and rent that arrives on time. That&rsquo;s the job."),
        ("Experience", "A licensed Texas broker and five agents, not a leasing app."),
        ("Commitment", "Your property treated like it&rsquo;s ours. Because ours are next door."),
        ("Straightforward", "Auto-deposit, a direct line, and no surprises. You hear from us when it matters."),
        ("Local", "5117 Williams Drive. One office for every property we manage."),
        ("Licensed", "TREC Broker License #9000508. Jon Roel, Designated Broker, License #0547401.")])
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap center"><div class="eyebrow c">Three Companies</div><h2 class="big">We build it, fill it, manage it, and sell it.</h2><p class="lead">Manhattan Builders, CC Lease Locators and Urban Properties share one office and one owner.</p><div style="margin-top:28px"><a class="btn btn-p" href="{R}our-companies/">See how they fit together</a></div></div></section>''')
page("about/", "About Urban Properties", "Urban Properties: a Corpus Christi real estate brokerage since 2009. Property management, tenant placement and sales, led by broker Jon Roel.", about_body)

cos_body = (hero("One Office, Three Companies", "We build it, fill it, manage it, <em>and sell it.</em>",
                 "Manhattan Builders, CC Lease Locators and Urban Properties share one office at 5117 Williams Drive. Whatever stage your property is at, the next call is to the same people.",
                 "mb-modern.jpg", "<span>Our Companies</span>")
    + '''<section class="band sec"><div class="wrap"><div class="cos">
    <a class="co brand" href="https://manhattanbuilders.cc" target="_blank" rel="noopener"><div class="co-step">Builds it</div><div class="co-logo"><img src="{R}img/logo-manhattan.png" alt="Manhattan Builders" loading="lazy"></div><p>Custom homes, multifamily and light commercial across the Coastal Bend since 2003. Corpus Christi, Padre Island, Port Aransas, Rockport.</p><span class="co-link">manhattanbuilders.cc &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co brand" href="https://ccleaselocators.com" target="_blank" rel="noopener"><div class="co-step">Fills it</div><div class="co-logo"><img src="{R}img/logo-cclease.png" alt="CC Lease Locators" loading="lazy"></div><p>Free apartment locating for renters across Corpus Christi. 4.9 stars from 150 Google reviews.</p><span class="co-link">ccleaselocators.com &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co you" href="{R}property-management/"><div class="co-step">Manages &amp; sells it</div><div class="co-logo"><img src="{R}img/logo-light.png" alt="Urban Properties" loading="lazy"></div><p>Property management and a full brokerage since 2009, for the day you&rsquo;re ready to buy the next one or sell the last.</p><span class="co-link">You&rsquo;re here</span></a>
  </div><p class="co-note">Own land and thinking about building to rent? <a href="{R}build-to-rent/">Here&rsquo;s how that works.</a> One team takes it from dirt to deposit.</p></div></section>'''
    + gallery("Manhattan Builders", "Finished work", "Homes built by our sister company, Manhattan Builders, across the Coastal Bend.", [
        ("mb-white-modern.jpg", "Modern farmhouse exterior", "w2"),
        ("mb-red-modern.jpg", "Contemporary exterior, red accent wall", "w2"),
        ("mb-kitchen-island.jpg", "Kitchen with waterfall island", "w2"),
        ("mb-bedroom.jpg", "Primary bedroom", "w2"),
        ("mb-entry.jpg", "Front entry", ""),
        ("mb-bath.jpg", "Primary bath, freestanding tub", ""),
        ("mb-backsplash.jpg", "Patterned tile backsplash", ""),
        ("mb-red-entry.jpg", "Board-and-batten entry", "")], more="finished")
    + cards("Why It Matters To You", "One file, start to finish", [
        ("For owners", "The builder knows the building, the locator knows the renters, the manager knows the numbers. Nothing gets lost between companies."),
        ("For investors", "Buy a lot, build a duplex, lease it up, manage it, sell it. Same office, same people, one phone number."),
        ("For renters", "CC Lease Locators finds you a place for free. If it&rsquo;s one of ours, you already know who manages it.")], bg=False))
page("our-companies/", "Our Companies", "Manhattan Builders builds it, CC Lease Locators fills it, Urban Properties manages and sells it. One Corpus Christi office.", cos_body)

STAR = '<svg viewBox="0 0 24 24"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/></svg>'
def review(text, name, ini):
    return '<div class="rev"><div class="stars">%s</div><p>%s</p><div class="who"><div class="av">%s</div><div><div class="nm">%s</div><div class="src">Google Review</div></div></div></div>' % (STAR * 5, text, ini, name)
rev_body = (hero("Reviews", "Straight from <em>real clients.</em>",
                 "What owners and clients say about working with Jon and the office. Every one of these is a real Google review.",
                 "team.jpg", "<span>Reviews</span>")
    + '''<section class="sec"><div class="wrap"><div class="revs">%s%s</div>
  <p class="center" style="margin-top:36px;color:var(--muted)">Worked with us? <b>Search &ldquo;Urban Properties Corpus Christi&rdquo; on Google</b> and leave a review. It helps the next owner find us.</p></div></section>''' % (
        review("&ldquo;Mr. Jon Roel and Urban Properties is a very professional company that went above and beyond to get our house ready for rent! Jon has fantastic employees that will make your old house look very sellable!&rdquo;", "Albert Flores", "AF"),
        review("&ldquo;Jon is a wonderful realtor; he listened to us and helped achieve our desired outcomes. He stayed focused on our agenda and outlined different scenarios for us to reach our plans. He delivered on our requests and was flexible through the entire journey.&rdquo;", "Cynthia Flores", "CF"))
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap center"><div class="eyebrow c">Our Sister Firm</div><h2 class="big">4.9 stars from 150 reviews.</h2><p class="lead">CC Lease Locators, the tenant-placement side of our office, is one of the most reviewed locating services in Corpus Christi. Same people, same standard.</p><div style="margin-top:26px"><a class="btn btn-g" href="https://ccleaselocators.com" target="_blank" rel="noopener">ccleaselocators.com</a></div></div></section>''')
page("reviews/", "Reviews", "Google reviews for Urban Properties, Corpus Christi property management and real estate brokerage.", rev_body)

contact_form = '''<form class="form-plain" name="contact" method="POST" data-netlify="true" netlify-honeypot="company-website" id="cform">
  <input type="hidden" name="form-name" value="contact">
  <p class="hp"><label>Leave this empty: <input name="company-website"></label></p>
  <div class="fld"><label for="c-name">Your name</label><input id="c-name" name="name" autocomplete="name" placeholder="First and last"></div>
  <div class="fld"><label for="c-phone">Phone</label><input id="c-phone" name="phone" inputmode="tel" autocomplete="tel" placeholder="(361) 555-0123"></div>
  <div class="fld"><label for="c-email">Email <span style="font-weight:500;color:var(--muted)">(optional)</span></label><input id="c-email" type="email" name="email" placeholder="you@email.com"></div>
  <div class="fld"><label for="c-msg">How can we help?</label><textarea id="c-msg" name="message" rows="4" placeholder="Owner, tenant, buyer, seller. Tell us what&rsquo;s going on."></textarea></div>
  <button type="button" class="btn btn-p" id="c-send">Send</button>
</form>'''
contact_body = (hero("Contact", "Call, text, or <em>come by.</em>",
                     "5117 Williams Drive, Corpus Christi. Mon&ndash;Fri, 9:00am to 5:00pm. A real person answers.",
                     "prop-blue-street.jpg", "<span>Contact</span>", btn2='<a class="btn btn-o" href="%s">Text (361) 510-2325</a>' % JON_SMS)
    + '''<section class="sec"><div class="wrap g2" style="align-items:start">
  <div><div class="eyebrow">The Office</div><h2 class="big">Urban Properties</h2>
  <div class="prose"><p><b>5117 Williams Dr</b><br>Corpus Christi, TX 78411</p>
  <p><b>Office:</b> <a href="%s" style="color:var(--pur);font-weight:700">(361) 434-0040</a><br><b>Text or call Jon:</b> <a href="%s" style="color:var(--pur);font-weight:700">(361) 510-2325</a><br><b>Email:</b> <a href="mailto:jon@urbanpropertiescc.com" style="color:var(--pur);font-weight:700">jon@urbanpropertiescc.com</a></p>
  <p><b>Hours:</b> Mon&ndash;Fri, 9:00am to 5:00pm</p></div>
  <div class="mapbox" style="min-height:320px;margin-top:10px"><iframe src="https://www.google.com/maps?q=5117+Williams+Dr,+Corpus+Christi,+TX+78411&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Urban Properties office location" style="min-height:320px"></iframe></div>
  <p style="margin-top:22px;color:var(--muted)">Own a rental? The fastest way to a real number is the <a href="{R}rent-analysis/" style="color:var(--pur);font-weight:700">free rent analysis</a>.</p></div>
  %s</div></section>''' % (TEL, JON_TEL, contact_form)
    + '''<section class="sec" id="legal" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap" style="max-width:860px"><div class="eyebrow">Required Notices</div><h2 class="big">Brokerage information</h2>
  <div class="prose"><p>Corpus Christi Urban Properties, LLC is a licensed Texas real estate brokerage. Texas Real Estate Commission Broker License #9000508. Jon Roel, Designated Broker, License #0547401.</p>
  <p><a href="{R}docs/TREC-Information-About-Brokerage-Services.pdf" target="_blank" rel="noopener"><b>Texas Real Estate Commission Information About Brokerage Services</b></a><br><a href="{R}docs/TREC-Consumer-Protection-Notice.pdf" target="_blank" rel="noopener"><b>Texas Real Estate Commission Consumer Protection Notice</b></a></p>
  <p><a href="{R}privacy-policy/">Privacy Policy</a> &middot; <a href="{R}terms-of-use/">Terms of Use</a> &middot; <a href="{R}accessibility/">Accessibility</a> &middot; <a href="{R}fair-housing/">Fair Housing</a></p>
  <p>All information deemed reliable but not guaranteed. Equal Housing Opportunity.</p></div></div></section>''')
page("contact/", "Contact", "Contact Urban Properties: 5117 Williams Dr, Corpus Christi, TX 78411. Call (361) 434-0040 or text (361) 510-2325.", contact_body, has_form=True)


# ---- full photo gallery ---------------------------------------------------
import json as _json
_G = _json.load(open(os.path.join(ROOT, "_src-sheets", "gallery.json")))
def _gsec(key, eyebrow, h2, lead, bg):
    figs = "".join('<a class="fg-i" href="{R}img/gallery/%s.jpg" data-cap="%s"><picture><source srcset="{R}img/gallery/%s-t.webp" type="image/webp"><img src="{R}img/gallery/%s-t.jpg" alt="%s" loading="lazy" width="720" height="540"></picture><span>%s</span></a>' % (n, c, n, n, c, c) for n, c in _G[key])
    return ('<section class="sec" id="%s"%s><div class="wrap"><div class="center" style="margin-bottom:36px"><div class="eyebrow c">%s</div><h2 class="big">%s</h2><p class="lead">%s</p></div><div class="fg">%s</div></div></section>'
            % (key, ' style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"' if bg else "", eyebrow, h2, lead, figs))
GAL_CSS = """<style>
.gal-jump{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
@media(max-width:860px){.gal-hero .wrap{text-align:center}.gal-hero .crumb{justify-content:center}.gal-hero .lead{margin-left:auto;margin-right:auto}
  .gal-jump{flex-direction:column;align-items:stretch;max-width:400px;margin:22px auto 0}.gal-jump .btn{width:100%;font-size:16px;padding:16px 22px}}
.fg{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.fg-i{position:relative;display:block;border-radius:12px;overflow:hidden;background:var(--paper-2);aspect-ratio:4/3}
.fg-i img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}.fg-i:hover img{transform:scale(1.05)}
.fg-i span{position:absolute;left:0;right:0;bottom:0;padding:24px 12px 10px;color:#fff;font-size:14px;font-weight:600;background:linear-gradient(transparent,rgba(23,20,27,.78))}
@media(max-width:860px){.fg{grid-template-columns:repeat(2,1fr);gap:10px}.fg-i span{font-size:12.5px;padding:18px 9px 8px}}
</style>"""
GAL_JS = ""  # the shared photo viewer in src/home.html (COMMON_JS) drives .fg-i too
gal_body = (GAL_CSS + '<section class="sec legal-hero gal-hero" style="padding-bottom:40px"><div class="wrap"><div class="crumb" style="color:var(--muted)"><a href="{R}" style="color:var(--pur)">Home</a><span>/</span>Photo Gallery</div>'
    '<h1 class="big" style="font-size:clamp(36px,4.8vw,60px);margin:14px 0 12px">Photo gallery</h1><p class="lead" style="max-width:62ch">Properties we manage, homes our sister company Manhattan Builders has on the way up, and finished work. Tap any photo to see it full size.</p>'
    '<div class="gal-jump"><a class="btn btn-g" href="#managed">Properties we manage</a><a class="btn btn-g" href="#progress">Builds in progress</a><a class="btn btn-g" href="#finished">Finished homes</a></div></div></section>'
    + _gsec("managed", "Urban Properties", "Properties we manage", "Duplexes, townhomes and the units inside them, managed by our office.", True)
    + _gsec("progress", "Manhattan Builders", "Builds in progress", "Straight from the job site: homes on their way up across the Coastal Bend.", False)
    + _gsec("finished", "Manhattan Builders", "Finished homes", "New homes built by our sister company, Manhattan Builders.", True)
    + GAL_JS)
page("gallery/", "Photo Gallery", "Photos of rental properties managed by Urban Properties in Corpus Christi, plus Manhattan Builders homes in progress and finished.", gal_body)

# ---- legal pages --------------------------------------------------------
EFFECTIVE = "September 29, 2026"
FIRM = "Corpus Christi Urban Properties, LLC"
def legal_page(slug, title, lead, sections):
    body = ('<section class="sec legal-hero"><div class="wrap" style="max-width:860px"><div class="crumb" style="color:var(--muted)"><a href="{R}" style="color:var(--pur)">Home</a><span>/</span>%s</div>'
            '<h1 class="big" style="font-size:clamp(34px,4.4vw,52px);margin:14px 0 12px">%s</h1><p class="lead">%s</p><p style="color:var(--muted);font-size:14.5px">Effective %s</p></div></section>'
            '<section class="sec" style="padding-top:0"><div class="wrap prose" style="max-width:860px">%s</div></section>') % (
            title, title, lead, EFFECTIVE, "".join('<h3>%s</h3>%s' % (h, "".join('<p>%s</p>' % x for x in ps)) for h, ps in sections))
    page(slug, title, lead, body, cta_kind=None)

CONTACT_LINE = 'Corpus Christi Urban Properties, LLC, 5117 Williams Dr, Corpus Christi, TX 78411. Phone <a href="tel:+13614340040">(361) 434-0040</a>. Email <a href="mailto:info@urbanpropertiescc.com">info@urbanpropertiescc.com</a>.'

legal_page("privacy-policy/", "Privacy Policy", "How Urban Properties collects, uses and protects the information you share through this website.", [
  ("Who we are", ["This website is operated by %s (&ldquo;Urban Properties,&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;), a licensed Texas real estate brokerage (TREC Broker License #9000508). This policy covers information collected through this website and the forms on it." % FIRM]),
  ("Information you give us", ["When you request a rent analysis, send a maintenance request, contact us or apply for a rental, we collect what you choose to enter: typically your name, phone number, email address, property address, details about your property or request, and any message you include.",
     "Please do not send Social Security numbers, bank account numbers or other sensitive financial information through website forms. Rental applications and payment details are handled directly with our office."]),
  ("Information collected automatically", ["Like most websites, our hosting and analytics tools may record basic technical information such as your browser type, device, approximate location derived from your IP address, the pages you visit and how you arrived at the site. We use this to keep the site working and to understand which pages are useful. Some of this relies on cookies or similar technologies, which you can block or delete in your browser settings.",
     "Our contact page includes an embedded Google Map. Google may collect information when you interact with it, under Google&rsquo;s own privacy policy."]),
  ("How we use your information", ["To respond to your request, including by phone, text message or email about that request; to provide the property management, leasing and brokerage services you ask for; to schedule and coordinate maintenance; to comply with our legal and licensing obligations; and to improve this website.",
     "We do not sell your personal information, and we do not share it with third parties for their own marketing."]),
  ("When we share it", ["With service providers that help us run this website and our business, such as website hosting and form processing, only as needed to perform those services. With our affiliated companies in the same office, such as CC Lease Locators, only when it is needed to handle a request you made, such as placing a tenant. With vendors and contractors we dispatch for a maintenance request, limited to what they need to do the work. And when required by law, regulation or subpoena, or to protect our rights or the safety of others."]),
  ("How long we keep it", ["We keep inquiry information for as long as it is useful to respond to you and serve you, and longer where Texas law or TREC rules require us to keep transaction and management records."]),
  ("Security", ["We use reasonable administrative and technical safeguards to protect the information we receive. No website or email transmission is completely secure, so please avoid sending sensitive information through forms or email."]),
  ("Your choices", ["You can ask us what information we have from you through this website, ask us to correct it, or ask us to delete it where we are not required to keep it. You can also ask us to stop contacting you. Use the contact details below and we will respond within a reasonable time."]),
  ("Children", ["This website is not directed to children under 13, and we do not knowingly collect information from them."]),
  ("Links to other sites", ["This site links to other websites, including our affiliated companies and the Texas Real Estate Commission. Their privacy practices are their own."]),
  ("Changes to this policy", ["We may update this policy from time to time. The effective date at the top shows when it last changed."]),
  ("Contact", [CONTACT_LINE])])

legal_page("terms-of-use/", "Terms of Use", "The terms that apply when you use the Urban Properties website.", [
  ("Agreement", ["By using this website you agree to these terms. If you do not agree, please do not use the site. This website is operated by %s, a licensed Texas real estate brokerage (TREC Broker License #9000508; Jon Roel, Designated Broker, License #0547401)." % FIRM]),
  ("Information on this site", ["Property, rental, pricing and market information on this site is provided for general information. It is deemed reliable but not guaranteed, may change without notice, and should be independently verified. Availability, rents, fees and terms are confirmed only in a written agreement with our office."]),
  ("Rent analysis and estimates", ["A free rent analysis or any estimate of rent, value or cost is an opinion based on information available at the time. It is not an appraisal, a guarantee of rent or occupancy, or a promise of any result."]),
  ("No agency relationship", ['Using this website, submitting a form or contacting us does not by itself create a broker-client, agency or property management relationship. That relationship begins only when you and our office sign a written agreement. Texas law requires us to provide the <a href="{R}docs/TREC-Information-About-Brokerage-Services.pdf" target="_blank" rel="noopener">Information About Brokerage Services</a> notice, which explains the types of representation available.']),
  ("Not legal, tax or financial advice", ["Content on this site is not legal, tax, accounting or financial advice. Please consult a qualified professional about your specific situation."]),
  ("Communications", ["When you give us your phone number or email through this site, you agree that we may contact you by phone, text message or email about your request. Message and data rates may apply. You can ask us to stop at any time."]),
  ("Acceptable use", ["Please do not use this site to submit false information, interfere with its operation, attempt to access areas you are not authorized to access, copy it in bulk, or use it for any unlawful purpose."]),
  ("Intellectual property", ["The text, photos, logos and design of this site belong to Urban Properties, its affiliated companies or their licensors, and may not be copied or reused without permission."]),
  ("Links to other websites", ["We link to other websites for convenience. We are not responsible for their content, accuracy or practices."]),
  ("Disclaimer and limitation of liability", ["This website is provided &ldquo;as is&rdquo; without warranties of any kind, to the fullest extent permitted by law. Urban Properties is not liable for any indirect, incidental or consequential damages arising from your use of the site or reliance on its content. Nothing here limits any rights you have under Texas law that cannot be limited by agreement."]),
  ("Governing law", ["These terms are governed by the laws of the State of Texas. Any dispute relating to this website will be brought in the state or federal courts serving Nueces County, Texas."]),
  ("Changes", ["We may update these terms from time to time. The effective date at the top shows when they last changed."]),
  ("Contact", [CONTACT_LINE])])

legal_page("accessibility/", "Accessibility Statement", "Urban Properties wants everyone to be able to use this website, including people who use assistive technology.", [
  ("Our commitment", ["We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1, Level AA. We design and test this site to work with keyboards, screen readers and zoom, and we treat accessibility as ongoing work rather than a one-time project."]),
  ("What we do", ["Text is set to meet color-contrast guidelines against its background. Images carry descriptive alternative text, and purely decorative images are hidden from screen readers. Pages use clear headings and landmarks so they can be navigated by structure. Forms have visible labels and plain-language error messages. The site works at any zoom level and on phones, tablets and desktops, and respects your device&rsquo;s reduced-motion setting."]),
  ("Known limitations", ["Some documents we link to, such as forms published by the Texas Real Estate Commission, are provided by third parties and may not be fully accessible. The embedded map on our contact page is provided by Google. If you have trouble with any of these, contact us and we will provide the information another way."]),
  ("Need help or found a problem?", ['If any part of this website is hard to use, or you need information in a different format, please call <a href="tel:+13614340040">(361) 434-0040</a> or email <a href="mailto:info@urbanpropertiescc.com">info@urbanpropertiescc.com</a>. Tell us the page and what went wrong, and we will help you directly and work to fix it. You can also visit our office at 5117 Williams Dr, Corpus Christi, TX 78411, Monday through Friday, 9:00am to 5:00pm.'])])

legal_page("fair-housing/", "Fair Housing &amp; Equal Opportunity", "Urban Properties is committed to equal housing opportunity for every owner, tenant, applicant and buyer we work with.", [
  ("Equal Housing Opportunity", ["We do business in accordance with the federal Fair Housing Act and the Texas Fair Housing Act. We do not discriminate against anyone because of race, color, religion, sex (including sexual orientation and gender identity), disability, familial status or national origin, in renting, selling, advertising, screening or managing property."]),
  ("How we apply it", ["Every applicant for a property we manage is evaluated on the same written criteria for that property, and those criteria are provided with the application. We do not steer applicants toward or away from any property or neighborhood."]),
  ("Reasonable accommodations and modifications", ['If you have a disability and need a reasonable accommodation in our rules, policies or services, or a reasonable modification to a home, you can ask at any time and in any form. Contact our office at <a href="tel:+13614340040">(361) 434-0040</a> and we will work with you promptly.']),
  ("If you believe you have been treated unfairly", ["Please tell us so we can make it right: " + CONTACT_LINE,
     'You can also contact the U.S. Department of Housing and Urban Development (HUD) Fair Housing hotline at 1-800-669-9777, or the Texas Workforce Commission Civil Rights Division at 1-888-452-4778. Complaints about a real estate license holder can be filed with the Texas Real Estate Commission; see the <a href="{R}docs/TREC-Consumer-Protection-Notice.pdf" target="_blank" rel="noopener">TREC Consumer Protection Notice</a>.'])])

# ---------------------------------------------------------------- render subpages
SIMPLE_FORM_JS = """
/* ---- simple forms (contact / maintenance): demo alert ---- */
['c-send','m-send','t-send'].forEach(function(id){
  var b = document.getElementById(id); if(!b) return;
  b.onclick = function(){
    var f = b.closest('form'); var ok = true;
    f.querySelectorAll('input[name=name],input[name=phone]').forEach(function(i){
      if(!i.value.trim() || (i.name==='phone' && !validPhone(i.value))){ i.classList.add('bad'); ok=false; } else i.classList.remove('bad');
    });
    if(!ok) return;
    alert("Thanks! In the live site this sends straight to Urban Properties.\\n\\nThis is a demo — call Jeffrey at Zonkel Media on (361) 658-2912 with any questions.");
  };
});
"""
COMMON_JS = SCRIPT_COMMON.replace("var hero = document.querySelector('.hero');", "var hero = document.querySelector('.hero,.phero');")
FORM_JS = SCRIPT_FORM.replace("var ph = document.getElementById('ph');\nph.addEventListener", "var ph = document.getElementById('ph');\nif(ph) ph.addEventListener")
FORM_JS = FORM_JS.replace("var form = document.getElementById('wiz');", "var form = document.getElementById('wiz');\nif(form){")
FORM_JS = FORM_JS.replace("show(1);", "show(1);\n}")
# the simple-form js needs validPhone; it lives in FORM_JS, so always include FORM_JS on form pages

def head_for(title, desc, path):
    h = HEAD
    h = re.sub(r"<title>.*?</title>", "<title>%s | Urban Properties Corpus Christi</title>" % re.sub(r"&amp;", "&", title), h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(re.sub(r"<[^>]+>", "", desc).replace("&rsquo;", "'").replace("&ldquo;", "").replace("&rdquo;", ""), quote=True), h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(re.sub(r"&amp;", "&", title), quote=True), h, count=1)
    h = h.replace('content="https://jzonkel1.github.io/urban-properties/"', 'content="https://jzonkel1.github.io/urban-properties/%s"' % path)
    h = h.replace('href="https://jzonkel1.github.io/urban-properties/"', 'href="https://jzonkel1.github.io/urban-properties/%s"' % path)
    h = h.replace('href="img/', 'href="../img/').replace('href="fonts/', 'href="../fonts/').replace('url(fonts/', 'url(../fonts/')
    return h

import hashlib
_W = {}
def _ver(name):
    p = os.path.join(ROOT, "img", name)
    return hashlib.md5(open(p, "rb").read()).hexdigest()[:8]
def finalize(doc):
    """srcset (1200w + full) + ?v=digest on every photo. Full-bleed boxes crop 'cover', so
    they ask for 200vw on phones (tall box, wide photo) - see cover-crop-needs-bigger-sizes."""
    def sub(m):
        pre, base = m.group(1), m.group(2)
        if not os.path.exists(os.path.join(ROOT, "img", base + "-1200.webp")):
            return m.group(0)
        w = _W.setdefault(base, Image.open(os.path.join(ROOT, "img", base + ".jpg")).size[0])
        ctx = doc[max(0, m.start() - 160):m.start()]
        sizes = ("(max-width:700px) 200vw, 100vw" if ("hero-bg" in ctx or "pb-bg" in ctx)
                 else "(max-width:860px) 50vw, 50vw" if "<figure" in ctx else "(min-width:900px) 50vw, 100vw")
        return ('<source srcset="{p}img/{b}-1200.webp?v={v1} 1200w, {p}img/{b}.webp?v={v2} {w}w" sizes="{s}" type="image/webp">'
                '<img src="{p}img/{b}.jpg?v={v3}" srcset="{p}img/{b}-1200.jpg?v={v4} 1200w, {p}img/{b}.jpg?v={v3} {w}w" sizes="{s}"').format(
            p=pre, b=base, w=w, s=sizes, v1=_ver(base + "-1200.webp"), v2=_ver(base + ".webp"),
            v3=_ver(base + ".jpg"), v4=_ver(base + "-1200.jpg"))
    return re.sub(r'<source srcset="((?:\.\./)?)img/([\w-]+)\.webp" type="image/webp">\s*<img src="(?:\.\./)?img/[\w-]+\.jpg"', sub, doc)

count = 0
for pg in PAGES:
    R = "../"
    body = pg["body"] + (cta(pg["cta"]) if pg["cta"] else "")
    doc = (head_for(pg["title"], pg["desc"], pg["slug"]) + "</head>\n<body>" + TOPBAR + NAV + body + FOOTER
           + "<script>" + COMMON_JS + (FORM_JS + SIMPLE_FORM_JS if pg["form"] else "") + "</script>\n</body>\n</html>\n")
    if pg["cta"] == "tenant":   # tenant pages: the sticky bar's second button texts the office instead of selling a rent analysis
        doc = re.sub(r'<a class="c2" href="\{R\}rent-analysis/">\s*<svg.*?</svg>\s*Free Rent Analysis</a>',
                     '<a class="c2" href="%s"><svg viewBox="0 0 24 24"><path d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"/></svg> Text the Office</a>' % JON_SMS, doc, flags=re.S)
    doc = doc.replace("{R}", R)
    d = os.path.join(ROOT, pg["slug"].rstrip("/"))
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(finalize(doc))
    count += 1

# ---------------------------------------------------------------- render home
home = SRC
# nav/footer with real links
home = home[:nav_a] + NAV + home[nav_b:]
fa = home.index("<footer"); sa = home.index("<script>", fa)
home = home[:fa] + FOOTER + home[sa:]
home = home.replace("</style>", EXTRA_CSS + "</style>", 1)
# in-body CTA anchors -> pages
home = home.replace('href="#analysis"', 'href="#contact"')   # in-body rent CTAs scroll to the home wizard
home = home.replace('<a class="btn btn-g" href="tel:+13614340040">Talk to Jon</a>', '<a class="btn btn-g" href="{R}what-we-charge/">See what we charge</a>')
# About -> photo band
a = home.index("<!-- ============ ABOUT ============ -->"); b = home.index("<!-- ============ OUR COMPANIES ============ -->")
about_home = '''<!-- ============ ABOUT ============ -->
<section class="sec photo-band about-band" id="about">
  <div class="pb-bg">%s</div>
  <div class="wrap g2">
    <div>
      <div class="eyebrow">About Urban Properties</div>
      <h2 class="big">A Corpus Christi brokerage that actually answers the phone.</h2>
      <p class="lead">Full-service real estate since 2009. We manage rental property, place tenants through our sister firm CC Lease Locators, and help people buy and sell, all under one licensed roof, led by broker Jon Roel.</p>
      %s
      <div class="cta-row" style="margin-top:32px"><a class="btn btn-p btn-lg" href="{R}about/">Meet the team <svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a><a class="btn btn-o btn-lg" href="{R}reviews/">Read the reviews</a></div>
    </div>
    <div></div>
  </div>
</section>

''' % (pic("team-wide.jpg", "The Urban Properties team outside the office"), facts_html([("chart", "Results", "Occupied units and rent that arrives on time."), ("award", "Experience", "A licensed broker and five agents, not a leasing app."), ("heart", "Commitment", "Your property treated like it&rsquo;s ours. Ours are next door."), ("phone", "Straightforward", "Auto-deposit, a direct line, no surprises.")]))
home = home[:a] + about_home + home[b:]
# Service area -> photo band
home = home.replace('<section class="sec" id="areas" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">\n  <div class="wrap g2">',
                    '<section class="sec photo-band" id="areas">\n  <div class="pb-bg">%s</div>\n  <div class="wrap g2">' % pic("aerial-lot.jpg", "Aerial view of a Coastal Bend shoreline"))
_ta = home.index('<ul class="idx idx-towns">'); _tb = home.index('</ul>', _ta) + 5
home = home[:_ta] + idx([("{R}" + p, t) for p, t in TOWNS + [("service-areas/", "Surrounding Areas")]], None, "idx-towns") + home[_tb:]
home = home.replace('<p style="margin-top:26px;font-size:15px;color:var(--muted)">Own something just outside the list?', '<p style="margin-top:26px;font-size:15px;color:#E2DCE9">Own something just outside the list?')
# Home keeps its own copy of the wizard (Jeffrey 9/28: both places). Separate Netlify form name:
# two copies of one form name = fields silently dropped (netlify-form-fields-registered-once).
home = home.replace('name="owner-inquiry" method="POST"', 'name="owner-inquiry-home" method="POST"', 1)
home = home.replace('<input type="hidden" name="form-name" value="owner-inquiry">', '<input type="hidden" name="form-name" value="owner-inquiry-home">', 1)
# tenants section on home -> link cards
home = home.replace('<a class="btn btn-g" href="#" style="margin-top:16px">Download the application</a>', '<a class="btn btn-g" href="{R}apply/" style="margin-top:16px">How to apply</a>')
home = home.replace('<a class="btn btn-g" href="sms:+13615102325" style="margin-top:16px">Text a repair request</a>', '<a class="btn btn-g" href="{R}maintenance-request/" style="margin-top:16px">Report a repair</a>')
# scripts: common + wizard
sa = home.index("<script>", home.index('id="callbar"')); sb = home.index("</script>", sa)
home = home[:sa] + "<script>" + COMMON_JS + FORM_JS + "</script>" + home[sb + len("</script>"):]
home = home.replace("{R}", "")
io.open("index.html", "w", encoding="utf-8").write(finalize(home))
print("built home + %d pages" % count)

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
    "Information About Brokerage Services": "contact/#legal",
    "Consumer Protection Notice": "contact/#legal",
    "Privacy Policy": "contact/#legal",
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
    block = block.replace('<a href="#">Information About Brokerage Services</a>', '<a href="{R}contact/#legal">Information About Brokerage Services</a>')
    block = block.replace('<a href="#">Consumer Protection Notice</a>', '<a href="{R}contact/#legal">Consumer Protection Notice</a>')
    block = block.replace('<a href="#">Privacy Policy</a>', '<a href="{R}contact/#legal">Privacy Policy</a>')
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
.phero h1{color:#fff;font-size:clamp(36px,4.8vw,64px);line-height:1.04;letter-spacing:-.025em;max-width:17ch}
.phero h1 em{font-style:italic;color:#E2B4EE}
.phero p.hl{color:#DAD3E2;font-size:clamp(16.5px,1.3vw,19.5px);margin:18px 0 26px;max-width:54ch}
.crumb{font-size:13px;color:#A79FB2;margin-bottom:18px;display:flex;gap:8px;flex-wrap:wrap}.crumb a{color:#DCA8EA}
.photo-band{position:relative;overflow:hidden;background:var(--ink);color:#DAD3E2}
.photo-band .pb-bg{position:absolute;inset:0}.photo-band .pb-bg img{width:100%;height:100%;object-fit:cover}
.photo-band .pb-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(23,20,27,.95) 0%,rgba(23,20,27,.86) 45%,rgba(23,20,27,.66) 100%)}
.photo-band .wrap{position:relative;z-index:2}
.photo-band h2,.photo-band h3,.photo-band h4{color:#fff}.photo-band .lead{color:#DAD3E2}.photo-band p{color:#CFC8D8}
.photo-band .eyebrow{color:#DCA8EA}.photo-band .eyebrow::after,.photo-band .eyebrow::before{background:rgba(255,255,255,.25)}
.photo-band .town{background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.22)}
.photo-band .team{border-top-color:rgba(255,255,255,.15)}.photo-band .team-h{color:#DCA8EA}
.photo-band .team li{border-bottom-color:rgba(255,255,255,.15)}.photo-band .team li b{color:#fff}.photo-band .team li span{color:#C9C2CF}
.photo-band .mapbox{border-color:rgba(255,255,255,.15)}
.cta-band .pb-bg::after{background:linear-gradient(180deg,rgba(23,20,27,.8),rgba(23,20,27,.92))}
.cta-band .wrap{text-align:center}.cta-band .lead{margin-left:auto;margin-right:auto}
.facts{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:32px}
.facts div>div{font-family:var(--serif);font-size:19px;color:#fff}.facts p{font-size:14.5px;color:#C9C2CF;margin:4px 0 0}
.prose p{font-size:17px;color:var(--body);max-width:68ch;margin:0 0 18px;line-height:1.7}
.prose h3{font-size:26px;margin:34px 0 10px}
.faq details{border-top:1px solid var(--line);padding:18px 0}.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font-family:var(--serif);font-size:21px;color:var(--ink);list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--pur);font-size:26px;line-height:1;flex:none}.faq details[open] summary::after{content:"\\2013"}
.faq p{margin:12px 0 0;color:var(--body);max-width:70ch;font-size:16px}
.pill-list{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.pill-list span{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-size:14px;font-weight:600;color:var(--ink)}
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

def hero(eyebrow, h1, hl, img, crumb, btn2=None):
    b2 = btn2 or ('<a class="btn btn-o" href="{R}rent-analysis/">What will my property rent for?</a>')
    return '''<section class="phero">
  <div class="hero-bg">%s</div>
  <div class="hero-scrim"></div><div class="hero-scrim2"></div>
  <div class="wrap">
    <div class="crumb"><a href="{R}">Home</a><span>/</span>%s</div>
    <div class="eyebrow">%s</div>
    <h1>%s</h1>
    <p class="hl">%s</p>
    <div class="hero-btns">
      <a class="btn btn-p" href="%s">%s Call %s</a>
      %s
    </div>
  </div>
</section>''' % (pic(img, h1, lazy=False), crumb, eyebrow, h1, hl, TEL, CALL_SVG, PHONE, b2)

def cta(kind="owner"):
    if kind == "tenant":
        return '''<section class="sec photo-band cta-band">
  <div class="pb-bg">%s</div>
  <div class="wrap">
    <div class="eyebrow c">Questions?</div>
    <h2 class="big">Text the office. A real person answers.</h2>
    <p class="lead">Repairs, rent, applications, anything about your lease.</p>
    <div style="margin-top:30px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
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
    <div style="margin-top:30px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      <a class="btn btn-p" href="{R}rent-analysis/">Start my free rent analysis</a>
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
  <div class="fee-row big"><b>One month&rsquo;s rent</b><span>to find, screen and place your tenant. Collected out of their first month&rsquo;s rent, not from you.</span></div>
  <div class="fee-row big"><b>10% of rent</b><span>each month for ongoing management. Rent comes in, your share is deposited, the rest is handled.</span></div>
  <div class="fee-row big"><b>Either one on its own</b><span>Already have a tenant? Just the management. Want to manage it yourself? Just the placement.</span></div>
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
def service_links(current=None):
    return '<div class="pill-list">%s</div>' % "".join(
        '<span>%s</span>' % l if p == current else '<a href="{R}%s" style="text-decoration:none"><span>%s</span></a>' % (p, l)
        for p, l in SERVICE_LIST)

TOWNS = [("corpus-christi/", "Corpus Christi"), ("padre-island/", "Padre Island"), ("calallen/", "Calallen"), ("robstown/", "Robstown")]

# ---------------------------------------------------------------- pages
PAGES = []
def page(slug, title, desc, body, crumb_label=None, cta_kind="owner", has_form=False):
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
    [("How fast can you take over a property that already has a tenant?", "Usually inside a week. We collect the lease, the deposit records and the keys, introduce ourselves to the tenant, and rent comes to us from the next due date."),
     ("Do I approve the tenant?", "Yes. We screen and recommend; you say yes before anyone signs."),
     ("What if I only want part of this?", "Then you pay for that part. Placement only is one month&rsquo;s rent. Management only is 10%. See <a href=\"{R}what-we-charge/\">what we charge</a>.")],
    "int-kitchen-open.jpg")

service_page("tenant-screening-placement/", "Tenant Screening &amp; Placement", "Find The Right Tenant", "The decision that decides the next <em>two years.</em>",
    "Credit, income, rental history, background and eviction checks, then a signed lease. One month&rsquo;s rent, paid out of the tenant&rsquo;s first month.",
    "int-kitchen-white.jpg", "A good tenant is the whole game.",
    ["Most rental headaches trace back to one bad placement. So we treat screening like the most important thing we do, because it is.",
     "Our sister firm, CC Lease Locators, places renters across Corpus Christi every week, which means your vacancy gets a steady stream of candidates who are already looking."],
    ["Listed on the MLS and syndicated to Zillow, Realtor.com, Trulia, Redfin and Homes.com", "Showings handled by our agents", "Credit, income verification, rental history, background and eviction checks",
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
    "prop-yard.jpg")

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
    "int-kitchen-blue.jpg", "One call ends it. And it isn&rsquo;t to you.",
    ["A water heater doesn&rsquo;t care what time it is. Our tenants text or call the office, and the office decides what&rsquo;s urgent, who to send and what it should cost.",
     "We use plumbers, electricians and handymen we&rsquo;ve worked with for years, on our own buildings as well as yours."],
    ["Tenant requests by text or call to (361) 510-2325", "Vetted local trades, no markup on their invoice", "Your approval on anything over $250",
     "Emergencies handled the same day", "Photos before and after when it matters", "Preventive items caught at inspections"],
    [("Text or call", "Tenants text the office with the address and the problem. Photos help. Emergencies, they call."),
     ("Triage first", "Not every request is a repair. Some are a reset button or a filter. We sort that before anyone drives out."),
     ("Trades we already use", "The same people who service the eight-unit complex and the commercial building we own."),
     ("Your $250 line", "Under it, we handle it and note it. Over it, you approve it first."),
     ("No markup", "You pay what the trade charges. Coordination is part of the 10%."),
     ("Documented", "Every request, who went, what it cost. Ask any time.")],
    [("Do I have to approve every repair?", "Only over $250. Small items are handled so the tenant isn&rsquo;t waiting and you aren&rsquo;t getting a call about a faucet."),
     ("Can I use my own plumber?", "Yes. Tell us at onboarding and they go on the list for your property."),
     ("Who pays for tenant damage?", "The tenant, out of the deposit or by invoice, per the lease. Wear and tear is the owner&rsquo;s.")],
    "prop-tan-corner.jpg")

service_page("lease-renewals-enforcement/", "Lease Renewals &amp; Enforcement", "Written By A Broker", "Leases that hold up, and get <em>renewed.</em>",
    "Texas leases prepared and enforced by a licensed broker, renewals negotiated before the term ends, and rules that actually get followed.",
    "prop-grey-row.jpg", "A lease is only as good as the person enforcing it.",
    ["We use current Texas lease forms, filled out for your property and your rules: pets, smoking, occupancy, late fees, maintenance responsibilities.",
     "Sixty days before a lease ends we&rsquo;re already talking to the tenant about renewal and to you about the rent. Turnover is the most expensive thing that happens to a rental; we try not to let it happen by accident."],
    ["Texas lease forms, prepared by a licensed broker", "Your rules written in and enforced", "Renewal conversations start 60 days out",
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
    ["Before a tenant gets the keys, we walk the property and photograph every room, appliance and surface. When they leave, we do it again.",
     "That record is what makes a deposit deduction fair and defensible, and it&rsquo;s what tells you when a unit needs work before the next listing."],
    ["Room-by-room condition report with photos", "Tenant signs off on the move-in report", "Move-out walkthrough within days of vacancy",
     "Deposit itemization per Texas rules and timelines", "Make-ready list so the unit relists fast", "Records kept for the life of the tenancy"],
    [("Move-in", "Documented and signed before the first night. The tenant knows exactly what they&rsquo;re responsible for."),
     ("During", "Occasional check-ins and maintenance visits catch problems while they&rsquo;re small."),
     ("Move-out", "Compared against the move-in report. Damage beyond wear and tear comes out of the deposit."),
     ("Deposit handled", "Itemized and returned within the timeline Texas requires. We do the paperwork."),
     ("Make-ready", "Paint, clean, repair. We line up the trades so the unit is back on the market quickly."),
     ("Fewer vacant days", "The whole point. Turnover handled fast is money you don&rsquo;t lose.")],
    [("Do I need to be there?", "No. You&rsquo;re welcome to, but the report and photos come to you either way."),
     ("How long does a turnover take?", "Depends on condition. A clean unit relists in days. We tell you the make-ready scope and cost up front."),
     ("Who decides deposit deductions?", "We recommend based on the reports and Texas rules; you approve.")],
    "prop-yard.jpg")

service_page("investment-property-sales/", "Investment Property Sales", "Buy The Next Door", "The broker who manages it can help you <em>buy it.</em>",
    "Buying the next rental or selling the last one. A full Texas brokerage in the same office that manages your property.",
    "prop-blue-street.jpg", "We know what it will rent for before you make the offer.",
    ["Most investors buy with a guess about rent and a guess about expenses. We manage thirty doors in this market; we know what a duplex on that street rents for and what it costs to run.",
     "That&rsquo;s the advantage of buying through the office that will manage it: the numbers you underwrite are the numbers you&rsquo;ll actually see."],
    ["Off-market and MLS opportunities across Corpus Christi", "Rent and expense estimates from a manager, not a listing", "Offer, inspection and closing handled by a licensed broker",
     "Tenant placement lined up before you close", "Management ready on day one", "Sell the same way when you&rsquo;re ready to trade up"],
    [("Real rent numbers", "From the office that collects rent on thirty doors. Not a website estimate."),
     ("Real expense numbers", "We know what repairs, turnover and vacancy actually cost here."),
     ("Duplex to apartment", "Single family, duplexes, fourplexes, small complexes, commercial. We own and manage all of them."),
     ("Closing to keys", "Under contract to placed tenant, one office, one file."),
     ("Build it instead", "If the deal is land, Manhattan Builders can put the building on it. See <a href=\"{R}build-to-rent/\">build-to-rent</a>."),
     ("Selling", "When it&rsquo;s time, we list it with the rent roll and the records that make it easy to sell.")],
    [("Do I have to use you for management if I buy through you?", "No. But most do, because the analysis we used to buy it is the plan we manage it with."),
     ("Do you help with financing?", "We&rsquo;ll connect you with local lenders who do investment loans and know these numbers."),
     ("What about 1031 exchanges?", "We&rsquo;ve handled them. Tell us the timeline early.")],
    "prop-grey-row.jpg")

service_page("residential-sales/", "Residential Sales", "Buying &amp; Selling Homes", "A Corpus Christi brokerage with <em>six agents</em> and one broker.",
    "Buying or selling a home in Corpus Christi and the surrounding area, with agents who know what every block is worth because we manage rentals on them.",
    "prop-yard.jpg", "Local agents, licensed broker, straight answers.",
    ["Urban Properties is a full Texas real estate brokerage. Our agents help families buy and sell homes across Corpus Christi, Padre Island, Calallen and Robstown.",
     "Because the same office manages rental property, we see what homes actually rent for, what they cost to maintain, and which streets are moving. That&rsquo;s useful whether you&rsquo;re buying your first house or selling one you&rsquo;ve had for twenty years."],
    ["Six licensed agents under broker Jon Roel", "Listings on the MLS and every major site", "Pricing from real local comps",
     "Showings, offers and negotiation handled", "Inspection and closing coordinated", "Investors and first-time buyers alike"],
    [("Selling", "Priced from comps we trust, photographed, listed everywhere, shown by our agents."),
     ("Buying", "Tell us the budget and the neighborhoods. We find it, show it, write the offer, and get you to closing."),
     ("Rent it instead?", "Sometimes the better move is to keep the house and rent it. We&rsquo;ll run both numbers for you honestly."),
     ("Relocating", "Coming to Corpus for work or the base? We handle the search remotely and the closing in person."),
     ("Lots and land too", "Buying a lot to build on? See <a href=\"{R}lot-land-sales/\">lot and land sales</a>."),
     ("The team", "Laura Vasquez, Amy Soza, Danny Guerrero, Maria Cruz, Michael Benavidez. <a href=\"{R}about/\">Meet them</a>.")],
    [("Which areas do you cover for sales?", "Corpus Christi, Padre Island, Calallen, Robstown and the surrounding area."),
     ("Should I sell or rent my house out?", "Ask us. We&rsquo;ll give you the sale number and the rent number from the same office, and tell you which we&rsquo;d do."),
     ("Do you work with first-time buyers?", "Yes, and with the local lenders who make that easier.")],
    "int-kitchen-open.jpg")

service_page("lot-land-sales/", "Lot &amp; Land Sales", "Lots, Acreage, Infill", "Buy the dirt. <em>Build the deposit.</em>",
    "Lots, acreage and infill parcels across the Coastal Bend, from a brokerage that shares an office with a home builder.",
    "prop-tan-corner.jpg", "Land is where the whole chain starts.",
    ["We help buyers find and close on residential lots, small acreage and infill parcels in and around Corpus Christi, and we list land for owners ready to sell.",
     "The difference here: Manhattan Builders is down the hall. If you&rsquo;re buying to build, the person who can tell you what fits on the lot and what it costs is in the same building."],
    ["Residential lots, acreage and infill parcels", "Zoning, utilities and setback questions answered before you offer", "Build feasibility from Manhattan Builders",
     "Listing and marketing for land owners", "Closing handled by a licensed broker", "Build-to-rent path if you&rsquo;re investing"],
    [("Find the lot", "MLS and off-market parcels. We know which ones have water and sewer at the street."),
     ("Check the build", "Manhattan Builders reviews the lot for what can go on it and what that costs. Before you close."),
     ("Sell your land", "Priced, listed and marketed to builders and investors, not just posted."),
     ("Infill", "Corpus Christi has empty lots in good neighborhoods. Duplexes on them rent well. We know that firsthand."),
     ("Acreage", "Outside the city limits, we&rsquo;ll walk it with you and pull the county records."),
     ("Then build to rent", "Dirt to deposit, one office. See <a href=\"{R}build-to-rent/\">how that works</a>.")],
    [("Can you tell me if a lot is buildable?", "Yes. The builder reviews it before you make an offer."),
     ("Do you sell commercial land?", "Yes. Small commercial parcels and pad sites in the Corpus Christi area."),
     ("What does it cost to list land with you?", "Standard listing commission, agreed in writing up front.")],
    "prop-blue-street.jpg")

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
     ("Do you handle HOA finances?", "Dues collection, vendor payments and records, yes. Reserve studies and audits are coordinated with your CPA."),
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
            "Credit, income, history, background. You approve the tenant before anyone signs.",
            "Clear due dates, consistent follow-up, your share auto-deposited monthly.",
            "Tenants text the office. Vetted trades show up. You approve anything over $250.",
            "Texas leases prepared and enforced by a licensed broker. Renewals started 60 days out.",
            "Photos and a signed condition report both ways. Deposits settled on evidence.",
            "Buy the next door through the office that already knows what it rents for.",
            "Six agents, one broker, real local comps. Buying or selling a home.",
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
        ("Lease enforcement", "Your rules held, notices served correctly, renewals started 60 days out."),
        ("Inspections", "Move-in and move-out condition reports with photos."),
        ("Owner communication", "You hear from us when something needs a decision or costs over $250."),
        ("No extras", "No setup fee, no renewal fee, no markup on repairs. Ten percent of collected rent.")])
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
                 "prop-yard.jpg", "<span>How Onboarding Works</span>")
    + steps4("The Process", "What happens, in order", [
        ("Free rent analysis", "Tell us about the property. We come back with what it should rent for and what we&rsquo;d do first."),
        ("Sign &amp; onboard", "Management agreement, keys, a walkthrough. We photograph and document the condition."),
        ("We market and screen", "Listed on the MLS and everywhere it syndicates, shown, screened. You approve the tenant."),
        ("You get paid", "Rent lands in your account automatically. The phone calls come to us instead of you.")])
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap g2">
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div>
  <div><div class="eyebrow">What We Need From You</div><h2 class="big">About twenty minutes of your time.</h2>
  <ul class="checks" style="color:var(--body)">%s</ul></div></div></section>''' % (pic("int-living.jpg", "Managed rental interior"), "".join(CHECK % b for b in [
        "A signed management agreement (we send it, you sign on your phone)",
        "Keys, garage remotes, gate codes",
        "The current lease and deposit records, if there&rsquo;s a tenant in place",
        "The bank account your rent should be deposited to",
        "Any rules you want enforced: pets, smoking, occupancy",
        "Your preferred trades, if you have them. Otherwise we use ours."]))
    + faq("Timing", "How long things take", [
        ("How fast can you start?", "If the property already has a tenant, usually within a week. If it&rsquo;s vacant, we list it as soon as it&rsquo;s photographed and ready."),
        ("How long to find a tenant?", "Depends on price and condition. Priced right, most units in Corpus Christi lease within a few weeks, and CC Lease Locators has renters looking already."),
        ("When&rsquo;s the first deposit?", "After the first rent clears. Your share is deposited to the account you gave us.")]))
page("how-onboarding-works/", "How Onboarding Works", "How to hand your Corpus Christi rental to Urban Properties: rent analysis, agreement, marketing, first deposit. Four steps.", how_body)

btr_body = (hero("For Investors", "From dirt <em>to deposit.</em>",
                 "Manhattan Builders builds it. CC Lease Locators fills it. Urban Properties manages it and, when you&rsquo;re ready, sells it. One office, one team.",
                 "hero.jpg", "<span>Build-to-Rent</span>")
    + '''<section class="band sec"><div class="wrap">
  <div class="center" style="margin-bottom:46px"><div class="eyebrow c">One Office, Three Companies</div><h2 class="big">We build it, fill it, manage it, and sell it.</h2></div>
  <div class="cos">
    <a class="co" href="https://manhattanbuilders.cc" target="_blank" rel="noopener"><div class="co-step">Builds it</div><div class="co-name">Manhattan Builders</div><p>Custom homes, multifamily and light commercial across the Coastal Bend since 2003. The duplexes on this site are theirs.</p><span class="co-link">manhattanbuilders.cc &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co" href="https://ccleaselocators.com" target="_blank" rel="noopener"><div class="co-step">Fills it</div><div class="co-name">CC Lease Locators</div><p>Free apartment locating for renters across Corpus Christi. 4.9 stars from 150 Google reviews, placing tenants every week.</p><span class="co-link">ccleaselocators.com &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co you" href="{R}property-management/"><div class="co-step">Manages &amp; sells it</div><div class="co-name">Urban Properties</div><p>Property management and a full brokerage, for the day you&rsquo;re ready to buy the next one or sell the last.</p><span class="co-link">You&rsquo;re here</span></a>
  </div></div></section>'''
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
ten_hub = (hero("For Tenants", "Renting from us is <em>simple.</em>",
                "Apply, pay rent, report a repair. Everything you need is here, and a real person answers the office.",
                "int-living.jpg", "<span>Tenants</span>", btn2='<a class="btn btn-o" href="%s">Text (361) 510-2325</a>' % JON_SMS)
    + '''<section class="sec"><div class="wrap"><div class="g3">
  <a class="card" href="{R}available-rentals/" style="text-decoration:none;display:block"><h3>Available Rentals</h3><p>Our listings run on Zillow, Realtor.com and every MLS site. Here&rsquo;s how to find them.</p></a>
  <a class="card" href="{R}apply/" style="text-decoration:none;display:block"><h3>Apply for a Rental</h3><p>$50 application. Stable income and rental history preferred. Download the application here.</p></a>
  <a class="card" href="{R}pay-rent/" style="text-decoration:none;display:block"><h3>Pay Rent</h3><p>Drop off at the office, or Cash App, Avail, Venmo and PayPal.</p></a>
  <a class="card" href="{R}maintenance-request/" style="text-decoration:none;display:block"><h3>Maintenance Request</h3><p>Text or call the office, or send it through the form with a photo.</p></a>
  <a class="card" href="{R}tenant-faqs/" style="text-decoration:none;display:block"><h3>Tenant FAQs</h3><p>Due dates, late fees, deposits, moving out, pets. The answers.</p></a>
  <a class="card" href="{R}contact/" style="text-decoration:none;display:block"><h3>Contact the Office</h3><p>5117 Williams Dr, Corpus Christi. Mon&ndash;Fri, 9 to 5.</p></a>
</div></div></section>''')
page("tenants/", "For Tenants", "Urban Properties tenants: apply, pay rent, request maintenance and find available rentals in Corpus Christi.", ten_hub, cta_kind="tenant")

avail_body = (hero("Available Rentals", "Our listings are <em>everywhere</em> you already look.",
                   "Every Urban Properties rental goes on the MLS and syndicates to Zillow, Realtor.com, Trulia, Redfin and Homes.com the same day.",
                   "prop-blue-street.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Available Rentals</span>', btn2='<a class="btn btn-o" href="{R}apply/">How to apply</a>')
    + '''<section class="sec"><div class="wrap g2">
  <div><div class="eyebrow">Where To Look</div><h2 class="big">Search &ldquo;Urban Properties&rdquo; on any of these.</h2>
  <p class="lead">We list through the MLS, so the same units show up on every major site at once. Search the address or filter by the Corpus Christi area and look for our name.</p>
  <div class="pill-list"><a href="https://www.zillow.com/" target="_blank" rel="noopener" style="text-decoration:none"><span>Zillow &rarr;</span></a><a href="https://www.realtor.com/" target="_blank" rel="noopener" style="text-decoration:none"><span>Realtor.com &rarr;</span></a><a href="https://www.trulia.com/" target="_blank" rel="noopener" style="text-decoration:none"><span>Trulia &rarr;</span></a><a href="https://www.redfin.com/" target="_blank" rel="noopener" style="text-decoration:none"><span>Redfin &rarr;</span></a><a href="https://www.homes.com/" target="_blank" rel="noopener" style="text-decoration:none"><span>Homes.com &rarr;</span></a></div>
  <p style="color:var(--muted);margin-top:26px">Looking for an apartment rather than a house? Our sister firm <a href="https://ccleaselocators.com" target="_blank" rel="noopener" style="color:var(--pur);font-weight:700">CC Lease Locators</a> finds apartments across Corpus Christi for free.</p>
  <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-p" href="{R}apply/">Apply for a rental</a><a class="btn btn-g" href="%s">Text the office</a></div></div>
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div></div></section>''' % (JON_SMS, pic("int-kitchen-white.jpg", "Rental unit kitchen")))
page("available-rentals/", "Available Rentals", "Urban Properties rentals in Corpus Christi are listed on the MLS, Zillow, Realtor.com, Trulia, Redfin and Homes.com.", avail_body, cta_kind="tenant")

apply_body = (hero("Apply", "Apply for a <em>rental.</em>",
                   "$50 application fee per adult. Stable, verifiable income and rental history preferred. Download the application, fill it out, and bring or send it to the office.",
                   "int-kitchen-white.jpg", '<a href="{R}tenants/">Tenants</a><span>/</span><span>Apply</span>', btn2='<a class="btn btn-o" href="#">Download the application</a>')
    + '''<section class="sec"><div class="wrap g2">
  <div><div class="eyebrow">How It Works</div><h2 class="big">Three steps to the keys.</h2>
  <ul class="checks" style="color:var(--body)">%s</ul>
  <div class="note-box" style="margin-top:28px"><b>Application fee:</b> $50 per adult applicant, paid when you submit. <b>We look for:</b> stable, verifiable income and rental history. Pets and other specifics are set per property; ask before you apply.</div>
  <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-p" href="#">Download the application (PDF)</a><a class="btn btn-g" href="%s">Text a question</a></div></div>
  <div class="band-img" style="box-shadow:var(--sh-l)">%s</div></div></section>''' % ("".join(CHECK % b for b in [
        "Download the application and fill it out for every adult who will live there",
        "Bring it to 5117 Williams Dr (Mon&ndash;Fri, 9 to 5) or send it back the way we sent it to you, with the $50 fee",
        "We verify income, rental history and background, then call you with the answer"]), JON_SMS, pic("prop-yard.jpg", "Rental home with fenced yard"))
    + faq("Before You Apply", "Applicants usually ask", [
        ("What do I need to bring?", "Photo ID, proof of income (recent pay stubs or an offer letter), and your last two landlords&rsquo; contact info."),
        ("How long does approval take?", "Usually a day or two once we can reach your references."),
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
        ("How fast will someone come?", "Emergencies same day. Everything else is scheduled with you, usually within a few days depending on the trade."),
        ("Do I have to be home?", "Not if you tell us it&rsquo;s OK to enter. If you have pets or would rather be there, say so and we&rsquo;ll schedule around you."),
        ("Who pays for the repair?", "Normal wear and repairs are on the owner. Damage caused by the tenant is charged back per the lease."),
        ("What counts as an emergency?", "Anything that&rsquo;s a safety issue or is actively damaging the property: water where it shouldn&rsquo;t be, no power, no working toilet, no A/C in extreme heat.")]))
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
        ("Can I renew?", "We&rsquo;ll reach out about 60 days before your lease ends. If you want to stay, say so and we&rsquo;ll send the renewal."),
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
  <div class="towns">%s</div>
  <div style="margin-top:30px">%s</div></div>
  <div class="mapbox"><iframe src="https://www.google.com/maps?q=%s&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of %s"></iframe></div></div></section>''' % (
            name, "".join('<span class="town">%s</span>' % t if p == slug else '<a href="{R}%s" style="text-decoration:none"><span class="town">%s</span></a>' % (p, t) for p, t in TOWNS + [("service-areas/", "Surrounding Areas")]),
            FEES.replace('id="fees"', ''), mapq, name)
        + '<section class="sec-tight"><div class="wrap"><div class="eyebrow">What We Handle In %s</div>%s</div></section>' % (name, service_links()))
    page(slug, "Property Management in " + name, hl, body, crumb_label=name)

town_page("corpus-christi/", "Corpus Christi", "Corpus Christi rental property, <em>managed from Williams Drive.</em>",
    "Single-family homes, duplexes, small apartment communities and commercial space across Corpus Christi, managed by a licensed local brokerage.",
    "prop-blue-street.jpg",
    "Corpus Christi is home. Our office, our own rentals and most of the doors we manage are here, from the Southside to Calallen to the Island.",
    "That means when a tenant reports a leak on Everhart, someone who knows the property is twenty minutes away, and when you ask what a duplex near the base should rent for, the answer comes from units we already manage.",
    ["Southside, Westside, Flour Bluff, downtown and the Bay area", "Single family, duplex, fourplex, multifamily and commercial", "Tenants placed through CC Lease Locators", "Rent auto-deposited, one point of contact"],
    "Corpus+Christi,+TX")
town_page("padre-island/", "Padre Island", "Island rentals, <em>handled from the mainland.</em>",
    "Property management for homes, condos and townhomes on Padre Island, with tenant placement, rent collection and maintenance handled by our Corpus Christi office.",
    "prop-yard.jpg",
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
  <div><div class="eyebrow">The Office</div><h2 class="big">5117 Williams Drive, Corpus Christi.</h2><p class="lead">Mon&ndash;Fri, 9:00am to 5:00pm. Tenants drop rent here; owners are welcome any time.</p>
  <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-p" href="%s">%s Call %s</a><a class="btn btn-g" href="{R}contact/">Contact</a></div></div>
  <div class="mapbox"><iframe src="https://www.google.com/maps?q=5117+Williams+Dr,+Corpus+Christi,+TX+78411&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Urban Properties office location"></iframe></div></div></section>''' % (TEL, CALL_SVG, PHONE))
page("service-areas/", "Service Areas", "Urban Properties manages rental property across Corpus Christi, Padre Island, Calallen, Robstown and the surrounding Coastal Bend.", areas_hub)

# ---- about / companies / reviews / contact -----------------------------
TEAM = [("Jon Roel", "Broker"), ("Laura Vasquez", "Realtor"), ("Amy Soza", "Realtor"), ("Danny Guerrero", "Realtor"), ("Maria Cruz", "Realtor"), ("Michael Benavidez", "Realtor")]
about_body = (hero("About Urban Properties", "A Corpus Christi brokerage that <em>actually answers the phone.</em>",
                   "Full-service real estate since 2009. Property management, tenant placement, sales, and a builder down the hall. All under one licensed roof, led by broker Jon Roel.",
                   "prop-grey-row.jpg", "<span>About</span>")
    + intro("Since 2009", "The same person who manages your rental can tell you what to buy next.", [
        "Urban Properties started in 2009 as the brokerage side of a family that was already building homes in Corpus Christi. Sixteen years on, we manage rental property, place tenants through our sister firm CC Lease Locators, and help people buy and sell, all from one office on Williams Drive.",
        "We own and manage our own buildings, an eight-unit townhome complex, an eight-tenant commercial building, a duplex and houses, and we run yours the same way. You&rsquo;re not handing your investment to a call center three states away."],
        [], "int-living.jpg", "Managed rental interior",
        extra='<div class="team" style="margin-top:30px"><div class="team-h">The team</div><ul>%s</ul></div>' % "".join('<li><b>%s</b><span>%s</span></li>' % t for t in TEAM))
    + cards("What We Stand On", "Four things you can hold us to", [
        ("Results", "Occupied units and rent that arrives on time. That&rsquo;s the job."),
        ("Experience", "A licensed Texas broker and six agents, not a leasing app."),
        ("Commitment", "Your property treated like it&rsquo;s ours. Because ours are next door."),
        ("Straightforward", "Auto-deposit, a direct line, and no surprises. You hear from us when it matters."),
        ("Local", "5117 Williams Drive. Twenty minutes from every property we manage."),
        ("Licensed", "TREC Broker License #9000508. Jon Roel, Designated Broker, License #0547401.")])
    + '''<section class="sec" style="background:var(--paper-2);border-top:1px solid var(--line)"><div class="wrap center"><div class="eyebrow c">Three Companies</div><h2 class="big">We build it, fill it, manage it, and sell it.</h2><p class="lead">Manhattan Builders, CC Lease Locators and Urban Properties share one office and one owner.</p><div style="margin-top:28px"><a class="btn btn-p" href="{R}our-companies/">See how they fit together</a></div></div></section>''')
page("about/", "About Urban Properties", "Urban Properties: a Corpus Christi real estate brokerage since 2009. Property management, tenant placement and sales, led by broker Jon Roel.", about_body)

cos_body = (hero("One Office, Three Companies", "We build it, fill it, manage it, <em>and sell it.</em>",
                 "Manhattan Builders, CC Lease Locators and Urban Properties share one office at 5117 Williams Drive. Whatever stage your property is at, the next call is to the same people.",
                 "hero.jpg", "<span>Our Companies</span>")
    + '''<section class="band sec"><div class="wrap"><div class="cos">
    <a class="co" href="https://manhattanbuilders.cc" target="_blank" rel="noopener"><div class="co-step">Builds it</div><div class="co-name">Manhattan Builders</div><p>Custom homes, multifamily and light commercial across the Coastal Bend since 2003. Corpus Christi, Padre Island, Port Aransas, Rockport.</p><span class="co-link">manhattanbuilders.cc &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co" href="https://ccleaselocators.com" target="_blank" rel="noopener"><div class="co-step">Fills it</div><div class="co-name">CC Lease Locators</div><p>Free apartment locating for renters across Corpus Christi. 4.9 stars from 150 Google reviews, placing tenants every week.</p><span class="co-link">ccleaselocators.com &rarr;</span></a>
    <div class="co-arr">&rarr;</div>
    <a class="co you" href="{R}property-management/"><div class="co-step">Manages &amp; sells it</div><div class="co-name">Urban Properties</div><p>Property management and a full brokerage since 2009, for the day you&rsquo;re ready to buy the next one or sell the last.</p><span class="co-link">You&rsquo;re here</span></a>
  </div><p class="co-note">Own land and thinking about building to rent? <a href="{R}build-to-rent/">Here&rsquo;s how that works.</a> One team takes it from dirt to deposit.</p></div></section>'''
    + cards("Why It Matters To You", "One file, start to finish", [
        ("For owners", "The builder knows the building, the locator knows the renters, the manager knows the numbers. Nothing gets lost between companies."),
        ("For investors", "Buy a lot, build a duplex, lease it up, manage it, sell it. Same office, same people, one phone number."),
        ("For renters", "CC Lease Locators finds you a place for free. If it&rsquo;s one of ours, you already know who manages it.")], bg=False))
page("our-companies/", "Our Companies", "Manhattan Builders builds it, CC Lease Locators fills it, Urban Properties manages and sells it. One Corpus Christi office.", cos_body)

STAR = '<svg viewBox="0 0 24 24"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/></svg>'
def review(text, name, ini):
    return '<div class="rev"><div class="stars">%s</div><p>%s</p><div class="who"><div class="av">%s</div><div><div class="nm">%s</div><div class="src">Google Review</div></div></div></div>' % (STAR * 5, text, ini, name)
rev_body = (hero("Reviews", "Straight from <em>Google.</em>",
                 "What owners and clients say about working with Jon and the office. Every one of these is a real Google review.",
                 "int-kitchen-open.jpg", "<span>Reviews</span>")
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
  <p>Texas law requires all real estate license holders to provide the <b>Information About Brokerage Services</b> notice to prospective clients, and the <b>Consumer Protection Notice</b> from the Texas Real Estate Commission. Both are available at the office and will be provided before any representation begins.</p>
  <p><b>Privacy:</b> information submitted through this website is used only to respond to your request and is not sold or shared with third parties.</p>
  <p>All information deemed reliable but not guaranteed. Equal Housing Opportunity.</p></div></div></section>''')
page("contact/", "Contact", "Contact Urban Properties: 5117 Williams Dr, Corpus Christi, TX 78411. Call (361) 434-0040 or text (361) 510-2325.", contact_body, has_form=True)

# ---------------------------------------------------------------- render subpages
SIMPLE_FORM_JS = """
/* ---- simple forms (contact / maintenance): demo alert ---- */
['c-send','m-send'].forEach(function(id){
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
    h = h.replace('href="img/', 'href="../img/')
    return h

count = 0
for pg in PAGES:
    R = "../"
    body = pg["body"] + cta(pg["cta"])
    doc = (head_for(pg["title"], pg["desc"], pg["slug"]) + "</head>\n<body>" + TOPBAR + NAV + body + FOOTER
           + "<script>" + COMMON_JS + (FORM_JS + SIMPLE_FORM_JS if pg["form"] else "") + "</script>\n</body>\n</html>\n")
    doc = doc.replace("{R}", R)
    d = os.path.join(ROOT, pg["slug"].rstrip("/"))
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
    count += 1

# ---------------------------------------------------------------- render home
home = SRC
# nav/footer with real links
home = home[:nav_a] + NAV + home[nav_b:]
fa = home.index("<footer"); sa = home.index("<script>", fa)
home = home[:fa] + FOOTER + home[sa:]
home = home.replace("</style>", EXTRA_CSS + "</style>", 1)
# in-body CTA anchors -> pages
home = home.replace('href="#analysis"', 'href="{R}rent-analysis/"').replace('href="#contact"', 'href="{R}rent-analysis/"')
home = home.replace('<a class="btn btn-g" href="tel:+13614340040">Talk to Jon</a>', '<a class="btn btn-g" href="{R}what-we-charge/">See what we charge</a>')
# About -> photo band
a = home.index("<!-- ============ ABOUT ============ -->"); b = home.index("<!-- ============ OUR COMPANIES ============ -->")
about_home = '''<!-- ============ ABOUT ============ -->
<section class="sec photo-band" id="about">
  <div class="pb-bg">%s</div>
  <div class="wrap g2">
    <div>
      <div class="eyebrow">About Urban Properties</div>
      <h2 class="big">A Corpus Christi brokerage that actually answers the phone.</h2>
      <p class="lead">Full-service real estate since 2009. We manage rental property, place tenants through our sister firm CC Lease Locators, and help people buy and sell, all under one licensed roof, led by broker Jon Roel.</p>
      <p style="margin-top:14px">The person managing your rental is the same person who can tell you whether the duplex down the street is worth buying. You&rsquo;re not handing your investment to a call center three states away.</p>
      <div class="facts">
        <div><div>Results</div><p>Occupied units and rent that arrives on time.</p></div>
        <div><div>Experience</div><p>A licensed broker and six agents, not a leasing app.</p></div>
        <div><div>Commitment</div><p>Your property treated like it&rsquo;s ours. Ours are next door.</p></div>
        <div><div>Straightforward</div><p>Auto-deposit, a direct line, no surprises.</p></div>
      </div>
      <div style="margin-top:32px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-p" href="{R}about/">More about us</a><a class="btn btn-o" href="{R}reviews/">Read the reviews</a></div>
    </div>
    <div class="team" style="border-top:0;padding-top:0;margin-top:0">
      <div class="team-h">The team</div>
      <ul style="grid-template-columns:1fr">%s</ul>
    </div>
  </div>
</section>

''' % (pic("prop-grey-row.jpg", ""), "".join('<li><b>%s</b><span>%s</span></li>' % t for t in TEAM))
home = home[:a] + about_home + home[b:]
# Service area -> photo band
home = home.replace('<section class="sec" id="areas" style="background:var(--paper-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)">\n  <div class="wrap g2">',
                    '<section class="sec photo-band" id="areas">\n  <div class="pb-bg">%s</div>\n  <div class="wrap g2">' % pic("prop-yard.jpg", ""))
home = home.replace('<span class="town">Corpus Christi</span><span class="town">Padre Island</span>\n        <span class="town">Calallen</span><span class="town">Robstown</span>\n        <span class="town">Surrounding Areas</span>',
                    "".join('<a href="{R}%s" style="text-decoration:none"><span class="town">%s</span></a>' % (p, t) for p, t in TOWNS + [("service-areas/", "Surrounding Areas")]))
home = home.replace('<p style="margin-top:26px;font-size:15px;color:var(--muted)">Own something just outside the list?', '<p style="margin-top:26px;font-size:15px;color:#C9C2CF">Own something just outside the list?')
# Contact/wizard -> CTA band linking to the rent-analysis page
a = home.index("<!-- ============ CONTACT / WIZARD ============ -->"); b = home.index("<footer")
home = home[:a] + "<!-- ============ CTA ============ -->\n" + cta("owner").replace('class="sec photo-band cta-band"', 'class="sec photo-band cta-band" id="contact"') + "\n\n" + home[b:]
# tenants section on home -> link cards
home = home.replace('<a class="btn btn-g" href="#" style="margin-top:16px">Download the application</a>', '<a class="btn btn-g" href="{R}apply/" style="margin-top:16px">How to apply</a>')
home = home.replace('<a class="btn btn-g" href="sms:+13615102325" style="margin-top:16px">Text a repair request</a>', '<a class="btn btn-g" href="{R}maintenance-request/" style="margin-top:16px">Report a repair</a>')
# scripts: wizard is gone from home
sa = home.index("<script>", home.index("demo-tag")); sb = home.index("</script>", sa)
home = home[:sa] + "<script>" + COMMON_JS + "</script>" + home[sb + len("</script>"):]
home = home.replace("{R}", "")
io.open("index.html", "w", encoding="utf-8").write(home)
print("built home + %d pages" % count)

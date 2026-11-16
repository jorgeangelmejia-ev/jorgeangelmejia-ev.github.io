# -*- coding: utf-8 -*-
"""Nexustate template library generator.

Renders the scenario tracks (sellers, brokers, investors, past clients) and the
content library (legal, lifestyle, bio, network) into email/<key>-<lang>.html in
the same layout as the Seven Moments set, and merges them into email/index.json.

Run from the repo root:  python3 _build/email_library.py
Facts used here were researched on 2026-11-16; sources are printed in each email.
"""
import html, json, os

BASE = "https://jorgeangelmejia-ev.github.io"
FORM = "https://form.jotform.com/263176099225059"
WA = "https://wa.me/message/A6LXEFOC6VP3D1"
LI = "https://www.linkedin.com/in/jorge1mejia/"
ADDR = "Engel & Völkers Tulum · LT B88, Itzama, Aldea Zama Manzana 26, 77760 Tulum, Q.R., Mexico"
NAME = "Jorge Ángel Mejía"
# Privacy notice of the E&V Tulum shop (controller). Replace with the Mexican aviso de privacidad URL once adopted.
PRIVACY = "https://evtulum.com/terms-and-conditions"
PRIV_LABEL = {"en": "Privacy notice", "es": "Aviso de privacidad"}

FONT = "font-family:Arial,Helvetica,sans-serif;"
P = f'<p style="margin:0 0 16px 0;{FONT}font-size:15px;line-height:24px;color:#333333;">'

REASON = {
    "buyer": {"en": "You are receiving this because you contacted us about property on the Riviera Maya.",
              "es": "Recibe este correo porque nos contactó sobre propiedades en la Riviera Maya."},
    "seller": {"en": "You are receiving this because you contacted us about selling or valuing a property.",
               "es": "Recibe este correo porque nos contactó para vender o valuar una propiedad."},
    "b2b": {"en": "You are receiving this as a real estate professional we have been in contact with.",
            "es": "Recibe este correo como profesional inmobiliario con quien hemos estado en contacto."},
    "client": {"en": "You are receiving this as a client of Engel & Völkers Tulum.",
               "es": "Recibe este correo como cliente de Engel & Völkers Tulum."},
}
UNSUB = {"en": 'Reply "unsubscribe" to stop receiving these emails.',
         "es": 'Responda "baja" para dejar de recibir estos correos.'}
DISCLAIMER = {"en": "General information, not legal or tax advice. Rules change; your notary and accountant confirm what applies to your case.",
              "es": "Información general, no constituye asesoría legal ni fiscal. Las reglas cambian; su notario y su contador confirman lo que aplica a su caso."}
SIGN = {"en": f"{NAME} · Sales Manager", "es": f"{NAME} · Gerente de Ventas"}


def e(s):
    return html.escape(s, quote=False)


def render(t, lang):
    c = t[lang]
    img = t.get("img")
    rows = []
    rows.append(f'<tr><td style="padding:28px 40px 0 40px;{FONT}font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#666666;">{e(NAME)} &nbsp;·&nbsp; Tulum, Riviera Maya</td></tr>')
    rows.append('<tr><td style="padding:14px 40px 0 40px;"><div style="height:1px;line-height:1px;background:#E60000;font-size:1px;">&nbsp;</div></td></tr>')
    rows.append(f'<tr><td style="padding:28px 40px 0 40px;{FONT}font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#999999;">{e(c["kicker"])}</td></tr>')
    rows.append(f'<tr><td style="padding:8px 40px 24px 40px;font-family:Georgia,\'Times New Roman\',serif;font-size:28px;line-height:34px;color:#1a1a1a;">{e(c["headline"])}</td></tr>')
    if img:
        slug, n, cap = img
        href = f"{BASE}/properties/{slug}/index.html"
        rows.append(f'<tr><td style="padding:0;"><a href="{href}" target="_blank"><img src="{BASE}/img/{slug}-{n}.jpg" width="600" alt="{e(cap)}" style="display:block;width:100%;max-width:600px;height:auto;border:0;"></a></td></tr>')
        rows.append(f'<tr><td style="padding:8px 40px 0 40px;{FONT}font-size:12px;color:#888888;font-style:italic;">{e(cap)}</td></tr>')
    greet = c.get("greet", "Dear #lead_first_name#," if lang == "en" else "Estimado/a #lead_first_name#:")
    body = P + e(greet) + "</p>" + "".join(P + p + "</p>" for p in c["paras"])
    if c.get("list"):
        body += f'<ul style="margin:0 0 16px 18px;padding:0;{FONT}font-size:15px;line-height:24px;color:#333333;">' + "".join(f'<li style="margin:0 0 8px 0;">{li}</li>' for li in c["list"]) + "</ul>"
    if c.get("after"):
        body += "".join(P + p + "</p>" for p in c["after"])
    rows.append(f'<tr><td style="padding:24px 40px 8px 40px;">{body}</td></tr>')
    cta_label, cta_url = c["cta"]
    rows.append(f'<tr><td style="padding:0 40px 12px 40px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="background:#1a1a1a;"><a href="{cta_url}" target="_blank" style="display:inline-block;padding:14px 26px;{FONT}font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#ffffff;text-decoration:none;">{e(cta_label)}</a></td></tr></table></td></tr>')
    l2 = c.get("link2", ("Ask a question on WhatsApp" if lang == "en" else "Escríbame por WhatsApp", WA))
    rows.append(f'<tr><td style="padding:0 40px 28px 40px;{FONT}font-size:14px;"><a href="{l2[1]}" target="_blank" style="color:#1a1a1a;text-decoration:underline;">{e(l2[0])}</a></td></tr>')
    if c.get("read"):
        rows.append(f'<tr><td style="padding:0 40px 28px 40px;{FONT}font-size:14px;color:#333333;">→ <a href="{c["read"][1]}" target="_blank" style="color:#1a1a1a;">{e(c["read"][0])}</a></td></tr>')
    rows.append('<tr><td style="padding:0 40px;"><div style="height:1px;line-height:1px;background:#dddddd;font-size:1px;">&nbsp;</div></td></tr>')
    rows.append(f'<tr><td style="padding:20px 40px 4px 40px;font-family:Georgia,\'Times New Roman\',serif;font-size:16px;color:#1a1a1a;">{e(SIGN[lang])}</td></tr>')
    rows.append(f'<tr><td style="padding:0 40px 20px 40px;{FONT}font-size:13px;line-height:20px;color:#555555;"><a href="{WA}" style="color:#555555;">WhatsApp</a> &nbsp;·&nbsp; <a href="{BASE}" style="color:#555555;">jorgeangelmejia-ev.github.io</a> &nbsp;·&nbsp; <a href="{LI}" style="color:#555555;">LinkedIn</a></td></tr>')
    foot = e(ADDR) + "<br>" + ("Each Engel & Völkers shop is independently owned and operated." if lang == "en" else "Cada oficina Engel & Völkers es de propiedad y operación independiente.")
    if t.get("sources"):
        foot += "<br>" + ("Sources: " if lang == "en" else "Fuentes: ") + " · ".join(f'<a href="{u}" style="color:#888888;">{e(n)}</a>' for n, u in t["sources"])
    if t.get("legal"):
        foot += "<br>" + e(DISCLAIMER[lang])
    foot += f'<br>{PRIV_LABEL[lang]}: <a href="{PRIVACY}" style="color:#888888;">{PRIVACY.split("//")[1]}</a>'
    foot += "<br>" + e(REASON[t["audience"]][lang]) + " " + e(UNSUB[lang])
    rows.append(f'<tr><td style="padding:16px 40px 28px 40px;background:#fafafa;{FONT}font-size:11px;line-height:17px;color:#888888;">{foot}</td></tr>')
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(c["subject"])}</title></head>\n'
            f'<body style="margin:0;padding:0;background:#f4f4f4;">\n'
            f'<div style="display:none;max-height:0;overflow:hidden;font-size:1px;color:#f4f4f4;">{e(c["pre"])}</div>\n'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f4f4f4;"><tr><td align="center" style="padding:24px 12px;">\n'
            '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#ffffff;">\n'
            + "\n".join(rows) + "\n</table></td></tr></table></body></html>\n")


# ---------------------------------------------------------------- sources
S_EV = ("Engel & Völkers, About us (2026)", "https://www.engelvoelkers.com/es/en/company/about-us")
S_GG = ("GG Media Kit", "https://a.storyblok.com/f/209096/x/1c9692fbbc/gg-mediakit_2027_eng.pdf")
S_LISR160 = ("LISR Art. 160", "https://mley.mx/LISR/articulo/160/")
S_LISR158 = ("LISR Art. 158", "https://mley.mx/LISR/articulo/158/")
S_GAIN = ("El Imparcial / SAT, May 2026", "https://www.elimparcial.com/dinero/2026/05/09/sat-explica-cuando-debes-pagar-isr-por-vender-una-casa-en-mexico-y-en-que-casos-puedes-evitar-legalmente-el-impuesto/")
S_EXEMPT = ("IDC, Nov 2025", "https://idconline.mx/fiscal-contable/2025/11/24/residencia-fiscal-en-mexico-en-venta-de-casa-por-extranjeros")
S_SRE = ("SRE, permits and fees", "https://portales.sre.gob.mx/tramites-dgaj/art-27-constitucional/costos-y-tiempos")
S_BBVA = ("BBVA, fideicomiso", "https://www.bbva.mx/educacion-financiera/banca-digital/fideicomiso-para-extranjeros.html")
S_ISAI = ("Ley de Hacienda del Municipio de Tulum, Art. 50", "https://documentos.congresoqroo.gob.mx/leyes/L276-XVIII-20241209-L1820241209048-Ley-de-Hacienda-del-Mpio-de-Tulum.pdf")
S_HOSP = ("Ley del Impuesto al Hospedaje Q. Roo, Art. 8", "https://agqroo.qroo.gob.mx/wp-content/uploads/2026/01/1767992043_2_641.pdf")
S_INAH = ("INAH, 2025", "https://inah.gob.mx/images/boletines/2025/81/Boletin%2081.pdf")
S_UNESCO = ("UNESCO, Sian Ka'an", "https://whc.unesco.org/en/list/410/documents")

R_SELL = ("Read: Selling property in Tulum", f"{BASE}/insights/selling-property-in-tulum/index.html")
R_SELL_ES = ("Lea: Vender una propiedad en Tulum (en inglés)", f"{BASE}/insights/selling-property-in-tulum/index.html")
R_Q3 = ("Read: Tulum Q3 2026 intelligence report", f"{BASE}/insights/tulum-q3-2026-intelligence-report/index.html")
R_Q3_ES = ("Lea: Reporte de inteligencia Tulum T3 2026 (en inglés)", f"{BASE}/insights/tulum-q3-2026-intelligence-report/index.html")
R_MONEY = ("Read: Moving money to Mexico for a property purchase", f"{BASE}/insights/moving-money-to-mexico-for-a-property-purchase/index.html")
R_MONEY_ES = ("Lea: Cómo mover su dinero a México para comprar (en inglés)", f"{BASE}/insights/moving-money-to-mexico-for-a-property-purchase/index.html")
R_ADV = ("Read: What to expect from an advisor in Tulum", f"{BASE}/insights/what-to-expect-from-a-real-estate-advisor-in-tulum/index.html")
R_ADV_ES = ("Lea: Qué esperar de un asesor en Tulum (en inglés)", f"{BASE}/insights/what-to-expect-from-a-real-estate-advisor-in-tulum/index.html")
R_RIT = ("Read: Five rituals, one coast", f"{BASE}/insights/five-rituals-one-coast/index.html")
R_RIT_ES = ("Lea: Cinco rituales, una costa (en inglés)", f"{BASE}/insights/five-rituals-one-coast/index.html")
PROPS = (f"{BASE}/index.html#properties")

WA_EN = ("Message me on WhatsApp", WA)
WA_ES = ("Escríbame por WhatsApp", WA)

T = []

# ================================================================ SELLERS
T.append(dict(key="S0", track="Seller", audience="seller", day=0, img=("villa-hunab-ku", 1, "Villa Hunab Ku, Aldea Zamá"),
  en=dict(name="Seller 0 · Welcome", subject="#lead_first_name#, about your property: what happens next",
          pre="A clear valuation first, a decision later, no obligation.", kicker="Welcome", headline="A valuation first, a decision later",
          paras=["Thank you for reaching out about your property. Before anyone talks about listing, you deserve a clear view of what it is worth today and why.",
                 "Here is how I work: a short conversation about the home and your plans, a comparative market analysis built on closed and asking prices in your area, and an honest recommendation, including when the right answer is to wait.",
                 "Over the next weeks I will send a few short notes: how we price, how Engel & Völkers markets a home internationally, what the tax and notary side looks like, and how to prepare. Reply to any of them and I will answer personally."],
          cta=("Request your valuation", WA), link2=("Or reply to this email with the address", "mailto:jorge.mejia@engelvoelkers.com")),
  es=dict(name="Vendedor 0 · Bienvenida", subject="#lead_first_name#, sobre su propiedad: lo que sigue",
          pre="Primero una valuación clara, después una decisión, sin compromiso.", kicker="Bienvenida", headline="Primero la valuación, después la decisión",
          paras=["Gracias por escribirnos sobre su propiedad. Antes de hablar de ponerla en venta, usted merece una visión clara de cuánto vale hoy y por qué.",
                 "Así trabajo: una conversación breve sobre la propiedad y sus planes, un análisis comparativo de mercado con precios de cierre y de oferta en su zona, y una recomendación honesta, incluso cuando lo correcto es esperar.",
                 "En las próximas semanas le enviaré algunas notas breves: cómo fijamos el precio, cómo Engel & Völkers promueve una propiedad a nivel internacional, el lado fiscal y notarial, y cómo prepararse. Puede responder a cualquiera y le contestaré personalmente."],
          cta=("Solicite su valuación", WA), link2=("O responda a este correo con la dirección", "mailto:jorge.mejia@engelvoelkers.com"))))

T.append(dict(key="S1", track="Seller", audience="seller", day=2, img=("casa-mila", 1, "Casa Mila, Tulum"),
  en=dict(name="Seller 1 · Pricing", subject="How a Tulum home is priced, honestly",
          pre="Closed prices, asking prices and the gap between them.", kicker="Pricing", headline="The price the market will pay",
          paras=["In Tulum the asking prices you see online and the prices homes actually close at can be far apart. A price set from listings alone tends to sit on the market, and a home that sits loses negotiating power.",
                 "My comparative market analysis separates the two: documented closings where available, current competition at your price point, price per square metre for comparable construction, and how long similar homes have taken to sell.",
                 "You will see the evidence behind every number, and you decide the strategy."],
          cta=("Request your valuation", WA), read=R_SELL),
  es=dict(name="Vendedor 1 · Precio", subject="Cómo se fija el precio de una casa en Tulum, con honestidad",
          pre="Precios de cierre, precios de oferta y la distancia entre ambos.", kicker="Precio", headline="El precio que el mercado sí paga",
          paras=["En Tulum los precios de oferta que se ven en internet y los precios a los que realmente se cierran las operaciones pueden estar muy lejos. Un precio fijado solo con anuncios suele quedarse en el mercado, y una propiedad que se queda pierde poder de negociación.",
                 "Mi análisis comparativo separa ambos: cierres documentados cuando existen, la competencia actual en su rango de precio, el precio por metro cuadrado de construcciones comparables y el tiempo que han tardado en venderse propiedades similares.",
                 "Usted verá la evidencia detrás de cada cifra y decidirá la estrategia."],
          cta=("Solicite su valuación", WA), read=R_SELL_ES)))

T.append(dict(key="S2", track="Seller", audience="seller", day=5, img=("casa-carolina", 1, "Casa Carolina, Tulum"), sources=[S_EV, S_GG],
  en=dict(name="Seller 2 · Global reach", subject="Who will see your home, and where",
          pre="One local advisor, an international network behind the listing.", kicker="Reach", headline="Your buyer may not live in Mexico",
          paras=["Most buyers of homes like yours in Tulum come from abroad, so the question is not only how a listing looks, but who sees it and who brings them."],
          list=["Engel & Völkers reports more than 1,100 locations in over 35 countries on five continents, founded in Hamburg in 1977.",
                "GG, the brand's lifestyle magazine, is published in several language editions and reports roughly one million readers per edition.",
                "Advisors across the network refer qualified buyers to the local shop, and Private Office supports discreet, high-value sales."],
          after=["I combine that reach with local work: professional photography, a dedicated property page, and direct introductions to partner shops in the markets your buyer is most likely to come from."],
          cta=("Talk through a marketing plan", WA)),
  es=dict(name="Vendedor 2 · Alcance global", subject="Quién verá su propiedad, y desde dónde",
          pre="Un asesor local con una red internacional detrás.", kicker="Alcance", headline="Su comprador quizá no viva en México",
          paras=["La mayoría de los compradores de propiedades como la suya en Tulum vienen del extranjero; por eso la pregunta no es solo cómo se ve un anuncio, sino quién lo ve y quién lo trae."],
          list=["Engel & Völkers reporta más de 1,100 ubicaciones en más de 35 países de cinco continentes; fue fundada en Hamburgo en 1977.",
                "GG, la revista de estilo de vida de la marca, se publica en varias ediciones de idioma y reporta alrededor de un millón de lectores por edición.",
                "Asesores de toda la red refieren compradores calificados a la oficina local, y Private Office apoya ventas discretas de alto valor."],
          after=["Combino ese alcance con trabajo local: fotografía profesional, una página dedicada a la propiedad y presentaciones directas a oficinas aliadas en los mercados de donde probablemente venga su comprador."],
          cta=("Hablemos de un plan de comercialización", WA))))

T.append(dict(key="S3", track="Seller", audience="seller", day=9, img=None, legal=True, sources=[S_LISR160, S_GAIN, S_EXEMPT],
  en=dict(name="Seller 3 · Tax and notary", subject="What the notary will calculate when you sell",
          pre="Capital gains tax in Mexico, in plain terms.", kicker="Legal", headline="The tax side of selling, before you sign",
          paras=["In Mexico every property sale is formalised before a notary, and the notary calculates, withholds and pays the seller's income tax on the sale. Knowing the rules early avoids surprises at closing."],
          list=["Non-resident sellers: by default 25% of the gross sale price, with no deductions; alternatively, the tax can be calculated on the net gain at the top rate (currently 35%) when the requirements are met, and the notary applies it.",
                "Mexican tax residents: tax is on the gain, after deducting the updated purchase cost, documented improvements, notary fees, appraisals and documented commissions.",
                "Primary-home exemption: up to 700,000 UDIs, once every three years, for residents who prove the home is their residence. Foreign owners qualify only as Mexican tax residents, with a fiscal address, RFC or CURP and proof of tax residence."],
          after=["Gathering invoices for improvements and your original purchase documents now can make a real difference. I work with notaries in Tulum and can introduce you before you commit to a price."],
          cta=("Ask me about your case", WA)),
  es=dict(name="Vendedor 3 · Impuestos y notaría", subject="Lo que el notario calculará cuando venda",
          pre="El ISR por enajenación en México, en términos claros.", kicker="Legal", headline="El lado fiscal de vender, antes de firmar",
          paras=["En México toda compraventa se formaliza ante notario, y el notario calcula, retiene y entera el impuesto sobre la renta del vendedor. Conocer las reglas desde el inicio evita sorpresas al cierre."],
          list=["Vendedores no residentes: por defecto 25% sobre el precio total de venta, sin deducciones; alternativamente, el impuesto puede calcularse sobre la ganancia neta a la tasa máxima (actualmente 35%) si se cumplen los requisitos, y el notario lo aplica.",
                "Residentes fiscales en México: el impuesto es sobre la ganancia, tras deducir el costo de adquisición actualizado, mejoras comprobadas, honorarios notariales, avalúos y comisiones documentadas.",
                "Exención por casa habitación: hasta 700,000 UDIs, una vez cada tres años, para residentes que acrediten que es su domicilio. Los propietarios extranjeros califican solo como residentes fiscales en México, con domicilio fiscal, RFC o CURP y constancia de residencia fiscal."],
          after=["Reunir desde ahora las facturas de mejoras y los documentos de su compra original puede hacer una diferencia real. Trabajo con notarios en Tulum y puedo presentarle a uno antes de que fije un precio."],
          cta=("Consúlteme su caso", WA))))

T.append(dict(key="S4", track="Seller", audience="seller", day=14, img=("casa-escocesa", 3, "Casa Escocesa, Tulum"),
  en=dict(name="Seller 4 · Preparation", subject="Preparing your home, and your paperwork",
          pre="What buyers and notaries will ask for, ready in advance.", kicker="Preparation", headline="Ready before the first viewing",
          paras=["Well-prepared sales close faster and with fewer renegotiations. Two things matter: how the home presents, and how quickly you can answer a serious buyer's due diligence."],
          list=["Your deed (escritura) or, if you own through a bank trust, the trust documents.",
                "Current property-tax (predial) and water receipts, and recent condominium or HOA statements where applicable.",
                "Plans, permits and invoices for improvements, which also matter for your tax calculation.",
                "Small repairs, a deep clean and good light before photography; buyers abroad decide from images first."],
          after=["Your notary will confirm the final list for your property. I can review what you have and tell you what is missing."],
          cta=("Review my documents with Jorge", WA)),
  es=dict(name="Vendedor 4 · Preparación", subject="Preparar su propiedad, y sus documentos",
          pre="Lo que compradores y notarios pedirán, listo de antemano.", kicker="Preparación", headline="Lista antes de la primera visita",
          paras=["Las ventas bien preparadas cierran más rápido y con menos renegociaciones. Importan dos cosas: cómo se presenta la propiedad y qué tan rápido puede responder a la revisión de un comprador serio."],
          list=["Su escritura o, si es propietario a través de un fideicomiso, los documentos del fideicomiso.",
                "Recibos vigentes de predial y agua, y estados de cuenta recientes del condominio o administración cuando aplique.",
                "Planos, permisos y facturas de mejoras, que además cuentan para su cálculo fiscal.",
                "Pequeñas reparaciones, limpieza profunda y buena luz antes de las fotografías; los compradores en el extranjero deciden primero por las imágenes."],
          after=["Su notario confirmará la lista final para su propiedad. Puedo revisar lo que tiene y decirle qué falta."],
          cta=("Revisar mis documentos con Jorge", WA))))

T.append(dict(key="S5", track="Seller", audience="seller", day=21, img=None,
  en=dict(name="Seller 5 · Trust", subject="Whenever you are ready",
          pre="No pressure, and the door stays open.", kicker="Trust", headline="Whenever you are ready",
          paras=["I have lived in Tulum for nearly 20 years and have worked in leisure and hospitality real estate since 2002. What I can offer is a clear view of the market, honest pricing and a network that reaches buyers well beyond Mexico.",
                 "If now is not the moment, that is a perfectly good answer. I am happy to update your valuation whenever the market moves or your plans change."],
          cta=("Schedule a 15-minute call", WA), read=R_ADV),
  es=dict(name="Vendedor 5 · Confianza", subject="Cuando usted esté listo",
          pre="Sin presión, y la puerta sigue abierta.", kicker="Confianza", headline="Cuando usted esté listo",
          paras=["Vivo en Tulum desde hace casi 20 años y trabajo en bienes raíces turísticos y de hospitalidad desde 2002. Lo que puedo ofrecerle es una visión clara del mercado, un precio honesto y una red que llega a compradores mucho más allá de México.",
                 "Si este no es el momento, es una respuesta perfectamente válida. Con gusto actualizo su valuación cuando el mercado se mueva o sus planes cambien."],
          cta=("Agende una llamada de 15 minutos", WA), read=R_ADV_ES)))

# ================================================================ BROKERS / AGENTS (B2B, drafts only)
T.append(dict(key="B0", track="Broker", audience="b2b", day=0, img=("kokoon-villa", 1, "Kokoon Villa, Tulum"),
  en=dict(name="Broker 0 · Introduction", subject="Your clients in Tulum, looked after locally",
          pre="A local partner for buyers and sellers you refer to the Riviera Maya.", kicker="Partners", headline="A local partner in Tulum",
          greet="Dear #lead_first_name#,",
          paras=["When your clients look at Tulum, they need someone on the ground who checks title and permits, knows which developers deliver, and tells them plainly when a project does not fit.",
                 "That is my role at Engel & Völkers Tulum. I work in English and Spanish, alongside colleagues serving Russian- and Polish-speaking buyers, and I keep the referring advisor informed at every step."],
          cta=("Set up a 15-minute call", WA), read=R_Q3),
  es=dict(name="Agente 0 · Presentación", subject="Sus clientes en Tulum, atendidos localmente",
          pre="Un aliado local para compradores y vendedores que refiera a la Riviera Maya.", kicker="Aliados", headline="Un aliado local en Tulum",
          greet="Estimado/a #lead_first_name#:",
          paras=["Cuando sus clientes miran Tulum necesitan a alguien en sitio que revise título y permisos, sepa qué desarrolladores cumplen y les diga con claridad cuando un proyecto no les conviene.",
                 "Ese es mi papel en Engel & Völkers Tulum. Trabajo en español e inglés, junto con colegas que atienden a compradores de habla rusa y polaca, y mantengo informado al asesor que refiere en cada paso."],
          cta=("Agendemos 15 minutos", WA), read=R_Q3_ES)))

T.append(dict(key="B1", track="Broker", audience="b2b", day=4, img=None,
  en=dict(name="Broker 1 · How referrals work", subject="How a referral to Tulum works, step by step",
          pre="Written terms first, regular updates, your client relationship intact.", kicker="Process", headline="How a referral works",
          greet="Dear #lead_first_name#,",
          list=["We agree the referral terms in writing before the introduction.",
                "You introduce the client by email; I respond within one business day.",
                "I handle search, viewings, due diligence and closing coordination with the notary.",
                "You receive an update at each milestone, and the referral fee is paid at closing as agreed."],
          paras=["A clear process protects your client and your relationship with them:"],
          cta=("Agree terms with Jorge", WA)),
  es=dict(name="Agente 1 · Cómo funciona la referencia", subject="Cómo funciona una referencia a Tulum, paso a paso",
          pre="Términos por escrito, actualizaciones constantes y su relación con el cliente intacta.", kicker="Proceso", headline="Cómo funciona una referencia",
          greet="Estimado/a #lead_first_name#:",
          list=["Acordamos por escrito los términos de la referencia antes de la presentación.",
                "Usted presenta al cliente por correo; respondo en un día hábil.",
                "Me encargo de la búsqueda, visitas, revisión legal y coordinación del cierre con el notario.",
                "Usted recibe una actualización en cada etapa, y la comisión de referencia se paga al cierre según lo acordado."],
          paras=["Un proceso claro protege a su cliente y su relación con él:"],
          cta=("Acordar términos con Jorge", WA))))

T.append(dict(key="B2", track="Broker", audience="b2b", day=10, img=("aflora", 1, "Aflora, Tulum"),
  en=dict(name="Broker 2 · Inventory", subject="What we can show your clients this month",
          pre="Current homes, with full details on one page each.", kicker="Inventory", headline="Homes we can show now",
          greet="Dear #lead_first_name#,",
          paras=["Every home we represent has its own page with photographs, specifications and price, so you can share it with a client directly.",
                 "Availability changes, so I confirm each home with the owner or developer before any viewing."],
          cta=("See current homes", PROPS)),
  es=dict(name="Agente 2 · Inventario", subject="Lo que podemos mostrar a sus clientes este mes",
          pre="Propiedades actuales, con detalles completos en una página cada una.", kicker="Inventario", headline="Propiedades que podemos mostrar hoy",
          greet="Estimado/a #lead_first_name#:",
          paras=["Cada propiedad que representamos tiene su propia página con fotografías, especificaciones y precio, para que pueda compartirla con su cliente directamente.",
                 "La disponibilidad cambia, así que confirmo cada propiedad con el propietario o desarrollador antes de cualquier visita."],
          cta=("Ver propiedades actuales", PROPS))))

T.append(dict(key="B3", track="Broker", audience="b2b", day=20, img=None,
  en=dict(name="Broker 3 · Market brief", subject="A short brief on the Tulum market, for your clients",
          pre="Evidence-led, with sources, ready to forward.", kicker="Evidence", headline="A brief you can forward",
          greet="Dear #lead_first_name#,",
          paras=["Clients ask referring advisors about Tulum before they ask anyone else. I publish evidence-led market notes with named sources, written to be forwarded as they are.",
                 "If a client of yours has a specific question, about an area, a developer or the buying process, send it to me and I will answer within a day."],
          cta=("Read the latest market report", R_Q3[1])),
  es=dict(name="Agente 3 · Nota de mercado", subject="Una nota breve sobre el mercado de Tulum, para sus clientes",
          pre="Con evidencia y fuentes, lista para reenviar.", kicker="Evidencia", headline="Una nota que puede reenviar",
          greet="Estimado/a #lead_first_name#:",
          paras=["Los clientes preguntan por Tulum a su asesor de confianza antes que a nadie. Publico notas de mercado con evidencia y fuentes nombradas, escritas para reenviarse tal cual.",
                 "Si algún cliente suyo tiene una pregunta concreta, sobre una zona, un desarrollador o el proceso de compra, envíemela y le responderé en un día."],
          cta=("Leer el reporte más reciente", R_Q3[1]))))

# ================================================================ INVESTORS
T.append(dict(key="INV1", track="Investor", audience="buyer", day=None, img=("arthouse", 1, "Arthouse, Tulum"), legal=True, sources=[S_LISR158, S_HOSP],
  en=dict(name="Investor 1 · Rental rules", subject="Renting out your Tulum home: the rules that apply",
          pre="Taxes and registrations for vacation rentals in Quintana Roo.", kicker="Evidence", headline="Before you count rental income",
          paras=["Rental projections often leave out the obligations that come with renting. In Quintana Roo, owners of vacation rentals should plan for these:"],
          list=["Non-resident owners: income tax of 25% of gross rental income, with no deductions.",
                "Furnished or lodging-type rentals are generally subject to VAT (IVA) at 16%.",
                "State lodging tax: 6% for private houses, apartments and villas rented directly or through platforms.",
                "Registration with the state taxpayer registry (REC) and the state tourism registry for platform-listed rentals."],
          after=["None of this rules out a good investment; it changes the numbers. I can share net-yield scenarios for specific homes, with every assumption visible."],
          cta=("Request a net-yield scenario", WA), read=R_MONEY),
  es=dict(name="Inversionista 1 · Reglas de renta", subject="Rentar su casa en Tulum: las reglas que aplican",
          pre="Impuestos y registros para rentas vacacionales en Quintana Roo.", kicker="Evidencia", headline="Antes de contar el ingreso por renta",
          paras=["Las proyecciones de renta suelen omitir las obligaciones que trae rentar. En Quintana Roo, los propietarios de rentas vacacionales deben considerar:"],
          list=["Propietarios no residentes: ISR de 25% sobre el ingreso bruto por renta, sin deducciones.",
                "Las rentas amuebladas o de tipo hospedaje generalmente causan IVA del 16%.",
                "Impuesto estatal al hospedaje: 6% para casas, departamentos y villas rentados directamente o por plataformas.",
                "Inscripción en el Registro Estatal de Contribuyentes (REC) y en el registro turístico estatal para rentas en plataformas."],
          after=["Nada de esto descarta una buena inversión; cambia los números. Puedo compartirle escenarios de rendimiento neto para propiedades concretas, con cada supuesto a la vista."],
          cta=("Solicitar un escenario de rendimiento neto", WA), read=R_MONEY_ES)))

# ================================================================ CONTENT LIBRARY
T.append(dict(key="L-LEGAL", track="Library", audience="buyer", day=None, img=None, legal=True, sources=[S_SRE, S_BBVA, S_ISAI],
  en=dict(name="Library · Buying in Mexico as a foreigner", subject="Owning near the coast in Mexico, explained",
          pre="The bank trust, the permit, the notary and the acquisition tax.", kicker="Legal", headline="How foreigners own near the coast",
          paras=["Mexico's Constitution reserves direct ownership of land within 50 km of the coast to Mexicans, and Tulum is inside that zone. Foreign buyers own securely through one of two routes:"],
          list=["A bank trust (fideicomiso): the bank holds title on your behalf and you hold the full rights to use, rent, sell and bequeath the home. The initial term is 50 years and is renewable.",
                "A Mexican company, used mainly for non-residential or investment purposes.",
                "The trust needs a permit from the Ministry of Foreign Affairs (SRE), requested by the bank; the 2026 fee is MXN 21,650 and SRE resolves within five business days.",
                "The deed is signed before a notary public, who also verifies title and taxes. In Tulum the acquisition tax (ISAI) is 4% of the property value."],
          after=["Bank trust fees vary by bank and are not published as a fixed tariff, so I ask for current quotes for each purchase."],
          cta=("Ask me about the process", WA)),
  es=dict(name="Biblioteca · Comprar en México siendo extranjero", subject="Ser propietario cerca de la costa en México, explicado",
          pre="El fideicomiso, el permiso, el notario y el impuesto de adquisición.", kicker="Legal", headline="Cómo compran los extranjeros cerca de la costa",
          paras=["La Constitución reserva a los mexicanos la propiedad directa del suelo a menos de 50 km de la costa, y Tulum está dentro de esa zona. Los compradores extranjeros adquieren con seguridad por una de dos vías:"],
          list=["Un fideicomiso bancario: el banco es titular en su nombre y usted conserva todos los derechos de uso, renta, venta y herencia. La duración inicial es de 50 años y es renovable.",
                "Una sociedad mexicana, usada principalmente para fines no residenciales o de inversión.",
                "El fideicomiso requiere un permiso de la Secretaría de Relaciones Exteriores (SRE) que solicita el banco; el derecho en 2026 es de MXN 21,650 y la SRE resuelve en cinco días hábiles.",
                "La escritura se firma ante notario público, que además verifica título e impuestos. En Tulum el impuesto sobre adquisición de inmuebles (ISAI) es del 4% del valor."],
          after=["Las comisiones del fideicomiso varían por banco y no se publican como tarifa fija, por eso pido cotizaciones vigentes para cada compra."],
          cta=("Consúlteme el proceso", WA))))

T.append(dict(key="L-LIFE", track="Library", audience="buyer", day=None, img=("villa-coco", 1, "Villa Coco, Riviera Maya"), sources=[S_INAH, S_UNESCO],
  en=dict(name="Library · Living in Tulum", subject="Tulum today: getting here, and what surrounds you",
          pre="A new airport, the train, a national park and a biosphere reserve.", kicker="Lifestyle", headline="Closer than it used to be",
          paras=["Tulum has changed a great deal in a few years, and much of that change is about access and protected nature:"],
          list=["Tulum's international airport opened in December 2023, and the Tren Maya station in Tulum opened in 2024.",
                "Cancún is about 130 km away, roughly 1.5 to 2 hours by car.",
                "The Mayan site of Tulum sits inside the Parque del Jaguar, a protected park of 2,913 hectares on the coast.",
                "To the south, Sian Ka'an, a UNESCO World Heritage Site since 1987."],
          after=["Mornings on the beach, cenotes inland, long lunches in town: if you tell me how you like to spend a day, I will tell you which areas fit."],
          cta=("Tell me how you like to live", WA), read=R_RIT),
  es=dict(name="Biblioteca · Vivir en Tulum", subject="Tulum hoy: cómo llegar y qué le rodea",
          pre="Un aeropuerto nuevo, el tren, un parque nacional y una reserva de la biosfera.", kicker="Estilo de vida", headline="Más cerca que antes",
          paras=["Tulum ha cambiado mucho en pocos años, y gran parte de ese cambio tiene que ver con el acceso y la naturaleza protegida:"],
          list=["El aeropuerto internacional de Tulum abrió en diciembre de 2023, y la estación del Tren Maya en Tulum en 2024.",
                "Cancún está a unos 130 km, aproximadamente 1.5 a 2 horas en auto.",
                "La zona arqueológica de Tulum se encuentra dentro del Parque del Jaguar, un área protegida de 2,913 hectáreas frente al mar.",
                "Al sur, Sian Ka'an, Patrimonio de la Humanidad por la UNESCO desde 1987."],
          after=["Mañanas en la playa, cenotes tierra adentro, comidas largas en el pueblo: si me cuenta cómo le gusta pasar el día, le diré qué zonas le convienen."],
          cta=("Cuénteme cómo le gusta vivir", WA), read=R_RIT_ES)))

T.append(dict(key="L-BIO", track="Library", audience="buyer", day=None, img=None,
  en=dict(name="Library · Advisor bio (Jorge)", subject="A little about who you are speaking with",
          pre="Nearly 20 years in Tulum, and why that matters to you.", kicker="Your advisor", headline="Who you are speaking with",
          paras=["I am Jorge Ángel Mejía, Sales Manager at Engel & Völkers Tulum. I left Mexico City for Tulum almost 20 years ago, after a career in hospitality, leisure and marketing.",
                 "I have worked in leisure and hospitality real estate since 2002, with consulting experience in the United States, Canada, Southeast Asia, Ireland, Uruguay and Mexico. My focus is Tulum, the Riviera Maya and Cancún: branded residences, market analysis and valuations.",
                 "Our team also includes colleagues who advise Russian- and Polish-speaking buyers in their own language."],
          cta=("Schedule a 15-minute call", FORM), read=R_ADV),
  es=dict(name="Biblioteca · Perfil del asesor (Jorge)", subject="Un poco sobre quién le atiende",
          pre="Casi 20 años en Tulum, y por qué eso le importa.", kicker="Su asesor", headline="Quién le atiende",
          paras=["Soy Jorge Ángel Mejía, Gerente de Ventas en Engel & Völkers Tulum. Dejé la Ciudad de México por Tulum hace casi 20 años, después de una carrera en hospitalidad, turismo y marketing.",
                 "Trabajo en bienes raíces turísticos y de hospitalidad desde 2002, con experiencia de consultoría en Estados Unidos, Canadá, el Sudeste Asiático, Irlanda, Uruguay y México. Me especializo en Tulum, la Riviera Maya y Cancún: residencias de marca, análisis de mercado y valuaciones.",
                 "Nuestro equipo incluye también colegas que asesoran en su propio idioma a compradores de habla rusa y polaca."],
          cta=("Agende una llamada de 15 minutos", FORM), read=R_ADV_ES)))

T.append(dict(key="L-NETWORK", track="Library", audience="buyer", day=None, img=("miraluna-ph-335", 1, "Miraluna PH 335, Tulum"), sources=[S_EV, S_GG],
  en=dict(name="Library · The Engel & Völkers network", subject="What the Engel & Völkers network means for you",
          pre="A local advisor, a network on five continents.", kicker="Network", headline="One advisor, a network behind it",
          paras=["Buying abroad is easier when the firm on the ground is also present where you live."],
          list=["Engel & Völkers was founded in Hamburg in 1977 and reports more than 1,100 locations in over 35 countries.",
                "If you also own or plan to sell a home elsewhere, I can introduce you to a colleague in that market.",
                "Private Office offers discreet, tailored advice for high-value purchases across the network.",
                "Each shop is independently owned and operated, and works to the same brand standards."],
          after=["In Tulum, that means local knowledge with an international standard of service."],
          cta=("Speak with Jorge", FORM)),
  es=dict(name="Biblioteca · La red Engel & Völkers", subject="Lo que la red Engel & Völkers significa para usted",
          pre="Un asesor local, una red en cinco continentes.", kicker="Red", headline="Un asesor, y una red detrás",
          paras=["Comprar en el extranjero es más sencillo cuando la firma local también está presente donde usted vive."],
          list=["Engel & Völkers fue fundada en Hamburgo en 1977 y reporta más de 1,100 ubicaciones en más de 35 países.",
                "Si también tiene o planea vender una propiedad en otro lugar, puedo presentarle a un colega en ese mercado.",
                "Private Office ofrece asesoría discreta y a la medida para compras de alto valor en toda la red.",
                "Cada oficina es de propiedad y operación independiente, y trabaja con los mismos estándares de marca."],
          after=["En Tulum, eso significa conocimiento local con un estándar de servicio internacional."],
          cta=("Hable con Jorge", FORM))))

# ================================================================ PAST CLIENTS / SPHERE
T.append(dict(key="P1", track="Past client", audience="client", day=None, img=None,
  en=dict(name="Past client 1 · Home anniversary", subject="A year in your home, #lead_first_name#",
          pre="A short check-in, and an updated value if you would like one.", kicker="Anniversary", headline="A year in your home",
          paras=["It has been a year since you received your keys, and I hope the home is everything you wanted.",
                 "If it would help, I can prepare an updated market value, recommend trusted local services, or answer anything about rentals, maintenance or the trust. No reason needed, just reply."],
          cta=("Request an updated value", WA)),
  es=dict(name="Cliente 1 · Aniversario", subject="Un año en su casa, #lead_first_name#",
          pre="Un saludo breve, y un valor actualizado si lo desea.", kicker="Aniversario", headline="Un año en su casa",
          paras=["Hace un año recibió sus llaves y espero que la casa sea todo lo que buscaba.",
                 "Si le es útil, puedo preparar un valor de mercado actualizado, recomendarle servicios locales de confianza o resolver cualquier duda sobre rentas, mantenimiento o el fideicomiso. No necesita motivo, solo responda."],
          cta=("Solicitar un valor actualizado", WA))))

T.append(dict(key="P2", track="Past client", audience="client", day=None, img=None,
  en=dict(name="Past client 2 · Referral thanks", subject="Thank you for the introduction",
          pre="Your trust, passed on, is the best compliment.", kicker="Thank you", headline="Thank you for the introduction",
          paras=["Thank you for introducing someone you know. I will look after them with the same care you received, and I will keep you posted only as much as they are comfortable with.",
                 "If there is ever anything I can do for you in Tulum, you know where to find me."],
          cta=("Message Jorge", WA)),
  es=dict(name="Cliente 2 · Gracias por la referencia", subject="Gracias por la recomendación",
          pre="Su confianza, compartida, es el mejor cumplido.", kicker="Gracias", headline="Gracias por la recomendación",
          paras=["Gracias por presentarme a alguien de su confianza. Le atenderé con el mismo cuidado que usted recibió, y le mantendré al tanto solo en la medida en que esa persona lo desee.",
                 "Si alguna vez puedo ayudarle en algo en Tulum, ya sabe dónde encontrarme."],
          cta=("Escribir a Jorge", WA))))


def add_privacy_to_existing(out):
    """Insert the privacy-notice line into the approved Buyer templates (footer only, text unchanged)."""
    n = 0
    for fn in sorted(os.listdir(out)):
        if not fn.endswith(".html"):
            continue
        path = os.path.join(out, fn)
        h = open(path, encoding="utf-8").read()
        if PRIVACY in h:
            continue
        for lang, marker in (("en", "<br>You are receiving"), ("es", "<br>Recibe este correo")):
            if marker in h:
                link = f'<br>{PRIV_LABEL[lang]}: <a href="{PRIVACY}" style="color:#888888;">{PRIVACY.split("//")[1]}</a>'
                h = h.replace(marker, link + marker, 1)
                open(path, "w", encoding="utf-8").write(h)
                n += 1
                break
    return n


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "email")
    idx_path = os.path.join(out, "index.json")
    index = json.load(open(idx_path, encoding="utf-8"))
    keep = [r for r in index if r.get("track") in (None, "Buyer")]
    for r in keep:
        r.setdefault("track", "Buyer"); r.setdefault("status", "approved")
    new = []
    for t in T:
        for lang in ("en", "es"):
            c = t[lang]
            fn = f'{t["key"].lower()}-{lang}.html'
            open(os.path.join(out, fn), "w", encoding="utf-8").write(render(t, lang))
            new.append({"file": fn, "lang": lang, "key": t["key"], "track": t["track"], "name": c["name"] + f" ({lang.upper()})",
                        "subject": c["subject"], "pre": c["pre"], "day": t["day"],
                        "status": "draft - pending Jorge's approval", "sources": [u for _, u in t.get("sources", [])]})
    json.dump(keep + new, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(new)} templates written; index has {len(keep) + len(new)} entries")
    print(f"privacy line added to {add_privacy_to_existing(out)} existing templates")


if __name__ == "__main__":
    main()

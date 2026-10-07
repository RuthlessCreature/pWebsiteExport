#!/usr/bin/env python3
"""Build the Pomerol flagship sourcing-agent page in the five published locales."""

from __future__ import annotations

import html
import re
from pathlib import Path

import build_seo as seo
import build_guides_i18n as guides


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BASE = seo.BASE
EN_ROUTE = "/china-sourcing-agent/"
LOCALES = {
    "zh": {"hreflang": "zh-CN", "language": "zh-CN", "name": "简体中文", "home": "/zh/", "services": "/zh/services/", "contact": "/zh/contact/", "cases": "/zh/cases/"},
    "ja": {"hreflang": "ja", "language": "ja", "name": "日本語", "home": "/ja/", "services": "/ja/services/", "contact": "/ja/contact/", "cases": "/ja/cases/"},
    "ru": {"hreflang": "ru", "language": "ru", "name": "Русский", "home": "/ru/", "services": "/ru/services/", "contact": "/ru/contact/", "cases": "/ru/cases/"},
    "es": {"hreflang": "es", "language": "es", "name": "Español", "home": "/es/", "services": "/es/services/", "contact": "/es/contact/", "cases": "/es/cases/"},
    "pt": {"hreflang": "pt", "language": "pt", "name": "Português", "home": "/pt/", "services": "/pt/services/", "contact": "/pt/contact/", "cases": "/pt/cases/"},
}

PAGES = {
    "zh": {
        "title": "中国采购代理｜面向海外买家的供应商开发与采购执行｜Pomerol",
        "description": "珠海 Pomerol 为海外买家提供中国采购代理服务：梳理需求、筛选供应商、标准化 RFQ、跟进样品、规划质量节点并协调集货与出口。",
        "eyebrow": "中国采购代理",
        "h1": "面向海外买家的中国采购代理：从找厂到交付准备",
        "intro": "Pomerol International 位于广东珠海，为海外采购方提供中国侧的供应商寻源与执行协调。我们把产品要求整理成可比的采购简报，按技术与商业条件筛选工厂，跟进询价与样品，并明确质量检查和发运准备中的责任节点。",
        "problem_title": "找到供应商只是第一个控制点。",
        "problem": "真正的采购偏差往往发生在后续环节：报价口径不同、样品未按图纸更新、包装未经确认就变更、生产节点延迟，或多家工厂交付的文件无法对应。我们通过记录假设、版本和责任，帮助买方在下单前看清这些差异。",
        "buyers": "适合进口商、经销商、工程公司、自有品牌团队和项目承包商，尤其是需要从多个中国产业带采购，或需要一个中国本地协调窗口的买方。",
        "scope_title": "可按项目约定的工作范围",
        "scope": ["梳理产品要求并形成寻源简报", "按制造工艺和技术匹配度开发供应商短名单", "统一 RFQ 条件并整理可比报价矩阵", "协调样品、修订意见和量产前确认", "核对供应商资料并规划质量检查节点", "协调多供应商集货及出口交接准备"],
        "workflow_title": "从需求到发运准备的六个步骤",
        "workflow": ["明确产品规格、版本、数量和验收条件", "按工艺能力、产品匹配度寻找候选供应商", "统一报价中的 MOQ、模具、包装、付款和交期假设", "记录样品版本、测试资料和待关闭偏差", "按风险设定过程、出货前或第三方检查节点", "核对数量、包装、文件和货代交接要求"],
        "disclaimer": "页面中的采购场景用于解释流程和控制方法，不代表已完成的客户项目、实际出货、业绩或客户背书。供应商与工厂属于第三方；核查和协调不构成对质量、合规或交期结果的保证。",
        "contact": "提交采购需求 →", "cases": "浏览采购场景", "switch": "选择页面语言", "service_card_title": "中国采购代理：供应商寻源与执行协调", "service_card_desc": "了解需求简报、供应商比选、RFQ 标准化、样品跟进、质量节点和出口交接如何组成一个可追踪流程。", "card_link": "查看采购代理服务 →", "brand_sub": "中国采购与供应链执行", "nav_services": "服务", "nav_cases": "案例", "nav_about": "关于", "nav_resources": "资源", "nav_contact": "提交需求"},
    "ja": {
        "title": "中国調達代行｜海外バイヤー向けの仕入先開拓・購買支援｜Pomerol",
        "description": "広東省珠海のPomerol Internationalが、要件整理、仕入先選定、RFQ比較、サンプル調整、品質確認の計画、複数社の集約と輸出準備を支援します。",
        "eyebrow": "中国調達代行",
        "h1": "海外バイヤーのための中国調達代行。工場探しから出荷準備まで。",
        "intro": "Pomerol Internationalは広東省珠海を拠点に、海外バイヤー向けの中国側調達と実行調整を行います。製品要件を比較可能な調達ブリーフにまとめ、技術面と商務面から候補先を絞り、見積もりとサンプルの進行、品質確認および出荷準備の責任範囲を整理します。",
        "problem_title": "仕入先探しは、最初の管理ポイントにすぎません。",
        "problem": "見積条件の違い、図面と合わないサンプル、未承認の包装変更、生産日程の遅れ、複数工場から届く書類の不整合など、調達のずれは選定後に起こりがちです。前提、版数、担当範囲を記録し、発注前に差異を確認できるよう支援します。",
        "buyers": "輸入業者、販売代理店、エンジニアリング会社、プライベートブランド事業者、プロジェクト請負会社に適しています。複数の中国製造集積地から調達する場合や、中国側の連絡窓口が必要な場合にご利用いただけます。",
        "scope_title": "案件に応じて合意する支援範囲",
        "scope": ["製品要件を整理し、調達ブリーフを作成", "製造工程と技術適合性に基づく候補先の選定", "RFQ条件の統一と比較可能な見積表の作成", "サンプル、修正内容、量産前確認の調整", "仕入先資料の確認と品質チェック計画", "複数社の集約と輸出引渡し準備の調整"],
        "workflow_title": "要件整理から出荷準備までの6ステップ",
        "workflow": ["仕様、版数、数量、受入基準を明確化", "工程能力と製品適合性から候補を探す", "MOQ、金型、包装、支払、納期の条件を統一", "サンプル版数、試験資料、未解決事項を記録", "リスクに応じた工程・出荷前・第三者検査を計画", "数量、包装、書類、フォワーダー引渡しを確認"],
        "disclaimer": "掲載する調達シナリオは工程や管理方法を説明するための例示であり、完了した顧客案件、実出荷、実績または顧客推薦を示すものではありません。仕入先と工場は第三者です。確認や調整によって品質、法令適合性、納期を保証するものではありません。",
        "contact": "調達要件を送る →", "cases": "調達シナリオを見る", "switch": "表示言語を選択", "service_card_title": "中国調達代行：仕入先開拓と購買実行", "service_card_desc": "要件整理、仕入先比較、RFQの標準化、サンプル管理、品質確認、輸出引渡しを一つの追跡可能な流れでご案内します。", "card_link": "中国調達代行を見る →", "brand_sub": "中国調達・購買実行", "nav_services": "サービス", "nav_cases": "事例", "nav_about": "会社情報", "nav_resources": "資料", "nav_contact": "RFQを開始"},
    "ru": {
        "title": "Агент по закупкам в Китае для зарубежных покупателей | Pomerol",
        "description": "Pomerol International из Чжухая помогает зарубежным покупателям с требованиями, поиском поставщиков, сравнением RFQ, образцами, планом контроля качества и подготовкой экспорта.",
        "eyebrow": "Агент по закупкам в Китае",
        "h1": "Закупочный представитель в Китае: от поиска фабрики до подготовки отправки",
        "intro": "Pomerol International работает в Чжухае, провинция Гуандун, и координирует закупки на стороне Китая для зарубежных покупателей. Мы превращаем требования к товару в сопоставимое закупочное задание, отбираем поставщиков по техническим и коммерческим критериям, сопровождаем запросы цен и образцы, а также согласуем контрольные точки качества и подготовки отгрузки.",
        "problem_title": "Поиск поставщика — только первая контрольная точка.",
        "problem": "Расхождения часто появляются позже: в предложениях используются разные условия, образцы не соответствуют чертежам, упаковка меняется без согласования, график производства сдвигается, а документы нескольких фабрик не совпадают. Мы фиксируем исходные допущения, версии и зоны ответственности, чтобы покупатель мог увидеть различия до размещения заказа.",
        "buyers": "Услуга подходит импортёрам, дистрибьюторам, инженерным компаниям, владельцам собственных брендов и проектным подрядчикам, особенно если закупки идут из нескольких промышленных кластеров Китая или нужен местный координатор.",
        "scope_title": "Объём работ согласуется для каждого проекта",
        "scope": ["Уточнение требований и подготовка закупочного задания", "Поиск и предварительный отбор поставщиков по процессу и техническому соответствию", "Единые условия RFQ и сопоставимая таблица предложений", "Координация образцов, правок и подтверждения перед серийным выпуском", "Проверка документов поставщика и планирование контроля качества", "Координация консолидации от нескольких поставщиков и экспортной передачи"],
        "workflow_title": "Шесть шагов от требований до готовности к отправке",
        "workflow": ["Уточнить спецификацию, версию, количество и критерии приёмки", "Найти кандидатов по производственному процессу и соответствию товара", "Сравнить MOQ, оснастку, упаковку, оплату и сроки на одинаковой основе", "Зафиксировать версии образцов, испытательные документы и открытые отклонения", "Запланировать контроль в процессе, перед отгрузкой или третьей стороной по риску", "Согласовать количество, упаковку, документы и передачу экспедитору"],
        "disclaimer": "Сценарии на этой странице приведены для объяснения процесса и методов контроля. Они не подтверждают завершённые проекты клиентов, фактические поставки, результаты или рекомендации. Поставщики и фабрики — независимые третьи стороны; координация и проверка не гарантируют качество, соответствие нормам или сроки.",
        "contact": "Отправить требования →", "cases": "Смотреть сценарии закупок", "switch": "Выбрать язык страницы", "service_card_title": "Агент по закупкам в Китае: поиск поставщиков и сопровождение", "service_card_desc": "Как требования, отбор поставщиков, RFQ, образцы, контрольные точки качества и экспортная передача объединяются в отслеживаемый процесс.", "card_link": "Услуги закупочного агента →", "brand_sub": "Закупки и исполнение в Китае", "nav_services": "Услуги", "nav_cases": "Сценарии", "nav_about": "О компании", "nav_resources": "Материалы", "nav_contact": "Отправить RFQ"},
    "es": {
        "title": "Agente de compras en China para compradores internacionales | Pomerol",
        "description": "Pomerol International, en Zhuhai, apoya a compradores con requisitos, búsqueda de proveedores en China, comparación de RFQ, muestras, controles de calidad y preparación de exportaciones.",
        "eyebrow": "Agente de compras en China",
        "h1": "Agente de compras en China: de la búsqueda de fábrica a la preparación del envío",
        "intro": "Pomerol International opera desde Zhuhai, Guangdong, y coordina la ejecución de compras en China para compradores internacionales. Convertimos los requisitos del producto en un brief comparable, seleccionamos proveedores según criterios técnicos y comerciales, coordinamos cotizaciones y muestras, y definimos responsabilidades para los controles de calidad y la preparación del envío.",
        "problem_title": "Encontrar un proveedor es solo el primer punto de control.",
        "problem": "Las desviaciones suelen aparecer después: cotizaciones con supuestos distintos, muestras que se apartan de los planos, cambios de embalaje sin aprobar, retrasos de producción o documentación incompatible entre fábricas. Registramos supuestos, versiones y responsabilidades para que el comprador pueda detectar diferencias antes de emitir el pedido.",
        "buyers": "Adecuado para importadores, distribuidores, empresas de ingeniería, marcas propias y contratistas de proyectos, especialmente cuando compran en varios clústeres industriales de China o necesitan un punto de coordinación local.",
        "scope_title": "Alcance acordado para cada proyecto",
        "scope": ["Aclaración de requisitos y preparación del brief de búsqueda", "Identificación y preselección de proveedores por proceso y adecuación técnica", "Condiciones RFQ uniformes y matriz de cotizaciones comparables", "Coordinación de muestras, revisiones y aprobación previa a producción", "Revisión de evidencias del proveedor y planificación de controles de calidad", "Coordinación de consolidación multiproveedor y preparación para la entrega de exportación"],
        "workflow_title": "Seis pasos desde los requisitos hasta el envío",
        "workflow": ["Definir especificación, versión, cantidad y criterios de aceptación", "Buscar candidatos por proceso de fabricación y adecuación del producto", "Normalizar MOQ, utillaje, embalaje, pago y plazos antes de comparar", "Registrar versiones de muestras, pruebas y desviaciones pendientes", "Planificar controles en proceso, preembarque o de terceros según el riesgo", "Confirmar cantidades, embalaje, documentos y entrega al transitario"],
        "disclaimer": "Los escenarios de esta página son ilustrativos y explican procesos y controles; no demuestran proyectos de clientes finalizados, envíos reales, resultados ni recomendaciones. Los proveedores y fábricas son terceros. La coordinación y las comprobaciones no garantizan calidad, cumplimiento normativo ni plazos.",
        "contact": "Enviar requisitos de compra →", "cases": "Ver escenarios de compra", "switch": "Elegir idioma", "service_card_title": "Agente de compras en China: búsqueda y coordinación de proveedores", "service_card_desc": "Cómo conectar el brief, la selección de proveedores, las RFQ, las muestras, los controles de calidad y la preparación de exportación en un proceso trazable.", "card_link": "Ver el servicio de compras →", "brand_sub": "Compras y ejecución en China", "nav_services": "Servicios", "nav_cases": "Escenarios", "nav_about": "Acerca de", "nav_resources": "Recursos", "nav_contact": "Iniciar RFQ"},
    "pt": {
        "title": "Agente de compras na China para compradores internacionais | Pomerol",
        "description": "A Pomerol International, em Zhuhai, apoia compradores com requisitos, busca de fornecedores na China, comparação de RFQs, amostras, controles de qualidade e preparação para exportação.",
        "eyebrow": "Agente de compras na China",
        "h1": "Agente de compras na China: da busca por fábricas à preparação do envio",
        "intro": "A Pomerol International atua em Zhuhai, Guangdong, coordenando compras na China para compradores internacionais. Transformamos os requisitos do produto em um briefing comparável, selecionamos fornecedores por critérios técnicos e comerciais, acompanhamos cotações e amostras e definimos responsabilidades para os pontos de controle de qualidade e preparação do embarque.",
        "problem_title": "Encontrar um fornecedor é apenas o primeiro ponto de controle.",
        "problem": "Os desvios costumam surgir depois: cotações com premissas diferentes, amostras fora do desenho, alterações de embalagem sem aprovação, atrasos de produção ou documentos incompatíveis entre fábricas. Registramos premissas, versões e responsabilidades para que o comprador identifique diferenças antes de emitir o pedido.",
        "buyers": "Indicado para importadores, distribuidores, empresas de engenharia, marcas próprias e contratantes de projetos, especialmente quando compram de vários polos industriais chineses ou precisam de um ponto de coordenação local.",
        "scope_title": "Escopo definido conforme cada projeto",
        "scope": ["Esclarecimento dos requisitos e preparação do briefing de compras", "Busca e pré-seleção de fornecedores por processo e compatibilidade técnica", "Condições de RFQ padronizadas e matriz comparável de cotações", "Coordenação de amostras, revisões e aprovação antes da produção", "Análise das evidências do fornecedor e planejamento dos controles de qualidade", "Coordenação da consolidação de vários fornecedores e preparação da entrega para exportação"],
        "workflow_title": "Seis etapas dos requisitos à preparação do embarque",
        "workflow": ["Definir especificação, versão, quantidade e critérios de aceitação", "Buscar candidatos por processo de fabricação e compatibilidade do produto", "Padronizar MOQ, ferramental, embalagem, pagamento e prazos para comparar", "Registrar versões de amostras, documentos de teste e desvios em aberto", "Planejar controles durante a produção, pré-embarque ou por terceiros conforme o risco", "Confirmar quantidades, embalagem, documentos e entrega ao agente de carga"],
        "disclaimer": "Os cenários desta página são ilustrativos e explicam processos e controles; não comprovam projetos concluídos para clientes, embarques reais, resultados ou recomendações. Fornecedores e fábricas são terceiros. A coordenação e as verificações não garantem qualidade, conformidade regulatória ou prazos.",
        "contact": "Enviar requisitos de compra →", "cases": "Ver cenários de compras", "switch": "Escolher idioma", "service_card_title": "Agente de compras na China: busca e coordenação de fornecedores", "service_card_desc": "Como conectar briefing, seleção de fornecedores, RFQs, amostras, controles de qualidade e preparação para exportação em um processo rastreável.", "card_link": "Ver serviço de compras →", "brand_sub": "Compras e execução na China", "nav_services": "Serviços", "nav_cases": "Cenários", "nav_about": "Sobre", "nav_resources": "Recursos", "nav_contact": "Iniciar RFQ"},
}


CLUSTER = {"en": EN_ROUTE, **{cfg["hreflang"]: f"/{code}/china-sourcing-agent/" for code, cfg in LOCALES.items()}, "x-default": EN_ROUTE}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def lang_switch(label: str) -> str:
    links = [f'<a href="{esc(EN_ROUTE)}">English</a>']
    links.extend(f'<a href="/{code}/china-sourcing-agent/">{esc(cfg["name"])}</a>' for code, cfg in LOCALES.items())
    return '<section class="section compact" data-language-versions><div class="wrap"><div class="eyebrow">' + esc(label) + '</div><nav class="case-index" aria-label="' + esc(label) + '">' + ''.join(links) + '</nav></div></section>'


def copy_header_footer(code: str) -> tuple[str, str]:
    source = (PUBLIC / code / "services" / "index.html").read_text(encoding="utf-8")
    header = re.search(r"<header\b[\s\S]*?</header>", source, flags=re.I)
    footer = re.search(r"<footer\b[\s\S]*?</footer>", source, flags=re.I)
    if not header or not footer:
        raise RuntimeError(f"localized services layout missing for {code}")
    return header.group(0), footer.group(0)


def breadcrumb(code: str, title: str) -> dict:
    home_name = {"zh": "Pomerol International", "ja": "Pomerol International", "ru": "Pomerol International", "es": "Pomerol International", "pt": "Pomerol International"}[code]
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_name, "item": BASE + LOCALES[code]["home"]},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + f"/{code}/china-sourcing-agent/"},
        ],
    }


def render_page(code: str) -> str:
    data = PAGES[code]
    cfg = LOCALES[code]
    route = f"/{code}/china-sourcing-agent/"
    can = BASE + route
    image = BASE + "/assets/photos/mixed-sku-warehouse.jpg"
    header, footer = copy_header_footer(code)
    alt_links = {key: value for key, value in CLUSTER.items()}
    service = {
        "@type": "Service",
        "@id": can + "#service",
        "name": data["title"].split(" | ")[0],
        "description": data["description"],
        "provider": {"@id": seo.ORG_ID},
        "areaServed": "Worldwide",
        "serviceType": data["eyebrow"],
        "url": can,
        "inLanguage": cfg["language"],
    }
    tags = seo.seo_tags(
        data["title"],
        seo.compact_description(data["description"]),
        can,
        cfg["language"],
        image,
        alts=alt_links,
        extra=[service, breadcrumb(code, data["title"])],
    )
    scope = "".join(f"<li>{esc(value)}</li>" for value in data["scope"])
    steps = "".join(f'<div class="step"><b>{i:02d}</b><h3>{esc(value)}</h3></div>' for i, value in enumerate(data["workflow"], 1))
    body = (
        f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(data["eyebrow"])}</div>'
        f'<h1 class="display">{esc(data["h1"])}</h1><p>{esc(data["intro"])}</p><div class="hero-actions">'
        f'<a class="btn primary" href="{cfg["contact"]}">{esc(data["contact"])}</a><a class="btn light" href="{cfg["cases"]}">{esc(data["cases"])}</a></div></div>'
        f'<div><img src="/assets/photos/mixed-sku-warehouse.jpg" alt="{esc(data["eyebrow"])}" loading="eager" fetchpriority="high" decoding="async"></div></div></section>'
        + lang_switch(data["switch"])
        + f'<section class="section"><div class="wrap split"><div><div class="eyebrow">{esc(data["scope_title"])}</div><h2 class="display" style="font-size:3rem">{esc(data["problem_title"])}</h2><p class="lead">{esc(data["problem"])}</p><p>{esc(data["buyers"])}</p></div>'
        f'<div class="card"><h3>{esc(data["scope_title"])}</h3><ul>{scope}</ul></div></div></section>'
        f'<section class="section dark"><div class="wrap"><div class="section-head"><div><div class="eyebrow">{esc(data["workflow_title"])}</div>'
        f'<h2 class="display">{esc(data["workflow_title"])}</h2></div></div><div class="process">{steps}</div></div></section>'
        f'<section class="section compact"><div class="wrap"><div class="notice-box">{esc(data["disclaimer"])}</div></div></section>'
        f'<section class="band"><div class="wrap band-grid"><h2 class="display">{esc(data["contact"])}</h2><div><a class="btn ghost" href="{cfg["contact"]}">{esc(data["contact"])}</a></div></div></section>'
    )
    return (
        f'<!doctype html><html lang="{esc(cfg["language"])}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(data["title"])}</title><meta name="description" content="{esc(seo.compact_description(data["description"]))}">'
        '<link rel="icon" href="/assets/logo.svg"><link rel="stylesheet" href="/assets/site.css"><script defer src="/assets/site.js"></script>'
        f'{tags}</head><body>{header}<main>{body}</main>{footer}</body></html>'
    )


def add_english_alternates_and_language_links() -> None:
    path = PUBLIC / "china-sourcing-agent" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<link rel="alternate" hreflang="(?:en|zh-CN|ja|ru|es|pt|x-default)"[^>]*>\s*', "", text, flags=re.I)
    tags = "".join(f'<link rel="alternate" hreflang="{esc(lang)}" href="{esc(BASE + route)}">' for lang, route in CLUSTER.items())
    if "</head>" not in text:
        raise RuntimeError("English sourcing agent page has no closing head")
    text = text.replace("</head>", tags + "\n</head>", 1)
    if "data-language-versions" not in text:
        hero = re.search(r"<section class=\"page-hero\"[\s\S]*?</section>", text, flags=re.I)
        if not hero:
            raise RuntimeError("English sourcing agent hero section not found")
        selector = lang_switch("Read this page in another language")
        text = text[:hero.end()] + selector + text[hero.end():]
    path.write_text(text, encoding="utf-8")


def link_from_localized_services(code: str) -> None:
    data = PAGES[code]
    path = PUBLIC / code / "services" / "index.html"
    text = path.read_text(encoding="utf-8")
    if "data-localized-sourcing-agent-link" in text:
        text = re.sub(r'<section\b[^>]*data-localized-sourcing-agent-link[\s\S]*?</section>', "", text, flags=re.I)
    block = (
        f'<section class="section compact" data-localized-sourcing-agent-link><div class="wrap"><article class="card">'
        f'<div class="eyebrow">{esc(data["eyebrow"])}</div><h2><a href="/{code}/china-sourcing-agent/">{esc(data["service_card_title"])}</a></h2>'
        f'<p>{esc(data["service_card_desc"])}</p><a class="small-link" href="/{code}/china-sourcing-agent/">{esc(data["card_link"])}</a>'
        f'</article></div></section>'
    )
    if "</main>" not in text:
        raise RuntimeError(f"localized services main section missing for {code}")
    text = text.replace("</main>", block + "</main>", 1)
    path.write_text(text, encoding="utf-8")


def update_llms() -> None:
    path = PUBLIC / "llms.txt"
    text = path.read_text(encoding="utf-8")
    marker = "## China sourcing agent pages by language"
    if marker in text:
        text = text[:text.index(marker)].rstrip()
    links = [f"- English: {BASE}{EN_ROUTE}"]
    links.extend(f"- {cfg['name']}: {BASE}/{code}/china-sourcing-agent/" for code, cfg in LOCALES.items())
    section = marker + "\n\n" + "\n".join(links) + "\n"
    path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")


def main() -> None:
    missing = set(PAGES) - set(LOCALES)
    if missing:
        raise RuntimeError(f"Missing locale routes: {sorted(missing)}")
    english = PUBLIC / "china-sourcing-agent" / "index.html"
    if not english.is_file():
        raise FileNotFoundError(english)
    add_english_alternates_and_language_links()
    for code in LOCALES:
        path = PUBLIC / code / "china-sourcing-agent" / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_page(code), encoding="utf-8")
        link_from_localized_services(code)
    update_llms()
    guides.rebuild_sitemap()

    urls = {BASE + EN_ROUTE, *(BASE + f"/{code}/china-sourcing-agent/" for code in LOCALES)}
    sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    if not urls <= set(re.findall(r"<loc>(.*?)</loc>", sitemap)):
        raise RuntimeError("Localized sourcing agent pages are missing from XML sitemap")
    for code in LOCALES:
        path = PUBLIC / code / "china-sourcing-agent" / "index.html"
        text = path.read_text(encoding="utf-8")
        if text.count("<h1") != 1 or '"@type":"Service"' not in text:
            raise RuntimeError(f"Localized service page is missing a single H1 or Service schema: {path}")
        for lang, route in CLUSTER.items():
            if f'hreflang="{lang}" href="{BASE + route}"' not in text:
                raise RuntimeError(f"Missing hreflang {lang} on {path}")
    print("Localized sourcing-agent cluster OK: six language pages, reciprocal hreflang, Service schema, internal links and sitemap entries")


if __name__ == "__main__":
    main()

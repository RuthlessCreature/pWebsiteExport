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


PROCUREMENT_PAGES = {
    "zh": {
        "title": "中国采购服务｜海外买家的采购执行与供应商管理｜Pomerol",
        "description": "面向海外买家的中国采购服务，涵盖供应商比选、RFQ 比价、订单跟进、样品与变更控制、质量检查协调及多供应商集货。",
        "eyebrow": "中国采购服务",
        "h1": "从询价、订单跟进到发运准备的中国采购服务",
        "intro": "Pomerol International 位于广东珠海，为海外买家协调中国侧采购流程。我们把采购要求、供应商报价、订单假设、样品版本、生产节点、质量检查和物流交接整理成可跟踪的记录，帮助买方在不同供应商和订单阶段之间保持同一套信息。",
        "problem_title": "采购流程分散，决定就容易失去上下文。",
        "problem": "当采购信息分散在邮件、平台聊天和货代沟通中，规格版本、价格前提、包装要求和交期责任很容易不一致。我们建立项目主记录并统一比较口径，让买方能看清哪些事项已确认、哪些仍待供应商回复，以及下一步由谁处理。",
        "buyers": "适合没有中国常驻采购团队、但需要持续管理询价、复购、项目采购或多 SKU 订单的进口商、经销商、工程公司和品牌团队。具体工作范围、商业条件及第三方费用会在项目开始前确认。",
        "scope_title": "可按项目约定的工作范围",
        "scope": ["建立采购需求、规格版本和供应商记录", "整理供应商报价并支持商业条件比较", "跟进订单假设、生产节点和待确认事项", "协调样品、修订意见和变更记录", "按产品风险协调质量检查及证据收集", "协调多供应商到货、集货和出口交接准备"],
        "workflow_title": "从采购简报到出货计划的六个步骤",
        "workflow": ["整理产品、数量、目标市场和验收要求", "设定供应商候选条件及统一询价模板", "比较报价、MOQ、付款、交期和排除项", "确认样品、订单版本和生产变更规则", "跟进生产里程碑并按风险协调检查", "核对数量、包装、单证和货代交接事项"],
        "disclaimer": "本页描述的是采购协调与供应商管理支持，不表示 Pomerol 作为买方、进口商、工厂或货代签约方。供应商和工厂为第三方。费用、付款、质量、合规及运输责任以具体项目协议和相关服务方文件为准；协调工作不构成结果保证。",
        "contact": "讨论采购项目 →", "cases": "浏览采购场景", "switch": "选择页面语言", "service_card_title": "中国采购服务：订单与供应商执行协调", "service_card_desc": "了解如何统一采购需求、报价、订单跟进、样品变更、质量节点和多供应商发运准备。", "card_link": "查看中国采购服务 →"},
    "ja": {
        "title": "中国購買・調達サービス｜海外バイヤー向けの発注管理｜Pomerol",
        "description": "海外バイヤー向けの中国購買支援。仕入先比較、RFQ、発注・生産フォロー、サンプル変更、品質確認の調整、複数社の集約を支援します。",
        "eyebrow": "中国購買・調達サービス",
        "h1": "見積もり、発注フォローから出荷準備までの中国調達サービス",
        "intro": "Pomerol Internationalは広東省珠海を拠点に、海外バイヤー向けの中国側購買プロセスを調整します。購買要件、仕入先見積もり、発注条件、サンプル版数、生産日程、品質確認、物流引渡しを追跡可能な記録にまとめ、仕入先や注文段階が変わっても情報の一貫性を保てるよう支援します。",
        "problem_title": "購買情報が分散すると、判断の前提が見えにくくなります。",
        "problem": "メール、プラットフォームのチャット、フォワーダーとの連絡に情報が分かれると、仕様版、価格前提、包装条件、納期の責任が食い違うことがあります。案件の主記録と比較基準を整え、確定事項、仕入先への確認事項、次の担当を把握しやすくします。",
        "buyers": "中国に常駐の購買チームはないものの、継続RFQ、リピート発注、プロジェクト購買、複数SKUの管理が必要な輸入業者、販売代理店、エンジニアリング会社、ブランド事業者向けです。具体的な範囲、商条件、第三者費用は開始前に確認します。",
        "scope_title": "案件に応じて合意する支援範囲",
        "scope": ["購買要件、仕様版、仕入先の記録を作成", "見積もりを整理し、商条件の比較を支援", "発注前提、生産日程、未確認事項をフォロー", "サンプル、修正内容、変更記録を調整", "製品リスクに応じて品質確認と証拠収集を調整", "複数社の納品集約と輸出引渡し準備を調整"],
        "workflow_title": "購買ブリーフから出荷計画までの6ステップ",
        "workflow": ["製品、数量、対象市場、受入基準を整理", "仕入先の選定条件と共通のRFQ様式を設定", "見積もり、MOQ、支払、納期、除外条件を比較", "サンプル、発注版数、生産変更ルールを確認", "生産マイルストーンを追跡し、リスクに応じて検査を調整", "数量、包装、書類、フォワーダー引渡しを確認"],
        "disclaimer": "本ページは購買調整と仕入先管理の支援内容を説明するもので、Pomerolが買主、輸入者、工場またはフォワーダーとして契約することを意味しません。仕入先と工場は第三者です。料金、支払、品質、法令適合性、輸送責任は個別契約および各サービス提供者の書類に従い、調整業務は結果を保証しません。",
        "contact": "購買案件を相談する →", "cases": "調達シナリオを見る", "switch": "表示言語を選択", "service_card_title": "中国購買サービス：発注と仕入先の実行調整", "service_card_desc": "購買要件、見積もり、発注フォロー、サンプル変更、品質確認、複数社の出荷準備をどう一元管理するかをご案内します。", "card_link": "中国購買サービスを見る →"},
    "ru": {
        "title": "Закупки в Китае для зарубежных компаний | Pomerol International",
        "description": "Закупочное сопровождение в Китае: сравнение поставщиков и RFQ, контроль заказов и образцов, координация качества и консолидация грузов.",
        "eyebrow": "Закупочные услуги в Китае",
        "h1": "Закупки в Китае: от запроса цены и сопровождения заказа до подготовки отправки",
        "intro": "Pomerol International работает в Чжухае, провинция Гуандун, и координирует закупочный процесс в Китае для зарубежных покупателей. Мы собираем требования, предложения поставщиков, условия заказа, версии образцов, производственные этапы, проверки качества и передачу логистике в единую отслеживаемую запись, чтобы информация оставалась согласованной между поставщиками и заказами.",
        "problem_title": "Когда закупочная информация разрознена, решения теряют контекст.",
        "problem": "Если детали распределены между электронной почтой, чатами на площадках и перепиской с экспедиторами, легко расходятся версии спецификаций, ценовые допущения, требования к упаковке и ответственность за сроки. Мы ведём основную запись проекта и единые критерии сравнения, чтобы было видно, что подтверждено, что нужно уточнить и кто отвечает за следующий шаг.",
        "buyers": "Для импортёров, дистрибьюторов, инженерных компаний и брендов без постоянной закупочной команды в Китае, которым нужно сопровождать регулярные RFQ, повторные заказы, проектные закупки или множество SKU. Конкретный объём работ, коммерческие условия и расходы третьих сторон согласуются до начала проекта.",
        "scope_title": "Объём работ согласуется для каждого проекта",
        "scope": ["Реестр требований, версий спецификаций и поставщиков", "Сведение предложений и поддержка сравнения коммерческих условий", "Сопровождение условий заказа, этапов производства и открытых вопросов", "Координация образцов, правок и записей об изменениях", "Координация контроля качества и сбора доказательств с учётом риска товара", "Координация консолидации нескольких поставщиков и экспортной передачи"],
        "workflow_title": "Шесть шагов от закупочного задания до плана отправки",
        "workflow": ["Собрать сведения о товаре, количестве, рынке и критериях приёмки", "Задать требования к кандидатам и общий шаблон RFQ", "Сравнить предложения, MOQ, оплату, сроки и исключения", "Подтвердить образцы, версию заказа и правила производственных изменений", "Отслеживать этапы производства и планировать контроль по риску", "Сверить количество, упаковку, документы и передачу экспедитору"],
        "disclaimer": "Страница описывает поддержку по координации закупок и управлению поставщиками и не означает, что Pomerol выступает покупателем, импортёром, фабрикой или стороной договора с экспедитором. Поставщики и фабрики являются третьими сторонами. Стоимость, оплата, качество, нормативное соответствие и транспортные обязанности определяются договором проекта и документами соответствующих исполнителей; координация не гарантирует результат.",
        "contact": "Обсудить закупочный проект →", "cases": "Смотреть сценарии закупок", "switch": "Выбрать язык страницы", "service_card_title": "Закупки в Китае: сопровождение заказов и поставщиков", "service_card_desc": "Как объединить требования, предложения, контроль заказов, образцы, качество и подготовку поставок от нескольких поставщиков.", "card_link": "Услуги закупочного сопровождения →"},
    "es": {
        "title": "Servicios de compras en China para empresas internacionales | Pomerol",
        "description": "Gestión de compras en China: comparación de proveedores y RFQ, seguimiento de pedidos y muestras, coordinación de calidad y consolidación de envíos.",
        "eyebrow": "Servicios de compras en China",
        "h1": "Compras en China: de la solicitud de cotización al pedido listo para envío",
        "intro": "Pomerol International opera desde Zhuhai, Guangdong, y coordina procesos de compra en China para compradores internacionales. Reunimos requisitos, ofertas de proveedores, condiciones de pedido, versiones de muestras, hitos de producción, controles de calidad y entrega logística en un registro trazable para mantener la información alineada entre proveedores y pedidos.",
        "problem_title": "Cuando la información de compras se dispersa, las decisiones pierden contexto.",
        "problem": "Si los datos están repartidos entre correos, chats de plataformas y conversaciones con transitarios, pueden divergir las versiones de especificaciones, las premisas de precio, el embalaje y la responsabilidad sobre los plazos. Mantenemos un registro principal del proyecto y criterios comunes para mostrar qué está confirmado, qué falta por consultar y quién lleva el siguiente paso.",
        "buyers": "Para importadores, distribuidores, empresas de ingeniería y marcas que no tienen un equipo de compras permanente en China, pero necesitan gestionar RFQ recurrentes, reposiciones, compras de proyectos o muchos SKU. El alcance, las condiciones comerciales y los costes de terceros se confirman antes de empezar.",
        "scope_title": "Alcance acordado para cada proyecto",
        "scope": ["Registro de requisitos, versiones de especificación y proveedores", "Organización de ofertas y apoyo para comparar condiciones comerciales", "Seguimiento de supuestos del pedido, hitos de producción y asuntos pendientes", "Coordinación de muestras, revisiones y registro de cambios", "Coordinación de controles de calidad y evidencias según el riesgo del producto", "Coordinación de consolidación multiproveedor y preparación de la entrega de exportación"],
        "workflow_title": "Seis pasos desde el brief de compras hasta el plan de envío",
        "workflow": ["Reunir producto, cantidad, mercado y criterios de aceptación", "Definir requisitos de selección y un formato RFQ común", "Comparar ofertas, MOQ, pagos, plazos y exclusiones", "Confirmar muestras, versión del pedido y reglas de cambios de producción", "Seguir hitos de producción y planificar controles según el riesgo", "Verificar cantidades, embalaje, documentos y entrega al transitario"],
        "disclaimer": "Esta página describe apoyo de coordinación de compras y gestión de proveedores; no significa que Pomerol actúe como comprador, importador, fábrica o parte contractual del transitario. Proveedores y fábricas son terceros. Los honorarios, pagos, calidad, cumplimiento normativo y responsabilidades de transporte se rigen por el acuerdo del proyecto y los documentos de cada proveedor; la coordinación no garantiza resultados.",
        "contact": "Consultar un proyecto de compras →", "cases": "Ver escenarios de compra", "switch": "Elegir idioma", "service_card_title": "Compras en China: coordinación de pedidos y proveedores", "service_card_desc": "Cómo unificar requisitos, cotizaciones, seguimiento de pedidos, muestras, controles de calidad y preparación de envíos multiproveedor.", "card_link": "Ver servicios de compras →"},
    "pt": {
        "title": "Serviços de compras na China para empresas internacionais | Pomerol",
        "description": "Gestão de compras na China: comparação de fornecedores e RFQs, acompanhamento de pedidos e amostras, coordenação de qualidade e consolidação de cargas.",
        "eyebrow": "Serviços de compras na China",
        "h1": "Compras na China: da cotação ao pedido preparado para embarque",
        "intro": "A Pomerol International atua em Zhuhai, Guangdong, coordenando processos de compras na China para compradores internacionais. Reunimos requisitos, propostas de fornecedores, condições do pedido, versões de amostras, marcos de produção, controles de qualidade e entrega logística em um registro rastreável para manter as informações alinhadas entre fornecedores e pedidos.",
        "problem_title": "Quando as informações de compras ficam dispersas, as decisões perdem contexto.",
        "problem": "Se os dados ficam espalhados entre e-mails, chats de plataformas e conversas com agentes de carga, podem divergir as versões de especificação, as premissas de preço, os requisitos de embalagem e a responsabilidade pelos prazos. Mantemos um registro principal do projeto e critérios comuns para mostrar o que foi confirmado, o que precisa ser consultado e quem conduz a próxima etapa.",
        "buyers": "Para importadores, distribuidores, empresas de engenharia e marcas sem uma equipe de compras permanente na China, mas que precisam acompanhar RFQs recorrentes, reposições, compras de projetos ou muitos SKUs. O escopo, as condições comerciais e os custos de terceiros são confirmados antes do início.",
        "scope_title": "Escopo definido conforme cada projeto",
        "scope": ["Registro de requisitos, versões de especificação e fornecedores", "Organização de propostas e apoio na comparação de condições comerciais", "Acompanhamento de premissas do pedido, marcos de produção e pendências", "Coordenação de amostras, revisões e registro de alterações", "Coordenação de controles de qualidade e evidências conforme o risco do produto", "Coordenação da consolidação de vários fornecedores e preparação da entrega para exportação"],
        "workflow_title": "Seis etapas do briefing de compras ao plano de embarque",
        "workflow": ["Reunir produto, quantidade, mercado e critérios de aceitação", "Definir requisitos de seleção e um formato comum de RFQ", "Comparar propostas, MOQ, pagamentos, prazos e exclusões", "Confirmar amostras, versão do pedido e regras para mudanças na produção", "Acompanhar marcos de produção e planejar controles conforme o risco", "Conferir quantidades, embalagem, documentos e entrega ao agente de carga"],
        "disclaimer": "Esta página descreve apoio de coordenação de compras e gestão de fornecedores; não significa que a Pomerol atue como compradora, importadora, fábrica ou parte contratual do agente de carga. Fornecedores e fábricas são terceiros. Honorários, pagamentos, qualidade, conformidade regulatória e responsabilidades de transporte seguem o acordo do projeto e os documentos dos prestadores; a coordenação não garante resultados.",
        "contact": "Conversar sobre um projeto de compras →", "cases": "Ver cenários de compras", "switch": "Escolher idioma", "service_card_title": "Compras na China: coordenação de pedidos e fornecedores", "service_card_desc": "Como reunir requisitos, cotações, acompanhamento de pedidos, amostras, controles de qualidade e preparação de envios de vários fornecedores.", "card_link": "Ver serviços de compras →"},
}

SERVICE_CLUSTERS = {
    "china-sourcing-agent": PAGES,
    "china-procurement-services": PROCUREMENT_PAGES,
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def cluster_for(slug: str) -> dict[str, str]:
    return {"en": f"/{slug}/", **{cfg["hreflang"]: f"/{code}/{slug}/" for code, cfg in LOCALES.items()}, "x-default": f"/{slug}/"}


def lang_switch(label: str, slug: str) -> str:
    links = [f'<a href="/{slug}/">English</a>']
    links.extend(f'<a href="/{code}/{slug}/">{esc(cfg["name"])}</a>' for code, cfg in LOCALES.items())
    return '<section class="section compact" data-language-versions><div class="wrap"><div class="eyebrow">' + esc(label) + '</div><nav class="case-index" aria-label="' + esc(label) + '">' + ''.join(links) + '</nav></div></section>'


def copy_header_footer(code: str) -> tuple[str, str]:
    source = (PUBLIC / code / "services" / "index.html").read_text(encoding="utf-8")
    header = re.search(r"<header\b[\s\S]*?</header>", source, flags=re.I)
    footer = re.search(r"<footer\b[\s\S]*?</footer>", source, flags=re.I)
    if not header or not footer:
        raise RuntimeError(f"localized services layout missing for {code}")
    return header.group(0), footer.group(0)


def breadcrumb(code: str, title: str, slug: str) -> dict:
    home_name = {"zh": "Pomerol International", "ja": "Pomerol International", "ru": "Pomerol International", "es": "Pomerol International", "pt": "Pomerol International"}[code]
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_name, "item": BASE + LOCALES[code]["home"]},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + f"/{code}/{slug}/"},
        ],
    }


def render_page(code: str, slug: str, pages: dict[str, dict]) -> str:
    data = pages[code]
    cfg = LOCALES[code]
    route = f"/{code}/{slug}/"
    can = BASE + route
    image = BASE + "/assets/photos/mixed-sku-warehouse.jpg"
    header, footer = copy_header_footer(code)
    alt_links = cluster_for(slug)
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
        extra=[service, breadcrumb(code, data["title"], slug)],
    )
    scope = "".join(f"<li>{esc(value)}</li>" for value in data["scope"])
    steps = "".join(f'<div class="step"><b>{i:02d}</b><h3>{esc(value)}</h3></div>' for i, value in enumerate(data["workflow"], 1))
    body = (
        f'<section class="page-hero"><div class="wrap page-hero-grid"><div><div class="eyebrow">{esc(data["eyebrow"])}</div>'
        f'<h1 class="display">{esc(data["h1"])}</h1><p>{esc(data["intro"])}</p><div class="hero-actions">'
        f'<a class="btn primary" href="{cfg["contact"]}">{esc(data["contact"])}</a><a class="btn light" href="{cfg["cases"]}">{esc(data["cases"])}</a></div></div>'
        f'<div><img src="/assets/photos/mixed-sku-warehouse.jpg" alt="{esc(data["eyebrow"])}" loading="eager" fetchpriority="high" decoding="async"></div></div></section>'
        + lang_switch(data["switch"], slug)
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


def add_english_alternates_and_language_links(slug: str) -> None:
    path = PUBLIC / slug / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<link rel="alternate" hreflang="(?:en|zh-CN|ja|ru|es|pt|x-default)"[^>]*>\s*', "", text, flags=re.I)
    tags = "".join(f'<link rel="alternate" hreflang="{esc(lang)}" href="{esc(BASE + route)}">' for lang, route in cluster_for(slug).items())
    if "</head>" not in text:
        raise RuntimeError(f"English service page has no closing head: {slug}")
    text = text.replace("</head>", tags + "\n</head>", 1)
    if "data-language-versions" not in text:
        hero = re.search(r"<section class=\"page-hero\"[\s\S]*?</section>", text, flags=re.I)
        if not hero:
            raise RuntimeError(f"English service hero section not found: {slug}")
        selector = lang_switch("Read this page in another language", slug)
        text = text[:hero.end()] + selector + text[hero.end():]
    path.write_text(text, encoding="utf-8")


def clear_legacy_service_links(code: str) -> None:
    path = PUBLIC / code / "services" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<section\b[^>]*data-localized-sourcing-agent-link[^>]*>[\s\S]*?</section>', "", text, flags=re.I)
    path.write_text(text, encoding="utf-8")


def link_from_localized_services(code: str, slug: str, pages: dict[str, dict]) -> None:
    data = pages[code]
    path = PUBLIC / code / "services" / "index.html"
    text = path.read_text(encoding="utf-8")
    marker = f'data-localized-service-page="{slug}"'
    text = re.sub(r'<section\b[^>]*data-localized-service-page="' + re.escape(slug) + r'"[^>]*>[\s\S]*?</section>', "", text, flags=re.I)
    block = (
        f'<section class="section compact" {marker}><div class="wrap"><article class="card">'
        f'<div class="eyebrow">{esc(data["eyebrow"])}</div><h2><a href="/{code}/{slug}/">{esc(data["service_card_title"])}</a></h2>'
        f'<p>{esc(data["service_card_desc"])}</p><a class="small-link" href="/{code}/{slug}/">{esc(data["card_link"])}</a>'
        f'</article></div></section>'
    )
    if "</main>" not in text:
        raise RuntimeError(f"localized services main section missing for {code}")
    text = text.replace("</main>", block + "</main>", 1)
    path.write_text(text, encoding="utf-8")


def update_llms() -> None:
    path = PUBLIC / "llms.txt"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^## (?:China sourcing agent pages by language|Service pages by language)\n[\s\S]*$", "", text).rstrip()
    marker = "## Service pages by language"
    headings = {
        "china-sourcing-agent": "China sourcing agent",
        "china-procurement-services": "China procurement services",
    }
    groups = []
    for slug, pages in SERVICE_CLUSTERS.items():
        links = [f"- English: {BASE}/{slug}/"]
        links.extend(f"- {cfg['name']}: {BASE}/{code}/{slug}/" for code, cfg in LOCALES.items())
        groups.append(f"### {headings[slug]}\n\n" + "\n".join(links))
    section = marker + "\n\n" + "\n\n".join(groups) + "\n"
    path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")


def main() -> None:
    for slug, pages in SERVICE_CLUSTERS.items():
        missing = set(pages) - set(LOCALES)
        if missing:
            raise RuntimeError(f"Missing locale routes for {slug}: {sorted(missing)}")
        english = PUBLIC / slug / "index.html"
        if not english.is_file():
            raise FileNotFoundError(english)
        add_english_alternates_and_language_links(slug)
        for code in LOCALES:
            path = PUBLIC / code / slug / "index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render_page(code, slug, pages), encoding="utf-8")
            link_from_localized_services(code, slug, pages)
    for code in LOCALES:
        clear_legacy_service_links(code)
    update_llms()
    guides.rebuild_sitemap()

    urls = {BASE + f"/{slug}/" for slug in SERVICE_CLUSTERS}
    urls.update(BASE + f"/{code}/{slug}/" for slug in SERVICE_CLUSTERS for code in LOCALES)
    sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
    if not urls <= set(re.findall(r"<loc>(.*?)</loc>", sitemap)):
        raise RuntimeError("Localized service pages are missing from XML sitemap")
    for slug, pages in SERVICE_CLUSTERS.items():
        cluster = cluster_for(slug)
        for code in LOCALES:
            path = PUBLIC / code / slug / "index.html"
            text = path.read_text(encoding="utf-8")
            if text.count("<h1") != 1 or '"@type":"Service"' not in text:
                raise RuntimeError(f"Localized service page is missing a single H1 or Service schema: {path}")
            for lang, route in cluster.items():
                if f'hreflang="{lang}" href="{BASE + route}"' not in text:
                    raise RuntimeError(f"Missing hreflang {lang} on {path}")
    print(f"Localized service clusters OK: {len(SERVICE_CLUSTERS) * 6} pages, reciprocal hreflang, Service schema, internal links and sitemap entries")


if __name__ == "__main__":
    main()

"""Build the 6 PDF products for NEXUS PDF — futuristic dark layout."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, math

BG = HexColor("#08060d")
BG2 = HexColor("#12091f")
PURPLE = HexColor("#c63dff")
MAGENTA = HexColor("#ff2bd1")
BLUE = HexColor("#4f8fff")
RED = HexColor("#ff2e2e")
TEXT = HexColor("#f0ecf7")
MUTED = HexColor("#8a87a3")
DIM = HexColor("#3a3450")

PAGE_W, PAGE_H = A4

PRODUCTS = [
    {
        "filename": "ia-para-negocios-2026.pdf",
        "title": "IA PARA NEGÓCIOS",
        "edition": "Edição 2026",
        "tag": "INTELIGÊNCIA ARTIFICIAL",
        "subtitle": "Aplicações práticas de IA em empresas, com cases reais e análise de ROI.",
        "accent": MAGENTA,
        "accent2": PURPLE,
        "chapters": [
            ("01", "O Estado da IA em 2026",
             "A inteligência artificial deixou de ser promessa e virou infraestrutura. Em 2026, mais de 78% das empresas Fortune 500 operam com modelos de linguagem em pelo menos um processo crítico. Este capítulo mapeia o cenário atual: quem está usando, como está usando, e o que separa as empresas que extraem valor real daquelas que apenas gastam com hype.",
             ["Adoção corporativa por setor (2024 → 2026)",
              "ROI médio de projetos de IA generativa",
              "Os 5 erros mais caros na implementação",
              "Por que 70% dos pilotos nunca chegam à produção"]),
            ("02", "Casos de Uso de Alto Impacto",
             "Nem todo problema é problema de IA. Selecionamos 12 aplicações com retorno comprovado: atendimento, vendas, operações, P&D, marketing e back-office. Cada caso vem com métricas reais, custos de implementação e tempo até o break-even.",
             ["Atendimento: redução de 40% em ticket médio",
              "Vendas: conversão +23% com agentes de qualificação",
              "Operações: previsão de demanda com erro < 6%",
              "P&D: aceleração de prototipagem em 4x"]),
            ("03", "Stack Tecnológica Mínima",
             "Você não precisa contratar uma equipe de ML para começar. Apresentamos a stack de menor custo e maior alavancagem: modelos via API, RAG simples, orquestração e observabilidade. Inclui comparativo de custos entre OpenAI, Anthropic, Google e modelos open-source self-hosted.",
             ["Custo por 1M tokens: comparativo atualizado",
              "Quando self-host compensa (e quando não)",
              "Arquitetura RAG de referência",
              "Ferramentas de avaliação contínua"]),
            ("04", "Governança, Risco e Compliance",
             "AI Act europeu, regulamentação brasileira em formação e expectativas crescentes de clientes. Como estruturar um framework interno de governança que não trava a inovação, mas protege a empresa de exposição legal e reputacional.",
             ["Checklist de compliance AI Act",
              "Política de uso aceitável (template)",
              "Auditoria de viés: o que medir",
              "Logs e rastreabilidade obrigatórios"]),
            ("05", "Roadmap 90 Dias",
             "Plano executável para times pequenos. Semana a semana, do diagnóstico ao primeiro projeto em produção. Inclui templates de business case, planilha de priorização e roteiro de stakeholder management.",
             ["Diagnóstico: identificar 3 oportunidades",
              "Quick win: piloto em 30 dias",
              "Escala: governança e segundo projeto",
              "KPIs de acompanhamento mensal"]),
        ],
    },
    {
        "filename": "guia-web3-completo.pdf",
        "title": "GUIA WEB3 COMPLETO",
        "edition": "Manual Definitivo",
        "tag": "WEB3 & BLOCKCHAIN",
        "subtitle": "Do básico ao avançado: blockchain, DeFi, NFTs e DAOs sem fluff.",
        "accent": RED,
        "accent2": PURPLE,
        "chapters": [
            ("01", "Fundamentos da Descentralização",
             "Por que blockchain importa para além de cripto. Conceitos essenciais: consenso, imutabilidade, chaves públicas, carteiras custodial vs. não-custodial. Linguagem direta, sem mistificação.",
             ["Como funciona uma transação on-chain",
              "Bitcoin vs. Ethereum vs. L2s",
              "Custódia: o que você precisa entender",
              "Os mitos mais comuns desmontados"]),
            ("02", "DeFi: Finanças Programáveis",
             "Empréstimos, derivativos, exchanges descentralizadas e yield farming. Como funcionam, quais riscos reais existem (impermanent loss, contratos, oráculos) e como avaliar protocolos.",
             ["TVL e por que ele engana",
              "Análise de risco de smart contracts",
              "Liquidez e slippage explicados",
              "Os 7 maiores hacks e o que aprender"]),
            ("03", "NFTs: Além da Imagem JPG",
             "Para o que NFTs realmente servem: tokenização de ativos, identidade, certificação, royalties. Casos de uso corporativos que não são especulação.",
             ["Padrões ERC-721, ERC-1155 e SBT",
              "NFTs em propriedade intelectual",
              "Tokenização de ativos do mundo real",
              "Por que a maioria dos projetos falhou"]),
            ("04", "DAOs e Governança Descentralizada",
             "Organizações coordenadas por código. Quando faz sentido, quando vira teatro. Estrutura legal, ferramentas de voto e exemplos de DAOs que funcionam.",
             ["Estruturas legais (Wyoming, Marshall Islands)",
              "Mecanismos de votação comparados",
              "Tesouraria multi-sig em prática",
              "Anti-padrões de governança"]),
            ("05", "Construindo no Web3",
             "Stack de desenvolvimento, ferramentas indispensáveis e roadmap para devs e fundadores. Como evitar os erros comuns de quem entra no setor.",
             ["Solidity, Vyper ou Rust?",
              "Ambientes: Hardhat, Foundry, Anchor",
              "Auditoria: quando e quanto custa",
              "Indo a mainnet sem queimar capital"]),
        ],
    },
    {
        "filename": "prompt-engineering-avancado.pdf",
        "title": "PROMPT ENGINEERING",
        "edition": "Técnicas Avançadas",
        "tag": "INTELIGÊNCIA ARTIFICIAL",
        "subtitle": "Técnicas premium para extrair o máximo de LLMs em produção.",
        "accent": BLUE,
        "accent2": PURPLE,
        "chapters": [
            ("01", "Anatomia de um Prompt Eficaz",
             "Estrutura, contexto, exemplos e restrições. Por que prompts curtos quase sempre rendem menos, e como expandir sem virar ruído.",
             ["Os 6 componentes de um prompt robusto",
              "Sistema vs. usuário: separação clara",
              "Few-shot: quantos exemplos ideais",
              "Anti-padrões mais comuns"]),
            ("02", "Chain-of-Thought e Raciocínio",
             "Quando pedir raciocínio passo-a-passo, quando ele atrapalha, e como combinar CoT com auto-consistência para tarefas complexas.",
             ["CoT clássico vs. CoT estruturado",
              "Self-consistency: quando vale o custo",
              "Tree-of-thought na prática",
              "Modelos com reasoning nativo"]),
            ("03", "Tool Use e Agentes",
             "Como descrever ferramentas para o modelo usar bem. Padrões de design de agentes, loops de execução e limites de autonomia.",
             ["Schemas de função claros",
              "Orquestração: ReAct, plan-and-execute",
              "Recuperação de erros e retries",
              "Quando NÃO usar agente"]),
            ("04", "Avaliação Sistemática",
             "Você não pode melhorar o que não mede. Como montar eval sets, escolher métricas, usar LLM-as-judge sem se enganar e iterar com disciplina.",
             ["Construindo um eval set útil",
              "Métricas: exact match, BLEU, judge",
              "A/B test de prompts em produção",
              "Detectando regressões silenciosas"]),
            ("05", "Produção: Custo, Latência, Segurança",
             "Cache, streaming, prompt compression, guardrails contra prompt injection e PII. O que muda quando seu prompt atende 1 milhão de usuários.",
             ["Prompt caching: economia real",
              "Mitigando injection e jailbreak",
              "Filtros de saída e PII",
              "Observabilidade: o que logar"]),
        ],
    },
    {
        "filename": "futuro-do-trabalho.pdf",
        "title": "FUTURO DO TRABALHO",
        "edition": "Carreiras 2030",
        "tag": "CARREIRA TECH",
        "subtitle": "Carreiras emergentes e habilidades essenciais para os próximos 5 anos.",
        "accent": MAGENTA,
        "accent2": RED,
        "chapters": [
            ("01", "O Trabalho Que Está Sumindo",
             "Quais funções estão sendo automatizadas agora, quais virão a seguir, e por que a narrativa de 'IA não tira empregos, só transforma' é parcialmente verdadeira e perigosamente incompleta.",
             ["Funções com risco alto (próximos 24 meses)",
              "Funções com risco médio (3-5 anos)",
              "O que de fato sobrevive à automação",
              "Sinais de alerta na sua área"]),
            ("02", "As 12 Carreiras Emergentes",
             "Funções que mal existiam em 2020 e hoje pagam acima da média do mercado. AI engineer, prompt designer, governance lead, model risk officer, e outras.",
             ["Salário e progressão por função",
              "Skills requeridas (técnicas e soft)",
              "Caminhos de transição realistas",
              "Onde estão sendo contratadas"]),
            ("03", "Skills Que Não Envelhecem",
             "Habilidades anti-frágeis: raciocínio probabilístico, comunicação clara sob ambiguidade, design de sistemas, julgamento ético e gestão de stakeholders.",
             ["Como desenvolver pensamento crítico",
              "Escrita técnica de alto impacto",
              "Negociação em ambientes de incerteza",
              "Aprendizado contínuo (modelo prático)"]),
            ("04", "Construindo Marca Profissional",
             "Por que portfólio público venceu currículo. Como construir autoridade em uma vertical específica sem virar influencer.",
             ["Conteúdo: o que escrever (e onde)",
              "Open source como currículo",
              "Networking sem cringe",
              "Reputação digital de longo prazo"]),
            ("05", "Modelos de Trabalho Pós-2026",
             "Fractional, contractor, equity-only, residências. Os novos formatos contratuais e quando cada um faz sentido na trajetória.",
             ["Comparativo: CLT, PJ, fractional",
              "Como precificar (e renegociar)",
              "Equity: o que aceitar e recusar",
              "Construindo opcionalidade real"]),
        ],
    },
    {
        "filename": "seguranca-digital.pdf",
        "title": "SEGURANÇA DIGITAL",
        "edition": "Manual Pessoal",
        "tag": "TENDÊNCIAS",
        "subtitle": "Proteja dados, identidade e ativos digitais com práticas profissionais.",
        "accent": BLUE,
        "accent2": MAGENTA,
        "chapters": [
            ("01", "Modelo de Ameaça Pessoal",
             "Antes de comprar ferramenta, defina o que você protege e contra quem. Frameworks usados por profissionais para mapear riscos sem paranoia.",
             ["Identificando seus ativos críticos",
              "Adversários realistas vs. fantasia",
              "Trade-off conveniência x segurança",
              "Templates de threat model pessoal"]),
            ("02", "Autenticação: O Que Realmente Funciona",
             "Senhas, gerenciadores, MFA, passkeys, hardware keys. O que migrar primeiro e por quê. Por que SMS-2FA é pior do que nada em certos casos.",
             ["Gerenciador de senhas: como escolher",
              "Passkeys explicadas em 10 minutos",
              "Hardware keys (YubiKey) na prática",
              "Recuperação de conta sem expor-se"]),
            ("03", "Privacidade Aplicada",
             "Reduzindo seu rastro digital sem sair do mundo. Configurações reais em iOS, Android, navegadores e redes sociais. Limites do VPN.",
             ["Auditoria de privacidade em 1h",
              "Hardening de smartphone passo-a-passo",
              "Navegação: extensões essenciais",
              "Mitos sobre VPN desmontados"]),
            ("04", "Proteção de Ativos Digitais",
             "Cripto, contas em corretoras, propriedade intelectual e backups soberanos. Custódia, multi-sig e planos de continuidade.",
             ["Hot wallet vs. cold storage",
              "Multi-sig pessoal explicado",
              "Backups 3-2-1 atualizado",
              "Plano de sucessão digital"]),
            ("05", "Resposta a Incidentes",
             "O que fazer nas primeiras 24h se você for comprometido. Checklists prontos para vazamento de senha, conta sequestrada e dispositivo perdido.",
             ["Checklist: senha vazou",
              "Checklist: conta sequestrada",
              "Checklist: celular roubado",
              "Documentos legais úteis"]),
        ],
    },
    {
        "filename": "tendencias-globais-2026.pdf",
        "title": "TENDÊNCIAS GLOBAIS",
        "edition": "Relatório 2026",
        "tag": "TENDÊNCIAS GLOBAIS",
        "subtitle": "Análise geopolítica, econômica e tecnológica do ano que está em curso.",
        "accent": PURPLE,
        "accent2": BLUE,
        "chapters": [
            ("01", "Geopolítica Multipolar",
             "O fim definitivo do mundo unipolar. EUA, China, UE, Índia e blocos emergentes. Onde estão se formando as novas fronteiras de influência e o que isso significa para negócios.",
             ["Mapa de blocos econômicos 2026",
              "Tecnologia como arma geopolítica",
              "Riscos por região (matriz visual)",
              "Janelas de oportunidade emergentes"]),
            ("02", "Economia em Transição",
             "Inflação estrutural, juros reais positivos, desglobalização parcial e o retorno da política industrial. Cenários macro e o que monitorar.",
             ["Indicadores que importam (e os que não)",
              "Cadeias de suprimento: friend-shoring",
              "Mercados de capital em rotação",
              "Cenários: base, otimista, pessimista"]),
            ("03", "Tecnologia e Poder",
             "IA generativa, semicondutores, energia e biotecnologia. As quatro frentes onde se decide a próxima década. Quem está liderando, quem está sendo deixado para trás.",
             ["Corrida dos chips: estado atual",
              "Energia: fusão, nuclear, renováveis",
              "Biotech: CRISPR e medicina de precisão",
              "Espaço: nova economia orbital"]),
            ("04", "Clima e Adaptação",
             "Do net-zero ao realismo climático. Mercados de carbono, transição energética e como empresas estão se posicionando além do greenwashing.",
             ["Mercados de carbono em 2026",
              "Setores mais expostos ao risco físico",
              "Tecnologias de adaptação em ascensão",
              "Regulação climática por região"]),
            ("05", "Sociedade e Cultura",
             "Demografia em colapso no Norte global, migrações em escala, polarização e fragmentação midiática. Os tensionamentos que moldam o consumo, a política e o trabalho.",
             ["Pirâmides etárias e seus impactos",
              "Migração: rotas e tensões",
              "Mídia fragmentada: novo consumo",
              "Confiança institucional em queda"]),
        ],
    },
]


def draw_cover_bg(c, accent, accent2):
    """Dark cover with concentric portal rings + grid."""
    # Solid dark background
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Background grid (subtle)
    c.setStrokeColor(HexColor("#1a1430"))
    c.setLineWidth(0.4)
    step = 1.2 * cm
    for x in [i * step for i in range(int(PAGE_W / step) + 1)]:
        c.line(x, 0, x, PAGE_H)
    for y in [i * step for i in range(int(PAGE_H / step) + 1)]:
        c.line(0, y, PAGE_W, y)

    # Portal: concentric rings centered upper-right area
    cx, cy = PAGE_W * 0.72, PAGE_H * 0.62
    c.setLineWidth(1.0)
    rings = [
        (30, accent, 1.0),
        (55, accent, 0.9),
        (85, accent2, 0.8),
        (120, accent2, 0.65),
        (160, accent2, 0.5),
        (205, HexColor("#5a1fa0"), 0.4),
        (255, HexColor("#3f1675"), 0.3),
        (310, HexColor("#2a0e54"), 0.2),
    ]
    for r, col, alpha in rings:
        c.setStrokeColor(col)
        try:
            c.setStrokeAlpha(alpha)
        except Exception:
            pass
        c.circle(cx, cy, r, fill=0, stroke=1)
    try:
        c.setStrokeAlpha(1)
    except Exception:
        pass

    # Glow core
    c.setFillColor(accent)
    try:
        c.setFillAlpha(0.7)
    except Exception:
        pass
    c.circle(cx, cy, 18, fill=1, stroke=0)
    try:
        c.setFillAlpha(1)
    except Exception:
        pass


def draw_checker(c, x, y, size, cols=4, rows=4, color=RED):
    """Checkered flag pattern accent."""
    cell = size / cols
    for i in range(cols):
        for j in range(rows):
            if (i + j) % 2 == 0:
                c.setFillColor(color)
            else:
                c.setFillColor(white)
            c.rect(x + i * cell, y + j * cell, cell, cell, fill=1, stroke=0)


def build_cover(c, product):
    accent = product["accent"]
    accent2 = product["accent2"]
    draw_cover_bg(c, accent, accent2)

    # Top tag line
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, PAGE_H - 2 * cm, "NEXUS PDF  //  CONHECIMENTO DO FUTURO")

    # Edition badge upper-right
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    edition_text = product["edition"].upper()
    c.drawRightString(PAGE_W - 2 * cm, PAGE_H - 2 * cm, edition_text)

    # Category tag
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, PAGE_H - 8 * cm, product["tag"])

    # Title (large stacked)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 64)
    title_words = product["title"].split()
    y = PAGE_H - 11 * cm
    for word in title_words:
        c.drawString(2 * cm, y, word)
        y -= 2 * cm

    # Checker accent next to title
    draw_checker(c, PAGE_W - 5 * cm, PAGE_H - 11 * cm, 2.4 * cm, 4, 4, RED)

    # Subtitle
    c.setFillColor(HexColor("#cfc6e0"))
    c.setFont("Helvetica", 14)
    sub = product["subtitle"]
    # Simple wrap
    max_chars = 50
    line = ""
    sy = y - 0.3 * cm
    for word in sub.split():
        if len(line) + len(word) + 1 <= max_chars:
            line = (line + " " + word).strip()
        else:
            c.drawString(2 * cm, sy, line)
            sy -= 0.7 * cm
            line = word
    if line:
        c.drawString(2 * cm, sy, line)

    # Bottom: discount badge
    bx, by = 2 * cm, 3.2 * cm
    bw, bh = 6.2 * cm, 2.6 * cm
    c.setStrokeColor(white)
    c.setLineWidth(1.4)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(bx + 0.6 * cm, by + 1 * cm, "50% OFF")
    c.setFont("Helvetica", 9)
    c.drawString(bx + 0.65 * cm, by + 0.4 * cm, "LANÇAMENTO EXCLUSIVO")

    # Bottom-right small meta
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawRightString(PAGE_W - 2 * cm, 2 * cm, "WWW.NEXUSPDF.COM")

    c.showPage()


def draw_inner_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Side accent strip
    c.setFillColor(HexColor("#0f0a1c"))
    c.rect(0, 0, 1.2 * cm, PAGE_H, fill=1, stroke=0)


def draw_page_header(c, product, page_num):
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, PAGE_H - 1.4 * cm, "NEXUS PDF")
    c.setFillColor(product["accent"])
    c.drawString(4.5 * cm, PAGE_H - 1.4 * cm, "// " + product["tag"])
    c.setFillColor(MUTED)
    c.drawRightString(PAGE_W - 2 * cm, PAGE_H - 1.4 * cm, product["title"])
    # thin line
    c.setStrokeColor(DIM)
    c.setLineWidth(0.3)
    c.line(2 * cm, PAGE_H - 1.6 * cm, PAGE_W - 2 * cm, PAGE_H - 1.6 * cm)
    # page num footer
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawRightString(PAGE_W - 2 * cm, 1.4 * cm, f"PG. {page_num:02d}")
    c.setFillColor(product["accent"])
    c.drawString(2 * cm, 1.4 * cm, "—")


def build_toc(c, product, page_num):
    draw_inner_bg(c)
    draw_page_header(c, product, page_num)

    # Big section label
    c.setFillColor(product["accent"])
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, PAGE_H - 3.5 * cm, "// SUMÁRIO")

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 46)
    c.drawString(2 * cm, PAGE_H - 6 * cm, "ÍNDICE")

    # Chapter list
    y = PAGE_H - 9 * cm
    for num, title, _, _ in product["chapters"]:
        c.setFillColor(product["accent"])
        c.setFont("Helvetica-Bold", 28)
        c.drawString(2 * cm, y, num)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(4.5 * cm, y + 0.2 * cm, title)
        # dotted line + page
        c.setStrokeColor(DIM)
        c.setDash(1, 2)
        c.line(4.5 * cm + c.stringWidth(title, "Helvetica-Bold", 20) + 0.5 * cm,
               y + 0.4 * cm, PAGE_W - 3 * cm, y + 0.4 * cm)
        c.setDash()
        y -= 2.3 * cm

    c.showPage()


def build_chapter(c, product, chapter, page_num):
    num, title, body, bullets = chapter

    # Chapter opener page
    draw_inner_bg(c)
    draw_page_header(c, product, page_num)

    # Huge number
    c.setFillColor(product["accent"])
    try:
        c.setFillAlpha(0.18)
    except Exception:
        pass
    c.setFont("Helvetica-Bold", 220)
    c.drawString(2 * cm, PAGE_H - 14 * cm, num)
    try:
        c.setFillAlpha(1)
    except Exception:
        pass

    # Section tag
    c.setFillColor(product["accent"])
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, PAGE_H - 3.5 * cm, f"CAPÍTULO {num}")

    # Chapter title
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 42)
    # wrap title
    words = title.upper().split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if c.stringWidth(test, "Helvetica-Bold", 42) < PAGE_W - 4 * cm:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    ty = PAGE_H - 6 * cm
    for ln in lines:
        c.drawString(2 * cm, ty, ln)
        ty -= 1.4 * cm

    # Body intro
    c.setFillColor(HexColor("#cfc6e0"))
    c.setFont("Helvetica", 14)
    # wrap body
    body_y = ty - 0.8 * cm
    max_w = PAGE_W - 4 * cm
    words = body.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "Helvetica", 14) < max_w:
            line = test
        else:
            c.drawString(2 * cm, body_y, line)
            body_y -= 0.68 * cm
            line = w
    if line:
        c.drawString(2 * cm, body_y, line)
        body_y -= 0.68 * cm

    # Bullets header
    body_y -= 0.8 * cm
    c.setFillColor(product["accent"])
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, body_y, "// VOCÊ VAI ENCONTRAR")
    body_y -= 0.9 * cm

    c.setFillColor(white)
    c.setFont("Helvetica", 14)
    for b in bullets:
        c.setFillColor(product["accent"])
        c.circle(2.2 * cm, body_y + 0.18 * cm, 0.11 * cm, fill=1, stroke=0)
        c.setFillColor(HexColor("#e8e2f5"))
        c.drawString(2.7 * cm, body_y, b)
        body_y -= 0.78 * cm

    # Bottom decorative line + checker
    c.setStrokeColor(product["accent"])
    c.setLineWidth(0.5)
    c.line(2 * cm, 3 * cm, 8 * cm, 3 * cm)
    draw_checker(c, PAGE_W - 4.5 * cm, 2.5 * cm, 1.2 * cm, 3, 3, product["accent"])

    c.showPage()


def build_outro(c, product, page_num):
    draw_cover_bg(c, product["accent"], product["accent2"])

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, PAGE_H - 2 * cm, "NEXUS PDF  //  OBRIGADO")

    c.setFillColor(product["accent"])
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, PAGE_H - 11 * cm, "// PRÓXIMOS PASSOS")

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 56)
    c.drawString(2 * cm, PAGE_H - 14 * cm, "CONTINUE")
    c.drawString(2 * cm, PAGE_H - 16 * cm, "EXPLORANDO.")

    c.setFillColor(HexColor("#cfc6e0"))
    c.setFont("Helvetica", 14)
    lines = [
        "Você acabou de ler um material do catálogo NEXUS PDF.",
        "Acesse o site para conhecer toda a biblioteca de PDFs",
        "sobre tecnologia, IA, Web3 e tendências globais.",
    ]
    ly = PAGE_H - 18 * cm
    for ln in lines:
        c.drawString(2 * cm, ly, ln)
        ly -= 0.72 * cm

    # CTA box
    bx, by = 2 * cm, 4 * cm
    bw, bh = 10 * cm, 2.4 * cm
    c.setStrokeColor(white)
    c.setLineWidth(1.4)
    c.rect(bx, by, bw, bh, fill=0, stroke=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(bx + 0.6 * cm, by + 0.85 * cm, "VER CATÁLOGO COMPLETO →")

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    c.drawRightString(PAGE_W - 2 * cm, 2 * cm, "WWW.NEXUSPDF.COM")

    c.showPage()


def build_pdf(product, out_dir):
    path = os.path.join(out_dir, product["filename"])
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(product["title"])
    c.setAuthor("NEXUS PDF")
    c.setSubject(product["subtitle"])

    # Cover
    build_cover(c, product)

    # TOC
    page_num = 2
    build_toc(c, product, page_num)

    # Chapters
    page_num = 3
    for ch in product["chapters"]:
        build_chapter(c, product, ch, page_num)
        page_num += 1

    # Outro
    build_outro(c, product, page_num)

    c.save()
    size_kb = os.path.getsize(path) / 1024
    print(f"OK  {product['filename']}  ({size_kb:.1f} KB)")


def main():
    out = os.path.dirname(os.path.abspath(__file__))
    for p in PRODUCTS:
        build_pdf(p, out)
    print(f"\nGerados {len(PRODUCTS)} PDFs em: {out}")


if __name__ == "__main__":
    main()


from pathlib import Path
import html
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

APP_DIR = Path(__file__).parent
DATA = APP_DIR / "data"

st.set_page_config(
    page_title="Máquina territorial | Presidencia 2026",
    layout="wide",
    page_icon="🧭",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.block-container {padding-top: 3.2rem; padding-bottom: 2.2rem; max-width: 1680px;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #0b1220 0%, #111827 100%);}
[data-testid="stSidebar"] * {color:#f8fafc;}
.main-title {font-size:2.25rem; line-height:1.12; font-weight:900; letter-spacing:-.04em; margin:0 0 .3rem 0;}
.main-subtitle {color:#b6c2d2; font-size:1rem; margin-bottom:1rem;}
.hero-box {
    border:1px solid rgba(148,163,184,.26); border-radius:22px; padding:18px 22px;
    background: radial-gradient(circle at top left, rgba(37,99,235,.22), transparent 32%), linear-gradient(135deg, rgba(15,23,42,.98), rgba(30,41,59,.92));
    box-shadow: 0 18px 40px rgba(0,0,0,.18); margin: 6px 0 14px 0;
}
.module-chip {display:inline-block; padding:5px 12px; border-radius:999px; font-size:.78rem; background:#dbeafe; color:#1e3a8a; font-weight:900; margin-bottom:10px;}
.hero-title {font-size:1.85rem; line-height:1.16; font-weight:900; color:#ffffff; margin:0 0 8px 0; letter-spacing:-.03em;}
.hero-desc {font-size:1rem; color:#d8e2ef; line-height:1.45; max-width:1050px;}
.kpi-grid {display:grid; grid-template-columns: repeat(auto-fit, minmax(245px, 1fr)); gap:14px; margin: 14px 0 12px 0;}
.kpi-card {
    position:relative; overflow:hidden; min-height:122px;
    background: linear-gradient(145deg, rgba(15,23,42,.96), rgba(31,41,55,.92));
    border:1px solid rgba(148,163,184,.28); border-radius:18px; padding:16px 18px;
    box-shadow: 0 12px 32px rgba(0,0,0,.16);
}
.kpi-card:before {content:""; position:absolute; inset:0 0 auto 0; height:3px; background:linear-gradient(90deg,#ef4444,#f59e0b,#3b82f6); opacity:.85;}
.kpi-label {color:#cbd5e1; font-size:.88rem; font-weight:800; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px;}
.kpi-value {color:#ffffff; font-size:2.05rem; line-height:1.05; font-weight:900; letter-spacing:-.04em; white-space:normal; overflow:visible; text-overflow:clip;}
.kpi-sub {color:#94a3b8; font-size:.88rem; margin-top:7px; line-height:1.25;}
.kpi-delta {color:#22c55e; font-size:.92rem; font-weight:900; margin-top:8px;}
.action-box {border-left:4px solid #60a5fa; padding:10px 12px; background:rgba(30,64,175,.24); border-radius:10px; color:#dbeafe; font-size:.92rem; margin:10px 0;}
.action-box b {color:#ffffff;}
.caption-soft {font-size:.9rem; color:#b6c2d2;}
hr.soft {border:0; border-top:1px solid rgba(148,163,184,.22); margin:18px 0;}
[data-testid="stDataFrame"] {border-radius:14px; overflow:hidden;}

.guide-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; margin: 10px 0 14px 0;}
.guide-card {
    border:1px solid rgba(148,163,184,.24); border-radius:16px; padding:12px 14px;
    background: linear-gradient(135deg, rgba(15,23,42,.78), rgba(30,41,59,.64));
    min-height:92px;
}
.guide-kicker {font-size:.76rem; color:#93c5fd; text-transform:uppercase; letter-spacing:.08em; font-weight:900; margin-bottom:5px;}
.guide-text {font-size:.92rem; color:#e5e7eb; line-height:1.35;}
.glossary-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:10px; margin:8px 0 2px 0;}
.glossary-card {
    border:1px solid rgba(148,163,184,.22); border-radius:14px; padding:10px 12px;
    background:rgba(15,23,42,.42); color:#dbeafe; font-size:.88rem; line-height:1.3;
}
.glossary-card b {color:#ffffff;}
.control-note {
    border:1px solid rgba(96,165,250,.24); background:rgba(15,23,42,.52);
    border-radius:14px; padding:10px 12px; color:#dbeafe; font-size:.9rem; margin:6px 0 12px 0;
}
.workflow-row {display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:10px; margin:12px 0;}
.workflow-step {
    border-radius:14px; padding:11px 13px; background:rgba(30,41,59,.68);
    border:1px solid rgba(148,163,184,.22); color:#e5e7eb; font-size:.9rem;
}
.workflow-step b {color:#ffffff;}


/* Oculta franja superior/toolbar de Streamlit que puede tapar títulos */

header[data-testid="stHeader"] {background: rgba(11,15,25,.92);}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_csv(name, **kwargs):
    return pd.read_csv(DATA / name, **kwargs)

@st.cache_data(show_spinner="Cargando motor territorial...")
def load_data():
    nat = load_csv('resumen_nacional_candidatos.csv')
    dep = load_csv('resultados_departamento_candidato.csv')
    mun = load_csv('resultados_municipio_candidato.csv')
    cls = load_csv('clasificacion_municipios.csv')
    margin_mun = load_csv('margen_abelardo_cepeda_municipio.csv')
    puestos = load_csv('resumen_puestos_criticos.csv.gz', compression='gzip')
    transfer = load_csv('transferencias_base_2v.csv')
    fuentes = load_csv('fuentes_contexto_2v.csv')
    return nat, dep, mun, cls, margin_mun, puestos, transfer, fuentes

nat, dep, mun, cls, margin_mun, puestos, transfer, fuentes = load_data()

CAND_AB = 'ABELARDO DE LA ESPRIELLA'
CAND_CE = 'IVAN CEPEDA'

MODULE_INFO = {
    "1. Comando nacional": {
        "tag": "Panorama general",
        "title": "Comando nacional",
        "desc": "Foto ejecutiva del resultado nacional, tamaño de cada candidatura, margen base y bolsas de transferencia para segunda vuelta.",
        "how": ["Revisa votos totales, válidos y margen base.", "Usa el ranking para identificar las bolsas electorales disponibles.", "La lectura estratégica muestra cuánto pesan eliminados, blanco, nulo y no marcado."]
    },
    "2. Dominio territorial": {
        "tag": "Fortalezas territoriales",
        "title": "Dominio territorial",
        "desc": "Identifica dónde cada candidato es fuerte por volumen, por porcentaje de dominio y por oportunidad territorial.",
        "how": ["Selecciona candidato y nivel: departamento o municipio.", "Ordena por votación, porcentaje de dominio o bolsa por definir.", "Usa los filtros laterales para analizar un departamento o municipio específico; en Bogotá, municipio equivale a localidad."]
    },
    "3. Municipios bisagra": {
        "tag": "Competencia cerrada",
        "title": "Municipios bisagra",
        "desc": "Detecta municipios donde Abelardo y Cepeda están cerca y donde una intervención territorial puede tener alto impacto.",
        "how": ["Sube votos válidos mínimos para evitar municipios pequeños.", "Baja el margen máximo para encontrar disputas más cerradas.", "Prioriza territorios con alta bolsa por definir y alto índice de oportunidad."]
    },
    "4. Bolsa por definir": {
        "tag": "Potencial electoral",
        "title": "Bolsa por definir",
        "desc": "Localiza reserva electoral: abstención estimada, voto blanco, voto nulo y no marcado.",
        "how": ["Escoge la variable principal que quieres leer.", "Filtra por departamento o municipio.", "Cruza bolsa alta con municipios cerrados para focalizar pedagogía y movilización."]
    },
    "5. Puestos críticos": {
        "tag": "Operación electoral",
        "title": "Puestos críticos",
        "desc": "Baja hasta puesto de votación para priorizar testigos, control electoral, pedagogía y operación de cierre.",
        "how": ["Filtra territorio y define votos mínimos por puesto.", "Ordena por índice estratégico, bolsa, margen o votación.", "Usa la tabla y el mapa para asignar recursos operativos."]
    },
    "6. Simulador 2ª vuelta": {
        "tag": "Escenarios 2V",
        "title": "Simulador de segunda vuelta",
        "desc": "Construye escenarios con transferencias de candidatos eliminados y captura parcial de la bolsa por definir.",
        "how": ["Elige escenario base: conservador, realista o agresivo.", "Ajusta sliders por candidato eliminado.", "Lee resultado nacional, composición del voto y municipios más cerrados."]
    },
    "7. Fuentes y metodología": {
        "tag": "Transparencia",
        "title": "Fuentes y metodología",
        "desc": "Documenta la construcción del tablero, los supuestos y el uso adecuado de las métricas.",
        "how": ["Valida la fuente de datos.", "Revisa cómo se calculan bolsa, margen e índice.", "Contrasta los supuestos antes de presentar conclusiones."]
    }
}

MODULE_GUIDE = {
    "1. Comando nacional": {
        "watch": "La diferencia Abelardo-Cepeda, el peso de candidatos eliminados y el tamaño de voto blanco/nulo/no marcado.",
        "adjust": "No requiere ajustes complejos: usa las pestañas Ranking y Lectura estratégica para pasar de foto general a lectura de oportunidad.",
        "decision": "Define el punto de partida nacional y el tamaño real de las bolsas que pueden moverse en segunda vuelta.",
        "glossary": [
            ("Votos MMV", "total registrado en el archivo de preconteo."),
            ("Votos válidos", "candidatos + voto en blanco."),
            ("Margen base", "diferencia inicial Abelardo - Cepeda antes de transferencias.")
        ]
    },
    "2. Dominio territorial": {
        "watch": "Dónde cada candidato tiene más votos, dónde domina porcentualmente y dónde existe oportunidad de crecimiento.",
        "adjust": "Cambia candidato, nivel territorial y criterio de ordenamiento. Usa filtros de departamento/municipio para análisis local.",
        "decision": "Clasifica territorios para defensa, expansión o contención política.",
        "glossary": [
            ("Mayor votación", "territorios que aportan más caudal electoral."),
            ("Mayor porcentaje de dominio", "territorios donde el candidato pesa más sobre votos válidos."),
            ("Bolsa por definir", "abstención estimada + blanco + nulo + no marcado.")
        ]
    },
    "3. Municipios bisagra": {
        "watch": "Municipios donde Abelardo y Cepeda están cerca y además existe bolsa por definir.",
        "adjust": "Sube votos válidos mínimos para enfocarte en territorios grandes; baja margen máximo para ver disputas más cerradas.",
        "decision": "Prioriza municipios donde una operación focalizada podría cambiar el resultado.",
        "glossary": [
            ("Margen máximo", "distancia permitida entre Abelardo y Cepeda."),
            ("Índice de oportunidad", "ranking que combina margen cerrado + bolsa por definir."),
            ("Ganador base 2V", "quién va arriba solo comparando Abelardo vs Cepeda en primera vuelta.")
        ]
    },
    "4. Bolsa por definir": {
        "watch": "Dónde hay mayor reserva electoral por abstención, voto blanco, nulo o no marcado.",
        "adjust": "Cambia la variable principal y cruza con filtros territoriales.",
        "decision": "Detecta territorios para pedagogía electoral, narrativa de segunda vuelta y movilización.",
        "glossary": [
            ("Abstención estimada", "potencial DIVIPOL menos votos registrados en MMV."),
            ("Voto blanco", "voto válido sin preferencia por candidatos."),
            ("Nulo/no marcado", "posible error, rechazo o baja pedagogía electoral.")
        ]
    },
    "5. Puestos críticos": {
        "watch": "Puestos de votación con margen estrecho, alta bolsa por definir o alta votación válida.",
        "adjust": "Define votos mínimos y criterio de priorización. Después revisa tabla o mapa.",
        "decision": "Asignación operativa de testigos, coordinadores, pedagogía y movilización de cierre.",
        "glossary": [
            ("Índice estratégico", "prioriza puestos cerrados y con potencial de crecimiento."),
            ("Menor margen", "puestos donde Abelardo y Cepeda están más cerca."),
            ("Mapa", "ubica espacialmente los puestos priorizados.")
        ]
    },
    "6. Simulador 2ª vuelta": {
        "watch": "Resultado nacional proyectado, composición del voto y municipios que se vuelven más cerrados.",
        "adjust": "Elige escenario base y mueve sliders de transferencias, fuga y captura de bolsa.",
        "decision": "Evalúa escenarios de segunda vuelta y detecta territorios sensibles bajo cada supuesto.",
        "glossary": [
            ("Transferencia", "votos de candidatos eliminados que migran a finalistas."),
            ("Fuga", "voto que no se convierte en segunda vuelta."),
            ("Bolsa activada", "parte de abstención/blanco/nulo/no marcado que se convierte en voto efectivo.")
        ]
    },
    "7. Fuentes y metodología": {
        "watch": "Origen de datos, reglas de cálculo y supuestos políticos del simulador.",
        "adjust": "No simula; sirve para auditar la lectura antes de presentar resultados.",
        "decision": "Permite explicar y defender técnicamente el tablero.",
        "glossary": [
            ("MMV", "preconteo por mesa y candidato/código."),
            ("DIVIPOL", "estructura territorial y puestos de votación."),
            ("Supuestos", "porcentajes editables, no hechos definitivos.")
        ]
    }
}


def fmt_int(x):
    try:
        return f"{int(round(float(x))):,}".replace(',', '.')
    except Exception:
        return "—"


def fmt_short(x):
    try:
        x = float(x)
    except Exception:
        return "—"
    sign = "-" if x < 0 else ""
    x = abs(x)
    if x >= 1_000_000:
        return sign + f"{x/1_000_000:.2f} M".replace('.', ',')
    if x >= 1_000:
        return sign + fmt_int(x)
    return sign + fmt_int(x)


def fmt_pct(x, decimals=1):
    try:
        return f"{float(x)*100:.{decimals}f}%".replace('.', ',')
    except Exception:
        return "—"


def kpi_grid(items):
    """items: list of dicts {label, value, sub, delta}. Uses custom HTML, no st.metric truncation."""
    cards = []
    for item in items:
        label = html.escape(str(item.get('label', '')))
        value = html.escape(str(item.get('value', '—')))
        sub = item.get('sub', '')
        delta = item.get('delta', '')
        sub_html = f'<div class="kpi-sub">{html.escape(str(sub))}</div>' if sub not in [None, ''] else ''
        delta_html = f'<div class="kpi-delta">↗ {html.escape(str(delta))}</div>' if delta not in [None, '', '—'] else ''
        cards.append(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub_html}{delta_html}</div>')
    st.markdown('<div class="kpi-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)


def module_header(key):
    meta = MODULE_INFO[key]
    guide = MODULE_GUIDE.get(key, {})
    st.markdown(
        f"""
        <div class="hero-box">
            <div class="module-chip">{html.escape(meta['tag'])}</div>
            <div class="hero-title">{html.escape(meta['title'])}</div>
            <div class="hero-desc">{html.escape(meta['desc'])}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="guide-grid">
            <div class="guide-card">
                <div class="guide-kicker">Qué mirar</div>
                <div class="guide-text">{html.escape(guide.get('watch', 'Identifica los indicadores principales del módulo.'))}</div>
            </div>
            <div class="guide-card">
                <div class="guide-kicker">Qué puedes ajustar</div>
                <div class="guide-text">{html.escape(guide.get('adjust', 'Usa filtros y controles para bajar el análisis.'))}</div>
            </div>
            <div class="guide-card">
                <div class="guide-kicker">Decisión que habilita</div>
                <div class="guide-text">{html.escape(guide.get('decision', 'Convierte datos en priorización territorial.'))}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Glosario rápido del módulo", expanded=False):
        cards = []
        for term, definition in guide.get('glossary', []):
            cards.append(f'<div class="glossary-card"><b>{html.escape(term)}</b><br>{html.escape(definition)}</div>')
        if cards:
            st.markdown('<div class="glossary-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
        else:
            for item in meta['how']:
                st.markdown(f"- {item}")


def action_note(text):
    st.markdown(f'<div class="action-box">{text}</div>', unsafe_allow_html=True)


def filter_df(df, depto_filter, mpio_filter):
    out = df.copy()
    if depto_filter != 'TODOS' and 'departamento_nombre' in out.columns:
        out = out[out['departamento_nombre'] == depto_filter]
    if mpio_filter != 'TODOS' and 'municipio_nombre' in out.columns:
        out = out[out['municipio_nombre'] == mpio_filter]
    return out


def get_scope_label(depto_filter, mpio_filter):
    if depto_filter == 'TODOS':
        return 'Colombia'
    if mpio_filter == 'TODOS':
        return depto_filter
    return f'{mpio_filter}, {depto_filter}'


def scoped_municipal_votes(depto_filter, mpio_filter):
    """Resultados por candidato/tipo de voto conectados al filtro territorial."""
    return filter_df(mun, depto_filter, mpio_filter)


def scoped_margin(depto_filter, mpio_filter):
    """Márgenes Abelardo-Cepeda y bolsa conectados al filtro territorial."""
    return filter_df(margin_mun, depto_filter, mpio_filter)


def build_scope_ranking(mun_scope):
    """Ranking por candidato/tipo de voto para el territorio filtrado."""
    if mun_scope.empty:
        return pd.DataFrame(columns=[
            'ranking_nacional', 'candidato', 'nombre_candidato', 'tipo_registro',
            'estado_primera_vuelta', 'votos', 'pct_validos', 'pct_total_mmv'
        ])
    group_cols = ['candidato', 'nombre_candidato', 'tipo_registro', 'estado_primera_vuelta']
    out = mun_scope.groupby(group_cols, as_index=False)['votos'].sum()
    total = out['votos'].sum()
    valid_mask = out['tipo_registro'].isin(['CANDIDATO', 'VOTO_EN_BLANCO'])
    valid = out.loc[valid_mask, 'votos'].sum()
    out['pct_validos'] = np.where(valid_mask & (valid > 0), out['votos'] / valid, np.nan)
    out['pct_total_mmv'] = np.where(total > 0, out['votos'] / total, np.nan)
    out = out.sort_values('votos', ascending=False).reset_index(drop=True)
    out.insert(0, 'ranking_nacional', range(1, len(out) + 1))
    return out


# Bases nacionales
nat_base = nat.copy()
ab_votes = nat_base.loc[nat_base['nombre_candidato'].eq(CAND_AB), 'votos'].sum()
ce_votes = nat_base.loc[nat_base['nombre_candidato'].eq(CAND_CE), 'votos'].sum()
valid_votes = nat_base.loc[nat_base['tipo_registro'].isin(['CANDIDATO', 'VOTO_EN_BLANCO']), 'votos'].sum()
total_votes = nat_base['votos'].sum()

with st.sidebar:
    st.title("🧭 Máquina territorial")
    st.caption("Presidencia 2026 | MMV + DIVIPOL")
    modulo = st.radio("Módulo", list(MODULE_INFO.keys()), help="Cambia entre lectura nacional, territorial, operativa y simulación de segunda vuelta.")
    st.divider()
    st.markdown("### Filtros territoriales")
    st.caption("Sirven para bajar el análisis de Nación a departamento o municipio. Casi todos los módulos se recalculan con estos filtros.")
    deptos = ['TODOS'] + sorted([x for x in mun['departamento_nombre'].dropna().unique()])
    depto_filter = st.selectbox("Departamento", deptos, help="Selecciona un departamento para recalcular gráficos, KPIs y tablas sobre ese territorio.")
    if depto_filter != 'TODOS':
        municipios = ['TODOS'] + sorted(mun.loc[mun['departamento_nombre'] == depto_filter, 'municipio_nombre'].dropna().unique().tolist())
    else:
        municipios = ['TODOS']
    mpio_filter = st.selectbox("Municipio", municipios, help="Disponible después de elegir departamento. Útil para análisis fino y operativo.")
    
    st.caption(f"Filtro activo: {depto_filter} / {mpio_filter}")
    if depto_filter == "BOGOTA D.C.":
        st.info("En Bogotá, el filtro Municipio se interpreta como localidad DIVIPOL: Zona 01 = Usaquén, Zona 02 = Chapinero, etc. También se conservan zonas especiales 90 y 98.")
    st.markdown("### Lectura del módulo")
    st.caption(MODULE_GUIDE[modulo]["decision"])


st.markdown('<div class="main-title">Presidencia 2026 | Máquina de estrategia territorial</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Lectura territorial, priorización operativa y simulación de segunda vuelta a partir de MMV + DIVIPOL. Bogotá se analiza por localidades derivadas de zona DIVIPOL.</div>', unsafe_allow_html=True)

with st.expander("Guía rápida del tablero: ruta sugerida de análisis", expanded=False):
    st.markdown("""
    - **Comando nacional:** foto macro y bolsas de transferencia.  
    - **Dominio territorial:** fortalezas por candidato.  
    - **Municipios bisagra:** competencia cerrada entre Abelardo y Cepeda.  
    - **Bolsa por definir:** reserva electoral y pedagogía.  
    - **Puestos críticos:** operación electoral focalizada.  
    - **Simulador:** escenarios de transferencia y segunda vuelta.  
    - **Bogotá:** el filtro de municipio equivale a localidad según zona DIVIPOL.
    """)

if modulo == "1. Comando nacional":
    module_header(modulo)
    scope_name = get_scope_label(depto_filter, mpio_filter)
    scope_votes = scoped_municipal_votes(depto_filter, mpio_filter)
    view = build_scope_ranking(scope_votes)

    scope_total = view['votos'].sum() if not view.empty else 0
    scope_valid = view.loc[view['tipo_registro'].isin(['CANDIDATO', 'VOTO_EN_BLANCO']), 'votos'].sum() if not view.empty else 0
    scope_ab = view.loc[view['nombre_candidato'].eq(CAND_AB), 'votos'].sum() if not view.empty else 0
    scope_ce = view.loc[view['nombre_candidato'].eq(CAND_CE), 'votos'].sum() if not view.empty else 0

    action_note(f"<b>Filtro activo:</b> {html.escape(scope_name)}. Todos los KPIs, ranking y lectura estratégica de este módulo se recalculan sobre este territorio.")

    if scope_total == 0:
        st.warning("No hay datos para el filtro territorial seleccionado.")
    else:
        kpi_grid([
            {'label': 'Votos MMV', 'value': fmt_short(scope_total), 'sub': f'{fmt_int(scope_total)} registros de voto'},
            {'label': 'Votos válidos', 'value': fmt_short(scope_valid), 'sub': f'{fmt_int(scope_valid)} votos válidos'},
            {'label': 'Abelardo', 'value': fmt_short(scope_ab), 'sub': f'{fmt_int(scope_ab)} votos', 'delta': fmt_pct(scope_ab / scope_valid) if scope_valid else '—'},
            {'label': 'Cepeda', 'value': fmt_short(scope_ce), 'sub': f'{fmt_int(scope_ce)} votos', 'delta': fmt_pct(scope_ce / scope_valid) if scope_valid else '—'},
            {'label': 'Margen base', 'value': fmt_short(scope_ab - scope_ce), 'sub': 'Abelardo - Cepeda', 'delta': fmt_pct((scope_ab - scope_ce) / scope_valid) if scope_valid else '—'},
        ])
        st.caption("Los porcentajes de Abelardo y Cepeda se calculan sobre votos válidos del filtro activo. El margen base es la diferencia antes de simular transferencias.")

        tab1, tab2 = st.tabs(["Ranking del territorio", "Lectura estratégica"])
        with tab1:
            fig = px.bar(
                view,
                x='nombre_candidato',
                y='votos',
                text=view['pct_validos'].apply(lambda x: fmt_pct(x) if pd.notna(x) else ''),
                color='tipo_registro',
                title=f'Resultado por candidato / tipo de voto · {scope_name}'
            )
            fig.update_layout(xaxis_title='', yaxis_title='Votos', xaxis_tickangle=-35, height=520)
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Tip: ordenado de mayor a menor votación. Úsalo para dimensionar las bolsas de transferencia del territorio seleccionado.")
            st.dataframe(view, use_container_width=True, hide_index=True)
            st.download_button("Descargar ranking del territorio", view.to_csv(index=False).encode('utf-8'), "ranking_territorial_presidencia_2026.csv", "text/csv")
        with tab2:
            action_note("<b>Lectura:</b> esta sección identifica cuántos votos podrían entrar en juego en segunda vuelta dentro del filtro activo: candidatos eliminados, voto blanco, voto nulo y no marcado.")
            otros = view[(view['tipo_registro'] == 'CANDIDATO') & (~view['nombre_candidato'].isin([CAND_AB, CAND_CE]))]['votos'].sum()
            blanco = view.loc[view['nombre_candidato'].eq('VOTO EN BLANCO'), 'votos'].sum()
            nulo_nm = view.loc[view['nombre_candidato'].isin(['VOTO NULO', 'NO MARCADOS']), 'votos'].sum()
            kpi_grid([
                {'label': 'Candidatos eliminados', 'value': fmt_short(otros), 'sub': f'{fmt_int(otros)} votos', 'delta': fmt_pct(otros / scope_total) if scope_total else '—'},
                {'label': 'Voto en blanco', 'value': fmt_short(blanco), 'sub': f'{fmt_int(blanco)} votos', 'delta': fmt_pct(blanco / scope_total) if scope_total else '—'},
                {'label': 'Nulo + no marcado', 'value': fmt_short(nulo_nm), 'sub': f'{fmt_int(nulo_nm)} votos', 'delta': fmt_pct(nulo_nm / scope_total) if scope_total else '—'},
            ])

elif modulo == "2. Dominio territorial":
    module_header(modulo)
    c0, c1, c2, c3 = st.columns([1, 1.35, 1.15, .85])
    nivel = c0.radio("Nivel", ['Departamento', 'Municipio'], horizontal=False, help="Departamento = lectura macro; Municipio = lectura fina para priorización territorial.")
    if mpio_filter != 'TODOS' and nivel == 'Departamento':
        action_note("<b>Filtro municipal activo:</b> para respetar el municipio seleccionado, la lectura cambia automáticamente a nivel municipal.")
        nivel = 'Municipio'
    candidatos = sorted(dep.loc[dep['tipo_registro'] == 'CANDIDATO', 'nombre_candidato'].dropna().unique().tolist())
    candidato = c1.selectbox("Candidato", candidatos, index=candidatos.index(CAND_AB) if CAND_AB in candidatos else 0, help="Permite comparar la geografía electoral de cada candidatura.")
    criterio_label = c2.selectbox("Ordenar por", ['Mayor votación', 'Mayor porcentaje de dominio', 'Mayor bolsa por definir'], help="Votación = volumen; porcentaje = dominancia; bolsa = oportunidad potencial.")
    topn = c3.slider("Top", 10, 80, 30, 5, help="Controla cuántos territorios se muestran en el gráfico principal.")
    criterio_map = {'Mayor votación': 'votos', 'Mayor porcentaje de dominio': 'pct_validos', 'Mayor bolsa por definir': 'bolsa_indefinida'}
    criterio = criterio_map[criterio_label]

    if nivel == 'Departamento':
        df = dep[(dep['nombre_candidato'] == candidato)].copy()
        dept_bolsa = margin_mun.groupby('departamento_nombre', as_index=False)['bolsa_indefinida'].sum()
        df = df.merge(dept_bolsa, on='departamento_nombre', how='left')
        df = filter_df(df, depto_filter, mpio_filter)
        sort_col = criterio if criterio in df.columns else 'votos'
        df = df.sort_values(sort_col, ascending=False)
        if df.empty:
            st.warning('No hay datos para el filtro territorial seleccionado.')
            st.stop()
        ycol = 'pct_validos' if criterio == 'pct_validos' else 'votos'
        fig = px.bar(df.head(topn), x='departamento_nombre', y=ycol, text='votos', title=f'{candidato} | Departamentos principales')
        fig.update_layout(xaxis_tickangle=-35, yaxis_title='Votos' if ycol == 'votos' else '% sobre válidos', height=520)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Votos muestra caudal; porcentaje de dominio muestra fuerza relativa; bolsa por definir muestra oportunidad de crecimiento.")
        st.dataframe(df[['departamento_nombre', 'votos', 'pct_validos', 'bolsa_indefinida', 'votos_validos', 'potencial', 'abstencion_estimada_depto']], use_container_width=True, hide_index=True)
    else:
        df = mun[(mun['nombre_candidato'] == candidato)].copy()
        df = filter_df(df, depto_filter, mpio_filter)
        df = df.merge(cls[['departamento', 'municipio', 'categoria_territorial', 'ganador', 'margen_pp', 'bolsa_indefinida']], on=['departamento', 'municipio'], how='left')
        sort_col = criterio if criterio in df.columns else 'votos'
        df = df.sort_values(sort_col, ascending=False)
        if df.empty:
            st.warning('No hay datos para el filtro territorial seleccionado.')
            st.stop()
        fig = px.scatter(df.head(700), x='pct_validos', y='votos', size='bolsa_indefinida', color='categoria_territorial', hover_name='municipio_nombre', hover_data=['departamento_nombre', 'ganador', 'margen_pp'], title=f'{candidato} | Fuerza municipal')
        fig.update_layout(xaxis_title='% sobre votos válidos', yaxis_title='Votos', height=560)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Punto alto = más votos; punto a la derecha = mayor dominio; círculo grande = mayor bolsa por definir.")
        st.dataframe(df[['departamento_nombre', 'municipio_nombre', 'nombre_candidato', 'votos', 'pct_validos', 'ganador', 'margen_pp', 'bolsa_indefinida', 'categoria_territorial']].head(1000), use_container_width=True, hide_index=True)
        st.download_button("Descargar municipios filtrados", df.to_csv(index=False).encode('utf-8'), "dominio_municipal.csv", "text/csv")

elif modulo == "3. Municipios bisagra":
    module_header(modulo)
    df = filter_df(margin_mun, depto_filter, mpio_filter)
    c1, c2 = st.columns(2)
    max_validos = int(max(1000, df['votos_validos'].max() if not df.empty else 1000))
    min_validos = c1.slider("Votos válidos mínimos", 0, max_validos, min(5000, max_validos), step=1000, help="Sirve para excluir municipios pequeños y concentrar el análisis en territorios con peso electoral.")
    margen_max = c2.slider("Margen máximo permitido", 0.0, 30.0, 7.0, step=0.5, help="Entre menor sea el margen, más cerrados serán los municipios seleccionados.") / 100
    df = df[(df['votos_validos'] >= min_validos) & (df['margen_pp_validos'] <= margen_max)].copy()
    df = df.sort_values(['score_oportunidad', 'bolsa_indefinida'], ascending=False)
    kpi_grid([
        {'label': 'Municipios bisagra', 'value': fmt_int(len(df)), 'sub': 'Cumplen el filtro de margen'},
        {'label': 'Bolsa por definir', 'value': fmt_short(df['bolsa_indefinida'].sum()), 'sub': f'{fmt_int(df["bolsa_indefinida"].sum())} votos potenciales'},
        {'label': 'Votos válidos involucrados', 'value': fmt_short(df['votos_validos'].sum()), 'sub': f'{fmt_int(df["votos_validos"].sum())} votos válidos'},
    ])
    action_note("<b>Índice de oportunidad:</b> prioriza municipios con dos señales juntas: margen cerrado y alta bolsa por definir.")
    if not df.empty:
        fig = px.scatter(df, x='margen_pp_validos', y='bolsa_indefinida', size='votos_validos', color='ganador_2v_base', hover_name='municipio_nombre', hover_data=['departamento_nombre', 'votos_abelardo', 'votos_cepeda', 'margen_abs', 'score_oportunidad'], title='Matriz bisagra: margen estrecho vs bolsa por definir')
        fig.update_layout(xaxis_title='Margen en puntos sobre votos válidos', yaxis_title='Bolsa por definir', height=560)
        st.plotly_chart(fig, use_container_width=True)
    display_bis = df[['departamento_nombre', 'municipio_nombre', 'ganador_2v_base', 'votos_abelardo', 'votos_cepeda', 'margen_abelardo_vs_cepeda', 'margen_pp_validos', 'bolsa_indefinida', 'score_oportunidad']].head(600).rename(columns={
        'departamento_nombre': 'Departamento', 'municipio_nombre': 'Municipio', 'ganador_2v_base': 'Ganador base 2V',
        'votos_abelardo': 'Votos Abelardo', 'votos_cepeda': 'Votos Cepeda', 'margen_abelardo_vs_cepeda': 'Margen Abelardo - Cepeda',
        'margen_pp_validos': 'Margen sobre válidos', 'bolsa_indefinida': 'Bolsa por definir', 'score_oportunidad': 'Índice de oportunidad'
    })
    st.dataframe(display_bis, use_container_width=True, hide_index=True)
    st.download_button("Descargar municipios bisagra", df.to_csv(index=False).encode('utf-8'), "municipios_bisagra.csv", "text/csv")

elif modulo == "4. Bolsa por definir":
    module_header(modulo)
    df = filter_df(margin_mun, depto_filter, mpio_filter)
    c1, c2 = st.columns([1, 1])
    var_label = c1.selectbox("Variable principal", ['Bolsa total', 'Abstención estimada', 'Voto en blanco', 'Voto nulo', 'No marcados'], help="Escoge qué tipo de reserva electoral quieres analizar.")
    var_map = {'Bolsa total': 'bolsa_indefinida', 'Abstención estimada': 'abstencion_estimada', 'Voto en blanco': 'voto_blanco', 'Voto nulo': 'voto_nulo', 'No marcados': 'no_marcados'}
    variable = var_map[var_label]
    topn = c2.slider("Top municipios", 10, 100, 30, 5, help="Número de municipios visibles en el ranking gráfico.")
    df = df.sort_values(variable, ascending=False)
    kpi_grid([
        {'label': 'Bolsa total', 'value': fmt_short(df['bolsa_indefinida'].sum()), 'sub': f'{fmt_int(df["bolsa_indefinida"].sum())} votos potenciales'},
        {'label': 'Abstención estimada', 'value': fmt_short(df['abstencion_estimada'].sum()), 'sub': f'{fmt_int(df["abstencion_estimada"].sum())} ciudadanos'},
        {'label': 'Blanco + nulo + no marcado', 'value': fmt_short(df[['voto_blanco', 'voto_nulo', 'no_marcados']].sum().sum()), 'sub': 'Voto inconforme o mal canalizado'},
        {'label': 'Municipios', 'value': fmt_int(len(df)), 'sub': 'En el filtro actual'},
    ])
    st.caption("La bolsa por definir no equivale a voto capturable automático. Es un indicador de potencial para pedagogía, narrativa y movilización.")
    fig = px.bar(df.head(topn), x='municipio_nombre', y=variable, color='departamento_nombre', hover_data=['ganador_2v_base', 'margen_pp_validos', 'votos_validos'], title=f'Top municipios por {var_label}')
    fig.update_layout(xaxis_tickangle=-35, xaxis_title='Municipio', height=540)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[['departamento_nombre', 'municipio_nombre', 'ganador_2v_base', 'votos_validos', 'margen_pp_validos', 'abstencion_estimada', 'voto_blanco', 'voto_nulo', 'no_marcados', 'bolsa_indefinida']].head(1000), use_container_width=True, hide_index=True)
    st.download_button("Descargar bolsa por definir", df.to_csv(index=False).encode('utf-8'), "bolsa_por_definir.csv", "text/csv")

elif modulo == "5. Puestos críticos":
    module_header(modulo)
    df = filter_df(puestos, depto_filter, mpio_filter)
    c1, c2 = st.columns(2)
    max_validos = int(max(1000, df['votos_validos'].max() if not df.empty else 1000))
    min_validos = c1.slider("Votos válidos mínimos por puesto", 0, max_validos, min(500, max_validos), step=100, help="Filtra puestos demasiado pequeños cuando quieras priorizar impacto operativo.")
    criterio_label = c2.selectbox("Priorizar por", ['Índice estratégico de oportunidad', 'Mayor bolsa por definir', 'Menor margen entre Abelardo y Cepeda', 'Mayor votación válida'], help="Índice = combina cierre competitivo y oportunidad. Margen = diferencia Abelardo-Cepeda. Bolsa = potencial de crecimiento.")
    criterio_map = {'Índice estratégico de oportunidad': 'score_oportunidad', 'Mayor bolsa por definir': 'bolsa_indefinida', 'Menor margen entre Abelardo y Cepeda': 'margen_abs', 'Mayor votación válida': 'votos_validos'}
    criterio = criterio_map[criterio_label]
    df = df[df['votos_validos'] >= min_validos].copy()
    asc = criterio == 'margen_abs'
    df = df.sort_values(criterio, ascending=asc)
    action_note("<b>Índice estratégico:</b> combina competencia cerrada y bolsa por definir. <b>Menor margen</b> identifica puestos donde la diferencia Abelardo-Cepeda es más pequeña.")
    kpi_grid([
        {'label': 'Puestos filtrados', 'value': fmt_int(len(df)), 'sub': 'Puestos que cumplen criterios'},
        {'label': 'Bolsa por definir', 'value': fmt_short(df['bolsa_indefinida'].sum()), 'sub': f'{fmt_int(df["bolsa_indefinida"].sum())} votos potenciales'},
        {'label': 'Votos válidos', 'value': fmt_short(df['votos_validos'].sum()), 'sub': f'{fmt_int(df["votos_validos"].sum())} votos válidos'},
    ])
    table = df[['departamento_nombre', 'municipio_nombre', 'zona', 'puesto', 'puesto_nombre', 'direccion', 'ganador_2v_base', 'votos_abelardo', 'votos_cepeda', 'margen_abelardo_vs_cepeda', 'margen_pp_validos', 'bolsa_indefinida', 'score_oportunidad', 'latitud', 'longitud']].head(1500).rename(columns={
        'departamento_nombre': 'Departamento', 'municipio_nombre': 'Municipio', 'zona': 'Zona', 'puesto': 'Código puesto', 'puesto_nombre': 'Puesto',
        'direccion': 'Dirección', 'ganador_2v_base': 'Ganador base 2V', 'votos_abelardo': 'Votos Abelardo', 'votos_cepeda': 'Votos Cepeda',
        'margen_abelardo_vs_cepeda': 'Margen Abelardo - Cepeda', 'margen_pp_validos': 'Margen sobre válidos', 'bolsa_indefinida': 'Bolsa por definir',
        'score_oportunidad': 'Índice estratégico', 'latitud': 'Latitud', 'longitud': 'Longitud'
    })
    tab1, tab2 = st.tabs(["Tabla priorizada", "Mapa de puestos"])
    with tab1:
        st.dataframe(table, use_container_width=True, hide_index=True)
    with tab2:
        mapdf = table.dropna(subset=['Latitud', 'Longitud']).copy()
        if len(mapdf) > 0:
            fig = px.scatter_mapbox(mapdf.head(1000), lat='Latitud', lon='Longitud', size='Bolsa por definir', color='Ganador base 2V', hover_name='Puesto', hover_data=['Departamento', 'Municipio', 'Dirección', 'Margen Abelardo - Cepeda'], zoom=4, height=650, mapbox_style='open-street-map', title='Mapa de puestos críticos')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay coordenadas disponibles para el filtro actual.")
    st.download_button("Descargar puestos críticos", df.to_csv(index=False).encode('utf-8'), "puestos_criticos.csv", "text/csv")

elif modulo == "6. Simulador 2ª vuelta":
    module_header(modulo)
    scope_name = get_scope_label(depto_filter, mpio_filter)
    mun_scope = scoped_municipal_votes(depto_filter, mpio_filter)
    margin_scope = scoped_margin(depto_filter, mpio_filter)

    action_note(f"<b>Filtro activo:</b> {html.escape(scope_name)}. La simulación nacional, la composición del voto y la lectura territorial se calculan sobre este territorio.")

    if mun_scope.empty:
        st.warning("No hay datos para el filtro territorial seleccionado.")
    else:
        cA, cB = st.columns([1.1, 1])
        escenario = cA.selectbox("Escenario base", ['realista', 'conservador', 'agresivo'], help="Carga un punto de partida. Conservador = menor transferencia/captura; agresivo = mayor transferencia/captura.")
        with cB:
            action_note("<b>Lectura:</b> cambia sliders y mira cómo varían el resultado del filtro activo, la composición del voto y los municipios más cerrados.")

        st.markdown("""
        <div class="workflow-row">
            <div class="workflow-step"><b>1. Escenario</b><br>Elige punto de partida.</div>
            <div class="workflow-step"><b>2. Transferencias</b><br>Ajusta voto de eliminados.</div>
            <div class="workflow-step"><b>3. Bolsa</b><br>Define cuánto voto nuevo entra.</div>
            <div class="workflow-step"><b>4. Territorio</b><br>Revisa municipios sensibles.</div>
        </div>
        """, unsafe_allow_html=True)

        rows = []
        colA, colB = st.columns([1.15, .85])
        with colA:
            st.markdown("#### Transferencia de candidatos eliminados")
            st.caption("Estos porcentajes se aplican sobre la votación de cada candidato eliminado dentro del filtro activo.")
            for _, r in transfer.iterrows():
                default_ab = int(r[f'pct_abelardo_{escenario}'])
                default_ce = int(r[f'pct_cepeda_{escenario}'])
                default_fuga = max(0, 100 - default_ab - default_ce)
                with st.expander(f"{r['candidato']}", expanded=False):
                    st.caption(r['nota'])
                    pct_ab = st.slider(f"% hacia Abelardo · {r['candidato']}", 0, 100, default_ab, 1, key=f"ab_{r['codigo']}_{scope_name}_{escenario}")
                    pct_fuga = st.slider(f"% fuga / abstención · {r['candidato']}", 0, 80, default_fuga, 1, key=f"fg_{r['codigo']}_{scope_name}_{escenario}")
                    pct_ce = max(0, 100 - pct_ab - pct_fuga)
                    st.caption(f"Cepeda recibiría automáticamente el {pct_ce}% restante.")
                rows.append({'codigo': int(r['codigo']), 'candidato': r['candidato'], 'pct_abelardo': pct_ab / 100, 'pct_cepeda': pct_ce / 100, 'pct_fuga': pct_fuga / 100})
        with colB:
            st.markdown("#### Captura de bolsa por definir")
            st.caption("Estos porcentajes se aplican sobre voto blanco, nulo/no marcado y abstención estimada del filtro activo.")
            activar_blanco = st.slider("% del voto blanco que se mueve", 0, 100, 35, 1, key=f"blanco_{scope_name}") / 100
            activar_nulo = st.slider("% del nulo / no marcado recuperable", 0, 100, 15, 1, key=f"nulo_{scope_name}") / 100
            activar_abst = st.slider("% de abstención movilizable", 0, 100, 8, 1, key=f"abst_{scope_name}") / 100
            split_ab = st.slider("De la bolsa activada, % que capta Abelardo", 0, 100, 52, 1, key=f"split_{scope_name}") / 100
            split_ce = 1 - split_ab
            st.caption(f"Cepeda captaría automáticamente el {split_ce * 100:.0f}% restante de la bolsa activada.")

        transfer_user = pd.DataFrame(rows)

        # Resultado proyectado sobre el filtro activo
        ranking_scope = build_scope_ranking(mun_scope)
        cand_scope = ranking_scope[ranking_scope['tipo_registro'] == 'CANDIDATO'].copy()
        base_ab = cand_scope.loc[cand_scope['nombre_candidato'].eq(CAND_AB), 'votos'].sum()
        base_ce = cand_scope.loc[cand_scope['nombre_candidato'].eq(CAND_CE), 'votos'].sum()

        elim = cand_scope[~cand_scope['nombre_candidato'].isin([CAND_AB, CAND_CE])][['candidato', 'nombre_candidato', 'votos']].merge(
            transfer_user, left_on='candidato', right_on='codigo', how='left'
        )
        ab_from_elim = (elim['votos'] * elim['pct_abelardo']).sum()
        ce_from_elim = (elim['votos'] * elim['pct_cepeda']).sum()
        fuga = (elim['votos'] * elim['pct_fuga']).sum()

        blanc = ranking_scope.loc[ranking_scope['nombre_candidato'].eq('VOTO EN BLANCO'), 'votos'].sum()
        nulos_nm = ranking_scope.loc[ranking_scope['nombre_candidato'].isin(['VOTO NULO', 'NO MARCADOS']), 'votos'].sum()
        abst = margin_scope['abstencion_estimada'].sum() if not margin_scope.empty else 0
        bolsa_activada = blanc * activar_blanco + nulos_nm * activar_nulo + abst * activar_abst

        ab_proj = base_ab + ab_from_elim + bolsa_activada * split_ab
        ce_proj = base_ce + ce_from_elim + bolsa_activada * split_ce
        valid_proj = ab_proj + ce_proj

        st.markdown(f"#### Resultado proyectado · {scope_name}")
        kpi_grid([
            {'label': 'Abelardo proyectado', 'value': fmt_short(ab_proj), 'sub': f'{fmt_int(ab_proj)} votos', 'delta': fmt_pct(ab_proj / valid_proj) if valid_proj else '—'},
            {'label': 'Cepeda proyectado', 'value': fmt_short(ce_proj), 'sub': f'{fmt_int(ce_proj)} votos', 'delta': fmt_pct(ce_proj / valid_proj) if valid_proj else '—'},
            {'label': 'Margen proyectado', 'value': fmt_short(ab_proj - ce_proj), 'sub': 'Abelardo - Cepeda', 'delta': fmt_pct((ab_proj - ce_proj) / valid_proj) if valid_proj else '—'},
            {'label': 'Voto que no se convierte', 'value': fmt_short(fuga + blanc * (1 - activar_blanco) + nulos_nm * (1 - activar_nulo) + abst * (1 - activar_abst)), 'sub': 'Fuga + bolsa no activada'},
        ])

        sim_nat = pd.DataFrame({'candidato': ['ABELARDO', 'CEPEDA'], 'votos_proyectados': [ab_proj, ce_proj], 'porcentaje': [ab_proj / valid_proj if valid_proj else 0, ce_proj / valid_proj if valid_proj else 0]})
        fig = px.bar(sim_nat, x='candidato', y='votos_proyectados', text=sim_nat['porcentaje'].apply(fmt_pct), title=f'Proyección de segunda vuelta · {scope_name}')
        fig.update_layout(yaxis_title='Votos proyectados', xaxis_title='', height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### Composición del voto proyectado")
        st.caption("Muestra de dónde sale el total del escenario para el filtro activo.")
        comp = pd.DataFrame([
            {'Componente': 'Base de primera vuelta', 'Abelardo': base_ab, 'Cepeda': base_ce},
            {'Componente': 'Transferencia de candidatos eliminados', 'Abelardo': ab_from_elim, 'Cepeda': ce_from_elim},
            {'Componente': 'Captura de bolsa por definir', 'Abelardo': bolsa_activada * split_ab, 'Cepeda': bolsa_activada * split_ce},
            {'Componente': 'TOTAL ESCENARIO', 'Abelardo': ab_proj, 'Cepeda': ce_proj},
        ])
        comp_display = comp.copy()
        comp_display['Abelardo'] = comp_display['Abelardo'].apply(fmt_int)
        comp_display['Cepeda'] = comp_display['Cepeda'].apply(fmt_int)
        st.dataframe(comp_display, use_container_width=True, hide_index=True)

        comp_chart = comp[comp['Componente'] != 'TOTAL ESCENARIO'].melt(id_vars='Componente', var_name='Candidato', value_name='Votos')
        fig_comp = px.bar(comp_chart, x='Candidato', y='Votos', color='Componente', title=f'Construcción del total proyectado · {scope_name}')
        fig_comp.update_layout(yaxis_title='Votos', xaxis_title='', height=500)
        st.plotly_chart(fig_comp, use_container_width=True)

        # Proyección territorial: usa únicamente el filtro activo
        wide = mun_scope[mun_scope['tipo_registro'].eq('CANDIDATO')].pivot_table(
            index=['departamento', 'municipio', 'departamento_nombre', 'municipio_nombre'],
            columns='candidato',
            values='votos',
            aggfunc='sum',
            fill_value=0
        ).reset_index()

        for code in cand_scope['candidato'].unique():
            if code not in wide.columns:
                wide[code] = 0

        wide['abelardo_base'] = wide.get(4, 0)
        wide['cepeda_base'] = wide.get(1, 0)
        wide = wide.merge(
            margin_scope[['departamento', 'municipio', 'voto_blanco', 'voto_nulo', 'no_marcados', 'abstencion_estimada', 'votos_validos']],
            on=['departamento', 'municipio'],
            how='left'
        )
        wide['abelardo_proy'] = wide['abelardo_base']
        wide['cepeda_proy'] = wide['cepeda_base']

        for _, r in transfer_user.iterrows():
            code = int(r['codigo'])
            if code in wide.columns:
                wide['abelardo_proy'] += wide[code] * r['pct_abelardo']
                wide['cepeda_proy'] += wide[code] * r['pct_cepeda']

        wide['bolsa_activada'] = (
            wide['voto_blanco'].fillna(0) * activar_blanco
            + (wide['voto_nulo'].fillna(0) + wide['no_marcados'].fillna(0)) * activar_nulo
            + wide['abstencion_estimada'].fillna(0) * activar_abst
        )
        wide['abelardo_proy'] += wide['bolsa_activada'] * split_ab
        wide['cepeda_proy'] += wide['bolsa_activada'] * split_ce
        wide['margen_proy'] = wide['abelardo_proy'] - wide['cepeda_proy']
        wide['ganador_proy'] = np.where(wide['margen_proy'] >= 0, 'ABELARDO', 'CEPEDA')
        wide['margen_abs_proy'] = wide['margen_proy'].abs()
        wide['pct_abelardo_proy'] = wide['abelardo_proy'] / (wide['abelardo_proy'] + wide['cepeda_proy'])
        wide['pct_cepeda_proy'] = 1 - wide['pct_abelardo_proy']

        st.markdown(f"#### Lectura territorial del escenario · {scope_name}")
        if not wide.empty:
            kpi_grid([
                {'label': 'Municipios Abelardo', 'value': fmt_int((wide['ganador_proy'] == 'ABELARDO').sum()), 'sub': 'Ganador proyectado'},
                {'label': 'Municipios Cepeda', 'value': fmt_int((wide['ganador_proy'] == 'CEPEDA').sum()), 'sub': 'Ganador proyectado'},
                {'label': 'Bolsa activada', 'value': fmt_short(wide['bolsa_activada'].sum()), 'sub': f'{fmt_int(wide["bolsa_activada"].sum())} votos'},
                {'label': 'Diferencia promedio', 'value': fmt_short(wide['margen_abs_proy'].mean()), 'sub': 'Entre Abelardo y Cepeda'},
            ])
            st.caption("Esta lectura territorial respeta el filtro activo. Si eliges un departamento, solo aparecen sus municipios; si eliges un municipio, la lectura baja a ese municipio.")

            resumen = wide.groupby('ganador_proy', as_index=False).agg(
                municipios=('municipio', 'count'),
                abelardo_proy=('abelardo_proy', 'sum'),
                cepeda_proy=('cepeda_proy', 'sum'),
                bolsa_activada=('bolsa_activada', 'sum')
            )
            resumen_display = resumen.rename(columns={
                'ganador_proy': 'Bloque de municipios donde ganaría',
                'municipios': 'Cantidad de municipios',
                'abelardo_proy': 'Votos proyectados de Abelardo',
                'cepeda_proy': 'Votos proyectados de Cepeda',
                'bolsa_activada': 'Votos potenciales activados'
            }).copy()
            for col in ['Votos proyectados de Abelardo', 'Votos proyectados de Cepeda', 'Votos potenciales activados']:
                resumen_display[col] = resumen_display[col].apply(fmt_int)

            tabs = st.tabs(["Resumen", "Municipios más cerrados", "Detalle municipal"])
            with tabs[0]:
                st.dataframe(resumen_display, use_container_width=True, hide_index=True)
            with tabs[1]:
                close = wide.sort_values('margen_abs_proy').head(30).copy()
                fig_close = px.bar(
                    close,
                    x='municipio_nombre',
                    y='margen_abs_proy',
                    color='ganador_proy',
                    hover_data=['departamento_nombre', 'abelardo_proy', 'cepeda_proy', 'bolsa_activada'],
                    title=f'Municipios más cerrados del escenario · {scope_name}'
                )
                fig_close.update_layout(xaxis_tickangle=-35, yaxis_title='Diferencia proyectada de votos', xaxis_title='Municipio', height=560)
                st.plotly_chart(fig_close, use_container_width=True)
            with tabs[2]:
                semaforo = wide.copy()
                semaforo['nivel_competencia'] = pd.cut(
                    semaforo['margen_abs_proy'],
                    bins=[-1, 100, 500, 2000, 10000, 10**12],
                    labels=['Ultra bisagra: 0-100 votos', 'Bisagra: 101-500 votos', 'Competido: 501-2.000 votos', 'Defendible: 2.001-10.000 votos', 'Consolidado: más de 10.000 votos']
                )
                sview = semaforo[['departamento_nombre', 'municipio_nombre', 'ganador_proy', 'nivel_competencia', 'abelardo_proy', 'cepeda_proy', 'margen_abs_proy', 'bolsa_activada']].sort_values('margen_abs_proy').head(1000).rename(columns={
                    'departamento_nombre': 'Departamento',
                    'municipio_nombre': 'Municipio',
                    'ganador_proy': 'Ganador proyectado',
                    'nivel_competencia': 'Nivel de competencia',
                    'abelardo_proy': 'Abelardo proyectado',
                    'cepeda_proy': 'Cepeda proyectado',
                    'margen_abs_proy': 'Diferencia absoluta',
                    'bolsa_activada': 'Bolsa activada'
                })
                for col in ['Abelardo proyectado', 'Cepeda proyectado', 'Diferencia absoluta', 'Bolsa activada']:
                    sview[col] = sview[col].apply(fmt_int)
                st.dataframe(sview, use_container_width=True, hide_index=True)
        else:
            st.warning("No hay municipios para el filtro seleccionado.")
        st.download_button("Descargar proyección territorial", wide.to_csv(index=False).encode('utf-8'), "proyeccion_territorial_segunda_vuelta.csv", "text/csv")

elif modulo == "7. Fuentes y metodología":
    module_header(modulo)
    tab1, tab2, tab3 = st.tabs(["Cómo se calcula", "Fuentes políticas", "Base de supuestos"])
    with tab1:
        st.markdown("""
        1. **MMV** aporta votos por mesa y candidato/código.  
        2. **DIVIPOL** aporta nombre de departamento, municipio, puesto, potencial y ubicación.  
        3. Se agregan resultados por nación, departamento, municipio y puesto.  
        4. Se calcula **bolsa por definir** como abstención estimada + voto blanco + voto nulo + no marcado.  
        5. Se clasifican municipios y puestos según margen, bolsa e índice estratégico. En Bogotá, el nivel municipal se reinterpreta como localidad a partir de la zona DIVIPOL.  
        6. El simulador aplica porcentajes de transferencia editables y captura parcial de bolsa indefinida.
        """)
        action_note("<b>Índice estratégico:</b> no es un resultado electoral. Es una métrica de priorización que combina competitividad y oportunidad territorial.")
    with tab2:
        st.dataframe(fuentes, use_container_width=True, hide_index=True)
    with tab3:
        st.dataframe(transfer, use_container_width=True, hide_index=True)

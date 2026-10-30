"""Animace (GIF) a schémata (SVG) k prezentaci „Claude pro stavaře“, česky.

Převzato z workshopu AI agentů (AI_agents_workshop/tools/make_figures.py)
a upraveno pro stavaře / detailera v Tekla Structures: smyčka agenta nad
exportovaným kusovníkem, úklid složky zakázky, cesta dotazu přes MCP do Tekly.
Animace jsou ilustrační, ne záznam skutečné session; čísla jsou vymyšlená.
Každý GIF začíná i končí finálním stavem (náhled i tisk ukáží výsledek).

Spuštění (ze složky workshop/):
    uv run --with matplotlib --with pillow python tools/make_figures.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / 'slides' / 'figures'

DARK, TEAL, BLUE, ORANGE = '#12355b', '#007f86', '#326ba8', '#d48a16'
PALE, GREY, RED, GREEN = '#eef7f8', '#60717b', '#b94032', '#2e7d32'
LIGHT = '#c9d6dd'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 17,
                     'svg.hashsalt': 'claude-pro-stavare-2026',
                     'figure.facecolor': 'white', 'figure.max_open_warning': 0})


WINDOW = 200_000
PIECES = [  # (popisek, tokeny, barva) - ilustrační velikosti
    ('CLAUDE.md + nástroje', 18_000, TEAL),
    ('vaše zadání', 2_000, BLUE),
    ('ukázka reportu', 12_000, '#6f9fd1'),
    ('skript + úpravy', 24_000, '#8fb7a9'),
    ('celý report v chatu', 95_000, RED),
    ('další kroky', 40_000, '#9aa8b1'),
]
AFTER = [('CLAUDE.md + nástroje', 18_000, TEAL), ('shrnutí', 7_000, ORANGE)]
NEW_PER_TURN = [10_000, 6_000, 4_000, 4_000, 6_000]  # ilustrační


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def canvas(h, w=12):
    """Axis units are inches: fonts keep their size relative to the geometry."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set(xlim=(0, w), ylim=(0, h))
    ax.axis('off')
    return fig, ax


def rbox(ax, x, y, w, h, edge=TEAL, fill=PALE, lw=2, ls='-', r=0.12, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.02,rounding_size={r}',
                                facecolor=fill, edgecolor=edge, linewidth=lw, linestyle=ls,
                                zorder=z))


def arrow(ax, a, b, color=GREY, lw=2, rad=0, z=2):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=20, linewidth=lw,
                                 color=color, connectionstyle=f'arc3,rad={rad}', zorder=z))


def save_gif(frames, durations, name, dpi=100):
    """Frames are figures; the first one must show the final state."""
    assert len(frames) == len(durations)
    images = []
    for fig in frames:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=dpi)
        plt.close(fig)
        buf.seek(0)
        images.append(Image.open(buf).convert('RGB').quantize(colors=64, method=Image.MEDIANCUT))
    path = OUT / f'{name}.gif'
    images[0].save(path, save_all=True, append_images=images[1:], duration=list(durations),
                   loop=0, optimize=True, disposal=2)
    mb = path.stat().st_size / 1e6
    assert mb < 1.5, (name, mb)
    print(f'  slides/figures/{name}.gif  {len(images)} frames, {mb:.2f} MB')


def lerp(a, b, t):
    return a + (b - a) * t


def ease(k, n):
    t = k / n
    return t * t * (3 - 2 * t)


# --------------------------------------------------------------------------
# 1  one tool call: model -> harness -> tool -> result back to the model
# --------------------------------------------------------------------------


def tool_call():
    """The exchange of the slide 'A tool is an action the harness performs'."""
    H = 4.7
    boxes = {'model': (0.3, 'Model', 'navrhne akci'),
             'harness': (4.45, 'Aplikace', 'Claude Desktop:\nověří oprávnění'),
             'tool': (8.6, 'Terminál', '')}
    cx = {k: v[0] + 1.55 for k, v in boxes.items()}
    REQ, RES = 'spusť: uv run hmotnosti.py', 'Uloženo hmotnosti.xlsx'
    Y_REQ, Y_RES = 3.72, 0.5
    captions = ['1 · Model požádá o akci', '2 · Aplikace ji provede (s vaším svolením)',
                '3 · Výsledek se vrátí modelu', 'Jeden krok: požadavek → spuštění → výsledek']

    def frame(active=(), req_x=None, res_x=None, term=2, caption=3, final=False):
        fig, ax = canvas(H)
        for k, (x, title, body) in boxes.items():
            on = k in active
            rbox(ax, x, 1.25, 3.1, 1.75, edge=ORANGE if on else TEAL,
                 fill='#fff3dd' if on else PALE, lw=3.5 if on else 2)
            ax.text(x + 1.55, 2.62, title, ha='center', va='center', fontsize=19,
                    fontweight='bold', color=ORANGE if on else TEAL)
            if body:
                ax.text(x + 1.55, 1.9, body, ha='center', va='center', fontsize=14.5,
                        color=DARK, linespacing=1.3)
        # terminal content
        x0 = boxes['tool'][0]
        ax.add_patch(Rectangle((x0 + .18, 1.42), 2.74, .95, facecolor=DARK, zorder=3))
        if term >= 1:
            ax.text(x0 + .28, 2.12, '> uv run hmotnosti.py', fontsize=12.5, color='white',
                    family='DejaVu Sans Mono', va='center', zorder=4)
        if term >= 2:
            ax.text(x0 + .28, 1.68, 'Uloženo hmotnosti.xlsx', fontsize=11.5,
                    color='#9be3c2', family='DejaVu Sans Mono', va='center', zorder=4)
        # lanes
        for a, b in (('model', 'harness'), ('harness', 'tool')):
            arrow(ax, (cx[a] + .2, 3.2), (cx[b] - .2, 3.2), color=LIGHT if not final else GREY)
            arrow(ax, (cx[b] - .2, 1.05), (cx[a] + .2, 1.05), color=LIGHT if not final else GREY)
        for text, xpos, y, col in ((REQ, req_x, Y_REQ, BLUE), (RES, res_x, Y_RES, GREEN)):
            if xpos is None:
                continue
            xpos = min(max(xpos, 2.2), 9.8)  # keep the card inside the canvas
            ax.text(xpos, y, text, ha='center', va='center', fontsize=14.5, color='white',
                    family='DejaVu Sans Mono', zorder=5,
                    bbox=dict(boxstyle='round,pad=0.35', facecolor=col, edgecolor='none'))
        ax.text(0.3, 4.42, captions[caption], ha='left', va='center', fontsize=16,
                color=DARK, fontweight='bold')
        return fig

    final = lambda: frame(req_x=(cx['model'] + cx['tool']) / 2, res_x=(cx['model'] + cx['tool']) / 2,
                          final=True)
    frames, dur = [final()], [2200]
    frames.append(frame(active=('model',), term=0, caption=0)); dur.append(900)
    n = 8
    # request travels model -> harness -> tool
    for a, b, act in (('model', 'harness', ('harness',)), ('harness', 'tool', ('tool',))):
        for k in range(1, n + 1):
            frames.append(frame(active=act if k == n else (), req_x=lerp(cx[a], cx[b], ease(k, n)),
                                term=0, caption=0 if a == 'model' else 1))
            dur.append(70)
        dur[-1] = 700
    frames.append(frame(active=('tool',), req_x=cx['tool'], term=1, caption=1)); dur.append(700)
    frames.append(frame(active=('tool',), req_x=cx['tool'], term=2, caption=1)); dur.append(1000)
    # result travels tool -> harness -> model
    for a, b, act in (('tool', 'harness', ('harness',)), ('harness', 'model', ('model',))):
        for k in range(1, n + 1):
            frames.append(frame(active=act if k == n else (), res_x=lerp(cx[a], cx[b], ease(k, n)),
                                caption=2))
            dur.append(70)
        dur[-1] = 700
    frames.append(final()); dur.append(4000)
    save_gif(frames, dur, 'anim_tool_call')


# --------------------------------------------------------------------------



def context_fill():
    """Drawn for a half-width column of the slide (7.2 x 5 in)."""
    total = sum(t for _, t, _ in PIECES)
    assert 0.9 < total / WINDOW < 1.0, total
    WF, H = 7.2, 5.0
    X0, W = 0.15, 6.9
    sx = W / WINDOW

    def bar(ax, y, pieces, title):
        ax.text(X0, y + 0.88, title, fontsize=16.5, color=DARK, fontweight='bold', va='center')
        rbox(ax, X0, y, W, 0.62, edge=DARK, fill='white', lw=2, r=0.05, z=1)
        x = X0
        for _, t, col in pieces:
            ax.add_patch(Rectangle((x, y + 0.04), t * sx, 0.54, facecolor=col, edgecolor='white',
                                   linewidth=1.5, zorder=2))
            x += t * sx
        used = sum(t for _, t, _ in pieces)
        ax.text(X0 + W, y + 0.88, f'{used / WINDOW:.0%} plné', ha='right', va='center',
                fontsize=16.5, fontweight='bold', color=RED if used / WINDOW > 0.9 else GREY)
        return x

    def legend(ax, y, items):
        for i, (lab, _, col) in enumerate(items):
            x, yy = X0 + (i % 2) * 3.5, y - (i // 2) * 0.42
            ax.add_patch(Rectangle((x, yy - 0.13), 0.26, 0.26, facecolor=col))
            ax.text(x + 0.36, yy, lab, fontsize=15, color=DARK, va='center')

    def frame(k, compact):
        fig, ax = canvas(H, WF)
        bar(ax, 3.85, PIECES[:k], 'Kontextové okno, krok za krokem')
        legend(ax, 3.45, PIECES[:k])
        if compact:
            bar(ax, 1.2, AFTER, 'Po shrnutí (/compact)')
            ax.text(X0, 0.95, 'pravidla + shrnutí: je místo pokračovat,\nale detaily logu jsou pryč',
                    fontsize=14.5, color=GREY, va='top', linespacing=1.3)
        return fig

    final = lambda: frame(len(PIECES), True)
    frames, dur = [final()], [2500]
    frames.append(frame(0, False)); dur.append(800)
    for k in range(1, len(PIECES) + 1):
        frames.append(frame(k, False)); dur.append(900 if k < len(PIECES) else 1600)
    frames.append(final()); dur.append(4500)
    save_gif(frames, dur, 'anim_context_fill')


def git_rhythm():
    H = 3.9
    Y_MAIN, Y_BR = 2.75, 1.35
    X_A1, X_A2, X_C, X_M = 5.4, 7.2, 9.0, 10.4

    def commit(ax, x, y, label, col=TEAL, ls='-', fill=None, below=False):
        ax.add_patch(plt.Circle((x, y), 0.25, facecolor=fill or col, edgecolor=col, lw=2.5,
                                linestyle=ls, zorder=4))
        ax.text(x, y + (-0.68 if below else 0.52), label, ha='center', va='center', fontsize=15.5,
                color=GREY if col == LIGHT else col, zorder=5, linespacing=1.2)

    def frame(stage, final=False):
        """stage 0..6; each stage adds one event."""
        fig, ax = canvas(H)
        ax.text(0.25, 3.62, 'main', fontsize=15, color=DARK, fontweight='bold', va='center')
        ax.plot([0.6, 11.4 if stage >= 6 else 4.2], [Y_MAIN, Y_MAIN], color=DARK, lw=3, zorder=1)
        commit(ax, 1.3, Y_MAIN, 'report se načte', col=DARK)
        commit(ax, 3.2, Y_MAIN, 'přehled funguje', col=DARK if stage < 1 else TEAL)
        if stage >= 1:
            ax.text(3.2, 3.62, 'bod uložení', ha='center', fontsize=13.5, color=TEAL,
                    fontweight='bold')
        if stage >= 2:
            tip = X_C if stage >= 6 else (X_A2 if stage >= 5 else X_A1) + 0.8
            ax.plot([3.2, 4.3, tip], [Y_MAIN, Y_BR, Y_BR], color=BLUE, lw=3, zorder=1)
            ax.text(X_A1 + 0.45, Y_BR + 0.42, 'větev „cena-za-kg“', fontsize=13.5, color=BLUE,
                    va='center')
            if stage >= 4:  # the failed attempt is thrown away
                commit(ax, X_A1, Y_BR, 'pokus 1\nnefunguje', col=LIGHT, ls='--', fill='white',
                       below=True)
                ax.text(X_A1, Y_BR, '×', ha='center', va='center', fontsize=20, color=RED, zorder=6)
                arrow(ax, (X_A1 - 0.2, Y_BR + 0.3), (3.45, Y_MAIN - 0.28), color=RED, rad=-0.3)
                ax.text(4.55, 2.35, 'zpět', fontsize=14, color=RED, fontweight='bold',
                        va='center')
            else:
                failed = stage >= 3
                commit(ax, X_A1, Y_BR, 'pokus 1\nnefunguje' if failed else 'pokus 1',
                       col=RED if failed else BLUE, ls='--', fill='white', below=True)
        if stage >= 5:
            commit(ax, X_A2, Y_BR, 'pokus 2\nfunguje', col=GREEN, ls='--', fill='white',
                   below=True)
        if stage >= 6:
            commit(ax, X_C, Y_BR, 'commit\n„cena za kg“', col=GREEN, below=True)
            ax.plot([X_C, X_M], [Y_BR, Y_MAIN], color=BLUE, lw=3, zorder=1)
            commit(ax, X_M, Y_MAIN, 'sloučeno', col=DARK)
        cap = ['Git: historie uložených verzí projektu',
               '1 · Bod uložení: stav, který funguje',
               '2 · Jedna změna, na vlastní větvi',
               '3 · Kontrola: nefunguje',
               'Zpět k bodu uložení',
               'Druhý pokus · 3 · Kontrola: funguje',
               '4 · Commit: co a proč; pak sloučit'][stage]
        if final:
            cap = 'uložit → změnit → zkontrolovat → commit, nebo zpět'
        ax.text(11.85, 0.05, cap, ha='right', va='bottom', fontsize=14.5, color=DARK,
                fontweight='bold')
        ax.text(11.85, 3.62, 'čárkovaně = zatím neuloženo', fontsize=13, color=GREY,
                va='center', ha='right')
        return fig

    frames, dur = [frame(6, final=True)], [2500]
    for s in range(7):
        frames.append(frame(s)); dur.append(1600)
    frames.append(frame(6, final=True)); dur.append(4500)
    save_gif(frames, dur, 'anim_git_rhythm')





def resend_input():
    rows = [sum(NEW_PER_TURN[:i + 1]) for i in range(len(NEW_PER_TURN))]
    billed = sum(rows)
    assert billed == 100_000, billed  # matches the 100,000-input example on the slide
    H = 2.5
    fig, ax = canvas(H)
    s = 6.4 / max(rows)
    for i, r in enumerate(rows):
        y = H - 0.45 - i * 0.42
        ax.text(1.05, y, f'Krok {i + 1}', ha='right', va='center', fontsize=14.5, color=DARK)
        old = r - NEW_PER_TURN[i]
        ax.add_patch(Rectangle((1.2, y - 0.15), old * s, 0.3, facecolor=LIGHT))
        ax.add_patch(Rectangle((1.2 + old * s, y - 0.15), NEW_PER_TURN[i] * s, 0.3, facecolor=BLUE))
        ax.text(1.3 + r * s, y, f'{r // 1000}k', va='center', fontsize=13.5, color=DARK)
    ax.add_patch(Rectangle((8.3, 1.62), 0.3, 0.26, facecolor=LIGHT))
    ax.text(8.7, 1.75, 'posláno znovu', va='center', fontsize=13.5, color=GREY)
    ax.add_patch(Rectangle((8.3, 1.2), 0.3, 0.26, facecolor=BLUE))
    ax.text(8.7, 1.33, 'nové v tomto kroku', va='center', fontsize=13.5, color=GREY)
    ax.text(8.3, 2.17, 'Vstupní tokeny v každém kroku\n(ilustrační)', va='center', fontsize=13.5,
            color=GREY, linespacing=1.25)
    ax.text(8.3, 0.6, f'Účtovaný vstup = součet řádků\n= {billed:,} tokenů'.replace(',', ' '), va='center',
            fontsize=15, color=DARK, fontweight='bold', linespacing=1.35)
    fig.savefig(OUT / 'resend_input.svg', metadata={'Date': None})
    plt.close(fig)
    print('  slides/figures/resend_input.svg')


# --------------------------------------------------------------------------
# smyčka agenta nad exportovaným kusovníkem: přečíst → napsat → spustit → chyba → opravit
# --------------------------------------------------------------------------

WEIGHTS = [  # (profil, tuny) - vymyšlené, součet 18,4 t odpovídá textu animace
    ('HEA 200', 5.2), ('IPE 300', 4.1), ('IPE 240', 3.0), ('SHS 120×6', 2.4),
    ('UPE 160', 1.6), ('L 70×7', 1.1), ('plechy', 1.0),
]
assert abs(sum(t for _, t in WEIGHTS) - 18.4) < 1e-9

LOOP = [  # (kdo, text, barva textu)
    ('Vy', 'Z hala_revB_part_list.csv udělej přehled hmotností do Excelu', DARK),
    ('nástroj', '> head -5 podklady/tekla/hala_revB_part_list.csv', DARK),
    ('výstup', 'TEKLA STRUCTURES REPORT … Pozice;Profil;Materiál;Ks;Hmotnost', GREY),
    ('agent', 'Hlavička z Tekly, oddělovač je středník. Napíšu hmotnosti.py.', DARK),
    ('nástroj', '> uv run hmotnosti.py', DARK),
    ('výstup', "ValueError: could not convert '1 245,6'", RED),
    ('agent', 'Tekla píše „1 245,6“. Upravím načítání, spustím znovu.', DARK),
    ('výstup', 'Uloženo vystupy/tekla/hmotnosti.xlsx (48 pozic, 18,4 t)', GREEN),
    ('agent', 'Hotovo. Pozor: B-17 nemá materiál, 3× „?“ v čísle.', ORANGE),
]
TAG = {'Vy': BLUE, 'agent': TEAL, 'nástroj': DARK, 'výstup': GREY}


def weight_chart():
    """Malý náhled výsledku (vodorovné sloupce), vrací obrázek PIL."""
    fig, ax = plt.subplots(figsize=(3.3, 3.9))
    names = [n for n, _ in WEIGHTS][::-1]
    vals = [t for _, t in WEIGHTS][::-1]
    ax.barh(names, vals, color=TEAL)
    for y, v in enumerate(vals):
        ax.text(v + 0.1, y, f'{v:.1f}'.replace('.', ','), va='center', fontsize=11, color=DARK)
    ax.set_title('Hmotnost podle profilu [t]\ncelkem 18,4 t', fontsize=12.5, color=DARK)
    ax.tick_params(labelsize=11, colors=DARK)
    ax.set_xlim(0, 6.4)
    ax.set_xticks([])
    for side in ('top', 'right', 'bottom'):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert('RGB')


def agent_loop():
    W, H = 12, 6.2
    thumb = weight_chart()

    def frame(k):
        fig, ax = canvas(H, W)
        ax.text(0.3, H - 0.4, 'Agent pracuje ve smyčce: přečte → napíše → spustí → opraví',
                fontsize=17, fontweight='bold', color=DARK, va='center')
        for i, (who, text, col) in enumerate(LOOP[:k]):
            y = H - 1.05 - i * 0.56
            ax.text(0.3, y, who, fontsize=12.5, color='white', va='center', ha='left',
                    fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor=TAG[who],
                                                 edgecolor='none'))
            mono = who in ('nástroj', 'výstup')
            ax.text(1.55, y, text, fontsize=12.5 if mono else 14, color=col, va='center',
                    family='DejaVu Sans Mono' if mono else 'DejaVu Sans',
                    fontweight='bold' if col in (RED, ORANGE, GREEN) else 'normal')
        if k >= 8:  # výsledek se objeví vpravo
            rbox(ax, 8.85, 0.25, 3.0, 3.75, edge=GREEN, fill='white', lw=2)
            iax = fig.add_axes([0.745, 0.05, 0.24, 0.6])
            iax.imshow(thumb)
            iax.axis('off')
        return fig

    frames, dur = [frame(len(LOOP))], [2500]
    frames.append(frame(1)); dur.append(1400)
    for k in range(2, len(LOOP) + 1):
        frames.append(frame(k)); dur.append(2200 if LOOP[k - 1][2] in (RED, ORANGE) else 1200)
    frames.append(frame(len(LOOP))); dur.append(5000)
    save_gif(frames, dur, 'anim_agent_loop')


# --------------------------------------------------------------------------
# úklid složky zakázky: nepořádek ze „Stažených“ → struktura zakázky
# --------------------------------------------------------------------------

FOLDERS = ['01_Podklady', '02_Vypocty', '04_Vykresy', '05_Korespondence', '06_Nabidky_a_fakturace']
MOVES = [  # (původní název, složka, nový název) - konvence jako v kancelar.qmd
    ('scan0012.pdf', 4, 'Z2026-014_SML_smlouva_o_dilo.pdf'),
    ('vykres A (2).pdf', 2, 'Z2026-014_VYK_V-101_A.pdf'),
    ('Výkres_final_FINAL.pdf', 2, 'Z2026-014_VYK_V-102_C.pdf'),
    ('part_list.csv', 0, 'Z2026-014_POD_part_list_revB.csv'),
    ('RE_ dotaz na kotvy.msg', 3, 'Z2026-014_KOR_dotaz_kotvy.msg'),
    ('Zápis KD.docx', 3, 'Z2026-014_ZAP_2026-03-12.docx'),
    ('statika_v3.pdf', 1, 'Z2026-014_VYP_statika_v3.pdf'),
    ('nabidka(1).xlsx', 4, 'Z2026-014_NAB_nabidka.xlsx'),
]


def folder_sort():
    W, H = 12, 6.4
    LX, RX = 0.3, 4.75
    caps = ['Stažené soubory jedné zakázky: nepořádek',
            '1 · Agent navrhne strukturu, vy ji schválíte',
            '2 · Přesouvá a přejmenovává podle pravidel',
            'Hotovo + seznam změn v prejmenovani.csv (dá se vrátit)']

    def frame(stage, moved):
        """stage 0 = nepořádek, 1 = složky, 2 = přesouvání, 3 = hotovo."""
        fig, ax = canvas(H, W)
        ax.text(LX, H - 0.4, caps[stage], fontsize=17, fontweight='bold', color=DARK,
                va='center')
        # vlevo: Stažené
        rbox(ax, LX, 0.35, 4.0, H - 1.25, edge=LIGHT, fill='#f6f8f9', lw=2)
        ax.text(LX + 0.2, H - 1.15, 'Stažené', fontsize=15, fontweight='bold', color=GREY,
                va='center')
        for i, (old, _, _) in enumerate(MOVES):
            y = H - 1.7 - i * 0.5
            done = i < moved
            ax.text(LX + 0.35, y, old, fontsize=13, va='center', family='DejaVu Sans Mono',
                    color=LIGHT if done else DARK)
            if done:
                ax.plot([LX + 0.3, LX + 0.4 + 0.105 * len(old)], [y, y], color=LIGHT, lw=1.5)
        if stage == 0:
            return fig
        # vpravo: struktura zakázky
        rbox(ax, RX, 0.35, W - RX - 0.2, H - 1.25, edge=TEAL, fill=PALE, lw=2)
        ax.text(RX + 0.2, H - 1.15, 'Z2026-014_Hala_Modrice/', fontsize=15, fontweight='bold',
                color=TEAL, va='center')
        y = H - 1.62
        for f, name in enumerate(FOLDERS):
            ax.text(RX + 0.45, y, name + '/', fontsize=13.5, va='center', color=DARK,
                    fontweight='bold')
            y -= 0.36
            for i, (_, folder, new) in enumerate(MOVES):
                if folder == f and i < moved:
                    last = stage == 2 and i == moved - 1
                    ax.text(RX + 0.85, y, new, fontsize=12, va='center',
                            family='DejaVu Sans Mono', color=ORANGE if last else DARK,
                            fontweight='bold' if last else 'normal')
                    y -= 0.32
        if stage == 2 and 0 < moved <= len(MOVES):
            arrow(ax, (LX + 3.7, H - 1.7 - (moved - 1) * 0.5), (RX + 0.3, H - 1.62),
                  color=ORANGE, rad=-0.15)
        return fig

    final = lambda: frame(3, len(MOVES))
    frames, dur = [final()], [2500]
    frames.append(frame(0, 0)); dur.append(1800)
    frames.append(frame(1, 0)); dur.append(1800)
    for m in range(1, len(MOVES) + 1):
        frames.append(frame(2, m)); dur.append(900)
    frames.append(final()); dur.append(5000)
    save_gif(frames, dur, 'anim_folder_sort')


# --------------------------------------------------------------------------
# MCP: Claude ↔ MCP server ↔ Tekla Open API ↔ model
# --------------------------------------------------------------------------

def mcp_flow():
    W, H = 12, 5.2
    BW = 2.55
    boxes = [(0.25, 'Claude', 'Desktop,\nzáložka Code'),
             (3.25, 'MCP server', 'program u vás,\nread-only režim'),
             (6.25, 'Tekla Open API', 'oficiální rozhraní\nTekla Structures'),
             (9.25, 'Model', 'otevřený\nv Tekle')]
    cx = [x + BW / 2 for x, _, _ in boxes]
    REQ = ['get_parts(phase=2)', 'Model.Select(…)', 'díly fáze 2?']
    RES = ['48 dílů, profily', '48 objektů', '{"dílů":48,"t":18.4}']  # model→API→MCP→Claude
    Y_REQ, Y_RES, BY = 3.55, 0.55, 1.35
    caps = ['Vy: „Kolik váží fáze 2?“', '1 · Claude zavolá nástroj MCP serveru',
            '2 · Server se zeptá Tekly přes Open API', '3 · Odpověď jde stejnou cestou zpět',
            'Claude: „Fáze 2 má 48 dílů, celkem 18,4 t.“']

    def frame(active=None, req=None, res=None, cap=4, final=False):
        fig, ax = canvas(H, W)
        for i, (x, title, body) in enumerate(boxes):
            on = i == active
            edge = ORANGE if on else (BLUE if i == 3 else TEAL)
            rbox(ax, x, BY, BW, 1.75, edge=edge, fill='#fff3dd' if on else PALE,
                 lw=3.5 if on else 2)
            ax.text(x + BW / 2, BY + 1.33, title, ha='center', va='center', fontsize=18,
                    fontweight='bold', color=edge)
            ax.text(x + BW / 2, BY + 0.6, body, ha='center', va='center', fontsize=13.5,
                    color=DARK, linespacing=1.3)
        for i in range(3):
            col = GREY if final else LIGHT
            arrow(ax, (cx[i] + .3, BY + 1.95), (cx[i + 1] - .3, BY + 1.95), color=col)
            arrow(ax, (cx[i + 1] - .3, BY - 0.2), (cx[i] + .3, BY - 0.2), color=col)
        ax.text(W / 2, BY - 0.62, 'vše běží na vašem počítači; do cloudu Anthropic odchází'
                ' jen to, co Claude dostane zpět', ha='center', fontsize=12.5, color=GREY,
                style='italic')
        for card, y, col in ((req, Y_REQ, BLUE), (res, Y_RES, GREEN)):
            if card is None:
                continue
            text, xpos = card
            xpos = min(max(xpos, 1.6), W - 1.6)
            ax.text(xpos, y, text, ha='center', va='center', fontsize=13.5, color='white',
                    family='DejaVu Sans Mono', zorder=5,
                    bbox=dict(boxstyle='round,pad=0.35', facecolor=col, edgecolor='none'))
        ax.text(0.25, H - 0.35, caps[cap], ha='left', va='center', fontsize=17, color=DARK,
                fontweight='bold')
        return fig

    final = lambda: frame(final=True)
    frames, dur = [final()], [2500]
    frames.append(frame(active=0, cap=0)); dur.append(1500)
    n = 7
    for hop in range(3):
        for k in range(1, n + 1):
            frames.append(frame(active=hop + 1 if k == n else None,
                                req=(REQ[hop], lerp(cx[hop], cx[hop + 1], ease(k, n))),
                                cap=1 if hop == 0 else 2))
            dur.append(80)
        dur[-1] = 900
    for hop in range(3):  # 3 → 2 → 1 → 0
        a, b = 3 - hop, 2 - hop
        for k in range(1, n + 1):
            frames.append(frame(active=b if k == n else None,
                                res=(RES[hop], lerp(cx[a], cx[b], ease(k, n))), cap=3))
            dur.append(80)
        dur[-1] = 900
    frames.append(final()); dur.append(5000)
    save_gif(frames, dur, 'anim_mcp_flow')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tool_call()
    agent_loop()
    folder_sort()
    mcp_flow()
    context_fill()
    git_rhythm()
    resend_input()


if __name__ == '__main__':
    main()

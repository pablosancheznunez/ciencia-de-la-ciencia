"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py [--png]
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def lienzo(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.2, fontweight=peso)


def flecha(ax, a, b, color=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def pagina(ax, x, y, w, h, titulo):
    caja(ax, x, y, w, h, None, fc=SUP, ec=TINTA2, r=0.06)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=CAJA, ec=TINTA2, lw=1.2))
    ax.text(x + 0.15, y + h - 0.175, titulo, ha="left", va="center", fontsize=9, color=TINTA2)
    for i in range(5):
        ax.plot([x + 0.2, x + w - 0.2 - (0.5 if i % 2 else 0)], [y + h - 0.7 - i * 0.32] * 2,
                color=GRIS, lw=3, solid_capstyle="round")





def c2_asimetria():
    import numpy as np
    rng = np.random.default_rng(4)
    citas = np.floor(rng.lognormal(1.6, 1.2, 2000)).astype(int)
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    ax.hist(np.clip(citas, 0, 100), bins=50, color=S[0], edgecolor=SUP, linewidth=.6)
    me, md = citas.mean(), np.median(citas)
    top = ax.get_ylim()[1]
    for v, t, c, yy in ((md, f"mediana = {md:.0f}", S[2], .9), (me, f"media = {me:.1f}".replace(".", ","), S[1], .7)):
        ax.axvline(v, color=c, lw=2.2); ax.text(v + 1.2, top * yy, t, color=TINTA, fontsize=10, fontweight="bold")
    ax.set_xlabel("Citas por artículo (los valores de más de 100 se agrupan en 100)", fontsize=10, color=TINTA2)
    ax.set_ylabel("Artículos", fontsize=10, color=TINTA2)
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    ax.tick_params(colors=TINTA2)
    ax.text(99, ax.get_ylim()[1] * .5, "datos simulados", ha="right", fontsize=8.5, color=TINTA2, style="italic")
    guardar(fig, "c2_asimetria.svg")


def c4_jardin():
    fig, ax = plt.subplots(figsize=(10, 4.2)); ax.set_xlim(0, 16); ax.set_ylim(0, 7); ax.axis("off")
    caja(ax, 0.2, 3.0, 2.4, 1.0, "Datos", fc=SUP, ec=TINTA2, fs=10.5, peso="bold")
    niveles = [("¿Excluir atípicos?", ["sí", "no"]), ("¿Qué variable?", ["VD1", "VD2"]), ("¿Covariable?", ["sí", "no"])]
    xs = [3.6, 7.6, 11.6]; pos = [(1.4, 3.5)]
    for k, (pregunta, ops) in enumerate(niveles):
        ax.text(xs[k] + 0.9, 6.7, pregunta, ha="center", fontsize=9.5, color=TINTA, fontweight="bold")
        nuevos = []
        n = len(pos) * 2; ys = [0.4 + (6.0 - 0.8) * (i + .5) / n for i in range(n)]
        for i, (px, py) in enumerate(pos):
            for j, o in enumerate(ops):
                y = ys[2 * i + j]
                ax.plot([px + (1.2 if k == 0 else 0.9), xs[k]], [py, y], color=GRIS, lw=1.4)
                caja(ax, xs[k], y - 0.25, 1.8, 0.5, o, fc=SUP, ec=S[k], fs=8.5)
                nuevos.append((xs[k] + 0.9, y))
        pos = nuevos
    for i, (px, py) in enumerate(pos):
        sig = i in (2, 5)
        ax.text(15.0, py, "p < 0,05" if sig else "p > 0,05", fontsize=8.5, va="center", ha="center", color="#a52a1a" if sig else TINTA2, fontweight="bold" if sig else "normal")
        ax.plot([px + 0.9, 14.3], [py, py], color=GRIS, lw=1, ls=":")
    ax.text(8, 0.0, "Ocho caminos razonables con los mismos datos: si se elige el camino después de ver el resultado, basta con que uno «salga».", ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "c4_jardin.svg")


def c5_informe():
    fig, ax = plt.subplots(figsize=(10.5, 4.2)); ax.set_xlim(0, 17); ax.set_ylim(0, 6.6); ax.axis("off")
    filas = [("Tradicional", ["Idea", "Diseño", "Datos", "Análisis", "Redacción", "Revisión\npor pares"], 4.6, 5),
             ("Informe registrado", ["Idea", "Diseño", "Revisión\nfase 1", "Datos", "Análisis", "Revisión\nfase 2"], 1.6, 2)]
    for t, pasos, y, rev in filas:
        ax.text(0.1, y + 1.25, t, fontsize=11, fontweight="bold", color=TINTA)
        for i, p_ in enumerate(pasos):
            x = 0.1 + i * 2.75
            col = S[1] if (t == "Tradicional" and i == rev) else (S[2] if (t != "Tradicional" and i == rev) else CAJA2)
            caja(ax, x, y, 2.3, 0.9, p_, fc=SUP, ec=col, lw=1.8 if col != CAJA2 else 1.2, fs=9.5)
            if i < len(pasos) - 1: flecha(ax, (x + 2.32, y + 0.45), (x + 2.73, y + 0.45))
    ax.text(16.8, 4.1, "La decisión depende del resultado", ha="right", fontsize=9, color="#a52a1a")
    ax.text(5.6 + 1.15, 1.1, "Aceptación en principio:\nse publicará sea cual sea el resultado", ha="center", va="top", fontsize=9, color="#0b6b4a")
    guardar(fig, "c5_informe.svg")



def c7_cobertura():
    from matplotlib.patches import Ellipse
    fig, ax = lienzo(8.4, 4.6, (0, 14), (0, 7.6))
    for (x, y, w, h, c, t, tx, ty) in ((8.3, 3.8, 10.6, 6.8, S[2], "OpenAlex", 12.2, 6.6), (7.2, 3.6, 8.6, 5.6, S[3], "Dimensions", 10.6, 5.9),
                                       (5.6, 3.6, 5.8, 4.2, S[1], "Scopus", 6.0, 5.2), (5.0, 3.5, 3.8, 2.8, S[0], "Web of Science", 5.0, 3.5)):
        ax.add_patch(Ellipse((x, y), w, h, fc=c, ec=c, alpha=0.18, lw=1.5))
        ax.text(tx, ty, t, ha="center", va="center", fontsize=11, fontweight="bold", color=TINTA)
    ax.text(11.6, 1.5, "Revistas regionales,\notros idiomas,\nlibros, preprints", ha="center", fontsize=9.5, color=TINTA2)
    ax.text(1.2, 7.0, "Tamaños ilustrativos, no a escala", fontsize=9, color=TINTA2, style="italic")
    guardar(fig, "c7_cobertura.svg")


def c8_asimetria():
    import random
    random.seed(7)
    x = [int(random.paretovariate(1.3) * 3) - 3 for _ in range(1500)]
    x = [v for v in x if v < 120]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.hist(x, bins=60, color=S[0], alpha=0.85, edgecolor="white")
    s = sorted(x); med = s[len(s) // 2]; media = sum(x) / len(x); p90 = s[int(len(s) * 0.9)]
    ax.set_xlim(-1, 60)
    for (v, t, c), fy in zip(((med, f"mediana: {med}", TINTA), (media, f"media: {media:.1f}".replace(".", ","), S[1]), (p90, f"umbral del 10 % más citado: {p90}", S[2])), (0.92, 0.74, 0.56)):
        ax.axvline(v, color=c, lw=2, ls="--"); ax.text(v + 0.8, ax.get_ylim()[1] * fy, t, color=c, fontsize=10, fontweight="bold")
    ax.set_xlabel("Citas por trabajo", color=TINTA2); ax.set_ylabel("Número de trabajos", color=TINTA2)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.tick_params(colors=TINTA2)
    guardar(fig, "c8_asimetria.svg")


def c9_relaciones():
    fig, ax = lienzo(9, 4.2, (0, 14), (0, 6.4))
    def doc(x, y, t, c): caja(ax, x - 0.9, y - 0.45, 1.8, 0.9, t, fc=c, fs=10)
    ax.text(3.4, 6.0, "Cocitación", ha="center", fontsize=12.5, fontweight="bold", color=TINTA)
    doc(3.4, 4.6, "Nuevo", "#d6e6f8"); doc(1.8, 1.4, "C", "#f6dccf"); doc(5.0, 1.4, "D", "#f6dccf")
    flecha(ax, (3.1, 4.1), (2.0, 1.9)); flecha(ax, (3.7, 4.1), (4.8, 1.9))
    ax.plot([2.7, 4.1], [1.4, 1.4], ls="--", color=S[1], lw=2); ax.text(3.4, 0.55, "C y D, citados juntos", ha="center", fontsize=9.5, color=TINTA2)
    ax.text(10.6, 6.0, "Acoplamiento bibliográfico", ha="center", fontsize=12.5, fontweight="bold", color=TINTA)
    doc(9.0, 4.6, "E", "#d6e6f8"); doc(12.2, 4.6, "F", "#d6e6f8"); doc(10.6, 1.4, "Ref.", "#f6dccf")
    flecha(ax, (9.2, 4.1), (10.3, 1.9)); flecha(ax, (12.0, 4.1), (10.9, 1.9))
    ax.plot([9.9, 11.3], [4.6, 4.6], ls="--", color=S[0], lw=2); ax.text(10.6, 0.55, "E y F comparten referencias", ha="center", fontsize=9.5, color=TINTA2)
    guardar(fig, "c9_relaciones.svg")


def c10_flujo():
    fig, ax = lienzo(10, 3.0, (0, 15.4), (0, 4.4))
    pasos = ["Pregunta", "Corpus", "Preproceso", "Modelo", "Validación"]
    for i, t in enumerate(pasos):
        caja(ax, 0.3 + i * 3.05, 2.4, 2.5, 1.1, t, fc="#d6e6f8" if i < 4 else "#d3efe3", fs=11, peso="bold")
        if i < 4: flecha(ax, (2.85 + i * 3.05, 2.95), (3.3 + i * 3.05, 2.95))
    ax.add_patch(FancyBboxPatch((0.3, 0.6), 14.7, 0.8, boxstyle="round,pad=0,rounding_size=0.1", fc="#fdf0d3", ec="none"))
    ax.text(7.65, 1.0, "Lectura humana en cada fase", ha="center", va="center", fontsize=10.5, color=TINTA)
    ax.add_patch(FancyArrowPatch((13.5, 3.55), (10.6, 3.55), connectionstyle="arc3,rad=0.5", arrowstyle="-|>", mutation_scale=12, color=S[1], lw=1.5))
    ax.text(12.05, 4.25, "ajustar", ha="center", fontsize=9.5, color=S[1])
    guardar(fig, "c10_flujo.svg")


def c12_capas():
    fig, ax = lienzo(9, 4.4, (0, 14), (0, 7))
    capas = [(0.4, "Datos bibliométricos y registros", "¿Qué ha cambiado?", S[0]), (2.5, "Diseños causales", "¿Lo ha causado la reforma?", S[2]), (4.6, "Métodos cualitativos y documentales", "¿Cómo y por qué?", S[3])]
    for y, t, q, c in capas:
        ax.add_patch(FancyBboxPatch((1.6, y), 10.8, 1.8, boxstyle="round,pad=0,rounding_size=0.12", fc=c, ec="none", alpha=0.2))
        ax.text(7.0, y + 1.15, t, ha="center", fontsize=12, fontweight="bold", color=TINTA); ax.text(7.0, y + 0.5, q, ha="center", fontsize=10.5, color=TINTA2)
    ax.add_patch(FancyArrowPatch((0.9, 0.5), (0.9, 6.3), arrowstyle="<|-|>", mutation_scale=12, color=TINTA2, lw=1.4))
    ax.text(0.45, 3.4, "Métodos mixtos", rotation=90, ha="center", va="center", fontsize=10, color=TINTA2)
    guardar(fig, "c12_capas.svg")


if __name__ == "__main__":
    c2_asimetria(); c4_jardin(); c5_informe(); c7_cobertura(); c8_asimetria(); c9_relaciones(); c10_flujo(); c12_capas()

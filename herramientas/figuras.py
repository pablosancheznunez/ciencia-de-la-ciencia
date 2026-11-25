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


if __name__ == "__main__":
    c2_asimetria(); c4_jardin(); c5_informe()

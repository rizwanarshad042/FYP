"""Rebuild the five Chapter 8 figures from the results tables in main.tex.

Run with Python and Matplotlib. The report includes the generated vector PDFs.
"""

from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT = Path(__file__).resolve().parent
SOURCE = (OUTPUT.parents[1] / "main.tex").read_text(encoding="utf-8")
BLUE = "#155774"
GRAY = "#89939b"
INK = "#212932"
GRID = "#d5d9dc"

plt.rcParams.update({
    "font.family": "STIXGeneral",
    "font.size": 10.5,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.axisbelow": True,
    "pdf.fonttype": 42,
})


def table_rows(label):
    """Read the body of a chapter table, retaining its row order and precision."""
    table = SOURCE.split(r"\label{tab:" + label + "}", 1)[1].split(r"\end{tabular}", 1)[0]
    rows = {}
    for line in table.splitlines():
        if "&" in line and r"\\" in line:
            cells = line.split(r"\\", 1)[0].split("&")
            cells = [re.sub(r"\\textbf\{([^}]*)\}", r"\1", c.strip()) for c in cells]
            rows[cells[0]] = cells[1:]
    return dict(list(rows.items())[1:])  # First row contains column headings.


def horizontal_axis(ax, labels, ticks, limit):
    ax.set(xlim=limit, ylim=(len(labels) - 0.5, -0.5), xticks=ticks)
    ax.set_yticks(range(len(labels)), labels)
    ax.tick_params(length=0, pad=4)
    ax.grid(axis="x", color=GRID, linewidth=0.6)


def bars(ax, labels, values, colors, ticks, limit, fmt):
    horizontal_axis(ax, labels, ticks, limit)
    marks = ax.barh(range(len(values)), values, height=0.44, color=colors)
    ax.bar_label(marks, labels=[fmt.format(v) for v in values], padding=4)


def save(fig, name):
    fig.savefig(OUTPUT / (name + ".pdf"), metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def baselines():
    overall = table_rows("exp1")
    names = sorted(overall, key=lambda name: float(overall[name][2]))
    labels = [name.replace(" (last value)", "").replace("--", "–") for name in names]
    colors = [BLUE if name == "LightGBM (global)" else GRAY for name in names]
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.35, 2.23), layout="constrained")
    bars(a, labels, [float(overall[n][2]) for n in names], colors,
         [0, 20, 40, 60], (0, 79), "{:.2f}")
    a.set_title("Overall forecast error", fontsize=11)
    a.set_xlabel("WAPE (%)")

    classes = table_rows("exp1-class")
    gain = [float(ma) - float(gbm) for ma, gbm in
            zip(classes["Moving average"], classes["LightGBM (global)"])]
    bars(b, ["Smooth", "Erratic", "Intermittent", "Lumpy"], gain, BLUE,
         [0, 1, 2, 3, 4], (0, 4.7), "{:.2f}")
    b.set_title("Gain over moving average", fontsize=11)
    b.set_xlabel("WAPE reduction (percentage points)")
    save(fig, "baselines")


def paired_bars(name, labels, colors, panels):
    fig, axes = plt.subplots(1, 2, figsize=(6.35, 1.46), layout="constrained")
    for ax, (title, values, ticks, limit, fmt) in zip(axes, panels):
        bars(ax, labels, values, colors, ticks, limit, fmt)
        if max(ticks) >= 1000:
            ax.xaxis.set_major_formatter("{x:,.0f}")
        ax.set_title(title, fontsize=11)
    save(fig, name)


def pooling():
    rows = table_rows("exp2")
    models = [rows["One global model per tenant"], rows["One model per series"]]
    paired_bars("pooling", ["Global", "Per series"], [BLUE, GRAY], [
        ("Forecast error (WAPE, %)", [float(r[1]) for r in models],
         [0, 10, 20, 30, 40, 50], (0, 58), "{:.2f}"),
        ("Training time (seconds)", [int(r[2].removesuffix(" s")) for r in models],
         [0, 20, 40, 60, 80, 100], (0, 108), "{:.0f}"),
    ])


def training_history():
    rows = table_rows("exp3")
    scores = [float(r[1]) for r in rows.values()]
    benchmark = float(table_rows("exp1")["Moving average"][2])
    fig, ax = plt.subplots(figsize=(6.35, 2.12), layout="constrained")
    ax.set(xlim=(-0.5, len(scores) - 0.5), ylim=(41.6, 46.8),
           ylabel="WAPE (%)", yticks=[42, 43, 44, 45, 46])
    ax.set_xticks(range(len(rows)), [n.replace("Full history (5 years)", "5 years (full)") for n in rows])
    ax.set_xlabel("Training history")
    ax.grid(axis="y", color=GRID, linewidth=0.6)
    ax.tick_params(length=0)
    ax.axhline(benchmark, color=INK, dashes=(4, 3), linewidth=1.1,
               label=f"Four-week moving average ({benchmark:.2f}%)")
    for i, score in enumerate(scores):
        ax.plot(i, score, "o", markersize=6, color=BLUE)
        dy = 7 if score > benchmark else -9
        ax.annotate(f"{score:.2f}", (i, score), xytext=(0, dy), textcoords="offset points",
                    ha="center", va="bottom" if dy > 0 else "top",
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.4})
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.22), frameon=False, fontsize=10)
    save(fig, "training-history")


def objectives():
    rows = table_rows("exp4")
    fig, axes = plt.subplots(1, 3, sharey=True, figsize=(6.35, 1.55), layout="constrained")
    panels = [
        ("RMSE (units)", [5.50, 5.55, 5.60, 5.65], (5.48, 5.70)),
        ("MAE (units)", [2.65, 2.70, 2.75, 2.80], (2.63, 2.84)),
        ("WAPE (%)", [42, 43, 44], (41.85, 44.1)),
    ]
    for col, (ax, (title, ticks, limit)) in enumerate(zip(axes, panels)):
        horizontal_axis(ax, list(rows), ticks, limit)
        ax.set_title(title, fontsize=11)
        for i, row in enumerate(rows.values()):
            value = float(row[col])
            ax.plot(value, i, "o", color=BLUE, markersize=6)
            ax.annotate(f"{value:.2f}", (value, i), xytext=(6, 0),
                        textcoords="offset points", va="center")
    save(fig, "objectives")


def redistribution():
    rows = table_rows("exp5")
    units = [int(c.replace(",", "")) for c in rows["Dead-stock units"][:2]]
    lost_sales = [int(c.replace(",", "")) for c in rows["Lost sales (units)"][:2]]
    if units != lost_sales:
        raise ValueError("The shared units panel requires equal dead-stock and lost-sales counts.")
    sell_through = [float(c) for c in rows[r"Sell-through rate (\%)"][:2]]
    paired_bars("redistribution", ["No action", "Transfers"], [GRAY, BLUE], [
        ("Dead stock and lost sales (units each)", units, [0, 20000, 40000, 60000],
         (0, 74000), "{:,.0f}"),
        ("Sell-through rate (%)", sell_through, [0, 25, 50, 75, 100], (0, 107), "{:.1f}"),
    ])


if __name__ == "__main__":
    baselines()
    pooling()
    training_history()
    objectives()
    redistribution()

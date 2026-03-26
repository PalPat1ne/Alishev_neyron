import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d  # noqa: F401


ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "results" / "results.json"
ASSETS_DIR = ROOT / "report_assets"
REPORT_PATH = ROOT / "report.md"


def load_results():
    with open(RESULTS_PATH, "r", encoding="utf-8") as source:
        return json.load(source)


def experiment_grid(experiment, gammas, sigmas):
    cell_map = {}
    for cell in experiment["cells"]:
        cell_map[(cell["sigma"], cell["gamma"])] = cell["plot_eps"]

    grid = []
    for sigma in sigmas:
        row = []
        for gamma in gammas:
            row.append(cell_map[(sigma, gamma)])
        grid.append(row)
    return np.array(grid)


def make_surface_plot(experiment, gammas, sigmas, output_path):
    z = experiment_grid(experiment, gammas, sigmas)
    x, y = np.meshgrid(np.array(gammas), np.array(sigmas))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    surface = ax.plot_surface(
        x,
        y,
        z,
        rstride=1,
        cstride=1,
        cmap="viridis",
        edgecolor="black",
        linewidth=0.3,
    )

    ax.set_xlabel("gamma", fontsize=12, fontweight="bold", labelpad=12)
    ax.set_ylabel("sigma", fontsize=12, fontweight="bold", labelpad=12)
    ax.set_zlabel("eps2", fontsize=12, fontweight="bold", labelpad=10)
    ax.set_title(f"LB2 Experiment {experiment['id']}", fontsize=14, fontweight="bold", pad=18)
    ax.view_init(elev=28, azim=-130)

    colorbar = fig.colorbar(surface, ax=ax, shrink=0.7, pad=0.1)
    colorbar.set_label("eps2", fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close(fig)


def table_markdown(experiment, gammas, sigmas):
    cell_map = {}
    for cell in experiment["cells"]:
        cell_map[(cell["sigma"], cell["gamma"])] = cell["table_value"]

    header = "| sigma / gamma | " + " | ".join(f"{gamma:.1f}" for gamma in gammas) + " |"
    sep = "|---" * (len(gammas) + 1) + "|"
    rows = [header, sep]

    for sigma in sigmas:
        values = [cell_map[(sigma, gamma)] for gamma in gammas]
        row = "| " + f"{sigma:.1f}" + " | " + " | ".join(values) + " |"
        rows.append(row)

    return "\n".join(rows)


def build_report(results):
    ASSETS_DIR.mkdir(exist_ok=True)
    gammas = results["gammas"]
    sigmas = results["sigmas"]
    lines = []

    lines.append("# Отчет по лабораторной работе №2")
    lines.append("")
    lines.append("## Условия экспериментов")
    lines.append("")
    lines.append(f"- Число шагов обучения: `{results['n_iter']}`")
    lines.append(f"- Порог успешного обучения: `eps2 < {results['threshold']}`")
    lines.append("- В таблицах:")
    lines.append("  - если обучение успешное, в ячейке записан номер шага")
    lines.append("  - если обучение неуспешное, в ячейке записано `eps2 / шаг / вариант`")
    lines.append("- Для графиков:")
    lines.append("  - если обучение успешное, по методичке использовано значение `0.1`")
    lines.append("  - если обучение неуспешное, использовано значение ошибки из отчета")
    lines.append("")

    for experiment in results["experiments"]:
        image_name = f"experiment_{experiment['id']}.png"
        image_path = ASSETS_DIR / image_name
        make_surface_plot(experiment, gammas, sigmas, image_path)

        coeffs = ", ".join(f"{value:.3f}" for value in experiment["coeffs"])
        success_count = sum(1 for cell in experiment["cells"] if cell["success"])

        lines.append(f"## Эксперимент {experiment['id']}")
        lines.append("")
        lines.append(f"- Файл коэффициентов: `{experiment['coef_file']}`")
        lines.append(f"- Коэффициенты: `{coeffs}`")
        lines.append(f"- Успешных запусков: `{success_count}` из `36`")
        lines.append("")
        lines.append(table_markdown(experiment, gammas, sigmas))
        lines.append("")
        lines.append(f"![Experiment {experiment['id']}](report_assets/{image_name})")
        lines.append("")

    with open(REPORT_PATH, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))


def main():
    results = load_results()
    build_report(results)
    print("saved:", REPORT_PATH)


if __name__ == "__main__":
    main()

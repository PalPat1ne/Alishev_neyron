import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent
RESULTS_PATH = ROOT / "results" / "results.json"
HISTORY_ASSETS = ROOT / "history_assets"
HISTORY_REPORT = ROOT / "history_report.md"


def load_results():
    with open(RESULTS_PATH, "r", encoding="utf-8") as source:
        return json.load(source)


def load_history(path):
    steps = []
    values = []
    with open(path, "r", encoding="utf-8") as source:
        for line in source:
            line = line.strip()
            if not line:
                continue
            step_text, value_text = line.split()[:2]
            steps.append(int(step_text))
            values.append(float(value_text))
    return steps, values


def plot_single_history(experiment_id, sigma, gamma, history_path):
    fig = plt.figure(figsize=(8, 4.8))
    ax = fig.add_subplot(111)
    steps, values = load_history(history_path)
    ax.plot(steps, values, linewidth=1.7, color="blue")
    ax.set_title(
        f"exp={experiment_id}  sigma={sigma:.1f}  gamma={gamma:.1f}",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("step", fontsize=12, fontweight="bold")
    ax.set_ylabel("eps2", fontsize=12, fontweight="bold")
    ax.set_xlim(1, 1000)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    out_path = HISTORY_ASSETS / f"exp{experiment_id}_sigma_{sigma:.1f}_gamma_{gamma:.1f}.png"
    plt.savefig(out_path, dpi=180)
    plt.close(fig)
    return out_path


def build_history_report(results):
    HISTORY_ASSETS.mkdir(exist_ok=True)
    lines = ["# Графики `eps2` по шагам", ""]

    for experiment in results["experiments"]:
        lines.append(f"## Эксперимент {experiment['id']}")
        lines.append("")

        for sigma in results["sigmas"]:
            lines.append(f"### sigma = {sigma:.1f}")
            lines.append("")
            for gamma in results["gammas"]:
                for cell in experiment["cells"]:
                    if cell["sigma"] == sigma and cell["gamma"] == gamma:
                        history_path = ROOT / cell["history_file"]
                        image_path = plot_single_history(experiment["id"], sigma, gamma, history_path)
                        lines.append(f"#### gamma = {gamma:.1f}")
                        lines.append("")
                        lines.append(
                            f'![exp {experiment["id"]} sigma {sigma:.1f} gamma {gamma:.1f}]({image_path.relative_to(ROOT)})'
                        )
                        lines.append("")
                        break

    with open(HISTORY_REPORT, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))


def main():
    results = load_results()
    build_history_report(results)
    print("saved:", HISTORY_REPORT)


if __name__ == "__main__":
    main()

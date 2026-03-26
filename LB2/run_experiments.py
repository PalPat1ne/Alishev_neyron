import json
import random
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BIN = ROOT / "lb2"
RESULTS_DIR = ROOT / "results"
HISTORY_DIR = RESULTS_DIR / "histories"
COEF_DIR = ROOT / "coefficients"

GAMMAS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
SIGMAS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
N_ITER = 1000
THRESHOLD = 0.1
EXPERIMENTS = 3
COEF_COUNT = 6
COEF_SEED = 26032026


def ensure_dirs():
    RESULTS_DIR.mkdir(exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    COEF_DIR.mkdir(exist_ok=True)


def compile_program():
    subprocess.run(
        ["clang++", "-std=c++17", "lb2.cpp", "-o", "lb2"],
        cwd=ROOT,
        check=True,
    )


def write_coefficients():
    rng = random.Random(COEF_SEED)
    coefficient_sets = []

    for exp_id in range(1, EXPERIMENTS + 1):
        coeffs = [round(rng.uniform(-1.2, 1.2), 3) for _ in range(COEF_COUNT)]
        path = COEF_DIR / f"coef_exp{exp_id}.txt"
        with open(path, "w", encoding="utf-8") as out:
            for value in coeffs:
                out.write(f"{value}\n")
        coefficient_sets.append((path, coeffs))

    return coefficient_sets


def load_history(path):
    history = []
    with open(path, "r", encoding="utf-8") as source:
        for line in source:
            line = line.strip()
            if not line:
                continue
            step_text, eps_text = line.split()[:2]
            history.append((int(step_text), float(eps_text)))
    return history


def classify_failure(history):
    values = [eps for _, eps in history]
    min_step, min_eps = min(history, key=lambda item: item[1])
    local_mins = []
    tol = 1e-4

    for i in range(1, len(values) - 1):
        if values[i] < values[i - 1] - tol and values[i] <= values[i + 1] + tol:
            local_mins.append(history[i])

    if len(local_mins) >= 2:
        report_step, report_eps = local_mins[0]
        return "В", report_step, report_eps, min_step, min_eps

    if min_step >= history[-1][0] - 5 or abs(values[-1] - min_eps) < 1e-3:
        report_step, report_eps = history[-1]
        return "А", report_step, report_eps, min_step, min_eps

    return "Б", min_step, min_eps, min_step, min_eps


def summarize_history(history):
    first_success_step = None
    for step, eps in history:
        if eps < THRESHOLD:
            first_success_step = step
            break

    if first_success_step is not None:
        min_step, min_eps = min(history, key=lambda item: item[1])
        return {
            "success": True,
            "first_success_step": first_success_step,
            "min_step": min_step,
            "min_eps": min_eps,
            "variant": "",
            "report_step": first_success_step,
            "report_eps": THRESHOLD,
            "plot_eps": THRESHOLD,
            "table_value": str(first_success_step),
        }

    variant, report_step, report_eps, min_step, min_eps = classify_failure(history)
    return {
        "success": False,
        "first_success_step": None,
        "min_step": min_step,
        "min_eps": min_eps,
        "variant": variant,
        "report_step": report_step,
        "report_eps": report_eps,
        "plot_eps": report_eps,
        "table_value": f"{report_eps:.3f} / {report_step} / {variant}",
    }


def run_single_experiment(exp_id, coef_path, coeffs):
    experiment = {
        "id": exp_id,
        "coef_file": coef_path.name,
        "coeffs": coeffs,
        "cells": [],
    }

    for sigma in SIGMAS:
        for gamma in GAMMAS:
            history_path = HISTORY_DIR / f"exp{exp_id}_g{gamma:.1f}_s{sigma:.1f}.txt"
            command = [
                str(BIN),
                str(coef_path),
                str(N_ITER),
                f"{gamma:.1f}",
                f"{sigma:.1f}",
                str(history_path),
            ]

            completed = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=True,
            )

            history = load_history(history_path)
            summary = summarize_history(history)
            summary["gamma"] = gamma
            summary["sigma"] = sigma
            summary["history_file"] = str(history_path.relative_to(ROOT))
            summary["stdout"] = completed.stdout
            experiment["cells"].append(summary)

            print(
                f"exp={exp_id} gamma={gamma:.1f} sigma={sigma:.1f} "
                f"success={summary['success']} value={summary['plot_eps']:.4f}"
            )

    return experiment


def main():
    ensure_dirs()
    compile_program()
    coefficient_sets = write_coefficients()

    results = {
        "n_iter": N_ITER,
        "threshold": THRESHOLD,
        "gammas": GAMMAS,
        "sigmas": SIGMAS,
        "experiments": [],
    }

    for exp_id, (coef_path, coeffs) in enumerate(coefficient_sets, start=1):
        results["experiments"].append(run_single_experiment(exp_id, coef_path, coeffs))

    with open(RESULTS_DIR / "results.json", "w", encoding="utf-8") as out:
        json.dump(results, out, ensure_ascii=False, indent=2)

    print("saved:", RESULTS_DIR / "results.json")


if __name__ == "__main__":
    main()

"""Read and plot local CSV files in data/ (or a supplied folder)."""

import argparse
import csv
import math
from pathlib import Path
import sys
from scipy.stats import linregress


def read_runs(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        time_column, *run_columns = reader.fieldnames or []
        rows = [row for row in reader if row[time_column].strip() != "s"]
        times = [float(row[time_column]) if row[time_column].strip() else math.nan for row in rows]

        runs = {}
        for name in run_columns:
            runs[name] = []
            for time, row in zip(times, rows):
                value = row[name].strip()
                if value == "":
                    break
                runs[name].append((time, float(value)))

        results = {}
        for each_run in runs:
            derivative = []
            for i in range(2, len(runs[each_run]) - 2):
                derivative.append((runs[each_run][i-2][1]-8*runs[each_run][i-1][1]+8*runs[each_run][i+1][1]-runs[each_run][i+2][1])/(12 * (times[1] - times[0])))

            x = derivative
            y = [temperature for _, temperature in runs[each_run][2:-2]]

            result = linregress(x, y)
            slope = result.slope
            intercept = result.intercept
            results[each_run] = {"slope": slope, "intercept": intercept,
                                 "x": x, "y": y}


    return runs, len(rows), results



def plot_file(path, runs, results):
    """Plot each temperature against its derivative, with the fitted line."""
    try:
        import matplotlib
    except ModuleNotFoundError:
        raise SystemExit("Install dependencies first: python -m pip install -r requirements.txt")

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = (len(runs) + 1) // 2
    figure, axes = plt.subplots(
        rows, 2, figsize=(14, 3.6 * rows), squeeze=False, layout="constrained"
    )
    try:
        figure.suptitle(f"{path.name}: temperature vs. temperature derivative", fontsize=16)
        for axis, (name, result) in zip(axes.flat, results.items()):
            x, y = result["x"], result["y"]
            axis.scatter(x, y, color="#2266bb", s=6, alpha=0.5)
            fit_x = [min(x), max(x)]
            fit_y = [result["slope"] * value + result["intercept"] for value in fit_x]
            axis.plot(fit_x, fit_y, color="#cc4422", linewidth=1.2)
            axis.set(
                title=name,
                xlabel="Temperature derivative (\N{DEGREE SIGN}C/s)",
                ylabel="Temperature (°C)",
            )
            axis.grid(alpha=0.25)
            axis.spines[["top", "right"]].set_visible(False)

        for axis in list(axes.flat)[len(runs):]:
            axis.set_visible(False)

        output = path.with_suffix(".png")
        figure.savefig(output, dpi=180, facecolor="white")
    finally:
        plt.close(figure)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "folder", nargs="?", type=Path, default=Path(__file__).resolve().parent / "data",
        help="Folder containing CSV files (default: data/ beside this script).",
    )
    args = parser.parse_args(argv)
    if not args.folder.is_dir():
        parser.error(f"Folder does not exist: {args.folder}")

    paths = sorted(
        (path for path in args.folder.iterdir() if path.is_file() and path.suffix.lower() == ".csv"),
        key=lambda path: path.name.casefold(),
    )
    if not paths:
        print(f"No CSV files found in {args.folder}. Add a CSV file and run again.")
        return 0

    failures = 0
    for path in paths:
        print(f"\nReading {path.name}")
        try:
            runs, count, results = read_runs(path)
            print(f"Processed {count} measurement rows.")
            for name, result in results.items():
                print(f"{name}: slope={result['slope']}, intercept={result['intercept']}")
            output = plot_file(path, runs, results)
            print(f"Saved {output.name}")
        except (OSError, UnicodeError, csv.Error, ValueError, KeyError, TypeError) as error:
            print(f"Could not process {path.name}: {error}", file=sys.stderr)
            failures += 1

    print(f"\nProcessed {len(paths) - failures} of {len(paths)} CSV files; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

import csv
from pathlib import Path


def write_csv(rows: list[dict], output_path: str):
    if not rows:
        print("[INFO] No data to write.")
        return

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    headers = rows[0].keys()

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[OK] CSV written to {output_path}")

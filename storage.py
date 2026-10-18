import json
from pathlib import Path


def ensure_file(file_path, default_data=None):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        save_data(path, [] if default_data is None else default_data)


def load_data(file_path, default_data=None):
    ensure_file(file_path, default_data)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON list in {file_path}")

        return data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {file_path}. Restore a valid backup before continuing."
        ) from error


def save_data(file_path, data):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")

    try:
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        temporary_path.replace(path)

    except OSError:
        if temporary_path.exists():
            temporary_path.unlink()
        raise


def next_id(records, prefix):
    numbers = []

    for record in records:
        record_id = str(record.get("id", ""))

        if record_id.startswith(prefix):
            suffix = record_id[len(prefix):]

            if suffix.isdigit():
                numbers.append(int(suffix))

    return f"{prefix}{max(numbers, default=0) + 1:04d}"

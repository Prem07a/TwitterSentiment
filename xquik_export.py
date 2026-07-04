import csv
import io


TEXT_COLUMNS = ("text", "tweet", "tweet_text", "full_text", "content")
ID_COLUMNS = ("id", "tweet_id", "post_id")
DATE_COLUMNS = ("created_at", "timestamp", "date", "published_at")


def normalize_xquik_csv(csv_text):
    """Return non-empty tweet rows from a saved Xquik CSV export."""
    reader = csv.DictReader(io.StringIO(csv_text))
    if not reader.fieldnames:
        raise ValueError("CSV header row is required.")

    field_map = {field.lower().strip(): field for field in reader.fieldnames}
    text_field = _first_present(field_map, TEXT_COLUMNS)
    if text_field is None:
        raise ValueError("CSV must include a text, tweet_text, full_text, or content column.")

    id_field = _first_present(field_map, ID_COLUMNS)
    date_field = _first_present(field_map, DATE_COLUMNS)

    rows = []
    for row in reader:
        text = str(row.get(text_field, "")).strip()
        if not text:
            continue
        rows.append(
            {
                "text": text,
                "tweet_id": str(row.get(id_field, "")).strip() if id_field else "",
                "created_at": str(row.get(date_field, "")).strip() if date_field else "",
            }
        )
    return rows


def _first_present(field_map, candidates):
    for candidate in candidates:
        if candidate in field_map:
            return field_map[candidate]
    return None

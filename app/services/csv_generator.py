from fastapi.responses import FileResponse
from io import BytesIO
import pandas as pd
import zipfile

def generate_csv_zip_from_json(data):
    metadata = {k: data.get(k, "") for k in ["user_id", "date", "logged_cycles", "most_common_symptom", "most_frequent_mood"]}
    sections = {
        "cycle_history": data.get("cycle_history", []),
        "symptom_logs": data.get("symptom_logs", []),
        "mood_logs": data.get("mood_logs", []),
        "most_common_symptoms": data.get("most_common_symptoms", []),
        "mood_distribution": data.get("mood_distribution", [])
    }

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for section, records in sections.items():
            if not records:
                continue
            enriched = [{**metadata, **record} for record in records]
            df = pd.DataFrame(enriched)
            if not df.empty:
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                zip_file.writestr(f"{section}.csv", csv_bytes)

    zip_path = "user_data_sections.zip"
    with open(zip_path, "wb") as f:
        f.write(zip_buffer.getvalue())

    return FileResponse(zip_path, media_type="application/zip", filename="user_data_sections.zip")

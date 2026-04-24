import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================

def process_pdf_data(raw_json: dict) -> dict:
    # Bước 1: Làm sạch nhiễu (Header/Footer) khỏi văn bản
    raw_text = raw_json.get("extractedText", "")
    cleaned_content = re.sub(r'(HEADER_PAGE_\d+|FOOTER_PAGE_\d+)', '', raw_text).strip()

    # Bước 2: Map dữ liệu thô sang định dạng chuẩn của UnifiedDocument
    return {
        "document_id": raw_json.get("docId", ""),
        "source_type": "PDF",
        "author": raw_json.get("authorName", "").strip(),
        "category": raw_json.get("docCategory", ""),
        "content": cleaned_content,
        "timestamp": raw_json.get("createdAt", ""),
    }

def process_video_data(raw_json: dict) -> dict:
    return {
        "document_id": raw_json.get("video_id", ""),
        "source_type": "Video",
        "author": raw_json.get("creator_name", "").strip(),
        "category": raw_json.get("category", ""),
        "content": raw_json.get("transcript", ""),
        "timestamp": raw_json.get("published_timestamp", ""),
    }

if __name__ == "__main__":
    import json, os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RAW_DATA_DIR = os.path.join(BASE_DIR, "..", "raw_data")

    # Test Group A - PDFs
    for fname in ["doc1_messy.json", "doc2_corrupt.json"]:
        path = os.path.join(RAW_DATA_DIR, "group_a_pdfs", fname)
        with open(path) as f:
            raw = json.load(f)
        result = process_pdf_data(raw)
        print(f"=== {fname} ===")
        print(result)
        assert result["source_type"] == "PDF"
        assert "HEADER" not in result["content"]
        assert "FOOTER" not in result["content"]
        print("OK\n")

    # Test Group B - Videos
    for fname in ["vid1_metadata.json", "vid2_missing_tags.json"]:
        path = os.path.join(RAW_DATA_DIR, "group_b_videos", fname)
        with open(path) as f:
            raw = json.load(f)
        result = process_video_data(raw)
        print(f"=== {fname} ===")
        print(result)
        assert result["source_type"] == "Video"
        print("OK\n")

    print("All tests passed!")

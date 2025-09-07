from typing import Dict, Any

def process_image(image_bytes: bytes, meta: str) -> Dict[str, Any]:
    """
    既存の二次元コード読み取りAPIへの窓口。
    実装は任意に置き換えてください。
    返却例:
      {"meta": "xxx", "decoded": [{"text":"...", "format":"QR", "bbox":[...]}], "ok": True}
    """
    # TODO: 実APIの呼び出しに差し替え
    return {"meta": meta, "decoded": None, "ok": True}

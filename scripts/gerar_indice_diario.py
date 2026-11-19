#!/usr/bin/env python3
"""Gerar índice público apenas de entradas explicitamente publicadas."""
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parent.parent
folder = root / "diario" / "publicacoes"
out = root / "diario" / "publicacoes.json"
items = []
for file in sorted([*folder.glob("*.yaml"), *folder.glob("*.yml")]) if folder.exists() else []:
    data = yaml.safe_load(file.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("publicado") is not True:
        continue
    category = data.get("categoria")
    caption = data.get("legenda")
    photo = data.get("fotografia") or ""
    if category not in {"casos", "bastidores", "reflexoes"} or not isinstance(caption, str) or not caption.strip():
        raise ValueError(f"Publicação inválida: {file.name}")
    if not isinstance(photo, str) or (photo and not photo.startswith("/diario/imagens/")):
        raise ValueError(f"Imagem inválida: {file.name}")
    items.append({"categoria":category,"fotografia":photo,"legenda":caption.strip(),"publicado":True})
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(items,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"{len(items)} publicações no índice")

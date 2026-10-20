from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROMPTS = RAIZ / "pipeline" / "prompts"
RUBRICAS = RAIZ / "rubricas"


def carregar_prompt(nome: str) -> str:
    return (PROMPTS / f"{nome}.md").read_text(encoding="utf-8")


def carregar_rubrica(nome: str) -> str:
    return (RUBRICAS / f"{nome}.md").read_text(encoding="utf-8")


@dataclass
class Config:
    """Modelos em camadas: barato para triagem, forte para criar e revisar."""

    modelo_rapido: str = field(default_factory=lambda: os.getenv(
        "BEDROCK_MODEL_FAST", "us.anthropic.claude-haiku-4-5-20251001-v1:0"))
    modelo_forte: str = field(default_factory=lambda: os.getenv(
        "BEDROCK_MODEL_STRONG", "us.anthropic.claude-sonnet-4-5-20250929-v1:0"))
    max_rodadas_revisao: int = 2
    meta_legibilidade: float = 50.0

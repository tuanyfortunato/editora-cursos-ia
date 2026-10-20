"""Cliente de LLM com saída estruturada e registro de custo/latência.

Usa a Converse API do Amazon Bedrock com uma "ferramenta" obrigatória cujo
schema é o modelo Pydantic esperado. Assim o modelo sempre devolve JSON válido.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


@dataclass
class Chamada:
    agente: str
    modelo: str
    tokens_entrada: int
    tokens_saida: int
    latencia_ms: int
    tentativa: int = 1


@dataclass
class Trace:
    chamadas: list[Chamada] = field(default_factory=list)

    def registrar(self, chamada: Chamada) -> None:
        self.chamadas.append(chamada)

    @property
    def total_tokens(self) -> int:
        return sum(c.tokens_entrada + c.tokens_saida for c in self.chamadas)

    def como_dict(self) -> list[dict]:
        return [c.__dict__ for c in self.chamadas]


class LLM(Protocol):
    def gerar(self, *, agente: str, modelo: str, sistema: str, prompt: str,
              saida: type[T], trace: Trace, temperatura: float = 0.4) -> T: ...


class BedrockLLM:
    """Implementação real sobre Amazon Bedrock (Converse API)."""

    def __init__(self, regiao: str | None = None, max_tentativas: int = 2):
        import boto3
        from botocore.config import Config as BotoConfig

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=regiao or os.getenv("AWS_REGION", "us-east-1"),
            # Repete automaticamente em throttling, com backoff
            config=BotoConfig(retries={"max_attempts": 6, "mode": "adaptive"}, read_timeout=120),
        )
        self.max_tentativas = max_tentativas

    def gerar(self, *, agente, modelo, sistema, prompt, saida, trace, temperatura=0.4):
        tool_name = "registrar_resultado"
        tool_config = {
            "tools": [{
                "toolSpec": {
                    "name": tool_name,
                    "description": f"Registra o resultado do agente {agente}.",
                    "inputSchema": {"json": saida.model_json_schema()},
                }
            }],
            "toolChoice": {"tool": {"name": tool_name}},
        }
        mensagens = [{"role": "user", "content": [{"text": prompt}]}]
        ultimo_erro: Exception | None = None

        for tentativa in range(1, self.max_tentativas + 1):
            inicio = time.perf_counter()
            resp = self.client.converse(
                modelId=modelo,
                system=[{"text": sistema}],
                messages=mensagens,
                toolConfig=tool_config,
                inferenceConfig={"temperature": temperatura, "maxTokens": 4096},
            )
            uso = resp.get("usage", {})
            trace.registrar(Chamada(
                agente=agente, modelo=modelo,
                tokens_entrada=uso.get("inputTokens", 0),
                tokens_saida=uso.get("outputTokens", 0),
                latencia_ms=int((time.perf_counter() - inicio) * 1000),
                tentativa=tentativa,
            ))
            blocos = resp["output"]["message"]["content"]
            dados = next((b["toolUse"]["input"] for b in blocos if "toolUse" in b), None)
            try:
                if dados is None:
                    raise ValueError("Modelo não chamou a ferramenta de resultado.")
                return saida.model_validate(dados)
            except (ValidationError, ValueError) as erro:
                ultimo_erro = erro
                mensagens.append(resp["output"]["message"])
                mensagens.append({"role": "user", "content": [{
                    "text": f"A saída não passou na validação: {erro}. Corrija e envie de novo."
                }]})
        raise RuntimeError(f"[{agente}] saída inválida após {self.max_tentativas} tentativas: {ultimo_erro}")


def dump(obj: BaseModel) -> str:
    return json.dumps(obj.model_dump(), ensure_ascii=False, indent=2)

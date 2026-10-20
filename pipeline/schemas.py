"""Contratos de dados entre os agentes.

Cada agente recebe e devolve objetos validados. Isso garante rastreabilidade:
todo curso publicado sabe de qual tema veio, quem produziu, quem revisou e por quê.
"""
from __future__ import annotations

from typing import Literal

import re
import unicodedata

from pydantic import BaseModel, Field, field_validator, model_validator


# ---------- Pesquisa ----------
class TemaCandidato(BaseModel):
    titulo: str = Field(description="Título curto do tema, em linguagem do dia a dia")
    publico: str = Field(description="Função do varejo que mais precisa disso (ex.: operador de caixa)")
    problema_real: str = Field(description="Situação concreta da rotina que o tema resolve")
    justificativa: str = Field(description="Por que é relevante agora")
    categoria: Literal[
        "atendimento", "vendas", "operacao", "seguranca", "lideranca",
        "comunicacao", "tecnologia", "inteligencia_emocional", "conhecimentos_gerais",
    ]


class ResultadoPesquisa(BaseModel):
    temas: list[TemaCandidato] = Field(min_length=3, max_length=8)


# ---------- Curadoria ----------
class TemaPriorizado(BaseModel):
    titulo: str
    impacto: int = Field(ge=1, le=5, description="Impacto na rotina e no negócio")
    urgencia: int = Field(ge=1, le=5, description="Quão atual/necessário é agora")
    viabilidade: int = Field(ge=1, le=5, description="Dá para ensinar bem em 5 a 7 minutos?")
    comentario: str


class ResultadoCuradoria(BaseModel):
    ranking: list[TemaPriorizado]
    escolhido: str = Field(description="Título exato do tema escolhido para virar microaula")
    motivo_escolha: str


# ---------- Produção ----------
class Passo(BaseModel):
    titulo: str = Field(description="Ação curta, no imperativo (ex.: 'Escute sem interromper')")
    explicacao: str = Field(description="Uma a três frases curtas")
    exemplo_fala: str | None = Field(default=None, description="Frase pronta que o profissional pode usar")


class QuestaoQuiz(BaseModel):
    pergunta: str
    alternativas: list[str] = Field(min_length=3, max_length=4)
    correta: int = Field(ge=0, le=3, description="Índice (0-based) da alternativa correta")
    explicacao: str = Field(description="Por que essa é a certa, em uma frase")

    @model_validator(mode="after")
    def _correta_existe(self):
        if self.correta >= len(self.alternativas):
            raise ValueError("'correta' aponta para uma alternativa que não existe")
        return self


class Microaula(BaseModel):
    titulo: str
    objetivo: str = Field(description="O que a pessoa vai conseguir fazer ao final, em uma frase")
    duracao_min: int = Field(ge=3, le=10)
    abertura: str = Field(description="Cena curta e realista que abre a aula (2 a 4 frases)")
    passos: list[Passo] = Field(min_length=3, max_length=6)
    o_que_evitar: list[str] = Field(min_length=2, max_length=5)
    exercicio_situacao: str = Field(description="Situação prática para a pessoa pensar como agiria")
    exercicio_resposta_modelo: str
    quiz: list[QuestaoQuiz] = Field(min_length=3, max_length=5)
    material_apoio: list[str] = Field(
        min_length=3, max_length=6,
        description="Cartão de bolso: frases curtas para lembrar no dia a dia",
    )


# ---------- Revisão ----------
class CriterioAvaliado(BaseModel):
    criterio: str
    nota: int = Field(ge=1, le=5)
    observacao: str


class Parecer(BaseModel):
    criterios: list[CriterioAvaliado]
    problemas: list[str] = Field(description="Problemas concretos encontrados (vazio se nenhum)")
    sugestoes: list[str] = Field(description="Ajustes objetivos para a próxima versão")
    aprovado: bool


# ---------- Organização ----------
class Catalogo(BaseModel):
    slug: str = Field(description="identificador-em-kebab-case, sem acentos")
    categoria: str
    subcategoria: str
    nivel: Literal["basico", "intermediario", "avancado"]
    publico_alvo: list[str]
    tags: list[str] = Field(min_length=3, max_length=10)
    resumo_catalogo: str = Field(description="Descrição de até 2 frases para a vitrine da biblioteca")

    @field_validator("slug")
    @classmethod
    def _slug_seguro(cls, v: str) -> str:
        # O slug vira nome de pasta: nunca confiar no texto do modelo
        v = unicodedata.normalize("NFKD", v).encode("ascii", "ignore").decode()
        v = re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")
        return v[:60] or "curso"

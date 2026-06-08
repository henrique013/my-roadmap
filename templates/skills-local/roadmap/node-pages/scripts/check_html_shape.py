#!/usr/bin/env python3
"""Validate the mechanical shape of a roadmap node HTML file."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


PROHIBITED_SECTIONS = (
    "Objetivo do node",
    "Ao final você vai saber",
    "Pré-requisitos herdados",
    "Critério de domínio",
    "Checklist final",
)

COMMAND_PATTERNS = (
    re.compile(r"(?m)^\s*(?:sudo|apt|dnf|yum|brew|docker|kubectl|psql|npm|pip|python3?)\s+\S+"),
    re.compile(r"(?m)^\s*(?:\$|#)\s+\S+"),
)

LEGACY_LIGHT_TOKENS = (
    "#ffffff",
    "#f8fafc",
    "#f1f5f9",
)

FORBIDDEN_CONTEXT_TEXTS = (
    "Label canônico",
    "Label canonico",
    "Node ID",
    "node_id",
    "primeiro node do nível",
    "primeiro node do nivel",
    "último node do nível",
    "ultimo node do nivel",
)

FORBIDDEN_REFERENCE_TITLES = (
    "Fontes usadas neste node",
    "Referências usadas",
    "Referencias usadas",
    "Referências comentadas",
    "Referencias comentadas",
)

FORBIDDEN_REFERENCE_CLASSES = (
    "refs",
    "references",
    "final-note",
)

TERMINAL_DIVIDER_SELECTORS = (
    ".refs",
    ".references",
    ".final-note",
    ".node-footer",
    ".node-closing",
)

NODE_ID_VISIBLE_RE = re.compile(
    r"\b(?:basico|intermediario|avancado)/\d{2}-[a-z0-9][a-z0-9-]*\b",
    re.IGNORECASE,
)

VISIBLE_TEXT_SKIP_TAGS = {"code", "pre", "script", "style", "kbd", "samp"}

UNACCENTED_PT_BR_VISIBLE_REPLACEMENTS = {
    "nao": "não",
    "Nao": "Não",
    "documentacao": "documentação",
    "Documentacao": "Documentação",
    "ate": "até",
    "Ate": "Até",
    "tambem": "também",
    "Tambem": "Também",
    "so": "só",
    "So": "Só",
    "especificacao": "especificação",
    "Especificacao": "Especificação",
    "publicacao": "publicação",
    "Publicacao": "Publicação",
    "relatorio": "relatório",
    "Relatorio": "Relatório",
    "criterio": "critério",
    "Criterio": "Critério",
    "criterios": "critérios",
    "Criterios": "Critérios",
    "possivel": "possível",
    "Possivel": "Possível",
    "decisao": "decisão",
    "Decisao": "Decisão",
    "binario": "binário",
    "Binario": "Binário",
    "logica": "lógica",
    "Logica": "Lógica",
    "conteudo": "conteúdo",
    "Conteudo": "Conteúdo",
    "ligacao": "ligação",
    "Ligacao": "Ligação",
    "combinacao": "combinação",
    "Combinacao": "Combinação",
    "sao": "são",
    "Sao": "São",
    "hierarquicas": "hierárquicas",
    "Hierarquicas": "Hierárquicas",
    "legiveis": "legíveis",
    "Legiveis": "Legíveis",
    "unica": "única",
    "Unica": "Única",
    "proprio": "próprio",
    "Proprio": "Próprio",
    "convencao": "convenção",
    "Convencao": "Convenção",
    "padrao": "padrão",
    "Padrao": "Padrão",
    "basico": "básico",
    "Basico": "Básico",
    "basicos": "básicos",
    "Basicos": "Básicos",
    "classicos": "clássicos",
    "Classicos": "Clássicos",
    "proximo": "próximo",
    "Proximo": "Próximo",
    "minimo": "mínimo",
    "Minimo": "Mínimo",
    "minimos": "mínimos",
    "Minimos": "Mínimos",
    "seguranca": "segurança",
    "Seguranca": "Segurança",
    "sensiveis": "sensíveis",
    "Sensiveis": "Sensíveis",
    "sensivel": "sensível",
    "Sensivel": "Sensível",
    "pagina": "página",
    "Pagina": "Página",
    "paginas": "páginas",
    "Paginas": "Páginas",
    "referencia": "referência",
    "Referencia": "Referência",
    "referencias": "referências",
    "Referencias": "Referências",
    "correcao": "correção",
    "Correcao": "Correção",
    "inspecao": "inspeção",
    "Inspecao": "Inspeção",
    "observacao": "observação",
    "Observacao": "Observação",
    "aplicacao": "aplicação",
    "Aplicacao": "Aplicação",
    "execucao": "execução",
    "Execucao": "Execução",
    "configuracao": "configuração",
    "Configuracao": "Configuração",
    "regiao": "região",
    "Regiao": "Região",
    "retencao": "retenção",
    "Retencao": "Retenção",
    "sequencia": "sequência",
    "Sequencia": "Sequência",
    "usuario": "usuário",
    "Usuario": "Usuário",
    "usuarios": "usuários",
    "Usuarios": "Usuários",
    "saida": "saída",
    "Saida": "Saída",
    "saidas": "saídas",
    "Saidas": "Saídas",
    "informacao": "informação",
    "Informacao": "Informação",
    "informacoes": "informações",
    "Informacoes": "Informações",
    "diagnostico": "diagnóstico",
    "Diagnostico": "Diagnóstico",
    "dificil": "difícil",
    "Dificil": "Difícil",
    "investigacao": "investigação",
    "Investigacao": "Investigação",
    "operacao": "operação",
    "Operacao": "Operação",
    "producao": "produção",
    "Producao": "Produção",
    "padronizacao": "padronização",
    "Padronizacao": "Padronização",
    "organizacao": "organização",
    "Organizacao": "Organização",
    "agregacoes": "agregações",
    "Agregacoes": "Agregações",
    "otimizacao": "otimização",
    "Otimizacao": "Otimização",
    "governanca": "governança",
    "Governanca": "Governança",
    "automacao": "automação",
    "Automacao": "Automação",
    "criacao": "criação",
    "Criacao": "Criação",
    "permissao": "permissão",
    "Permissao": "Permissão",
    "permissoes": "permissões",
    "Permissoes": "Permissões",
    "requisicao": "requisição",
    "Requisicao": "Requisição",
    "requisicoes": "requisições",
    "Requisicoes": "Requisições",
    "validacao": "validação",
    "Validacao": "Validação",
    "comparacao": "comparação",
    "Comparacao": "Comparação",
    "excecao": "exceção",
    "Excecao": "Exceção",
    "excecoes": "exceções",
    "Excecoes": "Exceções",
    "intermediario": "intermediário",
    "Intermediario": "Intermediário",
    "avancado": "avançado",
    "Avancado": "Avançado",
}

UNACCENTED_PT_BR_VISIBLE_RE = re.compile(
    r"\b("
    + "|".join(
        map(re.escape, sorted(UNACCENTED_PT_BR_VISIBLE_REPLACEMENTS, key=len, reverse=True))
    )
    + r")\b"
)


def attrs_to_map(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
    return {name.lower(): value or "" for name, value in attrs if name}


def classes_from(attrs_map: dict[str, str]) -> set[str]:
    return {part for part in attrs_map.get("class", "").split() if part}


def normalize_visible(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def strip_tags(html_fragment: str) -> str:
    class TextParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.parts: list[str] = []
            self._hidden_depth = 0

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag.lower() in {"style", "script"}:
                self._hidden_depth += 1

        def handle_endtag(self, tag: str) -> None:
            if tag.lower() in {"style", "script"} and self._hidden_depth:
                self._hidden_depth -= 1

        def handle_data(self, data: str) -> None:
            if self._hidden_depth == 0 and data.strip():
                self.parts.append(data)

    parser = TextParser()
    parser.feed(html_fragment)
    parser.close()
    return normalize_visible(" ".join(parser.parts))


class VisibleTextAccentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in VISIBLE_TEXT_SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in VISIBLE_TEXT_SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0 and data.strip():
            self.parts.append(data)


def visible_text_accent_failures(html_text: str) -> list[str]:
    parser = VisibleTextAccentParser()
    parser.feed(html_text)
    parser.close()
    visible_text = normalize_visible(" ".join(parser.parts))
    findings: list[str] = []
    for match in UNACCENTED_PT_BR_VISIBLE_RE.finditer(visible_text):
        original = match.group(1)
        corrected = UNACCENTED_PT_BR_VISIBLE_REPLACEMENTS[original]
        findings.append(f"texto visível sem acentuação pt-BR: {original} -> {corrected}")
    return sorted(set(findings))


class ShapeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_html_pt_br = False
        self.has_notion_dark_marker = False
        self.has_meta_charset_utf8 = False
        self.has_viewport = False
        self.has_style = False
        self.has_title = False
        self.h1_count = 0
        self.backlink_count = 0
        self.node_contexts: list[dict[str, Any]] = []
        self.node_closings: list[dict[str, Any]] = []
        self.node_footers: list[dict[str, Any]] = []
        self.direct_main_children: list[dict[str, Any]] = []
        self.class_counts: dict[str, int] = {}
        self.visible_parts: list[str] = []
        self._hidden_depth = 0
        self._main_depth: int | None = None
        self._components: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = attrs_to_map(attrs)
        class_names = classes_from(attrs_map)
        for class_name in class_names:
            self.class_counts[class_name] = self.class_counts.get(class_name, 0) + 1

        if self._main_depth is not None and self._main_depth == 1:
            self.direct_main_children.append(
                {"tag": tag, "attrs": attrs_map, "classes": class_names}
            )

        for component in self._components:
            component["depth"] += 1
            component["tags"].append(tag)
            if tag == "p":
                component["p_count"] += 1
            if tag == "h2":
                component["h2_count"] += 1
            if tag == "h3":
                component["h3_count"] += 1
            if tag == "table":
                component["table_count"] += 1
            if tag == "ol":
                component["ol_count"] += 1
            if tag == "ul":
                component["ul_classes"].append(class_names)
            if tag == "li":
                component["li_classes"].append(class_names)
            if tag == "a":
                component["anchor_stack"].append(
                    {
                        "href": attrs_map.get("href", ""),
                        "text_parts": [],
                    }
                )
            if "reference-note" in class_names:
                component["reference_note_count"] += 1

        component_kind: str | None = None
        if "node-context" in class_names:
            component_kind = "node-context"
        elif tag == "footer" and "node-footer" in class_names:
            component_kind = "node-footer"
        elif "node-closing" in class_names:
            component_kind = "node-closing"

        if component_kind:
            component = {
                "kind": component_kind,
                "tag": tag,
                "attrs": attrs_map,
                "depth": 1,
                "text_parts": [],
                "tags": [],
                "p_count": 0,
                "h2_count": 0,
                "h3_count": 0,
                "table_count": 0,
                "ol_count": 0,
                "ul_classes": [],
                "li_classes": [],
                "reference_note_count": 0,
                "anchors": [],
                "anchor_stack": [],
            }
            self._components.append(component)
            if component_kind == "node-context":
                self.node_contexts.append(component)
            elif component_kind == "node-footer":
                self.node_footers.append(component)
            elif component_kind == "node-closing":
                self.node_closings.append(component)

        if tag == "html":
            if attrs_map.get("lang", "").lower() == "pt-br":
                self.has_html_pt_br = True
            if attrs_map.get("data-visual-theme") == "notion-dark":
                self.has_notion_dark_marker = True
        elif tag == "meta":
            charset = (attrs_map.get("charset") or "").lower()
            name = (attrs_map.get("name") or "").lower()
            if charset == "utf-8":
                self.has_meta_charset_utf8 = True
            if name == "viewport" and attrs_map.get("content"):
                self.has_viewport = True
        elif tag == "style":
            self.has_style = True
        elif tag == "title":
            self.has_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "a" and attrs_map.get("href") == "../../roadmap.html":
            self.backlink_count += 1

        if tag in {"style", "script"}:
            self._hidden_depth += 1
        if tag == "main" and self._main_depth is None:
            self._main_depth = 1
        elif self._main_depth is not None:
            self._main_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        if tag in {"style", "script"} and self._hidden_depth:
            self._hidden_depth -= 1

        for component in list(self._components):
            if tag == "a" and component["anchor_stack"]:
                anchor = component["anchor_stack"].pop()
                anchor["text"] = normalize_visible(" ".join(anchor.pop("text_parts")))
                component["anchors"].append(anchor)
            component["depth"] -= 1
            if component["depth"] <= 0:
                component["text"] = normalize_visible(" ".join(component["text_parts"]))
                self._components.remove(component)

        if self._main_depth is not None:
            self._main_depth -= 1
            if tag == "main" and self._main_depth == 0:
                self._main_depth = None

    def handle_data(self, data: str) -> None:
        if self._hidden_depth == 0 and data.strip():
            self.visible_parts.append(data)
        for component in self._components:
            if data.strip():
                component["text_parts"].append(data)
                if component["anchor_stack"]:
                    component["anchor_stack"][-1]["text_parts"].append(data)

    @property
    def visible_text(self) -> str:
        return normalize_visible(" ".join(self.visible_parts))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida a forma mecânica mínima de node.html."
    )
    parser.add_argument("--html", required=True, help="Caminho para node.html.")
    return parser.parse_args()


def style_blocks(html_text: str) -> list[str]:
    return re.findall(r"(?is)<style\b[^>]*>(.*?)</style>", html_text)


def count_root_blocks(html_text: str) -> int:
    return sum(
        len(re.findall(r"(?is)(?:^|[{}])\s*:root\s*\{", style_text))
        for style_text in style_blocks(html_text)
    )


def terminal_divider_failures(html_text: str) -> list[str]:
    failures: list[str] = []
    for style_text in style_blocks(html_text):
        for selector, body in re.findall(r"(?is)([^{}]+)\{([^{}]*)\}", style_text):
            normalized_selector = normalize_visible(selector)
            if not any(marker in normalized_selector for marker in TERMINAL_DIVIDER_SELECTORS):
                continue
            if re.search(r"(?is)\bborder-top\s*:\s*(?!0\b|none\b)", body):
                failures.append(
                    f"divisor terminal duplicado em regra CSS: {normalized_selector}"
                )
    return failures


def footer_blocks(html_text: str) -> list[str]:
    return re.findall(
        r"(?is)<footer\b(?=[^>]*\bclass\s*=\s*['\"][^'\"]*\bnode-footer\b[^'\"]*['\"])[^>]*>.*?</footer>",
        html_text,
    )


def footer_shape_failures(html_text: str) -> list[str]:
    failures: list[str] = []
    blocks = footer_blocks(html_text)
    if len(blocks) != 1:
        failures.append("footer.node-footer deve aparecer exatamente uma vez")
        return failures

    footer_html = blocks[0]
    if not re.search(r"(?is)<h2\b[^>]*>\s*Referências\s*</h2>", footer_html):
        failures.append('footer.node-footer deve ter título visível h2 "Referências"')
    if not re.search(
        r"(?is)<ul\b(?=[^>]*\bclass\s*=\s*['\"][^'\"]*\breference-list\b[^'\"]*['\"])",
        footer_html,
    ):
        failures.append("footer.node-footer deve conter ul.reference-list")
    if re.search(r"(?is)<(?:table|ol|h3)\b", footer_html):
        failures.append("footer.node-footer não deve conter table, ol ou h3")

    items = re.findall(
        r"(?is)<li\b(?=[^>]*\bclass\s*=\s*['\"][^'\"]*\breference-item\b[^'\"]*['\"])[^>]*>.*?</li>",
        footer_html,
    )
    if not items:
        failures.append("footer.node-footer deve conter ao menos um li.reference-item")
    for index, item_html in enumerate(items, start=1):
        anchors = re.findall(r"(?is)<a\b(?=[^>]*\bhref\s*=)[^>]*>", item_html)
        if len(anchors) != 1:
            failures.append(
                f"reference-item {index} deve conter exatamente um link"
            )
        if not re.search(
            r"(?is)\bclass\s*=\s*['\"][^'\"]*\breference-note\b[^'\"]*['\"]",
            item_html,
        ):
            failures.append(
                f"reference-item {index} deve conter uma nota .reference-note"
            )
        note_text = strip_tags(item_html)
        if len(note_text.split()) < 6:
            failures.append(
                f"reference-item {index} deve ter nota curta de uso, não só link solto"
            )
    return failures


def shell_order_failures(parser: ShapeParser) -> list[str]:
    failures: list[str] = []
    children = parser.direct_main_children
    if not children:
        return ["<main> deve conter shell fixo do node"]

    if len(parser.node_contexts) != 1:
        failures.append(".node-context deve aparecer exatamente uma vez")
    if len(parser.node_footers) != 1:
        failures.append("footer.node-footer deve aparecer exatamente uma vez")
    if len(parser.node_closings) > 1:
        failures.append(".node-closing deve aparecer no máximo uma vez")

    def child_label(child: dict[str, Any]) -> str:
        class_suffix = "." + ".".join(sorted(child["classes"])) if child["classes"] else ""
        return f"{child['tag']}{class_suffix}"

    expected_prefix = [
        ("a", "backlink", "primeiro filho direto de main deve ser a.backlink"),
        ("div", "node-context", "segundo filho direto de main deve ser div.node-context"),
        ("h1", "", "terceiro filho direto de main deve ser h1"),
        ("p", "lead", "quarto filho direto de main deve ser p.lead"),
    ]
    for index, (tag, class_name, message) in enumerate(expected_prefix):
        if index >= len(children):
            failures.append(message)
            continue
        child = children[index]
        if child["tag"] != tag or (class_name and class_name not in child["classes"]):
            failures.append(f"{message}; encontrado {child_label(child)}")

    footer_indexes = [
        index for index, child in enumerate(children)
        if child["tag"] == "footer" and "node-footer" in child["classes"]
    ]
    if footer_indexes:
        footer_index = footer_indexes[0]
        if footer_index != len(children) - 1:
            failures.append("footer.node-footer deve ser o último filho direto de main")
        closing_indexes = [
            index for index, child in enumerate(children)
            if "node-closing" in child["classes"]
        ]
        if closing_indexes and closing_indexes[-1] != footer_index - 1:
            failures.append(".node-closing deve aparecer imediatamente antes de footer.node-footer")
    return failures


def node_context_failures(parser: ShapeParser) -> list[str]:
    failures: list[str] = []
    if len(parser.node_contexts) != 1:
        return failures
    context = parser.node_contexts[0]
    attrs = context["attrs"]
    required_attrs = (
        "data-node-position",
        "data-level",
        "data-node-order",
        "data-node-count",
        "data-roadmap-slug",
    )
    if context["tag"] != "div":
        failures.append(".node-context deve usar tag div")
    if attrs.get("data-node-position") != "true":
        failures.append('.node-context deve declarar data-node-position="true"')
    for attr_name in required_attrs:
        if not attrs.get(attr_name):
            failures.append(f".node-context deve declarar {attr_name}")
    if context["p_count"] != 4:
        failures.append(".node-context deve conter exatamente quatro linhas p")
    forbidden_child_tags = [
        tag for tag in ("h1", "h2", "h3", "table", "ul", "ol")
        if tag in context["tags"]
    ]
    if forbidden_child_tags:
        failures.append(
            ".node-context deve conter apenas linhas compactas de orientação, "
            f"não {', '.join(sorted(set(forbidden_child_tags)))}"
        )
    context_text = normalize_visible(context.get("text", ""))
    for forbidden in FORBIDDEN_CONTEXT_TEXTS:
        if forbidden.casefold() in context_text.casefold():
            failures.append(f".node-context contém texto proibido: {forbidden}")
    if NODE_ID_VISIBLE_RE.search(context_text):
        failures.append(".node-context contém node_id ou slug técnico visível")
    return failures


def forbidden_reference_shape_failures(parser: ShapeParser, html_text: str) -> list[str]:
    failures: list[str] = []
    visible_text = parser.visible_text
    for title in FORBIDDEN_REFERENCE_TITLES:
        if title.casefold() in visible_text.casefold():
            failures.append(f"título alternativo de referências proibido: {title}")
    for class_name in FORBIDDEN_REFERENCE_CLASSES:
        if parser.class_counts.get(class_name, 0):
            failures.append(f"classe de referência antiga proibida: .{class_name}")

    html_without_footer = re.sub(
        r"(?is)<footer\b(?=[^>]*\bclass\s*=\s*['\"][^'\"]*\bnode-footer\b[^'\"]*['\"])[^>]*>.*?</footer>",
        "",
        html_text,
    )
    if re.search(r"(?is)<h3\b[^>]*>\s*Refer[êe]ncias\s*</h3>", html_without_footer):
        failures.append("referências não devem aparecer como h3 no corpo")
    if re.search(
        r"(?is)<h[23]\b[^>]*>\s*(?:Refer[êe]ncias|Fontes usadas neste node)[^<]*</h[23]>\s*<table\b",
        html_without_footer,
    ):
        failures.append("referências não devem aparecer como tabela no corpo")
    return failures


def closing_failures(parser: ShapeParser) -> list[str]:
    failures: list[str] = []
    for closing in parser.node_closings:
        text = normalize_visible(closing.get("text", ""))
        if "refer" in text.casefold():
            failures.append(".node-closing não deve conter referências")
        if closing["table_count"] or closing["ol_count"]:
            failures.append(".node-closing deve conter apenas fechamento narrativo, não tabela ou ol")
        if closing["h3_count"]:
            failures.append(".node-closing não deve conter h3 de referências ou subtítulo terminal")
    return failures


def collect_failures(html_text: str) -> list[str]:
    lower_text = html_text.lower()
    failures: list[str] = []

    if not re.search(r"(?is)^\s*<!doctype\s+html\s*>", html_text):
        failures.append("doctype HTML ausente ou não está no início do arquivo")

    parser = ShapeParser()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception as exc:  # HTMLParser is permissive, but keep the contract explicit.
        failures.append(f"HTML não parseável: {exc}")

    if not parser.has_html_pt_br:
        failures.append('tag <html lang="pt-BR"> ausente')
    if not parser.has_notion_dark_marker:
        failures.append('tag <html> deve declarar data-visual-theme="notion-dark"')
    if not parser.has_meta_charset_utf8:
        failures.append('<meta charset="utf-8"> ausente')
    if not parser.has_viewport:
        failures.append("meta viewport ausente")
    if not parser.has_style:
        failures.append("<style> ausente")
    if not parser.has_title:
        failures.append("<title> ausente")
    if parser.h1_count != 1:
        failures.append("<h1> deve aparecer exatamente uma vez")
    if parser.backlink_count != 1:
        failures.append('link de retorno para ../../roadmap.html deve aparecer exatamente uma vez')
    if count_root_blocks(html_text) != 1:
        failures.append("CSS deve conter exatamente um bloco :root canônico")
    for token in LEGACY_LIGHT_TOKENS:
        if token in lower_text:
            failures.append(f"token claro legado proibido no HTML final: {token}")
    if "```" in html_text:
        failures.append("Markdown cru detectado: fence ```")

    visible_text = parser.visible_text
    for forbidden in ("Label canônico", "Label canonico", "Node ID", "node_id"):
        if forbidden.casefold() in visible_text.casefold():
            failures.append(f"metadado técnico visível proibido: {forbidden}")
    if NODE_ID_VISIBLE_RE.search(visible_text):
        failures.append("node_id ou slug técnico visível detectado no texto da página")
    failures.extend(visible_text_accent_failures(html_text))

    for section in PROHIBITED_SECTIONS:
        if section.lower() in lower_text:
            failures.append(f"seção proibida detectada: {section}")

    for pattern in COMMAND_PATTERNS:
        if pattern.search(html_text):
            failures.append("possível sequência de comandos como corpo operacional")
            break

    failures.extend(shell_order_failures(parser))
    failures.extend(node_context_failures(parser))
    failures.extend(footer_shape_failures(html_text))
    failures.extend(forbidden_reference_shape_failures(parser, html_text))
    failures.extend(closing_failures(parser))
    failures.extend(terminal_divider_failures(html_text))

    return failures


def main() -> int:
    args = parse_args()
    html_path = Path(args.html)

    if not html_path.exists():
        print(f"falha: HTML não encontrado: {html_path}")
        return 1

    html_text = html_path.read_text(encoding="utf-8")
    failures = collect_failures(html_text)

    if failures:
        print("falha: forma mecânica inválida")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("passa: forma mecânica mínima válida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

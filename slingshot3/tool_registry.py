"""Structured tool metadata for the next SlingShot UI.

This file intentionally separates tool metadata from tool execution so the UI can
search, filter, and warn users without importing every legacy tool dependency.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    category: str
    icon: str
    description: str
    handler_name: str
    risk: str = "low"
    requires_admin: bool = False
    windows_only: bool = False
    tags: tuple[str, ...] = ()


TOOL_REGISTRY: tuple[ToolDefinition, ...] = (
    ToolDefinition(
        name="System Snapshot",
        category="Dashboard",
        icon="📊",
        description="Quick local system health summary: OS, CPU, memory, disk, and uptime.",
        handler_name="system_snapshot",
        tags=("health", "system", "triage"),
    ),
    ToolDefinition(
        name="Process Review",
        category="Monitoring",
        icon="🧠",
        description="Shows top local processes by memory usage for quick troubleshooting.",
        handler_name="process_review",
        tags=("process", "memory", "triage"),
    ),
    ToolDefinition(
        name="Network Summary",
        category="Network",
        icon="🌐",
        description="Shows local hostname, addresses, and network counters.",
        handler_name="network_summary",
        tags=("network", "local", "triage"),
    ),
    ToolDefinition(
        name="Disk Usage Review",
        category="Utility",
        icon="💽",
        description="Lists local disk partitions and usage percentages.",
        handler_name="disk_usage_review",
        tags=("disk", "storage", "cleanup"),
    ),
    ToolDefinition(
        name="Config Audit",
        category="Utility",
        icon="🧾",
        description="Checks SlingShot config for invalid favorites, missing values, and bad defaults.",
        handler_name="config_audit",
        tags=("config", "audit", "repo"),
    ),
    ToolDefinition(
        name="Defender Status",
        category="Security",
        icon="🛡️",
        description="Reads Microsoft Defender status on Windows when PowerShell cmdlets are available.",
        handler_name="defender_status",
        risk="medium",
        windows_only=True,
        tags=("windows", "defender", "endpoint"),
    ),
    ToolDefinition(
        name="Firewall Status",
        category="Security",
        icon="🔥",
        description="Reads Windows Firewall profile status without changing settings.",
        handler_name="firewall_status",
        risk="medium",
        windows_only=True,
        tags=("windows", "firewall", "endpoint"),
    ),
    ToolDefinition(
        name="Generate Triage Report",
        category="Reports",
        icon="📄",
        description="Builds a local endpoint triage report from safe read-only checks.",
        handler_name="generate_triage_report",
        risk="low",
        tags=("report", "export", "triage"),
    ),
)


CATEGORY_ORDER = (
    "Dashboard",
    "Security",
    "Monitoring",
    "Network",
    "Utility",
    "Reports",
)


def all_tools() -> tuple[ToolDefinition, ...]:
    return TOOL_REGISTRY


def categories() -> tuple[str, ...]:
    known = {tool.category for tool in TOOL_REGISTRY}
    ordered = [category for category in CATEGORY_ORDER if category in known]
    extras = sorted(known.difference(ordered))
    return tuple(ordered + extras)


def find_tool(name: str) -> ToolDefinition | None:
    lowered = name.casefold()
    for tool in TOOL_REGISTRY:
        if tool.name.casefold() == lowered:
            return tool
    return None


def filter_tools(query: str = "", category: str | None = None) -> tuple[ToolDefinition, ...]:
    query = query.strip().casefold()
    results: list[ToolDefinition] = []
    for tool in TOOL_REGISTRY:
        if category and category != "All" and tool.category != category:
            continue
        haystack = " ".join((tool.name, tool.category, tool.description, " ".join(tool.tags))).casefold()
        if query and query not in haystack:
            continue
        results.append(tool)
    return tuple(results)


def risky_tools(tools: Iterable[ToolDefinition] = TOOL_REGISTRY) -> tuple[ToolDefinition, ...]:
    return tuple(tool for tool in tools if tool.risk in {"medium", "high", "critical"} or tool.requires_admin)

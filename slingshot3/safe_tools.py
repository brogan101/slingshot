"""Safe local tool handlers for the next SlingShot UI.

These handlers are intentionally read-only unless a future workflow explicitly
adds confirmation and dry-run behavior.
"""
from __future__ import annotations

import json
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import psutil

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
CONFIG_PATH = APP_DIR / "config.json"
REPORTS_DIR = ROOT / "reports"


def _format_bytes(value: float) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    number = float(value)
    for unit in units:
        if abs(number) < 1024 or unit == units[-1]:
            return f"{number:.1f} {unit}"
        number /= 1024
    return f"{number:.1f} TB"


def _safe_run_powershell(command: str, timeout: int = 20) -> str:
    if platform.system() != "Windows":
        return "This check is Windows-only."
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return "PowerShell was not found on this system."
    except subprocess.TimeoutExpired:
        return f"PowerShell check timed out after {timeout} seconds."

    output = result.stdout.strip()
    error = result.stderr.strip()
    if result.returncode != 0:
        return error or f"PowerShell exited with code {result.returncode}."
    return output or "No output returned."


def system_snapshot() -> str:
    boot = datetime.fromtimestamp(psutil.boot_time())
    uptime_seconds = int(time.time() - psutil.boot_time())
    uptime = f"{uptime_seconds // 86400}d {(uptime_seconds % 86400) // 3600}h {(uptime_seconds % 3600) // 60}m"
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(Path.home().anchor or "/")

    lines = [
        "SYSTEM SNAPSHOT",
        "=" * 15,
        f"Computer: {socket.gethostname()}",
        f"OS: {platform.system()} {platform.release()} ({platform.version()})",
        f"Python: {sys.version.split()[0]}",
        f"Boot time: {boot:%Y-%m-%d %H:%M:%S}",
        f"Uptime: {uptime}",
        f"CPU: {psutil.cpu_percent(interval=0.5):.1f}% used across {psutil.cpu_count(logical=True)} logical cores",
        f"Memory: {memory.percent:.1f}% used ({_format_bytes(memory.used)} / {_format_bytes(memory.total)})",
        f"Primary disk: {disk.percent:.1f}% used ({_format_bytes(disk.used)} / {_format_bytes(disk.total)})",
    ]
    return "\n".join(lines)


def process_review(limit: int = 15) -> str:
    rows: list[tuple[float, int, str, float]] = []
    for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            info = proc.info
            rows.append((float(info.get("memory_percent") or 0), int(info.get("pid") or 0), str(info.get("name") or "unknown"), proc.cpu_percent(interval=None)))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    rows.sort(reverse=True)
    lines = ["PROCESS REVIEW", "=" * 14, f"Top {limit} processes by memory usage:", ""]
    lines.append(f"{'PID':>7}  {'MEM%':>6}  NAME")
    lines.append("-" * 45)
    for mem_percent, pid, name, _cpu in rows[:limit]:
        lines.append(f"{pid:>7}  {mem_percent:>6.2f}  {name[:28]}")
    return "\n".join(lines)


def network_summary() -> str:
    counters = psutil.net_io_counters()
    addresses = []
    for name, values in psutil.net_if_addrs().items():
        for addr in values:
            if getattr(addr, "family", None) == socket.AF_INET:
                addresses.append(f"{name}: {addr.address}")

    lines = [
        "NETWORK SUMMARY",
        "=" * 15,
        f"Hostname: {socket.gethostname()}",
        f"Bytes sent: {_format_bytes(counters.bytes_sent)}",
        f"Bytes received: {_format_bytes(counters.bytes_recv)}",
        "",
        "IPv4 addresses:",
    ]
    lines.extend(f"- {entry}" for entry in addresses[:20])
    if not addresses:
        lines.append("- No IPv4 addresses found.")
    return "\n".join(lines)


def disk_usage_review() -> str:
    lines = ["DISK USAGE REVIEW", "=" * 17]
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            lines.append(f"{part.device} mounted at {part.mountpoint}: permission denied")
            continue
        lines.append(
            f"{part.device} mounted at {part.mountpoint}: {usage.percent:.1f}% used "
            f"({_format_bytes(usage.used)} / {_format_bytes(usage.total)})"
        )
    return "\n".join(lines)


def config_audit() -> str:
    if not CONFIG_PATH.exists():
        return "Config file is missing: slingshot3/config.json"
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"Config JSON is invalid: {exc}"

    problems: list[str] = []
    favorites = config.get("favorites", [])
    if not isinstance(favorites, list):
        problems.append("favorites must be a list")
    elif any(item is None or item == "" for item in favorites):
        problems.append("favorites contains blank/null entries")

    timeout = config.get("default_timeout")
    if not isinstance(timeout, int) or timeout <= 0:
        problems.append("default_timeout must be a positive integer")

    theme = config.get("theme")
    if theme not in {"Dark", "Light", "System"}:
        problems.append("theme should be Dark, Light, or System")

    if not problems:
        return "CONFIG AUDIT\n============\nOK - config looks sane."
    return "CONFIG AUDIT\n============\n" + "\n".join(f"- {problem}" for problem in problems)


def defender_status() -> str:
    command = "Get-MpComputerStatus | Select-Object AMServiceEnabled,AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated,QuickScanAge,FullScanAge | Format-List"
    return "DEFENDER STATUS\n===============\n" + _safe_run_powershell(command)


def firewall_status() -> str:
    command = "Get-NetFirewallProfile | Select-Object Name,Enabled,DefaultInboundAction,DefaultOutboundAction | Format-Table -AutoSize | Out-String -Width 200"
    return "FIREWALL STATUS\n===============\n" + _safe_run_powershell(command)


def generate_triage_report() -> str:
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"slingshot_triage_{timestamp}.txt"
    sections = [
        system_snapshot(),
        "\n" + process_review(),
        "\n" + network_summary(),
        "\n" + disk_usage_review(),
        "\n" + config_audit(),
    ]
    if platform.system() == "Windows":
        sections.append("\n" + defender_status())
        sections.append("\n" + firewall_status())
    report_path.write_text("\n\n".join(sections), encoding="utf-8")
    return f"Triage report created:\n{report_path}"


HANDLERS = {
    "system_snapshot": system_snapshot,
    "process_review": process_review,
    "network_summary": network_summary,
    "disk_usage_review": disk_usage_review,
    "config_audit": config_audit,
    "defender_status": defender_status,
    "firewall_status": firewall_status,
    "generate_triage_report": generate_triage_report,
}


def run_handler(handler_name: str) -> str:
    handler = HANDLERS.get(handler_name)
    if handler is None:
        return f"Unknown handler: {handler_name}"
    try:
        return handler()
    except Exception as exc:  # keep UI alive even if a tool fails
        return f"Tool failed: {type(exc).__name__}: {exc}"

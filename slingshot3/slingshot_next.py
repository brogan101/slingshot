"""Next-generation SlingShot UI path.

This file does not replace the legacy app yet. It provides a cleaner dashboard,
searchable registry, and safer read-only handlers so the project can move
forward without breaking the existing 4k+ line application.
"""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from safe_tools import run_handler
from tool_registry import ToolDefinition, categories, filter_tools

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SlingShotNext(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("SlingShot Next")
        self.geometry("1180x760")
        self.minsize(980, 640)

        self.result_queue: queue.Queue[str] = queue.Queue()
        self.selected_category = tk.StringVar(value="All")
        self.search_var = tk.StringVar(value="")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(20, weight=1)

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        self._build_sidebar()
        self._build_content()
        self.refresh_tools()
        self.after(100, self._drain_results)

    def _build_sidebar(self) -> None:
        title = ctk.CTkLabel(self.sidebar, text="SlingShot", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=(26, 2), sticky="w")

        subtitle = ctk.CTkLabel(self.sidebar, text="Next-gen local toolkit", text_color=("gray45", "gray70"))
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 22), sticky="w")

        all_button = ctk.CTkButton(self.sidebar, text="All Tools", command=lambda: self.set_category("All"), anchor="w")
        all_button.grid(row=2, column=0, padx=16, pady=5, sticky="ew")

        row = 3
        for category in categories():
            button = ctk.CTkButton(
                self.sidebar,
                text=category,
                command=lambda c=category: self.set_category(c),
                anchor="w",
                fg_color="transparent",
                hover_color=("gray80", "gray25"),
            )
            button.grid(row=row, column=0, padx=16, pady=4, sticky="ew")
            row += 1

        legacy = ctk.CTkLabel(
            self.sidebar,
            text="Legacy app is still available as slingshot.py. This path is the cleaned upgrade lane.",
            wraplength=185,
            justify="left",
            text_color=("gray45", "gray70"),
        )
        legacy.grid(row=20, column=0, padx=20, pady=20, sticky="sw")

    def _build_content(self) -> None:
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 10))
        header.grid_columnconfigure(0, weight=1)

        self.heading = ctk.CTkLabel(header, text="All Tools", font=ctk.CTkFont(size=24, weight="bold"))
        self.heading.grid(row=0, column=0, sticky="w")

        self.search = ctk.CTkEntry(header, textvariable=self.search_var, placeholder_text="Search tools, tags, descriptions...")
        self.search.grid(row=0, column=1, sticky="e", padx=(12, 0), ipadx=80)
        self.search_var.trace_add("write", lambda *_: self.refresh_tools())

        info = ctk.CTkFrame(self.content)
        info.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 12))
        info.grid_columnconfigure((0, 1, 2), weight=1)

        self.stat_tools = ctk.CTkLabel(info, text="Tools: 0", font=ctk.CTkFont(size=15, weight="bold"))
        self.stat_tools.grid(row=0, column=0, padx=18, pady=14, sticky="w")
        ctk.CTkLabel(info, text="Execution: threaded / UI-safe", text_color=("gray35", "gray70")).grid(row=0, column=1, padx=18, pady=14)
        ctk.CTkLabel(info, text="Mode: local-first", text_color=("gray35", "gray70")).grid(row=0, column=2, padx=18, pady=14, sticky="e")

        split = ctk.CTkFrame(self.content, fg_color="transparent")
        split.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 24))
        split.grid_columnconfigure(0, weight=1)
        split.grid_columnconfigure(1, weight=1)
        split.grid_rowconfigure(0, weight=1)

        self.tools_frame = ctk.CTkScrollableFrame(split, label_text="Toolbox")
        self.tools_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.tools_frame.grid_columnconfigure(0, weight=1)

        output_frame = ctk.CTkFrame(split)
        output_frame.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(output_frame, text="Output", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))
        self.output = ctk.CTkTextbox(output_frame, wrap="word")
        self.output.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        self.output.insert("1.0", "Ready. Select a tool to run.\n")

    def set_category(self, category: str) -> None:
        self.selected_category.set(category)
        self.heading.configure(text=category if category != "All" else "All Tools")
        self.refresh_tools()

    def refresh_tools(self) -> None:
        for child in self.tools_frame.winfo_children():
            child.destroy()

        tools = filter_tools(self.search_var.get(), self.selected_category.get())
        self.stat_tools.configure(text=f"Tools: {len(tools)}")

        if not tools:
            ctk.CTkLabel(self.tools_frame, text="No tools matched your search.").grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, tool in enumerate(tools):
            self._add_tool_card(index, tool)

    def _add_tool_card(self, row: int, tool: ToolDefinition) -> None:
        card = ctk.CTkFrame(self.tools_frame)
        card.grid(row=row, column=0, padx=12, pady=8, sticky="ew")
        card.grid_columnconfigure(1, weight=1)

        icon = ctk.CTkLabel(card, text=tool.icon, font=ctk.CTkFont(size=26))
        icon.grid(row=0, column=0, rowspan=3, padx=(14, 10), pady=12, sticky="n")

        title = ctk.CTkLabel(card, text=tool.name, font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=1, padx=0, pady=(12, 2), sticky="w")

        desc = ctk.CTkLabel(card, text=tool.description, wraplength=430, justify="left", text_color=("gray35", "gray70"))
        desc.grid(row=1, column=1, padx=0, pady=2, sticky="w")

        meta = f"{tool.category} • risk: {tool.risk}"
        if tool.windows_only:
            meta += " • Windows-only"
        if tool.requires_admin:
            meta += " • admin"
        ctk.CTkLabel(card, text=meta, text_color=("gray45", "gray65"), font=ctk.CTkFont(size=12)).grid(row=2, column=1, padx=0, pady=(2, 12), sticky="w")

        run_button = ctk.CTkButton(card, text="Run", width=82, command=lambda t=tool: self.run_tool(t))
        run_button.grid(row=0, column=2, rowspan=3, padx=14, pady=12)

    def run_tool(self, tool: ToolDefinition) -> None:
        if tool.risk in {"high", "critical"}:
            if not messagebox.askyesno("Confirm tool run", f"Run {tool.name}?\n\nRisk level: {tool.risk}"):
                return
        self.output.insert("end", f"\n\n▶ Running {tool.name}...\n")
        self.output.see("end")

        def worker() -> None:
            result = run_handler(tool.handler_name)
            self.result_queue.put(f"\n[{tool.name}]\n{result}\n")

        threading.Thread(target=worker, daemon=True).start()

    def _drain_results(self) -> None:
        while True:
            try:
                result = self.result_queue.get_nowait()
            except queue.Empty:
                break
            self.output.insert("end", result)
            self.output.see("end")
        self.after(100, self._drain_results)


def main() -> None:
    app = SlingShotNext()
    app.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Operational Stack Tree Synchronizer Script (OPSTACK-SYNC-v1.0)
License: Unlicense (Public Domain - Zero-Rent Federation)

Synchronizes Section 1 of README.md and specs/OPERATIONAL-STACK-MASTER-INDEX.md
with the exact, live filesystem tree across articles/, schema/, proofs/, and specs/.
Zero external dependencies.
"""

import os
import re
import sys

def sync_trees():
    articles = sorted(os.listdir("articles"))
    schemas = sorted(os.listdir("schema"))
    proofs = sorted(os.listdir("proofs"))
    specs = sorted(os.listdir("specs"))

    # Filter out hidden or non-repo files
    articles = [a for a in articles if not a.startswith(".")]
    schemas = [s for s in schemas if not s.startswith(".")]
    proofs = [p for p in proofs if not p.startswith(".")]
    specs = [sp for sp in specs if not sp.startswith(".") and sp != "OPERATIONAL-STACK-MASTER-INDEX.md" and sp != "README.md"]

    # 1. Update specs/OPERATIONAL-STACK-MASTER-INDEX.md
    master_index_lines = [
        "# OPERATIONAL STACK MASTER INDEX\n",
        "## KERNEL & SPECIFICATIONS",
        "- `KERNEL.md` - Operational Stack Core Axioms, Cybernetic Invariants, and Execution Gates."
    ]
    for s in specs:
        master_index_lines.append(f"- `specs/{s}`")

    master_index_lines.append("\n## SCHEMAS (`schema/`)")
    for sch in schemas:
        master_index_lines.append(f"- `schema/{sch}`")

    master_index_lines.append("\n## PROOFS & ENGINES (`proofs/`)")
    for pr in proofs:
        master_index_lines.append(f"- `proofs/{pr}`")

    with open("specs/OPERATIONAL-STACK-MASTER-INDEX.md", "w", encoding="utf-8") as f:
        f.write("\n".join(master_index_lines) + "\n")
    print("[+] Synchronized specs/OPERATIONAL-STACK-MASTER-INDEX.md")

    # 2. Update Section 1 of README.md
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Reconstruct the tree block for README.md
    tree_lines = [
        "```text",
        "move6729 / operational-stack:",
        "├── .gitignore",
        "├── CONVENTIONS.md                  [System Constraints & Architectural Writing Guidelines]",
        "├── fetch_substack.py               [Substack Publication Synchronizer Script]",
        "├── KERNEL.md                       [Hyper-Dense Axiomatic Baseline & Mathematical Invariants]",
        "├── LICENSE                         [Unlicense - Public Domain]",
        "├── prompt.txt                      [LLM System Invariant Baseline Context]",
        "├── README.md                       [Master Context & System Specification Index]",
        "├── run_all_proofs.sh               [Iterative Python Verification Engine Execution Script]",
        "│"
    ]

    # articles/
    tree_lines.append("├── articles/                       [Public Canonical Articles & Essays]")
    for i, a in enumerate(articles):
        prefix = "└── " if (i == len(articles) - 1) else "├── "
        tree_lines.append(f"│   {prefix}{a}")
    tree_lines.append("│")

    # schema/
    tree_lines.append("├── schema/                         [JSON Draft 2020-12 Structural Contracts]")
    for i, sch in enumerate(schemas):
        prefix = "└── " if (i == len(schemas) - 1) else "├── "
        tree_lines.append(f"│   {prefix}{sch}")
    tree_lines.append("│")

    # proofs/
    tree_lines.append("├── proofs/                         [Runnable Zero-Dependency Deterministic Verification Engines]")
    for i, pr in enumerate(proofs):
        prefix = "└── " if (i == len(proofs) - 1) else "├── "
        tree_lines.append(f"│   {prefix}{pr}")
    tree_lines.append("│")

    # specs/
    tree_lines.append("└── specs/                          [Canonical System Audits & Invariants]")
    for i, sp in enumerate(specs):
        prefix = "└── " if (i == len(specs) - 1) else "├── "
        tree_lines.append(f"    {prefix}{sp}")
    tree_lines.append("```")

    new_tree_str = "\n".join(tree_lines)

    # Replace Section 1 tree block in README.md
    pattern = r"(## 1\. SYSTEM DIRECTORY TREE & REPOSITORY MAP\s*\n\n)```text\n.*?```"
    new_readme, match_count = re.subn(pattern, r"\1" + new_tree_str, readme_content, count=1, flags=re.DOTALL)
    if match_count != 1:
        print(f"[-] ERROR: Failed to match Section 1 tree fence in README.md (matches={match_count})", file=sys.stderr)
        sys.exit(1)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)
    print("[+] Synchronized Section 1 of README.md")

if __name__ == "__main__":
    sync_trees()

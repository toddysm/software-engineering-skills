# Software Engineering Skills

A curated collection of AI agent skills for GitHub Copilot and Anthropic Claude that extend their capabilities for software engineering workflows. Each skill packages domain knowledge, structured workflows, and tool integrations into a reusable unit that can be invoked by natural language.

## What Are Skills?

Skills are instruction files (`.md`) that teach an AI agent how to perform a specific, repeatable engineering task. They define:
- **When to activate** — trigger phrases and use-case descriptions
- **How to execute** — step-by-step workflows, tool usage, and decision logic
- **What to produce** — output formats, file structures, and deliverables

Skills live under `.github/skills/{skill-name}/SKILL.md` and are referenced from the agent's configuration.

---

## Skills

### Codebase Architecture Analyst

> **Location**: [`.github/skills/codebase-architecture-analyst/SKILL.md`](.github/skills/codebase-architecture-analyst/SKILL.md)

Performs deep, file-level analysis of a codebase to reverse-engineer its architecture and produce comprehensive documentation and security reports.

**Trigger phrases**: "reverse engineer this project", "analyze codebase architecture", "explain this project", "run a security audit", "generate architecture from code"

**Capabilities**:
- Scans every source file to understand its purpose via documentation and code structure analysis
- Catalogs all functions, classes, and exports with their roles and responsibilities
- Maps bi-directional dependencies at file and function/class level, enabling impact analysis ("if I change X, what breaks?")
- Generates Mermaid architecture diagrams: component structure, data flow, deployment topology, and more
- Produces plain-English security analysis covering OWASP Top 10, secrets detection, attack surface mapping, and dependency CVEs
- Runs language-appropriate SAST tools (bandit, semgrep, gosec, eslint-security, brakeman, etc.) with fallback to Docker or documented manual instructions
- Saves all output to a **user-specified path** — the analyzed project is never modified

**Output** (saved under `{output-path}/{project-name}/{timestamp}/`):
| Folder | Contents |
|---|---|
| `source-files/` | File inventory, per-file analysis, documentation map |
| `dependencies/` | Dependency graph, function-level usage, impact analysis, circular dependency detection |
| `analysis/` | Security overview, architecture summary, component guide, technology decisions |
| `security/` | Detailed security report, vulnerability JSON, remediation guide, attack surface map, dependency audit, raw tool output |
| `interactive/` | Queryable dependency database, example queries |
| `visuals/` | Architecture diagrams, dependency graphs, security model |

**Prerequisites for comprehensive security analysis**:

> The skill performs AI-assisted analysis without any additional tools. For full automated security scanning, the following tools should be installed depending on the languages in the codebase being analyzed. The skill will detect what is available, use Docker as a fallback, and document any tools that were skipped.

| Language / Scope | Tools |
|---|---|
| Python | `bandit`, `semgrep`, `pip-audit`, `safety`, `detect-secrets`, `truffleHog3` |
| JavaScript / TypeScript | `semgrep`, `njsscan`, `eslint` + security plugins, `retire.js`, `gitleaks` |
| Go | `gosec`, `govulncheck`, `semgrep`, `nancy` |
| Java / Kotlin | `semgrep`, `SpotBugs` + `find-sec-bugs`, `PMD`, `grype` |
| C# / .NET | `semgrep`, `dotnet` CLI (built-in) |
| Ruby | `brakeman`, `bundle-audit`, `semgrep` |
| PHP | `psalm`, `phpcs` + `phpcs-security-audit`, `semgrep` |
| Rust | `cargo audit`, `cargo deny`, `semgrep` |
| C / C++ | `flawfinder`, `cppcheck`, `clang-tidy`, `semgrep` |
| Infrastructure as Code | `checkov`, `trivy`, `tfsec`, `kics`, `hadolint` |
| All projects (universal) | `gitleaks`, `truffleHog3`, `grype`, `syft`, `semgrep` (OWASP pack) |

See [SKILL.md](.github/skills/codebase-architecture-analyst/SKILL.md) for full workflow details, security test categories, automated tool reference, and AI-assisted analysis techniques.

---

## Contributing

Each skill lives in its own subdirectory under `.github/skills/`. To add a new skill:

1. Create `.github/skills/{skill-name}/SKILL.md`
2. Add supporting assets, reference docs, and scripts in subdirectories as needed
3. Add a section to this README following the pattern above


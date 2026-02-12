---
name: agents-md-generator
description: Analyze repository structure and generate standardized AGENTS.md files that serve as contributor guides for AI agents. Measures LOC to determine character limits and produces 5-section documents covering overview, folder structure, patterns, conventions, and working agreements.
---

# AGENTS.md Generation Capability

This skill enables the agent to analyze any repository and generate a comprehensive `AGENTS.md` file that serves as a contributor guide for AI agents working on the codebase.

## When to Use This Skill

Activate this skill when asked to:
- "Generate AGENTS.md"
- "Create a contributor guide for AI agents"
- "Analyze the repository structure"
- "Document the codebase for AI assistants"
- "Create documentation for this project"
- "Help AI understand this repository"

## Workflow Overview

1. **Measure Repository Size**: Use `tokei` to count LOC and determine character limits
2. **Analyze Structure**: Inspect directory tree, key files, and code patterns
3. **Extract Patterns**: Review code samples to identify conventions and behaviors
4. **Generate Document**: Create AGENTS.md with 5 standardized sections
5. **Validate**: Ensure output meets character limits and includes all required sections

## Core Capability

- **Function**: Analyze repository structure and generate a standardized `AGENTS.md` document
- **Output Format**: Markdown file with structured sections
- **Character Limit**: Dynamic, based on repository LOC (Lines of Code)
- **Analysis Method**: Read-only commands only (no execution, testing, or building)

## Output Sections

The generated `AGENTS.md` consists of exactly 5 sections:

| # | Section | Purpose |
|---|---------|---------|
| 1 | Overview | 1-2 sentence project description (abstract, no tool/framework lists) |
| 2 | Folder Structure | Key directories and their contents |
| 3 | Core Behaviors & Patterns | Logging, error handling, control flow patterns observed in code |
| 4 | Conventions | Naming, comments, code style derived from analysis |
| 5 | Working Agreements | Rules for agent behavior and communication |

## Domain Knowledge

- **LOC Measurement**: Capability to measure repository size and determine character limits. See [./references/loc_measurement.md](./references/loc_measurement.md)
- **Repository Analysis**: Capability to inspect and understand codebase structure. See [./references/read_only_commands.md](./references/read_only_commands.md)
- **Output Template**: Standardized AGENTS.md structure specification. See [./references/agents_md_template.md](./references/agents_md_template.md)
- **Working Agreements**: Agent behavior rules for generated documents. See [./references/working_agreements.md](./references/working_agreements.md)

## Constraints & Safety

- **Read-Only Analysis**: Repository inspection uses only non-destructive commands
- **No Run/Test/Build/Deploy**: Generated AGENTS.md excludes execution instructions
- **Files to Ignore**: Lock files (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, etc.)
- **Respect .gitignore**: Exclude build artifacts, node_modules, and generated files
- **Character Limits**: Strictly enforce limits based on repository size

## Step-by-Step Generation Process

### Step 1: Measure Repository Size

1. Run `tokei` to count LOC (see [./references/loc_measurement.md](./references/loc_measurement.md))
2. Determine character limit based on total LOC:
   - ≤ 10K LOC: 10,000 chars
   - 10K-50K LOC: 10,000 chars
   - 50K-100K LOC: 10,000 chars
   - 100K-500K LOC: 15,000 chars
   - 500K-1M LOC: 20,000 chars
   - > 1M LOC: 30,000 chars

### Step 2: Analyze Repository Structure

1. Use `tree` to visualize directory hierarchy (ignore node_modules, .git, build artifacts)
2. Identify key directories and their architectural roles
3. Read configuration files (.editorconfig, eslintrc, prettierrc, etc.)
4. Review README.md and documentation for context

### Step 3: Extract Code Patterns

1. Use `rg` (ripgrep) to search for common patterns (preferred over grep)
2. Sample up to 800 lines per file (excluding imports)
3. Identify:
   - Logging and debugging patterns
   - Error handling approaches
   - Control flow conventions
   - Module organization

### Step 4: Identify Conventions

1. Analyze naming patterns (camelCase, PascalCase, snake_case)
2. Review comment styles and documentation patterns
3. Note code organization and file structure preferences
4. Identify testing frameworks if present

### Step 5: Generate AGENTS.md

1. Write 5 sections in order (see [./references/agents_md_template.md](./references/agents_md_template.md)):
   - Overview (1-2 sentences)
   - Folder Structure (hierarchical, role-focused)
   - Core Behaviors & Patterns (from code analysis)
   - Conventions (naming, comments, style)
   - Working Agreements (compressed format)
2. Validate total character count
3. Write file to repository root

## Example Output Quality

### Good Overview Example
```markdown
## 1. Overview

A Groovy-based IntelliJ IDEA plugin providing AI-assisted code generation and refactoring capabilities.
```

### Bad Overview Example (Too Detailed)
```markdown
## 1. Overview

This is an IntelliJ IDEA plugin written in Groovy using Gradle 8.5 and JDK 17. It uses Micronaut for dependency injection, Spock for testing, and integrates with OpenAI's API. The plugin provides features like code generation, refactoring suggestions, and natural language processing.
```

## Common Mistakes to Avoid

- **Flat folder structure**: Always show hierarchy with nested bullets
- **Generic descriptions**: Explain roles, not just names ("UI components" not "UI folder")
- **Missing conventions**: Always analyze actual code patterns, don't assume
- **Character overflow**: Validate final output against limits
- **Execution instructions**: Never include build/run/test commands
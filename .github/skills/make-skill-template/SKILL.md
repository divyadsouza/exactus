---
name: make-skill-template
description: 'Create new Agent Skills for AI assistants from prompts or by duplicating this template. Use when asked to "create a skill", "make a new skill", "scaffold a skill", or when building specialized AI capabilities with bundled resources. Generates SKILL.md files with proper frontmatter, directory structure, and optional scripts/references/assets folders.'
---

# Make Skill Template

A meta-skill for creating new Agent Skills. Use this skill when you need to scaffold a new skill folder, generate a SKILL.md file, or help users understand the Agent Skills specification.

## When to Use This Skill

- User asks to "create a skill", "make a new skill", or "scaffold a skill"
- User wants to add a specialized capability to their AI assistant setup
- User needs help structuring a skill with bundled resources
- User wants to duplicate this template as a starting point

## Prerequisites

- Understanding of what the skill should accomplish
- A clear, keyword-rich description of capabilities and triggers
- Knowledge of any bundled resources needed (scripts, references, assets, templates)

## Creating a New Skill

### Step 1: Create the Skill Directory

Create a new folder with a lowercase, hyphenated name:

```
skills/<skill-name>/
└── SKILL.md          # Required
```

### Step 2: Generate SKILL.md with Frontmatter

Every skill requires YAML frontmatter with `name` and `description`:

```yaml
---
name: <skill-name>
description: '<What it does>. Use when <specific triggers, scenarios, keywords users might say>.'
---
```

#### Frontmatter Field Requirements

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | 1-64 chars, lowercase letters/numbers/hyphens only, must match folder name |
| `description` | **Yes** | 1-1024 chars, must describe WHAT it does AND WHEN to use it |
| `license` | No | License name or reference to bundled LICENSE.txt |
| `compatibility` | No | 1-500 chars, environment requirements if needed |
| `metadata` | No | Key-value pairs for additional properties (e.g., version, author) |
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental) - e.g., `read_file grep_search run_in_terminal` |

#### Description Best Practices

**CRITICAL**: The `description` is the PRIMARY mechanism for automatic skill discovery. Include:

1. **WHAT** the skill does (capabilities)
2. **WHEN** to use it (triggers, scenarios, file types)
3. **Keywords** users might mention in prompts

**Good example:**

```yaml
description: 'Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.'
```

**Poor example:**

```yaml
description: 'Helps with PDFs.'
```

#### Advanced Frontmatter Example

For skills with specific compatibility needs or metadata:

```yaml
---
name: database-optimizer
description: 'Analyzes SQL queries, suggests indexes, and optimizes database schema. Use when working with databases, SQL, performance issues, slow queries, or when the user mentions database optimization, indexing, or query tuning.'
compatibility: 'Requires PostgreSQL 12+, MySQL 8+, or SQLite 3.35+'
metadata:
  version: '1.2.0'
  author: 'Database Team'
  last-updated: '2026-01-15'
allowed-tools: 'read_file run_in_terminal grep_search'
---
```

### Step 3: Write the Skill Body

After the frontmatter, add markdown instructions. Recommended sections:

| Section | Purpose |
|---------|---------|
| `# Title` | Brief overview |
| `## When to Use This Skill` | Reinforces description triggers |
| `## Prerequisites` | Required tools, dependencies |
| `## Step-by-Step Workflows` | Numbered steps for tasks |
| `## Troubleshooting` | Common issues and solutions |
| `## References` | Links to bundled docs |

### Step 4: Add Optional Directories (If Needed)

| Folder | Purpose | When to Use | Examples |
|--------|---------|-------------|----------|
| `scripts/` | Executable code (Python, Bash, JS) | Automation that performs operations | `validate.py`, `setup.sh`, `migrate.js` |
| `references/` | Additional documentation loaded on demand | Detailed technical references, domain-specific docs | `REFERENCE.md`, `api_docs.md`, `examples.md` |
| `assets/` | Static resources | Templates, images, data files, schemas | `template.yaml`, `schema.json`, `diagram.png` |

**Best Practices for Bundled Resources:**

- Keep total skill size under 10MB for performance
- Use `references/` for content loaded on-demand via explicit file references
- Place frequently needed content directly in SKILL.md
- Store binary files (images, PDFs) in `assets/` only when essential
- Scripts should be self-contained with clear usage comments

## Example: Complete Skill Structure

```
my-awesome-skill/
├── SKILL.md                    # Required instructions
├── LICENSE.txt                 # Optional license file
├── scripts/
│   └── helper.py               # Executable automation
├── references/
│   ├── REFERENCE.md            # Detailed technical reference
│   └── examples.md             # Usage examples
├── assets/
│   ├── diagram.png             # Static resources
│   └── template.json           # Configuration templates
```

## Quick Start: Duplicate This Template

1. Copy the `make-skill-template/` folder
2. Rename to your skill name (lowercase, hyphens)
3. Update `SKILL.md`:
   - Change `name:` to match folder name
   - Write a keyword-rich `description:`
   - Replace body content with your instructions
4. Add bundled resources as needed (scripts, references, assets)
5. Test the skill with a real prompt to verify it triggers correctly
6. Validate with `skills-ref validate ./your-skill-name/` (if available)

## Testing Your Skill

Before deploying a new skill, verify it works correctly:

1. **Trigger Test**: Create a prompt that should activate the skill
   - Example: For a PDF skill, try "extract text from this PDF"
   - Verify the AI assistant loads and uses your skill

2. **Resource Test**: If you have bundled resources, reference them explicitly
   - Example: "Use the template in assets/config.json"
   - Confirm the assistant can access and use the resources

3. **Edge Case Test**: Try ambiguous prompts to ensure proper skill selection
   - Test with similar but different requests
   - Verify your skill only triggers for appropriate scenarios

4. **Validation**: Run formal validation if tools are available
   ```bash
   skills-ref validate ./your-skill-name/
   ```

## Validation Checklist

- [ ] Folder name is lowercase with hyphens, no special characters
- [ ] `name` field matches folder name exactly (case-sensitive)
- [ ] `description` is 1-1024 characters with WHAT, WHEN, and keywords
- [ ] `description` explains WHAT it does and WHEN to use it
- [ ] `description` includes specific keywords and trigger phrases
- [ ] Body content is under 500 lines (recommended for performance)
- [ ] File references are one level deep from SKILL.md
- [ ] Tested with real prompts that should trigger the skill
- [ ] No sensitive information or credentials in skill files
- [ ] All bundled scripts have clear usage documentation

## Concrete Example: Creating a JSON Formatter Skill

Here's a complete example of creating a simple skill:

**1. Create folder:**
```bash
mkdir -p skills/json-formatter
```

**2. Create SKILL.md:**
```yaml
---
name: json-formatter
description: 'Formats, validates, and minifies JSON data. Use when working with JSON files, formatting JSON, validating JSON syntax, or when the user mentions JSON, formatting, or prettifying data.'
---

# JSON Formatter

Formats and validates JSON data with proper indentation and error checking.

## When to Use This Skill

- User asks to format, prettify, or validate JSON
- Working with JSON configuration files
- Debugging malformed JSON

## Capabilities

- Format JSON with proper indentation
- Validate JSON syntax and report errors
- Minify JSON for production use
- Convert between JSON and other formats

## Usage Examples

**Format JSON:**
```bash
python scripts/format.py input.json --indent 2
```

**Validate JSON:**
```bash
python scripts/validate.py input.json
```
```

**3. Add script (optional):**
```python
# scripts/format.py
import json
import sys

with open(sys.argv[1], 'r') as f:
    data = json.load(f)
    print(json.dumps(data, indent=2))
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not discovered | Improve description with more keywords and triggers; test with various phrasings |
| Validation fails on name | Ensure lowercase, no consecutive hyphens, matches folder, doesn't start/end with hyphen |
| Description too short | Add capabilities, triggers, and keywords (1-1024 chars); include user-facing terms |
| Referenced files not found | Use relative paths from skill root, keep references one level deep |
| Skill triggers incorrectly | Narrow description to be more specific; remove ambiguous keywords |
| Large skill loads slowly | Reduce SKILL.md size; move detailed docs to `references/` |
| Script won't execute | Ensure executable permissions: `chmod +x scripts/*.sh` |

## Skill Lifecycle & Maintenance

### Versioning

Track skill versions in metadata:

```yaml
metadata:
  version: '1.0.0'  # MAJOR.MINOR.PATCH
  last-updated: '2026-01-21'
```

**Version Guidelines:**
- MAJOR: Breaking changes to skill behavior or required inputs
- MINOR: New capabilities or significant enhancements
- PATCH: Bug fixes, documentation updates, minor improvements

### Updating Skills

When modifying existing skills:

1. Test changes with previous working prompts to ensure backward compatibility
2. Update `last-updated` in metadata
3. Increment version appropriately
4. Document changes in skill body or changelog
5. Re-validate if making structural changes

### Deprecating Skills

To retire a skill:

1. Update description to note deprecation and suggest alternative
2. Keep skill functional but add deprecation notice in body
3. After transition period, remove skill folder

## References

- [Agent Skills Specification](https://agentskills.io/specification) - Official spec and schema
- [Agent Skills Home](https://agentskills.io/) - Documentation and guides
- [skills-ref validation library](https://github.com/agentskills/agentskills/tree/main/skills-ref) - CLI validation tool
- [Example skills](https://github.com/anthropics/skills) - Reference implementations

## See Also

- Other skills in this workspace for pattern examples
- Project-specific AGENTS.md files for integration guidance
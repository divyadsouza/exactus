# AI Agents Guide for Exactus

## Overview

This guide explains how to leverage AI coding assistants (agents) with specialized skills to accelerate development, validation, and maintenance of the Exactus project. AI agents can help with code generation, data validation, documentation, and workflow automation, making them invaluable for building a high-quality structured output model.

## Available Skills

The project leverages AI coding assistants with specialized skills stored in the `.github/skills/` directory. Skills are modular capabilities that enhance productivity and ensure consistency across the project.

### Current Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| `conventional-commit` | Creates conventional commit messages and commits changes to git following conventional commit standards | Committing code changes with proper formatting and semantic versioning |
| `agents-md-generator` | Analyzes repository structure and generates standardized AGENTS.md files that serve as contributor guides for AI agents | Producing contributor guides with LOC analysis and 5-section documentation covering overview, folder structure, patterns, conventions, and working agreements |
| `make-skill-template` | Creates new Agent Skills for AI assistants from prompts or by duplicating templates | Scaffolding new AI capabilities with bundled resources, generating SKILL.md files with proper frontmatter, directory structure, and optional scripts/assets folders |
| `training-data-validator` | Validates synthetic training data for structured output models, checking structural validity and semantic accuracy to ensure zero hallucinations | Verifying JSONL training data files, assessing data quality, and confirming AI-generated datasets contain only factual extractions without fabrications |

### Skill Integration

Skills are stored in the `.github/skills/` directory and can be invoked by AI assistants during development tasks. They help maintain code quality, validate training data, and automate common workflows specific to AI model development and structured output generation.

## Using AI Agents for Project Development

### Code Generation and Implementation
- **Task Planning**: Ask agents to break down complex tasks (e.g., implementing distillation pipelines) into actionable steps
- **Code Scaffolding**: Use agents to generate boilerplate code for training scripts, evaluation metrics, or deployment configurations
- **Bug Fixing**: Provide error messages and ask agents to diagnose and fix issues in training or inference code
- **Documentation**: Request agents to generate or update documentation, including API docs, code comments, and user guides

### Training Data Validation
- **Automated Validation**: Use the `training-data-validator` skill to check JSONL files for structural validity and semantic accuracy
- **Batch Processing**: Ask agents to validate entire datasets and generate reports on hallucination risks
- **Edge Case Detection**: Request agents to identify potential issues in training data, such as missing source attribution or format inconsistencies

### Workflow Automation
- **Commit Management**: Use `conventional-commit` skill for standardized git commits with proper semantic versioning
- **Documentation Generation**: Leverage `agents-md-generator` to create contributor guides and project documentation
- **Skill Creation**: Use `make-skill-template` to build new specialized skills for project-specific tasks

## Creating New Skills for Synthetic Dataset Generation

As the project grows, we can develop additional skills to automate synthetic data creation and augmentation. Here are proposed skills to consider:

### Proposed Skills

| Proposed Skill | Description | Purpose |
|----------------|-------------|---------|
| `synthetic-data-generator` | Generates synthetic training data for structured extraction tasks using teacher models | Create diverse, zero-hallucination training examples programmatically |
| `data-augmenter` | Augments existing training data with format variations and edge cases | Increase dataset diversity by converting JSON to XML/YAML or adding null scenarios |
| `hallucination-detector` | Analyzes model outputs for potential hallucinations and fabrication | Automated testing of trained models against hallucination benchmarks |
| `format-converter` | Converts training data between JSON, XML, CSV, and YAML formats | Ensure multi-format consistency in datasets |

### How to Create New Skills
1. Use the `make-skill-template` skill to scaffold a new skill directory and SKILL.md file
2. Define the skill's purpose, inputs, outputs, and usage examples
3. Implement the skill logic (scripts, prompts, or automation)
4. Test the skill with sample inputs
5. Document the skill in this guide and integrate it into project workflows

## Best Practices for AI Agent Usage

### Prompting Guidelines
- **Be Specific**: Provide clear, detailed descriptions of tasks with context from the project goals
- **Reference Documentation**: Point agents to relevant files (e.g., README.md, learning outcomes) for accurate implementation
- **Iterate**: Start with high-level requests, then refine based on agent outputs
- **Validate Outputs**: Always review and test agent-generated code or data before committing

### Integration with Development Workflow
- **Phase Alignment**: Use agents differently per project phase (e.g., data validation in Phase 1, code generation in Phase 2)
- **Collaboration**: Share agent outputs with team members for review and feedback
- **Version Control**: Commit agent-generated changes with conventional commits using the `conventional-commit` skill

### Quality Assurance
- **Manual Review**: Never commit agent-generated code without human verification
- **Testing**: Run automated tests on agent outputs, especially for training data and models
- **Documentation**: Update project docs when agents generate new code or skills

## Getting Started with AI Agents

1. **Explore Existing Skills**: Review the `.github/skills/` directory and try invoking skills on sample tasks
2. **Identify Automation Opportunities**: Look for repetitive tasks in the roadmap that could benefit from new skills
3. **Experiment**: Start with simple tasks like validating a training data file using `training-data-validator`
4. **Contribute**: If you create useful skills, share them with the project team and document in this guide

## Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot) - Official guide for AI coding assistants
- [Skill Template](.github/skills/make-skill-template/) - How to create new skills
- [Training Data Validator](.github/skills/training-data-validator/) - Example of a working skill
- [Learning Outcomes](learning_outcomes.md) - Project concepts for better agent prompting

---

> **Tip**: AI agents are powerful tools, but they're most effective when used with clear project context and human oversight. Always prioritize accuracy and validation in Exactus development.</content>
<parameter name="filePath">/Users/mlim/Projects/mlim-usfca/exactus/docs/ai_agents_guide.md
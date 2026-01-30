---
name: conventional-commit
description: 'Creates conventional commit messages and commits changes to git. Use when committing code changes, following conventional commit standards, or preparing commits with proper formatting.'
---

# Conventional Commit

This skill helps create and execute git commits following the conventional commit specification, ensuring consistent and meaningful commit messages.

## When to Use This Skill

- User asks to commit changes
- When preparing a commit with proper conventional format
- For projects requiring standardized commit messages
- When the user mentions "commit", "conventional commits", or "git commit"

## Prerequisites

- Git repository initialized
- Changes staged or ready to commit
- Understanding of conventional commit types (feat, fix, docs, etc.)

## Step-by-Step Workflow

1. **Check git status** to see what files have changed
2. **Analyze changes deeply** to determine appropriate commit type and scope
3. **Generate conventional commit message** based on analysis
4. **Stage changes** if not already staged
5. **Commit with the generated message**

### Deep Change Analysis

Before creating a commit, perform thorough analysis of the code changes to determine the correct type:

#### 1. Get the Diff
```bash
git diff --staged
```
If nothing staged, check unstaged changes:
```bash
git diff
```

#### 2. Analyze Change Patterns

**feat (New Feature):**
- New functions, classes, components, or modules added
- New API endpoints or routes
- New UI components or pages
- New configuration options or features
- Patterns: `+function`, `+class`, `+const ComponentName`, `+export`, new files with substantial code
- Keywords in diff: "add", "create", "implement", "introduce"

**fix (Bug Fix):**
- Corrections to existing functionality
- Fixing errors, exceptions, or incorrect behavior
- Resolving edge cases or validation issues
- Patterns: modifications to existing logic, conditional changes, error handling additions
- Keywords: "fix", "resolve", "correct", "repair", "patch"
- Changes to `if` conditions, error handlers, validation logic

**docs (Documentation):**
- README, comments, docstrings, or markdown files
- JSDoc, TypeScript type annotations (when primarily for documentation)
- Patterns: `.md` files, comment blocks, docstrings
- Changes ONLY to comments without logic changes
- Examples, guides, or API documentation

**style (Formatting):**
- Whitespace, indentation, formatting changes
- No functional changes to code
- Linting fixes that don't alter behavior
- Patterns: spacing changes, semicolons, quotes, line breaks
- NO logic changes, ONLY cosmetic

**refactor (Code Restructuring):**
- Restructuring code without changing behavior
- Renaming variables/functions for clarity
- Extracting functions or components
- Reorganizing file structure
- Patterns: moving code, renaming, extracting utilities
- Same inputs produce same outputs, but code is cleaner

**perf (Performance):**
- Optimizations for speed or memory
- Algorithm improvements
- Caching implementations
- Lazy loading, code splitting
- Patterns: algorithmic changes, memoization, debouncing
- Keywords: "optimize", "improve performance", "cache"

**test (Tests):**
- Adding, updating, or fixing tests
- Test configuration changes
- Patterns: `.test.js`, `.spec.js`, `describe(`, `it(`, `expect(`
- Changes primarily in test files

**chore (Maintenance):**
- Dependency updates
- Build configuration changes
- CI/CD modifications
- Package.json changes (not feature-related)
- Tooling and development setup
- Patterns: `package.json`, `vite.config.js`, `.github/workflows/`

**build (Build System):**
- Build tool configuration
- Webpack, Vite, Rollup configurations
- Compilation settings
- Patterns: build config files, bundler settings

**ci (Continuous Integration):**
- GitHub Actions, Travis, CircleCI changes
- Automated testing setup
- Deployment pipeline modifications
- Patterns: `.github/workflows/`, `.travis.yml`, `Jenkinsfile`

#### 3. Detect Breaking Changes

Breaking changes are NOT a separate type - they modify any type. Analyze the diff for:

**API Breaking Changes:**
- Function signature changes (parameters added/removed/reordered)
- Return type or structure changes
- Removed or renamed public methods/functions
- Changed prop names or types in components
- Modified endpoint URLs or request/response formats
- Patterns: `-function name(old)`, `+function name(new, params)`

**Behavioral Breaking Changes:**
- Changed default values that affect existing code
- Modified validation rules (stricter)
- Changed error handling behavior
- Removed backwards compatibility code
- Patterns: `-const DEFAULT =`, `+const DEFAULT =` (different value)

**Dependency Breaking Changes:**
- Major version updates with breaking changes
- Removed peer dependencies
- Changed minimum version requirements

**Indicators to Mark as Breaking:**
```diff
- export function login(username, password) {
+ export function login(credentials) {
```
→ `feat!: change login function signature` OR add `BREAKING CHANGE:` footer

**When in doubt:** If existing code using this API would break, it's a breaking change.

#### 4. Prioritization Rules

When changes span multiple types, use this priority:

1. **Breaking changes** → use `!` suffix or BREAKING CHANGE footer on primary type
2. **feat** > fix > perf (user-facing changes take priority)
3. **refactor** when no behavior change but significant restructuring
4. **docs** when documentation is the primary change
5. **test** when test files are primary
6. **chore/build/ci** for tooling/infrastructure

#### 4. Determine Scope

- **Component-based:** `(navbar)`, `(hero)`, `(coursecard)`
- **Feature-based:** `(auth)`, `(api)`, `(routing)`
- **File-based:** `(schedule)`, `(courses)`, `(utils)`
- **Tech-based:** `(tailwind)`, `(react)`, `(vite)`
- Omit scope if change is global or unclear

#### 5. Craft Description

- Use imperative mood: "add", "fix", "update" (not "added", "fixes", "updating")
- Be specific but concise
- Describe WHAT changed, not HOW
- Start with lowercase (after colon)
- No period at the end
- Max 50 characters for summary line

### Conventional Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or fixing tests
- `chore`: Maintenance tasks

**Scopes:** Component or file affected (optional)

## Analysis Examples

### Example 1: New Component
**Diff shows:**
```diff
+ export const ProfileCard = () => {
+   return <div>...</div>
+ }
```
**Analysis:** New component file, new export → **feat(components): add profile card component**

### Example 2: Bug Fix
**Diff shows:**
```diff
- if (date > today) {
+ if (date >= today) {
```
**Analysis:** Logic correction in conditional → **fix(schedule): correct date comparison logic**

### Example 3: Mixed Changes (feat + docs)
**Files changed:**
- `src/components/Header.jsx` - new navigation items added
- `README.md` - updated installation steps

**Analysis:** Primary change is feature, docs are secondary → **feat(header): add mobile navigation menu**
Then optionally follow up with: **docs: update installation instructions**

### Example 4: Refactor
**Diff shows:**
```diff
- function calculateTotal(items) {
-   let sum = 0;
-   for (let i = 0; i < items.length; i++) {
-     sum += items[i].price;
-   }
-   return sum;
- }
+ const calculateTotal = (items) => 
+   items.reduce((sum, item) => sum + item.price, 0);
```
**Analysis:** Same behavior, cleaner implementation → **refactor(utils): simplify calculateTotal using reduce**

### Example 5: Dependency Update
**Diff shows:**
```diff
  "dependencies": {
-   "react": "^18.2.0",
+   "react": "^18.3.1",
  }
```
**Analysis:** Package update, no code changes → **chore(deps): update react to 18.3.1**

### Example 6: Breaking Change
**Diff shows:**
```diff
- export const fetchCourses = (semester) => {
+ export const fetchCourses = (filters) => {
+   const { semester, year, department } = filters;
```
**Analysis:** Function signature changed, existing calls will break → **feat(api)!: change fetchCourses to accept filters object**

With body:
```
feat(api)!: change fetchCourses to accept filters object

BREAKING CHANGE: fetchCourses now accepts a filters object instead of 
a semester string. Update calls from fetchCourses('Fall') to 
fetchCourses({ semester: 'Fall' })
```

## Usage Examples

**Simple commit:**
```
feat: add user authentication
```

**With scope:**
```
fix(ui): resolve button alignment issue
```

**Breaking change:**
```
feat(api)!: change user endpoint structure
```

**Multi-line with body:**
```
refactor(courses): restructure data format

Reorganize course data to use normalized structure
with separate instructor and schedule objects
```

## Troubleshooting

- If no changes to commit: Check git status
- If message format invalid: Ensure type is correct and description is imperative
- For breaking changes: Add ! after type or BREAKING CHANGE: in footer
- **If uncertain about type:** Re-analyze the diff focusing on the primary impact to users/codebase
- **Multiple logical changes:** Consider splitting into separate commits
- **Large refactor:** May need both refactor and feat commits if new capabilities added

## Decision Tree

```
Is this a new file with new functionality? → feat
├─ Is it a test file? → test
├─ Is it documentation? → docs
└─ Is it configuration? → chore

Is this modifying existing code?
├─ Does it fix broken behavior? → fix
├─ Does it improve performance without changing behavior? → perf
├─ Does it restructure without changing behavior? → refactor
├─ Does it only change formatting/style? → style
└─ Does it add new capabilities? → feat

Is this changing project files?
├─ package.json dependencies? → chore(deps)
├─ Build configuration? → build
├─ CI/CD pipelines? → ci
└─ Documentation files? → docs
```

## References

- [Conventional Commits Specification](https://conventionalcommits.org/)
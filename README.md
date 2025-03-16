# Groove Sync Action

This GitHub Action allows you to sync groove definitions from YAML files with your Groove API endpoint. It supports both creating new grooves and updating existing ones, using the `toolName` as a unique identifier.

## Features

- Create and update grooves from YAML definitions
- Automatic fallback from update to create if groove doesn't exist
- Customizable file paths and patterns
- Detailed error reporting and logging
- GitHub-style workflow annotations for errors and notices

## Usage

```yaml
name: Sync Grooves

on:
  push:
    paths:
      - '.grooves/**/*.yml'
      - '.grooves/**/*.yaml'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Sync grooves
        uses: geoffwhittington/groove-sync-action@v1
        with:
          api-url: ${{ secrets.GROOVE_API_URL }}
          user-context-id: ${{ secrets.USER_CONTEXT_ID }}
          # Optional: customize groove files location
          grooves-path: 'grooves'
          file-pattern: '**/*.{yml,yaml}'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `api-url` | Base URL of your Groove API | No | `https://grooving.xyz` |
| `user-context-id` | User context ID with permission to create/update grooves | Yes | - |
| `grooves-path` | Path to directory containing groove YAML files | No | `.grooves` |
| `file-pattern` | Glob pattern for groove files | No | `**/*.{yml,yaml}` |

## Groove YAML Format

```yaml
name: My Groove
description: A description of what this groove does
toolName: unique_tool_name  # Used as unique identifier

inputSchema:
  type: object
  required:
    - parameter1
  properties:
    parameter1:
      type: string
      description: Description of the parameter

beats:
  - name: First Step
    template: "Template for {parameter1}"
  - name: Second Step
    template: "Another template"
```

## Example Workflow

1. Create a `.github/workflows/groove-sync.yml` file:

```yaml
name: Sync Grooves

on:
  push:
    paths:
      - '.grooves/**/*.yml'
      - '.grooves/**/*.yaml'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Sync grooves
        uses: your-username/groove-sync-action@v1
        with:
          user-context-id: ${{ secrets.USER_CONTEXT_ID }}
```

2. Add repository secrets:
   - `GROOVE_API_URL`: Your Groove API endpoint
   - `USER_CONTEXT_ID`: Your user context ID

3. Create groove definitions in the `grooves/` directory:

```yaml
# grooves/my-groove.yml
name: My Groove
description: Example groove
toolName: my_groove

inputSchema:
  type: object
  required:
    - text
  properties:
    text:
      type: string
      description: Input text

beats:
  - name: Process
    template: "Processing: {text}"
```

## Error Handling

The action will:
- Fail if any groove sync operation fails
- Provide detailed error messages in the workflow logs
- Add GitHub annotations for errors and notices
- Continue processing remaining files even if one fails

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details 

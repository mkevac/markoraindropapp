# Raindrop.io Bookmark CLI

A Python CLI application to interact with your Raindrop.io bookmarks.

## Setup

1. Install uv if you don't have it already:
   ```
   pip install uv
   ```

2. Set up the project environment:
   ```
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. Get your Raindrop.io API token:
   - Go to https://app.raindrop.io/settings/integrations
   - Create a new app
   - Copy your "Test token"

## Usage

The CLI has two main commands:
- `collections`: List all available collections
- `bookmarks`: Get bookmarks (default command if none specified)

You can provide your token in two ways:

### Method 1: Pass the token as a command-line argument

```
python -m markoraindrop.cli --token YOUR_TOKEN [command] [options]
```

### Method 2: Set an environment variable

```
export RAINDROP_TOKEN=YOUR_TOKEN
python -m markoraindrop.cli [command] [options]
```

## Examples

### List all collections

```
python -m markoraindrop.cli collections
```

### Fetch latest bookmarks (default: 10 most recent across all collections)

```
python -m markoraindrop.cli bookmarks
# or simply
python -m markoraindrop.cli
```

### Fetch bookmarks from a specific collection by name

```
python -m markoraindrop.cli bookmarks --collection "Development"
```

### Fetch 20 bookmarks from a collection, sorted alphabetically

```
python -m markoraindrop.cli bookmarks --collection "Articles" --limit 20 --sort "title"
```

### Available options for the bookmarks command

- `--collection`: Collection name to fetch bookmarks from
- `--limit`: Number of bookmarks to fetch (default: 10)
- `--sort`: Sort order (default: "-created")
  - "-created": Newest first
  - "created": Oldest first
  - "title": Alphabetical by title
  - "-title": Reverse alphabetical by title
  - "domain": By website domain
  - "-domain": Reverse by website domain
- `--page`: Page number for pagination (default: 0)

## Note

This application uses the Raindrop.io API to access your bookmarks. The API token is required for authentication. Keep your token secure and do not share it with others. 
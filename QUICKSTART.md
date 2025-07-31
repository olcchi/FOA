# Quick Start Guide

[English](#english) | [中文](./QUICKSTART_CN.md)

---

## English

## 🚀 Getting Started with Smart File Organizer Agent

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

1. Open `config.yaml` and add your DeepSeek API key:
   ```yaml
   ai_providers:
     deepseek:
       api_key: "your_actual_deepseek_api_key_here"
   ```

2. (Optional) Configure other AI providers if needed

### 3. Basic Usage

#### Preview Mode (Safe - No Changes Made)
```bash
# Preview what the agent would do
python file_organizer.py organize --dir ./test_files --preview
```

#### Organize Files
```bash
# Actually organize files
python file_organizer.py organize --dir ./test_files
```

#### Analyze Single File
```bash
# Analyze a specific file
python file_organizer.py analyze ./test_files/sample_document.txt
```

### 4. Available Commands

- `organize` - Organize files in a directory
- `analyze` - Analyze a single file
- `undo` - Undo the last organization operation
- `stats` - Show statistics from last operation

### 5. Command Options

- `--preview` - Preview mode (no actual changes)
- `--provider deepseek` - Use specific AI provider
- `--recursive` - Process subdirectories (default: true)
- `--interactive` - Confirm each operation

### 6. Example Workflow

```bash
# 1. First, preview what would happen
python file_organizer.py organize --dir ./downloads --preview

# 2. If satisfied, run the actual organization
python file_organizer.py organize --dir ./downloads

# 3. Check the results
python file_organizer.py stats --dir ./downloads

# 4. If needed, undo the operation
python file_organizer.py undo --dir ./downloads
```

### 7. Output Structure

After organization, your files will be organized like this:
```
your_directory/
├── organized/
│   ├── documents/
│   ├── images/
│   ├── videos/
│   ├── audio/
│   ├── code/
│   └── others/
├── backup/
│   └── 20241201_143022/  # Timestamp folder
└── file_organization_log.json
```

### 8. Tips

- Always use `--preview` first to see what changes would be made
- The agent creates backups by default, so your original files are safe
- Use `undo` command if you're not satisfied with the results
- Check the log file for detailed operation history

### 9. Troubleshooting

**API Key Issues:**
- Make sure your DeepSeek API key is correctly set in `config.yaml`
- Verify the API key has sufficient credits

**File Access Issues:**
- Ensure you have read/write permissions for the target directory
- Close any files that might be open in other applications

**Large Files:**
- The agent skips files larger than 50MB by default
- Adjust `max_file_size` in config.yaml if needed

### 10. Demo with Test Files

Try the agent with the included test files:

```bash
# Preview organization of test files
python file_organizer.py organize --dir ./test_files --preview

# Organize the test files
python file_organizer.py organize --dir ./test_files
```

This will demonstrate how the agent categorizes and renames different file types!
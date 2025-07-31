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

### 3. 🌟 Recommended: Interactive Mode (Easiest Way)

```bash
# Simply run the script - no arguments needed!
python file_organizer.py
```

**Why use Interactive Mode?**
- 🎯 **Beginner-friendly**: No need to memorize commands
- 🌍 **Multi-language**: Choose English or Chinese interface
- 📋 **Guided workflow**: Step-by-step menu navigation
- ⚡ **All features**: Access organize, analyze, undo, stats through menus
- 🛡️ **Safe**: Built-in preview and confirmation prompts

**Interactive Mode Features:**
1. **Language Selection**: Choose your preferred interface language
2. **Command Menu**: Select from organize, undo, stats, analyze, or exit
3. **Smart Configuration**: Interactive parameter selection for each command
4. **Real-time Guidance**: Helpful prompts and explanations

### 4. Traditional Command Line Usage (Advanced)

If you prefer command-line interface:

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

#### Chinese Interface
```bash
# Use Chinese interface
python file_organizer.py --language zh organize --dir ./test_files
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

### 6. Example Workflows

#### 🌟 Interactive Mode Workflow (Recommended)
```bash
# 1. Start interactive mode
python file_organizer.py

# 2. Follow the menu prompts:
#    - Select language (English/Chinese)
#    - Choose "Organize files"
#    - Enter target directory: ./downloads
#    - Select preview mode: Yes
#    - Review the preview results
#    - Confirm to proceed or cancel

# 3. Use menu to check stats or undo if needed
```

#### Traditional Command Line Workflow
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

#### 🌟 Interactive Mode Demo (Recommended)
```bash
# Start interactive mode and follow the prompts
python file_organizer.py

# In the interactive menu:
# 1. Select your language
# 2. Choose "Organize files"
# 3. Enter directory: ./test_files
# 4. Enable preview mode to see what would happen
# 5. Proceed with organization if satisfied
```

#### Command Line Demo
```bash
# Preview organization of test files
python file_organizer.py organize --dir ./test_files --preview

# Organize the test files
python file_organizer.py organize --dir ./test_files
```

This will demonstrate how the agent categorizes and renames different file types!

### 🎯 Quick Start Summary

**For beginners**: Just run `python file_organizer.py` and follow the interactive menu!

**For advanced users**: Use command-line arguments for automation and scripting.
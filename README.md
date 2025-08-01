# File Organizer Agent

[English](#english) | [中文](#chinese)

---

## English

An intelligent file organizing agent that automatically categorizes and renames files using AI.

### Features

- **🌟 Interactive Mode**: User-friendly menu interface with multi-language support
- **Smart File Classification**: Automatically categorize files by content and type
- **Intelligent Renaming**: Generate meaningful file names based on content analysis
- **Multiple AI Providers**: Support for DeepSeek, OpenAI, and other providers via API router
- **Batch Processing**: Process multiple files or entire directories
- **Safe Operations**: Preview mode and backup options
- **Dual Interface**: Both interactive menu and traditional CLI modes
- **Multi-language**: English and Chinese interface support

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Copy `config.example.yaml` to `config.yaml`
2. Add your API keys and configure settings

### Usage

#### 🌟 Recommended: Interactive Mode (Easiest)

```bash
# Simply run the script to enter interactive mode
python file_organizer.py
```

The interactive mode provides:
- User-friendly menu interface
- Step-by-step guidance
- Multi-language support (English/Chinese)
- All features accessible through simple selections
- No need to remember command-line arguments

#### Traditional Command Line Mode

```bash
# Organize files in current directory
python file_organizer.py organize --dir .

# Preview mode (no actual changes)
python file_organizer.py organize --dir ./downloads --preview

# Use specific AI provider
python file_organizer.py organize --dir ./documents --provider deepseek

# Chinese interface
python file_organizer.py --language zh organize --dir ./documents
```

### Project Structure

- `file_organizer.py` - Main CLI application
- `src/` - Core modules
  - `ai_client.py` - AI provider interface
  - `file_analyzer.py` - File content analysis
  - `organizer.py` - File organization logic
- `config/` - Configuration files
- `tests/` - Unit tests

---

## Chinese

智能文件整理代理，使用AI自动分类和重命名文件。

### 功能特性

- **交互式模式**: 友好的菜单界面，支持多语言
- **智能文件分类**: 根据内容和类型自动分类文件
- **智能重命名**: 基于内容分析生成有意义的文件名
- **多AI提供商**: 支持DeepSeek、OpenAI等多种AI提供商
- **批量处理**: 处理多个文件或整个目录
- **安全操作**: 预览模式和备份选项
- **双重界面**: 交互式菜单和传统命令行模式
- **多语言支持**: 中文和英文界面

### 安装

```bash
pip install -r requirements.txt
```

### 配置

1. 复制 `config.example.yaml` 为 `config.yaml`
2. 添加您的API密钥并配置设置

### 使用方法

#### 基础模式

```bash
# 直接运行脚本进入交互模式
python file_organizer.py
```

交互式模式提供：
- 友好的菜单界面
- 逐步指导
- 多语言支持（中文/英文）
- 通过选择访问所有功能
- 无需记忆命令行参数

#### 传统命令行模式

```bash
# 整理当前目录中的文件
python file_organizer.py organize --dir .

# 预览模式（不进行实际更改）
python file_organizer.py organize --dir ./downloads --preview

# 使用特定的AI提供商
python file_organizer.py organize --dir ./documents --provider deepseek

# 中文界面
python file_organizer.py --language zh organize --dir ./documents
```

### 项目结构

- `file_organizer.py` - 主CLI应用程序
- `src/` - 核心模块
  - `ai_client.py` - AI提供商接口
  - `file_analyzer.py` - 文件内容分析
  - `organizer.py` - 文件组织逻辑
- `config/` - 配置文件
- `tests/` - 单元测试
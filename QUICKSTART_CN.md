# 快速入门指南

[English](./QUICKSTART.md) | [中文](#chinese)

---

## Chinese

## 🚀 Smart File Organizer Agent 快速上手

### 1. 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

1. 打开 `config.yaml` 并添加您的 DeepSeek API 密钥：
   ```yaml
   ai_providers:
     deepseek:
       api_key: "your_actual_deepseek_api_key_here"
   ```

2. （可选）如需要可配置其他AI提供商

### 3. 基本使用

#### 预览模式（安全 - 不会进行实际更改）
```bash
# 预览代理将要执行的操作
python file_organizer.py organize --dir ./test_files --preview
```

#### 整理文件
```bash
# 实际整理文件
python file_organizer.py organize --dir ./test_files
```

#### 分析单个文件
```bash
# 分析特定文件
python file_organizer.py analyze ./test_files/sample_document.txt
```

### 4. 可用命令

- `organize` - 整理目录中的文件
- `analyze` - 分析单个文件
- `undo` - 撤销上次整理操作
- `stats` - 显示上次操作的统计信息

### 5. 命令选项

- `--preview` - 预览模式（不进行实际更改）
- `--provider deepseek` - 使用特定的AI提供商
- `--recursive` - 处理子目录（默认：true）
- `--interactive` - 确认每个操作

### 6. 示例工作流程

```bash
# 1. 首先预览将要发生的操作
python file_organizer.py organize --dir ./downloads --preview

# 2. 如果满意，执行实际的整理操作
python file_organizer.py organize --dir ./downloads

# 3. 检查结果
python file_organizer.py stats --dir ./downloads

# 4. 如需要，撤销操作
python file_organizer.py undo --dir ./downloads
```

### 7. 输出结构

整理后，您的文件将按以下结构组织：
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
│   └── 20241201_143022/  # 时间戳文件夹
└── file_organization_log.json
```

### 8. 使用技巧

- 始终先使用 `--preview` 查看将要进行的更改
- 代理默认创建备份，因此您的原始文件是安全的
- 如果对结果不满意，可使用 `undo` 命令
- 查看日志文件了解详细的操作历史

### 9. 故障排除

**API密钥问题：**
- 确保在 `config.yaml` 中正确设置了 DeepSeek API 密钥
- 验证API密钥有足够的额度

**文件访问问题：**
- 确保您对目标目录有读/写权限
- 关闭可能在其他应用程序中打开的文件

**大文件：**
- 代理默认跳过大于50MB的文件
- 如需要可在 config.yaml 中调整 `max_file_size`

### 10. 测试文件演示

使用包含的测试文件试用代理：

```bash
# 预览测试文件的整理
python file_organizer.py organize --dir ./test_files --preview

# 整理测试文件
python file_organizer.py organize --dir ./test_files
```

这将演示代理如何分类和重命名不同类型的文件！
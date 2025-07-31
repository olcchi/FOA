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

### 3. 基础交互

```bash
# 直接运行脚本 - 无需任何参数！
python file_organizer.py
```

**为什么使用交互式模式？**
- 🎯 **新手友好**：无需记忆命令
- 🌍 **多语言支持**：选择中文或英文界面
- 📋 **引导式工作流**：逐步菜单导航
- ⚡ **功能齐全**：通过菜单访问整理、分析、撤销、统计等所有功能
- 🛡️ **安全可靠**：内置预览和确认提示

**交互式模式特性：**
1. **语言选择**：选择您偏好的界面语言
2. **命令菜单**：从整理、撤销、统计、分析或退出中选择
3. **智能配置**：为每个命令交互式选择参数
4. **实时指导**：有用的提示和说明

### 4. 传统命令行使用（高级用户）

如果您偏好命令行界面：

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

#### 中文界面
```bash
# 使用中文界面
python file_organizer.py --language zh organize --dir ./test_files
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

#### 🌟 交互式模式工作流程（推荐）
```bash
# 1. 启动交互式模式
python file_organizer.py

# 2. 按照菜单提示操作：
#    - 选择语言（中文/英文）
#    - 选择"整理文件"
#    - 输入目标目录：./downloads
#    - 选择预览模式：是
#    - 查看预览结果
#    - 确认继续或取消

# 3. 使用菜单检查统计信息或在需要时撤销
```

#### 传统命令行工作流程
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

#### 🌟 交互式模式演示（推荐）
```bash
# 启动交互式模式并按照提示操作
python file_organizer.py

# 在交互式菜单中：
# 1. 选择您的语言
# 2. 选择"整理文件"
# 3. 输入目录：./test_files
# 4. 启用预览模式查看将要发生的操作
# 5. 如果满意则继续整理
```

#### 命令行演示
```bash
# 预览测试文件的整理
python file_organizer.py organize --dir ./test_files --preview

# 整理测试文件
python file_organizer.py organize --dir ./test_files
```

这将演示代理如何分类和重命名不同类型的文件！

### 🎯 快速开始总结

**新手用户**：直接运行 `python file_organizer.py` 并按照交互式菜单操作！

**高级用户**：使用命令行参数进行自动化和脚本编程。
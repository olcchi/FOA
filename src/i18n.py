#!/usr/bin/env python3
"""Internationalization module for Smart File Organizer Agent."""

import json
import os
from typing import Dict, Any


class I18n:
    """Internationalization handler for multi-language support."""
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation dictionaries."""
        return {
            'en': {
                # CLI Messages
                'app_title': 'Smart File Organizer Agent',
                'app_description': 'Intelligently organize and rename files using AI.',
                'directory': 'Directory',
                'ai_provider': 'AI Provider',
                'mode': 'Mode',
                'preview_mode': 'Preview',
                'execute_mode': 'Execute',
                'found_files': 'Found {count} files to analyze...',
                'no_files_found': 'No files found to process.',
                'analyzing_files': 'Analyzing files',
                'organizing_files': 'Organizing files...',
                'operation_cancelled': 'Operation cancelled.',
                'organization_complete': 'Organization complete!',
                'files_organized_in': 'Files organized in: {path}',
                'backups_saved_in': 'Backups saved in: {path}',
                'proceed_confirm': 'Proceed with organizing {count} files?',
                
                # Analysis Results
                'analysis_results_title': '=== File Analysis Results ===',
                'category': 'Category',
                'suggested': 'Suggested',
                'confidence': 'Confidence',
                'reason': 'Reason',
                
                # Operation Summary
                'operation_summary_title': '=== Operation Summary ===',
                'total_files_processed': 'Total files processed',
                'successful_operations': 'Successful operations',
                'failed_operations': 'Failed operations',
                'errors': 'Errors',
                'average_confidence': 'Average confidence',
                'category_distribution': 'Category Distribution',
                
                # Commands
                'organize_help': 'Organize files in the specified directory.',
                'undo_help': 'Undo the last organization operation.',
                'stats_help': 'Show statistics from the last organization operation.',
                'analyze_help': 'Analyze a single file and show naming suggestions.',
                
                # Options
                'dir_help': 'Directory to organize (default: current directory)',
                'provider_help': 'AI provider to use (deepseek, openai, router)',
                'config_help': 'Configuration file path',
                'preview_help': 'Preview mode - show what would be done without making changes',
                'recursive_help': 'Process files recursively',
                'interactive_help': 'Interactive mode - confirm each operation',
                'language_help': 'Interface language (en/zh)',
                
                # Errors
                'config_not_found': "Error: Configuration file '{path}' not found.",
                'config_copy_instruction': "Please copy 'config.example.yaml' to 'config.yaml' and configure your API keys.",
                'config_parse_error': 'Error parsing configuration file: {error}',
                'directory_not_exist': "Error: Directory '{path}' does not exist.",
                'file_not_exist': "Error: File '{path}' does not exist.",
                'errors_encountered': 'Errors encountered:',
                'undo_operation': 'Undoing last organization operation...',
                'no_stats_found': 'No organization statistics found for this directory.',
                'some_files_not_restored': 'Some files could not be restored:',
            },
            
            'zh': {
                # CLI Messages
                'app_title': '智能文件整理助手',
                'app_description': '使用AI智能整理和重命名文件。',
                'directory': '目录',
                'ai_provider': 'AI提供商',
                'mode': '模式',
                'preview_mode': '预览',
                'execute_mode': '执行',
                'found_files': '找到 {count} 个文件待分析...',
                'no_files_found': '未找到需要处理的文件。',
                'analyzing_files': '分析文件中',
                'organizing_files': '整理文件中...',
                'operation_cancelled': '操作已取消。',
                'organization_complete': '整理完成！',
                'files_organized_in': '文件已整理到: {path}',
                'backups_saved_in': '备份已保存到: {path}',
                'proceed_confirm': '确认整理 {count} 个文件？',
                
                # Analysis Results
                'analysis_results_title': '=== 文件分析结果 ===',
                'category': '分类',
                'suggested': '建议名称',
                'confidence': '置信度',
                'reason': '原因',
                
                # Operation Summary
                'operation_summary_title': '=== 操作摘要 ===',
                'total_files_processed': '处理文件总数',
                'successful_operations': '成功操作',
                'failed_operations': '失败操作',
                'errors': '错误',
                'average_confidence': '平均置信度',
                'category_distribution': '分类分布',
                
                # Commands
                'organize_help': '整理指定目录中的文件。',
                'undo_help': '撤销上次整理操作。',
                'stats_help': '显示上次整理操作的统计信息。',
                'analyze_help': '分析单个文件并显示命名建议。',
                
                # Options
                'dir_help': '要整理的目录（默认：当前目录）',
                'provider_help': '使用的AI提供商（deepseek, openai, router）',
                'config_help': '配置文件路径',
                'preview_help': '预览模式 - 显示将要执行的操作但不实际修改',
                'recursive_help': '递归处理文件',
                'interactive_help': '交互模式 - 确认每个操作',
                'language_help': '界面语言（en/zh）',
                
                # Errors
                'config_not_found': "错误：配置文件 '{path}' 未找到。",
                'config_copy_instruction': "请将 'config.example.yaml' 复制为 'config.yaml' 并配置您的API密钥。",
                'config_parse_error': '配置文件解析错误：{error}',
                'directory_not_exist': "错误：目录 '{path}' 不存在。",
                'file_not_exist': "错误：文件 '{path}' 不存在。",
                'errors_encountered': '遇到错误：',
                'undo_operation': '正在撤销上次整理操作...',
                'no_stats_found': '未找到此目录的整理统计信息。',
                'some_files_not_restored': '部分文件无法恢复：',
            }
        }
    
    def t(self, key: str, **kwargs) -> str:
        """Translate a key to the current language."""
        translation = self.translations.get(self.language, {}).get(key, key)
        if kwargs:
            return translation.format(**kwargs)
        return translation
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in self.translations:
            self.language = language
        else:
            raise ValueError(f"Unsupported language: {language}")
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.translations.keys())


# Global instance
_i18n = I18n()


def get_i18n() -> I18n:
    """Get the global i18n instance."""
    return _i18n


def t(key: str, **kwargs) -> str:
    """Shorthand for translation."""
    return _i18n.t(key, **kwargs)
# -*- coding: utf-8 -*-
"""
Internationalization (i18n) module for Smart File Organizer Agent.
Provides multi-language support for CLI messages and user interface.
"""

import os
import yaml
from typing import Dict, Any

class I18n:
    """Internationalization handler for the application."""
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.translations = {
            'en': {
                # CLI messages
                'app_title': 'Smart File Organizer Agent',
                'analyzing_directory': 'Analyzing directory: {dir}',
                'using_provider': 'Using AI provider: {provider}',
                'mode': 'Mode: {mode}',
                'found_files': 'Found {count} files to process',
                'analyzing_file': 'Analyzing: {}',
                'confirm_proceed': 'Do you want to proceed with organizing these files? [y/N]',
                'operation_cancelled': 'Operation cancelled.',
                'organizing_files': 'Organizing files...',
                'operation_completed': 'Operation completed successfully!',
                'error_occurred': 'Error occurred: {}',
                'undo_operation': 'Undoing last organization operation...',
                'some_files_not_restored': 'Some files could not be restored:',
                'no_stats_found': 'No organization statistics found for this directory.',
                'file_not_exist': "Error: File '{path}' does not exist.",
                
                # Analysis results
                'analysis_results': 'Analysis Results',
                'file': 'File',
                'category': 'Category',
                'confidence': 'Confidence',
                'suggested_name': 'Suggested Name',
                'suggested': 'Suggested',
                'reason': 'Reason',
                'reasoning': 'Reasoning',
                'content_analysis_not_supported': 'Content analysis not supported for this file type',
                
                # Operation summary
                'operation_summary': 'Operation Summary',
                'files_processed': 'Files processed',
                'successful_operations': 'Successful operations',
                'failed_operations': 'Failed operations',
                'average_confidence': 'Average confidence',
                'category_distribution': 'Category distribution',
                
                # Commands and options
                'organize_help': 'Organize files in a directory using AI analysis',
                'undo_help': 'Undo the last organization operation',
                'stats_help': 'Show statistics from the last organization operation',
                'analyze_help': 'Analyze a single file and show naming suggestions',
                'dir_help': 'Directory to organize',
                'provider_help': 'AI provider to use',
                'config_help': 'Configuration file path',
                'preview_help': 'Preview mode - show analysis without moving files',
                'recursive_help': 'Process subdirectories recursively',
                'interactive_help': 'Interactive mode with detailed prompts',
                
                # Error messages
                'config_not_found': 'Configuration file not found: {}',
                'invalid_directory': 'Invalid directory: {}',
                'no_files_found': 'No files found to process',
                'ai_analysis_failed': 'AI analysis failed: {}',
            },
            
            'zh': {
                # CLI messages
                'app_title': '智能文件整理助手',
                'analyzing_directory': '正在分析目录: {dir}',
                'using_provider': '使用AI提供商: {provider}',
                'mode': '模式: {mode}',
                'found_files': '找到 {count} 个文件需要处理',
                'analyzing_file': '正在分析: {}',
                'confirm_proceed': '是否继续整理这些文件? [y/N]',
                'operation_cancelled': '操作已取消。',
                'organizing_files': '正在整理文件...',
                'operation_completed': '操作成功完成！',
                'error_occurred': '发生错误: {}',
                'undo_operation': '正在撤销上次整理操作...',
                'some_files_not_restored': '部分文件无法恢复:',
                'no_stats_found': '此目录未找到整理操作统计信息。',
                'file_not_exist': "错误: 文件 '{path}' 不存在。",
                
                # Analysis results
                'analysis_results': '分析结果',
                'file': '文件',
                'category': '类别',
                'confidence': '置信度',
                'suggested_name': '建议名称',
                'suggested': '建议',
                'reason': '原因',
                'reasoning': '推理过程',
                'content_analysis_not_supported': '此文件类型不支持内容分析',
                
                # Operation summary
                'operation_summary': '操作摘要',
                'files_processed': '已处理文件',
                'successful_operations': '成功操作',
                'failed_operations': '失败操作',
                'average_confidence': '平均置信度',
                'category_distribution': '类别分布',
                
                # Commands and options
                'organize_help': '使用AI分析整理目录中的文件',
                'undo_help': '撤销上次整理操作',
                'stats_help': '显示上次整理操作的统计信息',
                'analyze_help': '分析单个文件并显示命名建议',
                'dir_help': '要整理的目录',
                'provider_help': '使用的AI提供商',
                'config_help': '配置文件路径',
                'preview_help': '预览模式 - 显示分析结果但不移动文件',
                'recursive_help': '递归处理子目录',
                'interactive_help': '交互模式，提供详细提示',
                
                # Error messages
                'config_not_found': '配置文件未找到: {}',
                'invalid_directory': '无效目录: {}',
                'no_files_found': '未找到需要处理的文件',
                'ai_analysis_failed': 'AI分析失败: {}',
            }
        }
    
    def set_language(self, language: str):
        """Set the current language."""
        if language in self.translations:
            self.language = language
        else:
            print(f"Warning: Language '{language}' not supported, using English.")
            self.language = 'en'
    
    def t(self, key: str, **kwargs) -> str:
        """Translate a key to the current language.
        
        Args:
            key: Translation key
            **kwargs: Format parameters for the translation string
            
        Returns:
            Translated string
        """
        translation = self.translations.get(self.language, {}).get(key)
        
        if translation is None:
            # Fallback to English
            translation = self.translations.get('en', {}).get(key, key)
        
        if kwargs:
            try:
                return translation.format(**kwargs)
            except (KeyError, ValueError):
                return translation
        
        return translation
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.translations.keys())
    
    def load_from_file(self, file_path: str):
        """Load translations from a YAML file.
        
        Args:
            file_path: Path to the translation file
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    custom_translations = yaml.safe_load(f)
                    if custom_translations:
                        # Merge with existing translations
                        for lang, translations in custom_translations.items():
                            if lang in self.translations:
                                self.translations[lang].update(translations)
                            else:
                                self.translations[lang] = translations
            except Exception as e:
                print(f"Warning: Failed to load translations from {file_path}: {e}")

# Global instance
_i18n = I18n()

def set_language(language: str):
    """Set the global language."""
    _i18n.set_language(language)

def t(key: str, **kwargs) -> str:
    """Global translation function."""
    return _i18n.t(key, **kwargs)

def get_available_languages() -> list:
    """Get available languages."""
    return _i18n.get_available_languages()

def load_translations_from_file(file_path: str):
    """Load custom translations from file."""
    _i18n.load_from_file(file_path)
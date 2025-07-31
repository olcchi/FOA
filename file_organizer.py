#!/usr/bin/env python3
"""Smart File Organizer Agent - Main CLI Application."""

import click
import yaml
import os
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init()

# Import our modules
from src.ai_client import AIClient
from src.file_analyzer import FileAnalyzer
from src.organizer import FileOrganizer
from src.i18n import get_i18n, t



def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        click.echo(f"Error: {t('config_not_found', path=config_path)}")
        click.echo(f"Warning: {t('config_copy_instruction')}")
        raise click.Abort()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        click.echo(f"Error: {t('config_parse_error', error=str(e))}")
        raise click.Abort()


def get_files_to_process(directory: str, recursive: bool = True) -> List[str]:
    """Get list of files to process from directory."""
    files = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        click.echo(f"Error: {t('directory_not_exist', path=directory)}")
        return files
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for file_path in dir_path.glob(pattern):
        if file_path.is_file():
            # Skip hidden files and system files
            if not file_path.name.startswith('.') and not file_path.name.startswith('~'):
                files.append(str(file_path))
    
    return files


def print_analysis_results(results: List[Dict[str, Any]], preview_mode: bool = True):
    """Print analysis results in a formatted way."""
    click.echo(f"\n▶ {t('analysis_results_title')}")
    click.echo("-" * (len(t('analysis_results_title')) + 2))
    
    for i, result in enumerate(results, 1):
        if "error" in result:
            click.echo(f"{i}. ERROR: {result['file_path']} - {result['error']}")
            continue
        
        original_name = result.get("original_name", "Unknown")
        suggested_name = result.get("suggested_name", "No suggestion")
        category = result.get("category", "unknown")
        confidence = result.get("confidence", 0)
        reason = result.get("reason", "No reason provided")
        
        click.echo(f"\n{i}. {original_name}") 
        click.echo(f"   {t('category')}: {category}")
        click.echo(f"   {t('suggested')}: {suggested_name}")
        click.echo(f"   {t('confidence')}: {confidence*100:.1f}%")
        click.echo(f"   {t('reason')}: {reason}")


def print_operation_summary(summary: Dict[str, Any]):
    """Print operation summary."""
    click.echo(f"\n▶ {t('operation_summary')}")
    click.echo("-" * (len(t('operation_summary')) + 2))
    
    click.echo(f"{t('files_processed')}: {summary['total_files']}")
    click.echo(f"{t('successful_operations')}: {summary['successful_operations']}")
    
    if summary['failed_operations'] > 0:
        click.echo(f"{t('failed_operations')}: {summary['failed_operations']}")
    
    if summary.get('errors', 0) > 0:
        click.echo(f"Errors: {summary['errors']}")
    
    click.echo(f"{t('average_confidence')}: {summary['average_confidence']*100:.1f}%")
    
    if summary['category_distribution']:
        click.echo(f"\n{t('category_distribution')}:")
        for category, count in summary['category_distribution'].items():
            click.echo(f"  {category}: {count} files")


@click.group()
@click.option('--language', '-l', default='en', type=click.Choice(['en', 'zh']), help='Interface language (en/zh) / 界面语言')
@click.version_option(version="1.0.0")
@click.pass_context
def cli(ctx, language):
    """Smart File Organizer Agent - Intelligently organize and rename files using AI.
    
    智能文件整理助手 - 使用AI智能整理和重命名文件。
    """
    # Initialize context
    ctx.ensure_object(dict)
    
    # Set language
    from i18n import set_language
    set_language(language)
    
    # Store in context for subcommands
    ctx.obj['language'] = language


@cli.command()
@click.option('--dir', '-d', default='.', help='Directory to organize (default: current directory) / 要整理的目录（默认：当前目录）')
@click.option('--provider', '-p', help='AI provider to use (deepseek, openai, router) / 使用的AI提供商')
@click.option('--config', '-c', default='config.yaml', help='Configuration file path / 配置文件路径')
@click.option('--preview', is_flag=True, help='Preview mode - show what would be done without making changes / 预览模式')
@click.option('--recursive/--no-recursive', default=True, help='Process files recursively / 递归处理文件')
@click.option('--interactive', is_flag=True, help='Interactive mode - confirm each operation / 交互模式')
@click.pass_context
def organize(ctx, dir, provider, config, preview, recursive, interactive):
    """Organize files in the specified directory. / 整理指定目录中的文件。"""
    try:
        # Load configuration
        config_data = load_config(config)
        
        # Initialize components
        ai_client = AIClient(config_data)
        file_analyzer = FileAnalyzer(ai_client, config_data)
        file_organizer = FileOrganizer(config_data)
        
        # Override provider if specified
        if provider:
            config_data['default_provider'] = provider
        
        # Print banner
        banner_text = t('app_title')
        click.echo("=" * 60)
        click.echo(f"|{banner_text:^58}|")
        click.echo("=" * 60)
        
        click.echo(t('analyzing_directory', dir=dir))
        click.echo(t('using_provider', provider=config_data.get('default_provider', 'deepseek')))
        click.echo(t('mode', mode='Preview' if preview else 'Execute'))
        
        # Get files to process
        files = get_files_to_process(dir, recursive)
        
        if not files:
            click.echo(f"Warning: {t('no_files_found')}")
            return
        
        click.echo(f"\n{t('found_files', count=len(files))}")
        
        # Analyze files with progress bar
        with tqdm(total=len(files), desc="Analyzing files", unit="file") as pbar:
            analysis_results = []
            for file_path in files:
                try:
                    result = file_analyzer.analyze_file(file_path)
                    result["file_path"] = file_path
                    analysis_results.append(result)
                except Exception as e:
                    analysis_results.append({
                        "file_path": file_path,
                        "error": str(e),
                        "original_name": Path(file_path).name
                    })
                pbar.update(1)
        
        # Show analysis results
        print_analysis_results(analysis_results, preview)
        
        # Ask for confirmation if not in preview mode
        if not preview:
            if interactive or click.confirm(f"\n{t('confirm_proceed')}"):
                click.echo(f"\n{t('organizing_files')}")
            else:
                click.echo(f"Warning: {t('operation_cancelled')}")
                return
        
        # Organize files
        organization_result = file_organizer.organize_files(
            analysis_results, dir, preview_mode=preview
        )
        
        # Show summary
        print_operation_summary(organization_result["summary"])
        
        # Show errors if any
        if organization_result["errors"]:
            click.echo(f"\nErrors encountered:")
            for error in organization_result["errors"]:
                click.echo(f"  {error['file']}: {error['error']}")
        
        if not preview:
            click.echo(f"\n{t('operation_completed')}")
            click.echo(f"Files organized in: {dir}/organized/")
            if config_data.get("organization", {}).get("create_backup", True):
                click.echo(f"Backups saved in: {dir}/backup/")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--dir', '-d', default='.', help='Directory where organization was performed / 执行整理操作的目录')
@click.option('--config', '-c', default='config.yaml', help='Configuration file path / 配置文件路径')
@click.pass_context
def undo(ctx, dir, config):
    """Undo the last organization operation. / 撤销上次整理操作。"""
    try:
        config_data = load_config(config)
        file_organizer = FileOrganizer(config_data)
        
        click.echo(f"Warning: {t('undo_operation')}")
        
        result = file_organizer.undo_last_operation(dir)
        
        if result["success"]:
            click.echo(result['message'])
            if result.get("errors"):
                click.echo(f"\nError: {t('some_files_not_restored')}")
                for error in result["errors"]:
                    click.echo(f"  {error['file']}: {error['error']}")
        else:
            click.echo(f"Error: {result['message']}")
    
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        raise click.Abort()


@cli.command()
@click.option('--dir', '-d', default='.', help='Directory to check / 要检查的目录')
@click.option('--config', '-c', default='config.yaml', help='Configuration file path / 配置文件路径')
@click.pass_context
def stats(ctx, dir, config):
    """Show statistics from the last organization operation. / 显示上次整理操作的统计信息。"""
    try:
        config_data = load_config(config)
        file_organizer = FileOrganizer(config_data)
        
        stats_data = file_organizer.get_organization_stats(dir)
        
        if stats_data:
            print_operation_summary(stats_data)
        else:
            click.echo(f"Warning: {t('no_stats_found')}")
    
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        raise click.Abort()


@cli.command()
@click.argument('file_path')
@click.option('--provider', '-p', help='AI provider to use / 使用的AI提供商')
@click.option('--config', '-c', default='config.yaml', help='Configuration file path / 配置文件路径')
@click.pass_context
def analyze(ctx, file_path, provider, config):
    """Analyze a single file and show naming suggestions. / 分析单个文件并显示命名建议。"""
    try:
        config_data = load_config(config)
        
        if provider:
            config_data['default_provider'] = provider
        
        ai_client = AIClient(config_data)
        file_analyzer = FileAnalyzer(ai_client, config_data)
        
        if not os.path.exists(file_path):
            click.echo(f"Error: {t('file_not_exist', path=file_path)}")
            return
        
        click.echo(f"Analyzing file: {file_path}")
        
        result = file_analyzer.analyze_file(file_path)
        result["file_path"] = file_path
        
        print_analysis_results([result], preview_mode=True)
    
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        raise click.Abort()


if __name__ == '__main__':
    cli()
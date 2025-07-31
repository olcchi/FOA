"""File organizer module for managing file operations."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


class FileOrganizer:
    """Handles file organization operations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.create_backup = config.get("organization", {}).get("create_backup", True)
        self.categories = config.get("organization", {}).get("categories", {})
    
    def organize_files(self, analysis_results: List[Dict[str, Any]], 
                      target_dir: str, preview_mode: bool = False) -> Dict[str, Any]:
        """Organize files based on analysis results."""
        target_path = Path(target_dir)
        
        # Create organized directory structure
        if not preview_mode:
            self._create_directory_structure(target_path)
        
        operations = []
        errors = []
        
        for result in analysis_results:
            try:
                if "error" in result:
                    errors.append({
                        "file": result["file_path"],
                        "error": result["error"]
                    })
                    continue
                
                operation = self._plan_file_operation(result, target_path)
                
                if not preview_mode:
                    success = self._execute_operation(operation)
                    operation["executed"] = success
                else:
                    operation["executed"] = False
                
                operations.append(operation)
                
            except Exception as e:
                errors.append({
                    "file": result.get("file_path", "unknown"),
                    "error": str(e)
                })
        
        # Generate summary
        summary = self._generate_summary(operations, errors, preview_mode)
        
        # Save operation log
        if not preview_mode:
            self._save_operation_log(operations, errors, target_dir)
        
        return {
            "operations": operations,
            "errors": errors,
            "summary": summary
        }
    
    def _create_directory_structure(self, target_path: Path):
        """Create organized directory structure."""
        # Create main organized directory
        organized_dir = target_path / "organized"
        organized_dir.mkdir(exist_ok=True)
        
        # Create category subdirectories
        for category in self.categories.keys():
            category_dir = organized_dir / category
            category_dir.mkdir(exist_ok=True)
        
        # Create 'others' directory for uncategorized files
        others_dir = organized_dir / "others"
        others_dir.mkdir(exist_ok=True)
        
        # Create backup directory if needed
        if self.create_backup:
            backup_dir = target_path / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _plan_file_operation(self, analysis_result: Dict[str, Any], target_path: Path) -> Dict[str, Any]:
        """Plan file operation based on analysis result."""
        source_path = Path(analysis_result["file_path"])
        category = analysis_result.get("category", "others")
        suggested_name = analysis_result.get("suggested_name", source_path.name)
        
        # Determine target directory
        organized_dir = target_path / "organized" / category
        target_file_path = organized_dir / suggested_name
        
        # Handle name conflicts
        if target_file_path.exists():
            target_file_path = self._resolve_name_conflict(target_file_path)
        
        # Plan backup if enabled
        backup_path = None
        if self.create_backup:
            backup_dir = target_path / "backup" / datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / source_path.name
        
        return {
            "source_path": str(source_path),
            "target_path": str(target_file_path),
            "backup_path": str(backup_path) if backup_path else None,
            "original_name": source_path.name,
            "suggested_name": suggested_name,
            "category": category,
            "reason": analysis_result.get("reason", "No reason provided"),
            "confidence": analysis_result.get("confidence", 0.5),
            "operation_type": "move_and_rename"
        }
    
    def _resolve_name_conflict(self, target_path: Path) -> Path:
        """Resolve filename conflicts by adding a counter."""
        base_name = target_path.stem
        extension = target_path.suffix
        parent_dir = target_path.parent
        
        counter = 1
        while target_path.exists():
            new_name = f"{base_name}_{counter:03d}{extension}"
            target_path = parent_dir / new_name
            counter += 1
        
        return target_path
    
    def _execute_operation(self, operation: Dict[str, Any]) -> bool:
        """Execute a single file operation."""
        try:
            source_path = Path(operation["source_path"])
            target_path = Path(operation["target_path"])
            backup_path = Path(operation["backup_path"]) if operation["backup_path"] else None
            
            # Create backup if enabled
            if backup_path:
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, backup_path)
            
            # Ensure target directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move and rename file
            shutil.move(str(source_path), str(target_path))
            
            return True
            
        except Exception as e:
            operation["execution_error"] = str(e)
            return False
    
    def _generate_summary(self, operations: List[Dict[str, Any]], 
                         errors: List[Dict[str, Any]], preview_mode: bool) -> Dict[str, Any]:
        """Generate operation summary."""
        total_files = len(operations) + len(errors)
        successful_operations = sum(1 for op in operations if op.get("executed", False))
        
        # Count by category
        category_counts = {}
        for operation in operations:
            category = operation["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Calculate confidence statistics
        confidences = [op["confidence"] for op in operations if "confidence" in op]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            "total_files": total_files,
            "successful_operations": successful_operations,
            "failed_operations": len(operations) - successful_operations,
            "errors": len(errors),
            "category_distribution": category_counts,
            "average_confidence": round(avg_confidence, 2),
            "preview_mode": preview_mode,
            "timestamp": datetime.now().isoformat()
        }
    
    def _save_operation_log(self, operations: List[Dict[str, Any]], 
                           errors: List[Dict[str, Any]], target_dir: str):
        """Save operation log to file."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "target_directory": target_dir,
            "operations": operations,
            "errors": errors,
            "summary": self._generate_summary(operations, errors, False)
        }
        
        log_file = Path(target_dir) / "file_organization_log.json"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save operation log: {e}")
    
    def undo_last_operation(self, target_dir: str) -> Dict[str, Any]:
        """Undo the last organization operation."""
        log_file = Path(target_dir) / "file_organization_log.json"
        
        if not log_file.exists():
            return {"success": False, "message": "No operation log found"}
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            operations = log_data.get("operations", [])
            restored_count = 0
            errors = []
            
            # Reverse the operations
            for operation in reversed(operations):
                if not operation.get("executed", False):
                    continue
                
                try:
                    # Restore from backup if available
                    if operation.get("backup_path") and Path(operation["backup_path"]).exists():
                        shutil.move(operation["backup_path"], operation["source_path"])
                        restored_count += 1
                    elif Path(operation["target_path"]).exists():
                        # Move back to original location
                        shutil.move(operation["target_path"], operation["source_path"])
                        restored_count += 1
                
                except Exception as e:
                    errors.append({
                        "file": operation["original_name"],
                        "error": str(e)
                    })
            
            return {
                "success": True,
                "restored_files": restored_count,
                "errors": errors,
                "message": f"Restored {restored_count} files"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during undo operation: {str(e)}"
            }
    
    def get_organization_stats(self, target_dir: str) -> Optional[Dict[str, Any]]:
        """Get statistics from the last organization operation."""
        log_file = Path(target_dir) / "file_organization_log.json"
        
        if not log_file.exists():
            return None
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            return log_data.get("summary", {})
            
        except Exception:
            return None
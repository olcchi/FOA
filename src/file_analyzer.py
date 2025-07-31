"""File analyzer module for content analysis and intelligent naming."""

import os
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, List
import filetype
from datetime import datetime


class FileAnalyzer:
    """Analyzes files and generates intelligent naming suggestions."""
    
    def __init__(self, ai_client, config: Dict[str, Any]):
        self.ai_client = ai_client
        self.config = config
        self.max_file_size = config.get("organization", {}).get("max_file_size", 50) * 1024 * 1024  # Convert MB to bytes
        self.supported_types = config.get("organization", {}).get("supported_types", [])
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a file and return metadata and suggestions."""
        path = Path(file_path)
        
        # Basic file information
        file_info = {
            "original_name": path.name,
            "extension": path.suffix.lower(),
            "size": path.stat().st_size,
            "created_time": datetime.fromtimestamp(path.stat().st_ctime),
            "modified_time": datetime.fromtimestamp(path.stat().st_mtime),
            "mime_type": mimetypes.guess_type(file_path)[0],
        }
        
        # Detect file type using filetype library
        detected_type = filetype.guess(file_path)
        if detected_type:
            file_info["detected_type"] = detected_type.extension
            file_info["detected_mime"] = detected_type.mime
        
        # Determine category
        file_info["category"] = self._determine_category(file_info["extension"])
        
        # Generate intelligent suggestions if file is supported
        if self._is_analyzable(file_path, file_info):
            suggestions = self._generate_suggestions(file_path, file_info)
            file_info.update(suggestions)
        else:
            file_info["suggested_name"] = self._generate_basic_name(file_info)
            file_info["reason"] = "File type not supported for content analysis"
            file_info["confidence"] = 0.0
        
        return file_info
    
    def _determine_category(self, extension: str) -> str:
        """Determine file category based on extension."""
        categories = self.config.get("organization", {}).get("categories", {})
        
        extension = extension.lstrip(".")
        for category, extensions in categories.items():
            if extension in extensions:
                return category
        
        return "others"
    
    def _is_analyzable(self, file_path: str, file_info: Dict[str, Any]) -> bool:
        """Check if file can be analyzed for content."""
        # Check file size
        if file_info["size"] > self.max_file_size:
            return False
        
        # Check if extension is supported
        # file_info["extension"] already includes the dot, so we need to match it properly
        if file_info["extension"] not in self.supported_types:
            return False
        
        # Check if file exists and is readable
        try:
            with open(file_path, 'rb') as f:
                f.read(1)  # Try to read first byte
            return True
        except (IOError, OSError):
            return False
    
    def _generate_suggestions(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent naming suggestions using AI."""
        try:
            # Read file content based on type
            content_preview = self._extract_content_preview(file_path, file_info)
            
            # Create prompt for AI
            prompt = self._create_naming_prompt(file_info, content_preview)
            
            # Get AI response
            ai_response = self.ai_client.generate_response(prompt)
            
            # Parse AI response
            suggestions = self._parse_ai_response(ai_response, file_info)
            
            return suggestions
            
        except Exception as e:
            return {
                "suggested_name": self._generate_basic_name(file_info),
                "reason": f"AI analysis failed: {str(e)}",
                "confidence": 0.3
            }
    
    def _extract_content_preview(self, file_path: str, file_info: Dict[str, Any]) -> str:
        """Extract content preview from file."""
        extension = file_info["extension"]
        
        try:
            if extension in [".txt", ".md", ".py", ".js", ".html", ".css", ".yaml", ".yml"]:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(2000)  # First 2000 characters
            
            elif extension in [".pdf"]:
                # For PDF files, we'll just use filename and metadata
                return f"PDF file: {file_info['original_name']}"
            
            elif extension in [".jpg", ".jpeg", ".png"]:
                # For images, we'll use filename and basic info
                return f"Image file: {file_info['original_name']}, Size: {file_info['size']} bytes"
            
            else:
                # For other files, use basic info
                return f"File: {file_info['original_name']}, Type: {extension}"
                
        except Exception:
            return f"File: {file_info['original_name']}"
    
    def _create_naming_prompt(self, file_info: Dict[str, Any], content_preview: str) -> str:
        """Create prompt for AI naming suggestion."""
        prompt = f"""You are a file organization expert. Analyze the following file and suggest a better, more descriptive filename.

File Information:
- Original name: {file_info['original_name']}
- File type: {file_info['extension']}
- Category: {file_info['category']}
- Size: {file_info['size']} bytes
- Created: {file_info['created_time'].strftime('%Y-%m-%d')}

Content Preview:
{content_preview[:1000]}

Please suggest a new filename that is:
1. Descriptive and meaningful
2. Uses proper naming conventions (no spaces, use underscores or hyphens)
3. Keeps the original file extension
4. Is concise but informative
5. Follows format: descriptive_name{file_info['extension']}

Respond in JSON format:
{{
    "suggested_name": "new_filename{file_info['extension']}",
    "reason": "Brief explanation of why this name is better",
    "confidence": 0.8
}}"""
        
        return prompt
    
    def _parse_ai_response(self, ai_response: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response and extract suggestions."""
        try:
            import json
            
            # Try to extract JSON from response
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                parsed = json.loads(json_str)
                
                # Validate and clean the suggested name
                suggested_name = parsed.get("suggested_name", "")
                if suggested_name:
                    # Ensure proper extension
                    if not suggested_name.endswith(file_info["extension"]):
                        suggested_name = suggested_name.split('.')[0] + file_info["extension"]
                    
                    # Clean filename (remove invalid characters)
                    suggested_name = self._clean_filename(suggested_name)
                    
                    return {
                        "suggested_name": suggested_name,
                        "reason": parsed.get("reason", "AI generated suggestion"),
                        "confidence": min(max(parsed.get("confidence", 0.7), 0.0), 1.0)
                    }
            
            # Fallback if JSON parsing fails
            return {
                "suggested_name": self._generate_basic_name(file_info),
                "reason": "Could not parse AI response",
                "confidence": 0.3
            }
            
        except Exception:
            return {
                "suggested_name": self._generate_basic_name(file_info),
                "reason": "Error parsing AI response",
                "confidence": 0.3
            }
    
    def _generate_basic_name(self, file_info: Dict[str, Any]) -> str:
        """Generate basic filename based on category and timestamp."""
        category = file_info["category"]
        timestamp = file_info["created_time"].strftime("%Y%m%d_%H%M%S")
        extension = file_info["extension"]
        
        return f"{category}_{timestamp}{extension}"
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename by removing invalid characters."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove multiple consecutive underscores
        while '__' in filename:
            filename = filename.replace('__', '_')
        
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        
        return filename
    
    def batch_analyze(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple files in batch."""
        results = []
        
        for file_path in file_paths:
            try:
                result = self.analyze_file(file_path)
                result["file_path"] = file_path
                results.append(result)
            except Exception as e:
                results.append({
                    "file_path": file_path,
                    "error": str(e),
                    "original_name": Path(file_path).name
                })
        
        return results
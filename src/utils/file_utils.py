import os
import stat
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileUtils:
    @staticmethod
    def get_file_permissions(path: Path) -> str:
        """Get file/folder permissions in octal format."""
        try:
            return oct(path.stat().st_mode)[-3:]
        except Exception as e:
            logger.warning(f"Failed to get permissions for {path}: {str(e)}")
            return "N/A"

    @staticmethod
    def get_file_owner(path: Path) -> str:
        """Get the owner of the file/folder."""
        try:
            return path.owner()
        except Exception as e:
            logger.warning(f"Failed to get owner for {path}: {str(e)}")
            return "N/A"

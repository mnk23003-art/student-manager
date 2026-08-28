import os
import re
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.utils import timezone


def get_backup_dir():
    backup_dir = Path(settings.BASE_DIR) / 'backups'
    backup_dir.mkdir(exist_ok=True)
    return backup_dir


def _validate_backup_filename(filename):
    """Validate backup filename to prevent path traversal."""
    if not filename:
        raise ValueError("Filename is required")
    # Only allow alphanumeric, underscore, dot, and hyphen
    if not re.match(r'^backup_\d{8}_\d{6}\.sqlite3$', filename):
        raise ValueError("Invalid backup filename format")
    # Ensure no path separators
    if '/' in filename or '\\' in filename or '..' in filename:
        raise ValueError("Invalid backup filename")
    return filename


def create_backup():
    db_path = settings.DATABASES['default']['NAME']
    backup_dir = get_backup_dir()
    
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'backup_{timestamp}.sqlite3'
    backup_path = backup_dir / backup_filename
    
    shutil.copy2(db_path, backup_path)
    
    metadata = {
        'filename': backup_filename,
        'created_at': timezone.now().isoformat(),
        'size': backup_path.stat().st_size,
    }
    
    return metadata


def list_backups():
    backup_dir = get_backup_dir()
    backups = []
    
    for f in sorted(backup_dir.glob('backup_*.sqlite3'), reverse=True):
        backups.append({
            'filename': f.name,
            'path': str(f),
            'created_at': datetime.fromtimestamp(f.stat().st_mtime),
            'size': f.stat().st_size,
        })
    
    return backups


def restore_backup(backup_filename):
    _validate_backup_filename(backup_filename)
    
    backup_dir = get_backup_dir()
    backup_path = backup_dir / backup_filename
    
    # Resolve to absolute path and verify it's within backup dir
    backup_path = backup_path.resolve()
    backup_dir = backup_dir.resolve()
    
    if not str(backup_path).startswith(str(backup_dir)):
        raise ValueError("Access denied: path traversal detected")
    
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_filename}")
    
    db_path = settings.DATABASES['default']['NAME']
    
    pre_backup = create_backup()
    
    shutil.copy2(backup_path, db_path)
    
    return True


def delete_backup(backup_filename):
    _validate_backup_filename(backup_filename)
    
    backup_dir = get_backup_dir()
    backup_path = backup_dir / backup_filename
    
    # Resolve to absolute path and verify it's within backup dir
    backup_path = backup_path.resolve()
    backup_dir = backup_dir.resolve()
    
    if not str(backup_path).startswith(str(backup_dir)):
        raise ValueError("Access denied: path traversal detected")
    
    if backup_path.exists():
        backup_path.unlink()
        return True
    return False


def get_backup_size_display(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

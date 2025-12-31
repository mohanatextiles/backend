"""
Storage Service
===============
Validates Google Drive URLs for product images
"""


def validate_drive_url(url: str) -> tuple[bool, str]:
    """Validate Google Drive URL format"""
    if not url:
        return False, "URL cannot be empty"
    
    if "drive.google.com" not in url and "googleusercontent.com" not in url:
        return False, "Must be a Google Drive URL"
    
    return True, ""


def extract_drive_file_id(url: str) -> str:
    """Extract file ID from Google Drive URL"""
    import re
    
    # Format: /file/d/FILE_ID/
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format: ?id=FILE_ID or &id=FILE_ID
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format: uc?export=view&id=FILE_ID
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return ""


def get_drive_thumbnail_url(file_id: str, size: int = 400) -> str:
    """Get thumbnail URL for Drive file"""
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{size}"


def get_drive_view_url(file_id: str) -> str:
    """Get direct view URL for Drive file"""
    return f"https://drive.google.com/uc?export=view&id={file_id}"

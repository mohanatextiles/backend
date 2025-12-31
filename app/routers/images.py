"""
Image Proxy Router
==================
Proxies Google Drive images to avoid CORS issues
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import re

router = APIRouter(prefix="/api/images", tags=["Images"])


def extract_file_id(url: str) -> str:
    """Extract Google Drive file ID from various URL formats"""
    if not url:
        return ""
    
    # Format: lh3.googleusercontent.com/d/FILE_ID
    match = re.search(r'googleusercontent\.com/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format: drive.google.com/file/d/FILE_ID/view
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format: id=FILE_ID
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format: /d/FILE_ID
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return ""


@router.get("/proxy")
async def proxy_image(url: str):
    """
    Proxy Google Drive images to avoid CORS issues.
    Accepts any Google Drive URL format and serves the image.
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter required")
    
    # Extract file ID
    file_id = extract_file_id(url)
    
    if not file_id:
        # Not a Google Drive URL, try to fetch directly
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return StreamingResponse(
                        iter([response.content]),
                        media_type=response.headers.get("content-type", "image/jpeg")
                    )
        except Exception:
            pass
        raise HTTPException(status_code=400, detail="Invalid URL or unable to fetch")
    
    # Try multiple Google Drive URL formats
    urls_to_try = [
        f"https://drive.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/thumbnail?id={file_id}&sz=w800",
        f"https://lh3.googleusercontent.com/d/{file_id}",
    ]
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        for drive_url in urls_to_try:
            try:
                response = await client.get(drive_url)
                if response.status_code == 200 and len(response.content) > 1000:
                    content_type = response.headers.get("content-type", "image/jpeg")
                    if "text/html" not in content_type:
                        return StreamingResponse(
                            iter([response.content]),
                            media_type=content_type,
                            headers={
                                "Cache-Control": "public, max-age=86400",
                                "Access-Control-Allow-Origin": "*"
                            }
                        )
            except Exception:
                continue
    
    raise HTTPException(status_code=404, detail="Image not found or not accessible")


@router.get("/drive/{file_id}")
async def get_drive_image(file_id: str):
    """
    Get image directly by Google Drive file ID.
    """
    if not file_id or len(file_id) < 10:
        raise HTTPException(status_code=400, detail="Invalid file ID")
    
    urls_to_try = [
        f"https://drive.google.com/uc?export=download&id={file_id}",
        f"https://drive.google.com/thumbnail?id={file_id}&sz=w800",
    ]
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        for url in urls_to_try:
            try:
                response = await client.get(url)
                if response.status_code == 200 and len(response.content) > 1000:
                    content_type = response.headers.get("content-type", "image/jpeg")
                    if "text/html" not in content_type:
                        return StreamingResponse(
                            iter([response.content]),
                            media_type=content_type,
                            headers={
                                "Cache-Control": "public, max-age=86400",
                                "Access-Control-Allow-Origin": "*"
                            }
                        )
            except Exception:
                continue
    
    raise HTTPException(status_code=404, detail="Image not found")

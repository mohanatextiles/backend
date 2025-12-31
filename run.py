"""
Production Server Entry Point
==============================
Optimized for Hugging Face Spaces deployment
"""

import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment (Hugging Face uses 7860)
    port = int(os.getenv("PORT", 7860))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
    )

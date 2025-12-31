"""
Production server entry point for Hugging Face Spaces
Reads configuration from environment variables
"""
import os
import uvicorn

if __name__ == "__main__":
    # Hugging Face Spaces uses port 7860 by default
    port = int(os.environ.get("PORT", 7860))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
    )

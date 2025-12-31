"""
LLM Service
===========
OpenRouter integration for AI-powered product descriptions
"""

import httpx
import base64
from typing import Optional
from app.config import settings


class LLMService:
    """Service for generating product descriptions using OpenRouter LLM"""
    
    # Free models available on OpenRouter (Dec 2025)
    FREE_MODELS = [
        "google/gemini-2.0-flash-exp:free",  # Best: 1M context, experimental
        "nvidia/nemotron-nano-12b-v2-vl:free",  # Vision model, 128k context
        "google/gemma-3-27b-it:free",  # Large model, 131k context
        "mistralai/mistral-small-3.1-24b-instruct:free",  # 128k context
        "qwen/qwen-2.5-vl-7b-instruct:free",  # Vision model, 32k context
        "google/gemma-3-12b-it:free",  # 32k context
        "google/gemma-3-4b-it:free",  # Smallest/fastest, 32k context
    ]
    
    DEFAULT_MODEL = "nvidia/nemotron-nano-12b-v2-vl:free"
    
    @staticmethod
    async def generate_description(
        image_base64: str,
        product_name: str,
        category: str,
        model: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Generate product description from image using OpenRouter
        Returns: (description, error_message)
        """
        if not settings.openrouter_api_key:
            return "", "OpenRouter API key not configured"
        
        try:
            model = model or LLMService.DEFAULT_MODEL
            
            # Prepare the prompt
            prompt = f"""You are an expert fashion copywriter for a premium textile e-commerce store.

Product: {product_name}
Category: {category}

Carefully analyze the image and create an ATTRACTIVE, COMPELLING product description that:

1. Opens with an eye-catching statement about the product's most striking visual feature
2. Describes the fabric texture, quality, and feel (infer from visual appearance)
3. Highlights the color palette, patterns, prints, or embellishments you see
4. Mentions the design style (formal, casual, traditional, modern, etc.)
5. Suggests occasions or styling ideas based on the look
6. Ends with a persuasive call-to-action feeling

Write in an engaging, emotive tone that makes customers want to buy. Use sensory words and fashion terminology.
Length: 120-180 words.

IMPORTANT: Base your description ONLY on what you actually see in the image. Be specific and descriptive about visible details like patterns, colors, textures, cuts, and style elements."""

            # Prepare the request
            headers = {
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://mohana-textiles.com",  # Optional
                "X-Title": "Mohana Textiles",  # Optional
            }
            
            # Build message with image
            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    description = data["choices"][0]["message"]["content"].strip()
                    return description, ""
                elif response.status_code == 429:
                    error_msg = "Rate limit exceeded. Please wait a few minutes or add credits to your OpenRouter account."
                    return "", error_msg
                elif response.status_code == 401:
                    error_msg = "Invalid API key. Please check your OPENROUTER_API_KEY in .env file."
                    return "", error_msg
                else:
                    error_msg = f"OpenRouter API error: {response.status_code}"
                    return "", error_msg
                    
        except Exception as e:
            return "", f"LLM generation failed: {str(e)}"
    
    @staticmethod
    async def enhance_description(
        current_description: str,
        product_name: str,
        category: str
    ) -> tuple[str, str]:
        """
        Enhance existing product description without image
        Returns: (enhanced_description, error_message)
        """
        if not settings.openrouter_api_key:
            return current_description, "OpenRouter API key not configured"
        
        try:
            prompt = (
                f"Enhance this product description for a textile e-commerce website.\n\n"
                f"Product: {product_name}\n"
                f"Category: {category}\n"
                f"Current Description: {current_description}\n\n"
                f"Improve the description to be more engaging and professional while keeping it concise (100-150 words). "
                f"Maintain all factual information but make it more appealing to customers."
            )

            headers = {
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "model": LLMService.DEFAULT_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 300,
                "temperature": 0.7,
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    enhanced = data["choices"][0]["message"]["content"].strip()
                    return enhanced, ""
                else:
                    return current_description, f"API error: {response.status_code}"
                    
        except Exception as e:
            return current_description, f"Enhancement failed: {str(e)}"

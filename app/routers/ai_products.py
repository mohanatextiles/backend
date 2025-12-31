"""
AI Product Router
=================
Endpoints for creating products with AI-generated descriptions
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import base64
from typing import List, Optional
import json

from app.database import get_db
from app.services.auth import AuthService, get_current_admin
from app.services.llm import LLMService
from app.models.product import Product


router = APIRouter(prefix="/api/ai-products", tags=["AI Products"])


@router.post("/create-with-ai")
async def create_product_with_ai(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    discount: float = Form(0),
    sizes: str = Form("[]"),  # JSON array as string
    colors: str = Form("[]"),  # JSON array as string
    image: UploadFile = File(...),
    generate_description: bool = Form(True),
    custom_description: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Create a product with AI-generated description from image
    """
    try:
        # Read and encode image
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Generate description using AI if requested
        description = custom_description or ""
        if generate_description:
            ai_description, error = await LLMService.generate_description(
                image_base64=image_base64,
                product_name=name,
                category=category
            )
            if ai_description:
                description = ai_description
            elif not custom_description:
                # Fallback if AI fails and no custom description
                description = f"High-quality {category} - {name}"
        
        # Parse sizes and colors
        sizes_list = json.loads(sizes) if sizes else []
        colors_list = json.loads(colors) if colors else []
        
        # Calculate final price
        final_price = price * (1 - discount / 100)
        
        # Create product
        product = Product(
            name=name,
            category=category,
            price=price,
            discount=discount,
            final_price=final_price,
            description=description,
            image_data=f"data:image/{image.content_type.split('/')[-1]};base64,{image_base64}",
            sizes=sizes_list,
            colors=colors_list,
            enabled=True
        )
        
        db.add(product)
        await db.commit()
        await db.refresh(product)
        
        return {
            "success": True,
            "product": product.to_dict(),
            "ai_generated": generate_description and ai_description != ""
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-description")
async def generate_description_from_image(
    image: UploadFile = File(...),
    product_name: str = Form(...),
    category: str = Form(...)
):
    """
    Generate AI description from image without creating product
    Returns description that can be used in the form
    """
    try:
        # Read and encode image
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Generate description
        description, error = await LLMService.generate_description(
            image_base64=image_base64,
            product_name=product_name,
            category=category
        )
        
        if error:
            return {
                "success": False,
                "error": error,
                "description": f"High-quality {category} - {product_name}"
            }
        
        return {
            "success": True,
            "description": description
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "description": f"High-quality {category} - {product_name}"
        }


@router.post("/{product_id}/regenerate-description")
async def regenerate_description(
    product_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    """
    Regenerate AI description for existing product
    """
    try:
        # Get product
        result = await db.execute(
            f"SELECT * FROM products WHERE id = '{product_id}'"
        )
        product = result.first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Extract base64 from data URL
        if product.image_data and "base64," in product.image_data:
            image_base64 = product.image_data.split("base64,")[1]
            
            # Generate new description
            new_description, error = await LLMService.generate_description(
                image_base64=image_base64,
                product_name=product.name,
                category=product.category
            )
            
            if error:
                raise HTTPException(status_code=500, detail=error)
            
            # Update product
            product.description = new_description
            await db.commit()
            
            return {
                "success": True,
                "description": new_description
            }
        else:
            raise HTTPException(status_code=400, detail="No image data found")
            
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

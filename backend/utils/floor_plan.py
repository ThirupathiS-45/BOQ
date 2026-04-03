"""
Floor plan image generation using Hugging Face Inference API with Stable Diffusion XL.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def generate_floor_plan(prompt: str, timeout: int = 60) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Generate floor plan image using Hugging Face Inference API with Stable Diffusion XL.
    
    Args:
        prompt: Floor plan description
        timeout: API timeout in seconds
        
    Returns:
        Tuple of (success, image_data_url, error_message)
    """
    try:
        from huggingface_hub import InferenceClient
        import base64
        
        api_token = os.getenv("HUGGING_FACE_API_KEY")
        if not api_token:
            logger.error("HUGGING_FACE_API_KEY not configured")
            return False, None, "Hugging Face API key not configured"
        
        logger.info(f"Generating floor plan: {prompt[:50]}...")
        
        # Create Inference Client
        client = InferenceClient(api_key=api_token, model="stabilityai/stable-diffusion-xl-base-1.0")
        
        # Generate image
        image_output = client.text_to_image(
            prompt=prompt,
            negative_prompt="3D, perspective, realistic, colors, shadows, furniture, people",
        )
        
        # Convert PIL Image to bytes
        from io import BytesIO
        image_buffer = BytesIO()
        image_output.save(image_buffer, format="PNG")
        image_bytes = image_buffer.getvalue()
        
        # Convert to base64 data URL
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/png;base64,{image_base64}"
        
        logger.info(f"Floor plan generated successfully ({len(image_bytes)} bytes)")
        return True, image_url, None
        
    except ImportError:
        logger.error("huggingface_hub library not installed")
        return False, None, "huggingface_hub library not available - run: pip install huggingface_hub"
    except Exception as e:
        error_str = str(e)
        logger.error(f"Floor plan generation error: {error_str}")
        return False, None, error_str


def create_floor_plan_prompt(input_data: dict) -> str:
    """
    Create floor plan prompt from structured input.
    
    Args:
        input_data: Structured building parameters
        
    Returns:
        Floor plan description prompt
    """
    area = input_data.get("area_sqft", 1000)
    floors = input_data.get("floors", 1)
    bedrooms = input_data.get("bedrooms", 2)
    bathrooms = input_data.get("bathrooms", 1)
    quality = input_data.get("quality", 1)
    
    quality_map = {0: "simple", 1: "standard", 2: "luxury"}
    quality_str = quality_map.get(quality, "standard")
    
    prompt = (
        f"Top-down architectural floor plan for a {quality_str} "
        f"{floors}-floor residential building with {bedrooms} bedrooms, "
        f"{bathrooms} bathrooms, approximately {area} square feet. "
        f"Clean lines, technical drawing style, grid background, "
        f"labeled rooms, professional blueprint aesthetic."
    )
    
    return prompt

"""
NLP parsing using OpenRouter API to convert natural language to structured JSON.
"""

import os
import json
import logging
import httpx
from typing import Dict, Optional, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class NLPInput(BaseModel):
    """Structured output from NLP parsing."""
    area_sqft: int = Field(..., description="Area in square feet")
    floors: int = Field(default=1, description="Number of floors")
    bedrooms: int = Field(default=2, description="Number of bedrooms")
    bathrooms: int = Field(default=1, description="Number of bathrooms")
    kitchen: int = Field(default=1, description="Number of kitchens")
    hall: int = Field(default=1, description="Number of halls/living rooms")
    dining: int = Field(default=1, description="Number of dining areas")
    balcony: int = Field(default=1, description="Number of balconies")
    portico: int = Field(default=0, description="Number of porticos")
    quality: int = Field(default=1, description="Quality tier (0=budget, 1=standard, 2=premium)")


class NLPParser:
    """Parse natural language to structured JSON using OpenRouter API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NLP parser with OpenRouter API key.
        
        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set. NLP parsing will fail.")
        
        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-7b-instruct"  # Default model
        self.timeout = 30
    
    def parse(self, query: str) -> Tuple[bool, Dict, Optional[str]]:
        """
        Parse natural language query to structured JSON.
        
        Args:
            query: Natural language description (e.g., "2 floor house with 3 bedrooms")
            
        Returns:
            Tuple of (success, parsed_data, error_message)
        """
        if not self.api_key:
            return False, {}, "OpenRouter API key not configured"
        
        if not query or not query.strip():
            return False, {}, "Query cannot be empty"
        
        try:
            # Prepare prompt
            prompt = self._prepare_prompt(query)
            
            # Call OpenRouter API
            response = self._call_api(prompt)
            
            if not response:
                return False, {}, "Failed to get response from OpenRouter API"
            
            # Extract JSON from response
            parsed_data = self._extract_json(response)
            
            if not parsed_data:
                return False, {}, "Failed to parse JSON from API response"
            
            # Validate extracted data
            is_valid, validated_data = self._validate_and_normalize(parsed_data)
            
            if not is_valid:
                return False, {}, f"Validation failed: {validated_data}"
            
            logger.info(f"Successfully parsed query: {query}")
            return True, validated_data, None
            
        except Exception as e:
            logger.error(f"Error parsing query: {str(e)}")
            return False, {}, str(e)
    
    def _prepare_prompt(self, query: str) -> str:
        """Prepare prompt for NLP model."""
        return f"""Convert this natural language description into a JSON object with these exact fields:
- area_sqft (number): Total area in square feet
- floors (number): Number of floors
- bedrooms (number): Number of bedrooms
- bathrooms (number): Number of bathrooms
- kitchen (number): Number of kitchens
- hall (number): Number of halls/living areas
- dining (number): Number of dining areas
- balcony (number): Number of balconies
- portico (number): Number of porticos (0 if not mentioned)
- quality (number): 0 for budget, 1 for standard (default), 2 for premium

Rules:
- Use 0 for missing fields (except area_sqft which is required)
- All values must be non-negative integers
- Return only valid JSON, no explanation
- Quality defaults to 1 if not specified

Description: {query}

Return ONLY the JSON object, no other text."""
    
    def _call_api(self, prompt: str) -> Optional[str]:
        """Call OpenRouter API and return response text."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.3,  # Low temperature for deterministic output
            "max_tokens": 500,
        }
        
        try:
            response = httpx.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Extract message content
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                return content
            
            return None
            
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            return None
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from text response."""
        # Try direct parsing first
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        text = text.strip()
        
        try:
            parsed = json.loads(text)
            return parsed
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON: {text}")
            return None
    
    def _validate_and_normalize(self, data: Dict) -> Tuple[bool, Dict | str]:
        """Validate and normalize parsed data."""
        required_fields = {
            "area_sqft": int,
            "floors": int,
            "bedrooms": int,
            "bathrooms": int,
            "kitchen": int,
            "hall": int,
            "dining": int,
            "balcony": int,
            "portico": int,
            "quality": int,
        }
        
        normalized = {}
        
        # Check required fields and types
        for field, expected_type in required_fields.items():
            if field not in data:
                if field == "area_sqft":
                    return False, f"Missing required field: {field}"
                # Use default for optional fields
                normalized[field] = 0 if field != "quality" else 1
            else:
                try:
                    value = int(data[field])
                    if value < 0:
                        return False, f"Negative value not allowed for {field}: {value}"
                    normalized[field] = value
                except (ValueError, TypeError):
                    return False, f"Invalid type for {field}: {data[field]}"
        
        # Validate quality
        if normalized["quality"] not in [0, 1, 2]:
            logger.warning(f"Invalid quality value: {normalized['quality']}, defaulting to 1")
            normalized["quality"] = 1
        
        return True, normalized
    
    def set_model(self, model: str) -> None:
        """Change the model used for parsing."""
        self.model = model
        logger.info(f"Model changed to: {model}")


# Fallback parser for when API fails
class FallbackParser:
    """Fallback parser using regex/heuristics when NLP API is unavailable."""
    
    @staticmethod
    def parse(query: str) -> Dict:
        """
        Parse query using simple regex patterns.
        
        Args:
            query: Natural language description
            
        Returns:
            Parsed dictionary with defaults for unparseable fields
        """
        import re
        
        result = {
            "area_sqft": 1000,
            "floors": 1,
            "bedrooms": 2,
            "bathrooms": 1,
            "kitchen": 1,
            "hall": 1,
            "dining": 1,
            "balcony": 1,
            "portico": 0,
            "quality": 1,
        }
        
        query_lower = query.lower()
        
        # Extract numbers for various patterns
        patterns = {
            "area_sqft": [
                r"(\d+)\s*(?:sqft|sq\.?\s*ft|square\s*feet)",
                r"(\d+)\s*(?:sq\s*m|square\s*meter)",  # Will need conversion
            ],
            "floors": [r"(\d+)\s*(?:floor|storey|story)"],
            "bedrooms": [r"(\d+)\s*(?:bedroom|bhk|bed room|br)"],
            "bathrooms": [r"(\d+)\s*(?:bathroom|bath|washroom)"],
            "balcony": [r"(\d+)\s*(?:balcon|patio)"],
        }
        
        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, query_lower)
                if match:
                    try:
                        value = int(match.group(1))
                        if field == "area_sqft":
                            # If it's sq.m, convert to sq.ft
                            if "sq\s*m" in pattern or "square\s*meter" in pattern:
                                value = int(value * 10.764)
                        result[field] = value
                        break
                    except (ValueError, IndexError):
                        pass
        
        # Detect quality
        if any(word in query_lower for word in ["premium", "luxury", "high-end", "deluxe"]):
            result["quality"] = 2
        elif any(word in query_lower for word in ["budget", "basic", "economy", "simple"]):
            result["quality"] = 0
        
        logger.info(f"Fallback parsed query: {query} -> {result}")
        return result

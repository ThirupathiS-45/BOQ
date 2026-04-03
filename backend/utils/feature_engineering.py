"""
Feature engineering for ML model predictions.
Handles transformation of raw inputs to model features.
"""

import pandas as pd
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Handle feature engineering for BOQ prediction model."""
    
    # Base input features (must be present in input)
    BASE_FEATURES = [
        "area_sqft",
        "floors",
        "bedrooms",
        "bathrooms",
        "kitchen",
        "hall",
        "dining",
        "balcony",
        "portico",
        "quality",
    ]
    
    # Derived features (generated during engineering)
    DERIVED_FEATURES = [
        "total_built_up",
        "bedrooms_per_floor",
        "bath_per_bedroom",
        "area_sq",
        "floors_x_bedrooms",
        "floors_x_bath",
        "total_rooms",
        "rooms_density",
    ]
    
    # All features combined
    ALL_FEATURES = BASE_FEATURES + DERIVED_FEATURES
    
    def __init__(self):
        """Initialize feature engineer."""
        pass
    
    @staticmethod
    def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived features to dataframe.
        
        Args:
            df: DataFrame with base features
            
        Returns:
            DataFrame with derived features added
        """
        df = df.copy()
        
        # Avoid division by zero
        floors_safe = df["floors"].replace(0, 1)
        bedrooms_safe = df["bedrooms"].replace(0, 1)
        
        # Derived features
        df["total_built_up"] = df["area_sqft"] * df["floors"]
        df["bedrooms_per_floor"] = df["bedrooms"] / floors_safe
        df["bath_per_bedroom"] = df["bathrooms"] / bedrooms_safe
        df["area_sq"] = (df["area_sqft"] ** 2) / 1e6
        df["floors_x_bedrooms"] = df["floors"] * df["bedrooms"]
        df["floors_x_bath"] = df["floors"] * df["bathrooms"]
        df["total_rooms"] = (
            df["bedrooms"] +
            df["kitchen"] +
            df["hall"] +
            df["dining"]
        )
        df["rooms_density"] = df["total_rooms"] / df["area_sqft"]
        
        return df
    
    @staticmethod
    def validate_inputs(data: Dict) -> Tuple[bool, str]:
        """
        Validate input data has required features with valid values.
        
        Args:
            data: Input dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required = FeatureEngineer.BASE_FEATURES
        
        # Check all required fields present
        missing = [f for f in required if f not in data]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        # Check numeric values
        numeric_fields = [f for f in required if f != "quality"]
        for field in numeric_fields:
            try:
                val = float(data[field])
                if val < 0:
                    return False, f"Field '{field}' cannot be negative: {val}"
            except (ValueError, TypeError):
                return False, f"Field '{field}' must be numeric, got: {data[field]}"
        
        # Check quality value
        quality = data.get("quality", 1)
        if isinstance(quality, int):
            if quality not in [0, 1, 2]:
                return False, f"Quality must be 0 (budget), 1 (standard), or 2 (premium), got: {quality}"
        elif isinstance(quality, str):
            if quality.lower() not in ["budget", "standard", "premium"]:
                return False, f"Quality must be 'budget', 'standard', or 'premium', got: {quality}"
        
        return True, ""
    
    @staticmethod
    def apply_defaults(data: Dict) -> Dict:
        """
        Apply default values for missing optional fields.
        
        Args:
            data: Input dictionary
            
        Returns:
            Dictionary with defaults applied
        """
        defaults = {
            "area_sqft": 1000,
            "floors": 1,
            "bedrooms": 2,
            "bathrooms": 1,
            "kitchen": 1,
            "hall": 1,
            "dining": 1,
            "balcony": 1,
            "portico": 0,
            "quality": 1,  # standard
        }
        
        result = defaults.copy()
        result.update(data)
        
        return result
    
    @staticmethod
    def prepare_for_model(
        data: Dict,
        model_features: List[str]
    ) -> pd.DataFrame:
        """
        Prepare input data for model prediction.
        
        Args:
            data: Raw input dictionary
            model_features: List of features expected by model
            
        Returns:
            DataFrame aligned with model features
            
        Raises:
            ValueError: If validation fails
        """
        # Apply defaults
        data = FeatureEngineer.apply_defaults(data)
        
        # Validate
        is_valid, error = FeatureEngineer.validate_inputs(data)
        if not is_valid:
            raise ValueError(f"Input validation failed: {error}")
        
        # Create DataFrame
        df = pd.DataFrame([data])
        
        # Add derived features
        df = FeatureEngineer.add_derived_features(df)
        
        # Align with model features
        for col in model_features:
            if col not in df.columns:
                df[col] = 0
        
        df = df[model_features]
        
        logger.info(f"Features prepared: {len(df.columns)} features aligned")
        
        return df

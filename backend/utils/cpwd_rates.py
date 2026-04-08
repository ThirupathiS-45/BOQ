"""
CPWD-based rate table with dynamic cost estimation.
Support for location-based multipliers and quality tiers.
"""

from typing import Dict, Literal
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QualityTier(str, Enum):
    """Quality tiers for cost estimation."""
    BUDGET = "budget"
    STANDARD = "standard"
    PREMIUM = "premium"


class CPWDRates:
    """CPWD-like rate table for material cost estimation."""
    
    # Base rates (₹) - ranges for different quality tiers
    BASE_RATES = {
        "cement_bags": {"min": 380, "max": 450},
        "steel_kg": {"min": 65, "max": 80},
        "sand_cft": {"min": 50, "max": 75},
        "aggregate_cft": {"min": 45, "max": 60},
        "bricks": {"min": 8, "max": 12},
        "tiles_sqft": {"min": 60, "max": 120},
        "paint_liters": {"min": 180, "max": 280},
        "putty_kg": {"min": 25, "max": 40},
        "wiring_meters": {"min": 30, "max": 50},
        "switches": {"min": 80, "max": 200},
        "lights": {"min": 150, "max": 400},
        "pipes_meters": {"min": 50, "max": 90},
        "bathroom_sets": {"min": 35000, "max": 50000},  # Minimum ₹35,000
    }
    
    # Location-based multipliers (can be customized)
    LOCATION_MULTIPLIERS = {
        "metro": 1.25,           # 25% premium for metros
        "tier1": 1.15,           # 15% premium for Tier-1 cities
        "tier2": 1.0,            # Standard rate for Tier-2
        "tier3": 0.85,           # 15% discount for Tier-3
        "rural": 0.75,           # 25% discount for rural
    }
    
    def __init__(self, location: str = "tier2", quality: str = "standard"):
        """
        Initialize CPWD rates with location and quality tier.
        
        Args:
            location: Location tier for rate multiplier
            quality: Quality tier (budget, standard, premium)
        """
        self.location = location.lower()
        self.quality = quality.lower()
        
        # Validate location
        if self.location not in self.LOCATION_MULTIPLIERS:
            logger.warning(f"Location '{location}' not found, using 'tier2' (standard)")
            self.location = "tier2"
        
        # Validate quality
        if self.quality not in [tier.value for tier in QualityTier]:
            logger.warning(f"Quality '{quality}' not found, using 'standard'")
            self.quality = "standard"
        
        self.location_multiplier = self.LOCATION_MULTIPLIERS[self.location]
    
    def get_rate(self, material: str) -> float:
        """
        Get the rate for a material based on quality tier and location.
        
        Args:
            material: Material name (must be in BASE_RATES)
            
        Returns:
            Rate in ₹ per unit
            
        Raises:
            ValueError: If material not found
        """
        if material not in self.BASE_RATES:
            raise ValueError(f"Material '{material}' not found in CPWD rates")
        
        rate_range = self.BASE_RATES[material]
        
        # Select rate based on quality
        if self.quality == "budget":
            base_rate = rate_range["min"]
        elif self.quality == "premium":
            base_rate = rate_range["max"]
        else:  # standard
            base_rate = (rate_range["min"] + rate_range["max"]) / 2
        
        # Apply location multiplier
        final_rate = base_rate * self.location_multiplier
        
        return round(final_rate, 2)
    
    def get_all_rates(self) -> Dict[str, float]:
        """Get all material rates for current configuration."""
        return {material: self.get_rate(material) for material in self.BASE_RATES.keys()}
    
    def get_quality_summary(self) -> Dict[str, str]:
        """Get current quality and location configuration."""
        return {
            "quality": self.quality,
            "location": self.location,
            "location_multiplier": self.location_multiplier,
        }


def parse_quality(quality_input: int | str) -> str:
    """
    Parse quality input to standard format.
    
    Args:
        quality_input: 0=budget, 1=standard, 2=premium, or string name
        
    Returns:
        Quality tier name (budget, standard, premium)
    """
    if isinstance(quality_input, int):
        quality_map = {0: "budget", 1: "standard", 2: "premium"}
        if quality_input in quality_map:
            return quality_map[quality_input]
        return "standard"
    
    quality_str = str(quality_input).lower()
    if quality_str in [tier.value for tier in QualityTier]:
        return quality_str
    
    logger.warning(f"Invalid quality input '{quality_input}', defaulting to 'standard'")
    return "standard"

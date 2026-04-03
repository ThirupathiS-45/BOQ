"""
Cost calculation and breakdown using CPWD rates.
"""

import logging
from typing import Dict, Optional
from .cpwd_rates import CPWDRates

logger = logging.getLogger(__name__)


class CostCalculator:
    """Calculate material and labor costs from BOQ predictions."""
    
    # Labor cost estimation (₹ per sq.ft)
    LABOR_RATES = {
        "budget": 150,      # ₹ per sq.ft
        "standard": 250,    # ₹ per sq.ft
        "premium": 400,     # ₹ per sq.ft
    }
    
    def __init__(
        self,
        quality: str = "standard",
        location: str = "tier2",
        labor_multiplier: float = 1.0,
    ):
        """
        Initialize cost calculator.
        
        Args:
            quality: Quality tier (budget, standard, premium)
            location: Location tier for rate multiplier
            labor_multiplier: Custom multiplier for labor costs
        """
        self.quality = quality.lower()
        self.location = location.lower()
        self.labor_multiplier = labor_multiplier
        self.cpwd_rates = CPWDRates(location=location, quality=quality)
    
    def calculate(
        self,
        boq: Dict[str, float],
        area_sqft: float,
    ) -> Dict[str, float | Dict]:
        """
        Calculate total cost from BOQ and area.
        
        Args:
            boq: Bill of Quantities with material quantities
            area_sqft: Built-up area in square feet
            
        Returns:
            Dictionary with material cost, labor cost, total cost, and breakdown
        """
        # Calculate material cost
        material_cost, material_breakdown = self._calculate_material_cost(boq)
        
        # Calculate labor cost
        labor_cost = self._calculate_labor_cost(area_sqft)
        
        # Total cost
        total_cost = material_cost + labor_cost
        
        return {
            "material_cost": round(material_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "total_cost": round(total_cost, 2),
            "cost_per_sqft": round(total_cost / area_sqft, 2) if area_sqft > 0 else 0,
            "breakdown": {
                "materials": material_breakdown,
                "labor": {
                    "rate_per_sqft": self.LABOR_RATES[self.quality],
                    "area_sqft": area_sqft,
                    "multiplier": self.labor_multiplier,
                    "total": round(labor_cost, 2),
                }
            }
        }
    
    def _calculate_material_cost(self, boq: Dict[str, float]) -> tuple:
        """
        Calculate material cost and breakdown from BOQ.
        
        Args:
            boq: Bill of Quantities dictionary
            
        Returns:
            Tuple of (total_cost, breakdown_dict)
        """
        total_cost = 0
        breakdown = {}
        
        # Get all CPWD rates
        rates = self.cpwd_rates.get_all_rates()
        
        # Calculate cost for each material in BOQ
        for material, quantity in boq.items():
            if material in rates:
                rate = rates[material]
                cost = quantity * rate
                total_cost += cost
                
                breakdown[material] = {
                    "quantity": round(quantity, 2),
                    "unit": self._get_unit(material),
                    "rate": rate,
                    "cost": round(cost, 2),
                }
                
                logger.debug(f"{material}: {quantity} × {rate} = {cost}")
        
        return total_cost, breakdown
    
    def _calculate_labor_cost(self, area_sqft: float) -> float:
        """
        Calculate labor cost based on area and quality.
        
        Args:
            area_sqft: Built-up area in square feet
            
        Returns:
            Total labor cost
        """
        base_rate = self.LABOR_RATES.get(self.quality, self.LABOR_RATES["standard"])
        labor_cost = area_sqft * base_rate * self.labor_multiplier
        
        logger.debug(
            f"Labor cost: {area_sqft} sqft × ₹{base_rate}/sqft × {self.labor_multiplier} = ₹{labor_cost}"
        )
        
        return labor_cost
    
    @staticmethod
    def _get_unit(material: str) -> str:
        """Get unit of measurement for material."""
        units = {
            "cement_bags": "bags",
            "steel_kg": "kg",
            "sand_cft": "cft",
            "aggregate_cft": "cft",
            "bricks": "nos",
            "tiles_sqft": "sqft",
            "paint_liters": "liters",
            "putty_kg": "kg",
            "wiring_meters": "meters",
            "switches": "nos",
            "lights": "nos",
            "pipes_meters": "meters",
            "bathroom_sets": "nos",
        }
        return units.get(material, "units")
    
    def get_cost_estimate_summary(
        self,
        boq: Dict[str, float],
        area_sqft: float,
    ) -> str:
        """
        Generate a formatted cost estimate summary.
        
        Args:
            boq: Bill of Quantities
            area_sqft: Built-up area in square feet
            
        Returns:
            Formatted summary string
        """
        cost_data = self.calculate(boq, area_sqft)
        
        summary = f"""
╔════════════════════════════════════════════╗
║       💰 COST ESTIMATION SUMMARY 💰        ║
╚════════════════════════════════════════════╝

Location Tier:        {self.location.upper()}
Quality Level:        {self.quality.upper()}

Material Cost:        ₹{cost_data['material_cost']:,.2f}
Labor Cost:           ₹{cost_data['labor_cost']:,.2f}
─────────────────────────────────────────────
Total Cost:           ₹{cost_data['total_cost']:,.2f}
─────────────────────────────────────────────
Cost per sq.ft:       ₹{cost_data['cost_per_sqft']:,.2f}
"""
        return summary

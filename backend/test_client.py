"""
Test client for BOQ Prediction API.
Demonstrates various API usage patterns.
"""

import json
import requests
from typing import Dict, Any
import time


class BOQAPIClient:
    """Client for BOQ Prediction API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize API client."""
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def predict(
        self,
        query: str,
        quality: int = 1,
        location: str = "tier2",
        use_nlp: bool = True,
    ) -> Dict[str, Any]:
        """
        Predict BOQ from natural language query.
        
        Args:
            query: Natural language description
            quality: 0=budget, 1=standard, 2=premium
            location: Location tier
            use_nlp: Use NLP parsing
            
        Returns:
            Prediction response
        """
        payload = {
            "query": query,
            "quality": quality,
            "location": location,
            "use_nlp": use_nlp,
        }
        
        response = self.session.post(
            f"{self.base_url}/predict",
            json=payload,
        )
        response.raise_for_status()
        return response.json()
    
    def predict_with_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict BOQ from structured input.
        
        Args:
            input_data: Structured input dictionary
            
        Returns:
            Prediction response
        """
        response = self.session.post(
            f"{self.base_url}/predict-with-input",
            json=input_data,
        )
        response.raise_for_status()
        return response.json()
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """Format API response for display."""
        if not response.get("success"):
            return f"❌ Error: {response.get('error', 'Unknown error')}"
        
        result = []
        result.append("\n" + "="*60)
        result.append("🏗️  BOQ PREDICTION RESULT")
        result.append("="*60)
        
        # Input summary
        input_data = response["input"]
        result.append("\n📝 INPUT PARAMETERS:")
        result.append(f"  Area: {input_data['area_sqft']:,} sqft")
        result.append(f"  Floors: {input_data['floors']}")
        result.append(f"  Bedrooms: {input_data['bedrooms']}")
        result.append(f"  Bathrooms: {input_data['bathrooms']}")
        result.append(f"  Quality: {response['metadata']['quality'].upper()}")
        result.append(f"  Location: {response['metadata']['location'].upper()}")
        
        # BOQ Summary
        boq = response["boq"]
        result.append("\n📦 BOQ (Top 5 Materials):")
        sorted_items = sorted(boq.items(), key=lambda x: x[1], reverse=True)[:5]
        for material, quantity in sorted_items:
            unit = self._get_unit(material)
            result.append(f"  {material:<20}: {quantity:>10.1f} {unit}")
        
        # Cost breakdown
        cost = response["cost"]
        result.append("\n💰 COST BREAKDOWN:")
        result.append(f"  Material Cost:      ₹{cost['material_cost']:>15,.2f}")
        result.append(f"  Labor Cost:         ₹{cost['labor_cost']:>15,.2f}")
        result.append("-" * 50)
        result.append(f"  Total Cost:         ₹{cost['total_cost']:>15,.2f}")
        result.append(f"  Cost per sq.ft:     ₹{cost['cost_per_sqft']:>15,.2f}")
        
        result.append("="*60 + "\n")
        
        return "\n".join(result)
    
    @staticmethod
    def _get_unit(material: str) -> str:
        """Get unit for material."""
        units = {
            "cement_bags": "bags",
            "steel_kg": "kg",
            "sand_cft": "cft",
            "aggregate_cft": "cft",
            "bricks": "nos",
            "tiles_sqft": "sqft",
            "paint_liters": "liters",
            "putty_kg": "kg",
            "wiring_meters": "m",
            "switches": "nos",
            "lights": "nos",
            "pipes_meters": "m",
            "bathroom_sets": "nos",
        }
        return units.get(material, "units")


def test_nlp_parsing():
    """Test NLP parsing with various queries."""
    client = BOQAPIClient()
    
    test_queries = [
        "2 floor house with 3 bedrooms in 1200 sqft",
        "Premium apartment, 4 bedrooms, 2500 sq ft",
        "Budget home, 1200 sqft, 2 floors",
        "Villa with 5 bedrooms, 3500 sqft, luxury finish",
        "Compact flat, 2 bedrooms, 800 sqft",
    ]
    
    print("\n" + "="*60)
    print("🧪 NLP PARSING TEST")
    print("="*60)
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        try:
            response = client.predict(query)
            print(client.format_response(response))
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def test_quality_variations():
    """Test cost variations across quality tiers."""
    client = BOQAPIClient()
    
    base_query = "2 floor house with 3 bedrooms in 1200 sqft"
    qualities = [
        (0, "Budget"),
        (1, "Standard"),
        (2, "Premium"),
    ]
    
    print("\n" + "="*60)
    print("💎 QUALITY TIER COMPARISON")
    print("="*60)
    
    results = []
    
    for quality_id, quality_name in qualities:
        print(f"\n🔄 Testing {quality_name} tier...")
        try:
            response = client.predict(base_query, quality=quality_id)
            if response.get("success"):
                cost = response["cost"]["total_cost"]
                results.append((quality_name, cost))
                print(f"  Total Cost: ₹{cost:,.2f}")
            else:
                print(f"  ❌ Error: {response.get('error')}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    # Summary
    print("\n" + "-"*60)
    print("📊 SUMMARY:")
    for quality, cost in results:
        percentage = (cost / results[0][1] * 100) if results else 0
        print(f"  {quality:<15}: ₹{cost:>12,.2f} ({percentage:>6.1f}%)")


def test_location_multipliers():
    """Test cost variations across locations."""
    client = BOQAPIClient()
    
    base_input = {
        "area_sqft": 1200,
        "floors": 2,
        "bedrooms": 3,
        "bathrooms": 2,
        "kitchen": 1,
        "hall": 1,
        "dining": 1,
        "balcony": 1,
        "portico": 0,
        "quality": 1,
    }
    
    locations = ["metro", "tier1", "tier2", "tier3", "rural"]
    
    print("\n" + "="*60)
    print("🗺️  LOCATION MULTIPLIER TEST")
    print("="*60)
    
    results = []
    
    for location in locations:
        print(f"\n🔄 Testing {location.upper()}...")
        try:
            input_data = base_input.copy()
            input_data["location"] = location
            response = client.predict_with_input(input_data)
            if response.get("success"):
                cost = response["cost"]["total_cost"]
                results.append((location, cost))
                print(f"  Total Cost: ₹{cost:,.2f}")
            else:
                print(f"  ❌ Error: {response.get('error')}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    # Summary
    print("\n" + "-"*60)
    print("📊 SUMMARY (Location Multipliers):")
    base_cost = results[2][1] if len(results) > 2 else results[0][1]  # tier2 as base
    for location, cost in results:
        multiplier = cost / base_cost
        print(f"  {location:<10}: ₹{cost:>12,.2f} ({multiplier:>5.2f}×)")


def test_area_variations():
    """Test cost variations for different areas."""
    client = BOQAPIClient()
    
    areas = [500, 800, 1200, 1800, 2500]
    
    print("\n" + "="*60)
    print("📐 AREA VARIATION TEST")
    print("="*60)
    
    results = []
    
    for area in areas:
        print(f"\n🔄 Testing {area} sqft...")
        try:
            input_data = {
                "area_sqft": area,
                "floors": 2,
                "bedrooms": 3,
                "bathrooms": 2,
                "kitchen": 1,
                "hall": 1,
                "dining": 1,
                "balcony": 1,
                "portico": 0,
                "quality": 1,
                "location": "tier2",
            }
            response = client.predict_with_input(input_data)
            if response.get("success"):
                cost = response["cost"]["total_cost"]
                cost_per_sqft = response["cost"]["cost_per_sqft"]
                results.append((area, cost, cost_per_sqft))
                print(f"  Total: ₹{cost:,.2f} | Per sqft: ₹{cost_per_sqft:,.2f}")
            else:
                print(f"  ❌ Error: {response.get('error')}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    # Summary
    print("\n" + "-"*60)
    print("📊 SUMMARY (Area Variations):")
    print(f"  {'Area':<10} {'Total Cost':<15} {'Cost/sqft':<15}")
    print("-" * 40)
    for area, cost, cost_per_sqft in results:
        print(f"  {area:<10} ₹{cost:>13,.0f} ₹{cost_per_sqft:>13,.2f}")


def test_structured_input():
    """Test direct structured input prediction."""
    client = BOQAPIClient()
    
    print("\n" + "="*60)
    print("📋 STRUCTURED INPUT TEST")
    print("="*60)
    
    input_data = {
        "area_sqft": 1500,
        "floors": 3,
        "bedrooms": 4,
        "bathrooms": 3,
        "kitchen": 1,
        "hall": 2,
        "dining": 1,
        "balcony": 2,
        "portico": 1,
        "quality": 2,  # Premium
        "location": "metro",
    }
    
    print(f"\n📝 Input: {json.dumps(input_data, indent=2)}")
    
    try:
        response = client.predict_with_input(input_data)
        print(client.format_response(response))
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all tests."""
    print("\n" + "🚀 "*20)
    print("BOQ PREDICTION API - COMPREHENSIVE TEST SUITE")
    print("🚀 "*20)
    
    # Check API health
    print("\n🏥 Health Check...")
    client = BOQAPIClient()
    try:
        health = client.health_check()
        if health.get("status") == "operational":
            print("✅ API is operational")
            print(f"   Model loaded: {health['model_loaded']}")
            print(f"   API key configured: {health['api_key_configured']}")
        else:
            print(f"⚠️  API status: {health['status']}")
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return
    
    # Run tests
    test_structured_input()
    test_nlp_parsing()
    test_quality_variations()
    test_location_multipliers()
    test_area_variations()
    
    print("\n" + "✅ "*20)
    print("TEST SUITE COMPLETED")
    print("✅ "*20 + "\n")


if __name__ == "__main__":
    main()

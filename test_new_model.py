#!/usr/bin/env python3
"""Test the new model with NLP parsing and quality differentiation"""

import requests
import json

BASE_URL = "http://localhost:8000"
PROMPT = "A luxurious 2 BHK apartment with 1200 sq ft, modern open kitchen, spacious living room, north-facing with natural light."

# Quality levels: 0=Budget, 1=Standard, 2=Premium
QUALITY_LEVELS = {
    0: "Budget",
    1: "Standard", 
    2: "Premium"
}

print("=" * 80)
print("Testing New Model with NLP Parsing & Quality Differentiation")
print("=" * 80)
print(f"\nPrompt: {PROMPT}\n")
print("=" * 80)

results = {}

for quality, quality_name in QUALITY_LEVELS.items():
    print(f"\n📊 Testing Quality Level: {quality_name} (q={quality})")
    print("-" * 80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json={
                "query": PROMPT,
                "quality": quality,
                "location": "tier2",
                "use_nlp": True
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            results[quality] = data
            
            if data.get("success"):
                # Extract key metrics from nested cost object
                cost_data = data.get("cost", {})
                material_cost = cost_data.get("material_cost", 0)
                labor_cost = cost_data.get("labor_cost", 0)
                total_cost = cost_data.get("total_cost", 0)
                
                print(f"✅ Status: SUCCESS")
                print(f"   Material Cost: ₹{material_cost:,.0f}")
                print(f"   Labor Cost:    ₹{labor_cost:,.0f}")
                print(f"   Total Cost:    ₹{total_cost:,.0f}")
                
                # Show BOQ items
                if data.get("boq"):
                    boq = data["boq"]
                    print(f"\n   BOQ Items ({len(boq)} materials):")
                    item_count = 0
                    for item_name, quantity in list(boq.items())[:5]:  # Show first 5
                        rate_info = cost_data.get("breakdown", {}).get("materials", {}).get(item_name, {})
                        rate = rate_info.get("rate", 0)
                        cost = rate_info.get("cost", 0)
                        unit = rate_info.get("unit", "unit")
                        print(f"      • {item_name}: {quantity:.0f} {unit} @ ₹{rate} = ₹{cost:,.0f}")
                        item_count += 1
                    if len(boq) > 5:
                        print(f"      ... and {len(boq) - 5} more items")
            else:
                print(f"❌ Status: FAILED - {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except requests.exceptions.Timeout:
        print(f"❌ Request Timeout (60s)")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Compare quality differentiation
print("\n" + "=" * 80)
print("QUALITY DIFFERENTIATION ANALYSIS")
print("=" * 80)

if all(q in results for q in [0, 1, 2]):
    budget_total = results[0].get("cost", {}).get("total_cost", 0)
    standard_total = results[1].get("cost", {}).get("total_cost", 0)
    premium_total = results[2].get("cost", {}).get("total_cost", 0)
    
    std_increase = ((standard_total - budget_total) / budget_total * 100) if budget_total > 0 else 0
    prem_increase = ((premium_total - budget_total) / budget_total * 100) if budget_total > 0 else 0
    
    print(f"\n💰 Cost Comparison:")
    print(f"   Budget (q=0):    ₹{budget_total:>12,.0f}  (baseline)")
    print(f"   Standard (q=1):  ₹{standard_total:>12,.0f}  (+{std_increase:.1f}%)")
    print(f"   Premium (q=2):   ₹{premium_total:>12,.0f}  (+{prem_increase:.1f}%)")
    
    print(f"\n✅ Quality Differentiation: {'WORKING' if 20 <= std_increase <= 50 and 30 <= prem_increase <= 60 else 'CHECK VALUES'}")
    print(f"   Expected range: Standard +20-40%, Premium +30-60%")
    print(f"   Actual:         Standard +{std_increase:.1f}%, Premium +{prem_increase:.1f}%")
else:
    print("❌ Not all quality levels returned valid results")

print("\n" + "=" * 80)

# Quick Test Commands

## Test API with curl

### Test 1: Basic prediction with all new features
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "query": "2 BHK apartment, 1000 sqft, modern design",
    "quality": 1,
    "location": "tier2",
    "contractor_margin": true,
    "permit_fee": 40000,
    "use_nlp": true
  }'
```

### Test 2: Without contractor margin
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "query": "3 BHK villa, 1500 sqft",
    "quality": 0,
    "contractor_margin": false,
    "permit_fee": 30000
  }'
```

### Test 3: Premium with custom permit fee
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "query": "4 BHK luxury apartment, 2500 sqft, premium finishes",
    "quality": 2,
    "location": "metro",
    "contractor_margin": true,
    "permit_fee": 75000
  }'
```

## Expected Response Structure

```json
{
  "success": true,
  "input": {...},
  "boq": {...},
  "cost": {
    "material_cost": 1000000,
    "labor_cost": 235000,
    "total_cost": 1500000,
    "cost_per_sqft": 1500,
    "hidden_costs": {
      "gst": 180000,
      "permit_fee": 40000,
      "contingency": 122300,
      "contractor_margin": 155160,
      "subtotal": 1737460
    },
    "breakdown": {
      "materials": {...},
      "labor": {
        "percentage": 0.235,
        "material_cost_base": 1000000,
        "multiplier": 1.0,
        "total": 235000
      }
    }
  },
  "floor_plan": "data:image/png;base64,...",
  "metadata": {...}
}
```

## Frontend Validation Checklist

- [ ] Input form has contractor margin toggle (default ON)
- [ ] Input form has permit fee field (default ₹40,000)
- [ ] BOQ table shows Quantity, Unit, Rate, Total Cost columns
- [ ] Cost breakdown shows Material, Labor, GST, Permit, Contingency, Contractor Margin
- [ ] "Additional Costs" section visible when hidden_costs present
- [ ] Subtotal shows sum of all components
- [ ] Final total includes contractor margin
- [ ] Floor plan shows room dimensions labeled inside rooms
- [ ] Bathroom cost minimum enforced (≥₹35,000)

## Labor Cost Verification

### Example Calculation (Standard Quality):
- Material Cost: ₹800,000
- Labor %: 23.5%
- Expected Labor: 800,000 × 0.235 = ₹188,000
- GST (18%): 800,000 × 0.18 = ₹144,000
- Permit Fee: ₹40,000
- Contingency (10% of material+labor+gst): (800,000 + 188,000 + 144,000) × 0.10 = ₹113,200
- Contractor Margin (12% of material+labor+gst): (800,000 + 188,000 + 144,000) × 0.12 = ₹135,840
- Subtotal: 800,000 + 188,000 + 144,000 + 40,000 + 113,200 = ₹1,285,200
- Final Total: 1,285,200 + 135,840 = ₹1,421,040

## Notes

1. **Labor now percentage-based** (not sqft-based)
2. **Bathroom minimum enforced** in CPWD rates (min ₹35,000)
3. **Contractor margin toggleable** via API & UI
4. **Permit fee editable** (default ₹40,000)
5. **Floor plan prompt enhanced** with dimension calculations
6. **No breaking changes** to existing logic

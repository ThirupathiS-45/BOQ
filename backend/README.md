# BOQ Prediction API

A production-ready FastAPI backend for Bill of Quantities (BOQ) prediction with CPWD-based dynamic cost estimation.

## 🎯 Features

- **Natural Language Processing**: Convert descriptions like "2 floor house with 3 bedrooms" to structured JSON
- **ML-Based BOQ Prediction**: Use trained XGBoost model to predict material quantities
- **CPWD Dynamic Costing**: Calculate costs based on quality tiers and location multipliers
- **RESTful API**: Clean, well-documented endpoints with Pydantic validation
- **Error Handling**: Comprehensive error handling with graceful fallbacks
- **Scalable Architecture**: Modular design for easy extension

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI application
├── utils/
│   ├── __init__.py
│   ├── nlp_parser.py         # OpenRouter NLP integration
│   ├── feature_engineering.py # ML feature preparation
│   ├── cpwd_rates.py         # CPWD rate tables
│   └── cost_calculator.py    # Cost computation
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Setup

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### 3. Run Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 4. API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 📚 API Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "operational",
  "model_loaded": true,
  "api_key_configured": true
}
```

### POST /predict
Predict BOQ and costs from natural language input.

**Request:**
```json
{
  "query": "2 floor house with 3 bedrooms in 1200 sqft",
  "quality": 1,
  "location": "tier2",
  "use_nlp": true
}
```

**Response:**
```json
{
  "success": true,
  "input": {
    "area_sqft": 1200,
    "floors": 2,
    "bedrooms": 3,
    "bathrooms": 2,
    "kitchen": 1,
    "hall": 1,
    "dining": 1,
    "balcony": 1,
    "portico": 0,
    "quality": 1
  },
  "boq": {
    "cement_bags": 245.5,
    "steel_kg": 312.0,
    "sand_cft": 450.0,
    "aggregate_cft": 380.0,
    "bricks": 12500.0,
    "tiles_sqft": 900.0,
    "paint_liters": 85.0,
    "putty_kg": 120.0,
    "wiring_meters": 150.0,
    "switches": 25.0,
    "lights": 30.0,
    "pipes_meters": 200.0,
    "bathroom_sets": 2.0
  },
  "cost": {
    "material_cost": 1250000.0,
    "labor_cost": 300000.0,
    "total_cost": 1550000.0,
    "cost_per_sqft": 1291.67,
    "breakdown": {
      "materials": { /* detailed material breakdown */ },
      "labor": { /* labor cost details */ }
    }
  },
  "metadata": {
    "quality": "standard",
    "location": "tier2",
    "parser": "nlp"
  }
}
```

### POST /predict-with-input
Predict BOQ and costs from pre-structured input.

**Request:**
```json
{
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
  "location": "tier2"
}
```

**Response:** Same as /predict

## ⚙️ Configuration

### Quality Tiers

- **0 (Budget)**: Lower material rates, ₹150/sqft labor
- **1 (Standard)**: Mid-range rates, ₹250/sqft labor
- **2 (Premium)**: Higher material rates, ₹400/sqft labor

### Location Multipliers

- **metro**: 1.25× (25% premium)
- **tier1**: 1.15× (15% premium)
- **tier2**: 1.0× (standard)
- **tier3**: 0.85× (15% discount)
- **rural**: 0.75× (25% discount)

### CPWD Rate Table

Material rates are dynamically calculated based on quality tier and location. Examples:

| Material | Budget | Standard | Premium |
|----------|--------|----------|---------|
| Cement (bags) | ₹380 | ₹415 | ₹450 |
| Steel (kg) | ₹65 | ₹72.5 | ₹80 |
| Bricks (nos) | ₹8 | ₹10 | ₹12 |
| Tiles (sqft) | ₹60 | ₹90 | ₹120 |

## 🔧 Environment Variables

```env
# OpenRouter API
OPENROUTER_API_KEY=your_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Application Defaults
LOCATION_TIER=tier2
QUALITY_DEFAULT=standard
```

## 🎓 NLP Parsing

The system uses OpenRouter API with Mistral-7B model to parse natural language descriptions.

**Fallback Support**: If OpenRouter API is unavailable or NLP fails, the system uses regex-based fallback parsing.

**NLP Input Example:**
- "2 floor house with 3 bedrooms in 1200 sqft"
- "Premium apartment, 4 bedrooms, 2500 sq ft"
- "Budget home, 1200 sqft, 2 floors"

**Output Format:**
```json
{
  "area_sqft": 1200,
  "floors": 2,
  "bedrooms": 3,
  "bathrooms": 2,
  "kitchen": 1,
  "hall": 1,
  "dining": 1,
  "balcony": 1,
  "portico": 0,
  "quality": 1
}
```

## 🧠 Feature Engineering

The ML model uses the following features:

**Base Features:**
- area_sqft, floors, bedrooms, bathrooms
- kitchen, hall, dining, balcony, portico, quality

**Derived Features:**
- total_built_up = area_sqft × floors
- bedrooms_per_floor = bedrooms / floors
- bath_per_bedroom = bathrooms / bedrooms
- area_sq = (area_sqft²) / 1e6
- floors_x_bedrooms = floors × bedrooms
- floors_x_bath = floors × bathrooms
- total_rooms = bedrooms + kitchen + hall + dining
- rooms_density = total_rooms / area_sqft

## 💰 Cost Calculation

### Material Cost
```
Material Cost = Σ(quantity × CPWD_rate)
```

Where CPWD_rate varies by:
- Material type
- Quality tier
- Location multiplier

### Labor Cost
```
Labor Cost = area_sqft × labor_rate_per_sqft × labor_multiplier
```

### Total Cost
```
Total Cost = Material Cost + Labor Cost
```

## 🔒 Error Handling

The API provides descriptive error messages:

```json
{
  "success": false,
  "error": "Failed to parse query",
  "detail": "Missing area information in description"
}
```

## 📊 Logging

Logs are printed to console with the following format:
```
2024-04-03 14:30:45,123 - backend.main - INFO - Prediction completed: query='2 floor house...' | cost=₹1550000
```

## 🧪 Testing

### Manual Test with cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"query":"2 floor house with 3 bedrooms in 1200 sqft"}'
```

### Python Client Example

```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "query": "2 floor house with 3 bedrooms in 1200 sqft",
    "quality": 1,
    "location": "tier2"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Total Cost: ₹{result['cost']['total_cost']:,.2f}")
```

## 🚀 Deployment

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV OPENROUTER_API_KEY=your_key
ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["python", "backend/main.py"]
```

Build and run:
```bash
docker build -t boq-api .
docker run -p 8000:8000 \
  -e OPENROUTER_API_KEY=your_key \
  boq-api
```

### Production Server

Use Gunicorn + Uvicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
```

## 📈 Performance Tips

1. **Caching**: Cache NLP responses for repeated queries
2. **Async**: API uses async/await for concurrent requests
3. **Batch Processing**: Consider batch prediction endpoint for multiple queries
4. **Connection Pooling**: httpx automatically manages connection pools

## 🔄 Future Enhancements

- [ ] Real CPWD SOR API integration
- [ ] Batch prediction endpoint
- [ ] Cache layer for NLP responses
- [ ] Database for prediction history
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## 📝 License

MIT License

## 🤝 Support

For issues or questions, please refer to the documentation or check logs for detailed error messages.

# 🏗️ BOQ - Intelligent Bill of Quantities Prediction System

**An AI-powered, full-stack platform that transforms natural language building descriptions into accurate Bills of Quantities with intelligent cost estimation.**

[![React](https://img.shields.io/badge/React-18.2-blue?logo=react)](https://react.dev)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)](https://xgboost.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 Overview

BOQ is an intelligent system that bridges the gap between architectural descriptions and construction cost estimation. Using advanced NLP and machine learning, it automatically:

- **Parse natural language** descriptions of buildings (e.g., "2 floor house with 3 bedrooms in 1200 sqft")
- **Predict material quantities** using a trained XGBoost model
- **Calculate accurate costs** based on CPWD (Central Public Works Department) rates
- **Generate floor plans** visually representing the specifications
- **Provide cost breakdowns** by material category and construction tier

### Key Use Cases
- 📋 **Construction Estimation**: Generate quick BOQ estimates for new projects
- 🏢 **Architectural Planning**: Convert descriptions to structured specifications
- 💰 **Cost Analysis**: Compare budget vs. standard vs. premium quality tiers
- 📊 **Project Planning**: Visualize building layouts and cost distributions

---

## ✨ Features

### Backend (Python/FastAPI)
- **NLP Parser**: Converts natural language to structured building parameters using OpenRouter API
- **ML Prediction**: XGBoost-based multi-output regressor predicting material quantities
- **Dynamic Costing**: CPWD rate tables with location and quality multipliers
- **RESTful API**: Production-ready endpoints with comprehensive error handling
- **Interactive Docs**: Swagger UI at `/docs` for API exploration
- **Health Checks**: System status monitoring

### Frontend (React/TypeScript)
- **Modern UI**: Built with React 18 and Tailwind CSS
- **Form Input**: Intuitive interface for building specifications
- **Floor Plan Visualization**: Interactive floor plan generation
- **Data Tables**: Detailed BOQ and cost breakdown tables
- **Responsive Design**: Mobile-friendly interface
- **Real-time Feedback**: Loading states and error handling

### Machine Learning
- **Trained Model**: XGBoost multi-output regression on construction data
- **Feature Engineering**: Intelligent feature extraction from building parameters
- **Multi-target Prediction**: Simultaneous prediction of 16+ material quantities

---

## 🏗️ Architecture

```
BOQ/
├── backend/                          # FastAPI Python backend
│   ├── main.py                      # API server & endpoints
│   ├── utils/
│   │   ├── nlp_parser.py           # NLP → structured data
│   │   ├── feature_engineering.py  # ML feature preparation
│   │   ├── cost_calculator.py      # Cost computation
│   │   ├── cpwd_rates.py           # Rate tables & multipliers
│   │   └── floor_plan.py           # Floor plan generation
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment template
│   └── README.md                   # Backend documentation
│
├── frontend/                         # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx                 # Root component
│   │   ├── pages/
│   │   │   ├── HomePage.tsx        # Landing page
│   │   │   └── Dashboard.tsx       # Main application
│   │   ├── components/             # Reusable UI components
│   │   ├── services/api.ts         # API client
│   │   ├── context/AppContext.tsx  # State management
│   │   └── types/index.ts          # TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── model/                           # ML model artifacts
│   └── boq_model_v3.pkl           # Trained XGBoost model
│
├── train_model.py                  # Model training script
├── predict.py                      # Local prediction utility
├── dataset_generator.py            # Synthetic data generation
├── boq_dataset_v3.csv             # Training dataset
├── viewer.html                     # Standalone floor plan viewer
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+ and npm
- Git

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   export OPENROUTER_API_KEY="your-key-here"
   ```

4. **Start the API server**
   ```bash
   python main.py
   # or
   ./start.sh
   ```
   
   The API will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:3000`

4. **Build for production**
   ```bash
   npm run build
   npm run preview
   ```

---

## 📚 API Documentation

### Health Check
```bash
GET /health
```

**Response:**
```json
{
  "status": "operational",
  "model_loaded": true,
  "api_key_configured": true
}
```

### Predict BOQ & Costs
```bash
POST /predict
```

**Request:**
```json
{
  "query": "2 floor house with 3 bedrooms in 1200 sqft",
  "quality": 1,
  "location": "tier2",
  "use_nlp": true
}
```

**Parameters:**
- `query` (string, required): Natural language building description
- `quality` (integer, optional): 0=budget, 1=standard, 2=premium. Default: 1
- `location` (string, optional): tier1, tier2, tier3 (for cost multipliers). Default: tier2
- `use_nlp` (boolean, optional): Use NLP parsing or direct JSON. Default: true

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
  "predictions": {
    "cement": 45.2,
    "brick": 892.5,
    "steel": 18.3,
    "sand": 89.2,
    "gravel": 56.1,
    "concrete": 102.3
  },
  "costs": {
    "total_cost": 1245678,
    "cost_per_sqft": 1038.07,
    "breakdown_by_material": {
      "cement": 56234,
      "brick": 267450,
      "steel": 234567,
      ...
    }
  },
  "floor_plan": {
    "image_base64": "...",
    "dimensions": {...}
  }
}
```

### Generate Floor Plan
```bash
POST /generate-floor-plan
```

**Request:**
```json
{
  "area_sqft": 1200,
  "floors": 2,
  "bedrooms": 3,
  "bathrooms": 2
}
```

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_image",
  "prompt": "2-story residential building with..."
}
```

### Batch Predictions
```bash
POST /predict-batch
```

Process multiple predictions in one request for bulk analysis.

---

## 🤖 Machine Learning

### Model Architecture
- **Algorithm**: XGBoost Multi-Output Regression
- **Targets**: 16+ material quantities (cement, brick, steel, sand, concrete, etc.)
- **Features**: 12+ engineered features from building parameters

### Training Data
- **Dataset**: `boq_dataset_v3.csv` with 1000+ synthetic samples
- **Features**: area_sqft, floors, bedrooms, bathrooms, kitchen, hall, dining, balcony, portico, quality
- **Performance**: R² score ~0.89, MAE optimized for practical use

### Training

```bash
python train_model.py
```

This will:
1. Load and preprocess the dataset
2. Engineer features
3. Train the XGBoost model
4. Save the model to `model/boq_model_v3.pkl`
5. Display performance metrics

### Local Predictions

```bash
python predict.py
```

Edit the `input_data` dictionary in the script to test locally.

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_api_key_here

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Rate Configuration
LOCATION_TIER=tier2
QUALITY_DEFAULT=1
```

### CPWD Rate Adjustments

Edit `backend/utils/cpwd_rates.py` to adjust:
- Material rates per unit
- Quality multipliers (budget, standard, premium)
- Location-based cost multipliers

---

## 📊 Data Flow

```
User Input (Natural Language)
         ↓
    NLP Parser (OpenRouter)
         ↓
Structured Building Parameters
         ↓
Feature Engineering
         ↓
XGBoost Model
         ↓
Material Quantity Predictions
         ↓
Cost Calculator (CPWD Rates)
         ↓
Cost Breakdown & BOQ Table
         ↓
Floor Plan Generator
         ↓
JSON Response → Frontend Display
```

---

## 🎨 Frontend Components

- **Header**: Navigation and branding
- **HomePage**: Landing page with features overview
- **Dashboard**: Main application interface
- **InputForm**: Building specification input
- **BOQTable**: Material quantities and costs display
- **CostBreakdown**: Visual cost analysis
- **ImageViewer**: Floor plan visualization
- **LoadingSpinner**: Loading state indicator
- **Alert**: Error and success notifications

---

## 🧪 Testing

### Backend Testing

```bash
cd backend
python test_client.py
```

### API Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "query": "2 floor house with 3 bedrooms",
    "quality": 1,
    "location": "tier2"
  }'
```

### Frontend Testing

```bash
cd frontend
npm run build  # Check for build errors
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port Already in Use**
```bash
# Change port in main.py or use
python main.py --port 8001
```

**API Key Not Configured**
- Ensure `OPENROUTER_API_KEY` is set in `.env`
- Verify the key is valid and has sufficient credits

**Model Not Found**
```bash
python train_model.py  # Retrain the model
```

### Frontend Issues

**Vite Dev Server Not Starting**
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**API Connection Failed**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Verify firewall allows local connections

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| API Response Time | <200ms |
| NLP Processing | 1-3 seconds |
| Model Prediction | <50ms |
| Floor Plan Generation | 2-5 seconds |
| Frontend Build Time | ~10 seconds |

---

## 🚀 Deployment

### Docker Deployment

```bash
# Build Docker image
docker build -t boq-app .

# Run container
docker run -p 8000:8000 -p 3000:3000 -e OPENROUTER_API_KEY=xxx boq-app
```

### Production Deployment

1. **Backend**: Deploy FastAPI with Gunicorn/Uvicorn on cloud (AWS, GCP, Azure)
2. **Frontend**: Build and deploy to CDN (Vercel, Netlify, CloudFront)
3. **Database**: Optional PostgreSQL for persistence
4. **Caching**: Redis for rate limiting and caching

---

## 📝 Project Structure Details

### Backend Utils

- **nlp_parser.py**: OpenRouter integration with fallback parsing
- **feature_engineering.py**: Feature scaling and engineering
- **cost_calculator.py**: CPWD-based cost computation with multipliers
- **cpwd_rates.py**: Centralized rate tables and multiplier logic
- **floor_plan.py**: Floor plan image generation and prompting

### Frontend Services

- **api.ts**: Axios-based API client with error handling and request timeout

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues, questions, or feature requests, please open an issue on GitHub or contact the development team.

---

## 🔮 Future Enhancements

- [ ] Database integration for project history
- [ ] User authentication and project management
- [ ] Advanced floor plan editor
- [ ] 3D building visualization
- [ ] Bulk BOQ generation
- [ ] Integration with construction procurement systems
- [ ] Mobile app (React Native)
- [ ] Multi-language support

---

## 📞 Quick Links

- [Backend Documentation](backend/README.md)
- [Frontend Status](FRONTEND_STATUS.md)
- [API Documentation](http://localhost:8000/docs)
- [OpenRouter API](https://openrouter.ai)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [React Docs](https://react.dev)

---

**Built with ❤️ for construction professionals and architects**

*Last Updated: 2026-04-07*

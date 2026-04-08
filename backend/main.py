"""
FastAPI backend for BOQ prediction system.
Production-ready API with NLP parsing, ML prediction, and CPWD-based costing.
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.utils.nlp_parser import NLPParser, FallbackParser
from backend.utils.feature_engineering import FeatureEngineer
from backend.utils.cpwd_rates import parse_quality
from backend.utils.cost_calculator import CostCalculator
from backend.utils.floor_plan import generate_floor_plan, create_floor_plan_prompt


# =========================================
# LOGGING CONFIGURATION
# =========================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# =========================================
# PYDANTIC MODELS
# =========================================
class PredictRequest(BaseModel):
    """Request model for prediction endpoint."""
    query: str = Field(..., description="Natural language description of the structure")
    quality: Optional[int] = Field(default=1, description="0=budget, 1=standard, 2=premium")
    location: Optional[str] = Field(default="tier2", description="Location tier for cost adjustment")
    use_nlp: Optional[bool] = Field(default=True, description="Use NLP parsing if available")
    contractor_margin: Optional[bool] = Field(default=True, description="Include contractor margin (12%)")


class BOQItem(BaseModel):
    """BOQ item with quantity and cost."""
    quantity: float
    unit: str
    rate: float
    cost: float


class CostBreakdown(BaseModel):
    """Cost breakdown details."""
    material_cost: float
    labor_cost: float
    total_cost: float
    cost_per_sqft: float


class PredictResponse(BaseModel):
    """Response model for prediction endpoint."""
    success: bool
    input: Dict[str, Any]
    boq: Dict[str, float]
    cost: Dict[str, Any]
    floor_plan: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    api_key_configured: bool


# =========================================
# FASTAPI APP SETUP
# =========================================
app = FastAPI(
    title="BOQ Prediction API",
    description="Production-ready API for Bill of Quantities prediction with CPWD costing",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# GLOBAL STATE
# =========================================
class AppState:
    """Application state management."""
    model = None
    model_features = None
    model_targets = None
    nlp_parser = None
    feature_engineer = None
    
    @classmethod
    def initialize(cls):
        """Initialize application state."""
        logger.info("Initializing application state...")
        
        # Load ML model
        cls.load_model()
        
        # Initialize NLP parser
        cls.setup_nlp_parser()
        
        # Initialize feature engineer
        cls.feature_engineer = FeatureEngineer()
        
        logger.info("✅ Application initialized successfully")
    
    @classmethod
    def load_model(cls):
        """Load the trained ML model."""
        try:
            model_path = Path(__file__).parent.parent / "model" / "boq_model_v3.pkl"
            
            if not model_path.exists():
                logger.error(f"Model file not found: {model_path}")
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            bundle = joblib.load(model_path)
            cls.model = bundle.get("model")
            cls.model_features = bundle.get("features", [])
            cls.model_targets = bundle.get("targets", [])
            cls.target_scalers = bundle.get("target_scalers", {})  # Load scalers
            
            logger.info(f"✅ Model loaded successfully")
            logger.info(f"   Features: {len(cls.model_features)}")
            logger.info(f"   Targets: {len(cls.model_targets)}")
            logger.info(f"   Scalers: {len(cls.target_scalers)}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    @classmethod
    def setup_nlp_parser(cls):
        """Initialize NLP parser."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
            cls.nlp_parser = NLPParser(api_key=api_key)
            logger.info("✅ NLP parser initialized with OpenRouter API")
        else:
            logger.warning("⚠️  OPENROUTER_API_KEY not set. Fallback parser will be used.")
            cls.nlp_parser = None


# =========================================
# HELPER FUNCTIONS
# =========================================
def parse_query_to_input(
    query: str,
    use_nlp: bool = True,
) -> tuple[bool, Dict[str, Any], Optional[str]]:
    """
    Parse natural language query to structured input.
    
    Args:
        query: Natural language description
        use_nlp: Whether to use NLP (fallback if False or if NLP fails)
        
    Returns:
        Tuple of (success, parsed_data, error_message)
    """
    try:
        if use_nlp and AppState.nlp_parser:
            logger.info(f"Parsing query with NLP: {query[:50]}...")
            success, parsed_data, error = AppState.nlp_parser.parse(query)
            
            if success:
                return True, parsed_data, None
            else:
                logger.warning(f"NLP parsing failed: {error}. Using fallback...")
        
        # Use fallback parser
        logger.info(f"Using fallback parser for: {query[:50]}...")
        fallback_data = FallbackParser.parse(query)
        return True, fallback_data, None
        
    except Exception as e:
        logger.error(f"Query parsing error: {str(e)}")
        return False, {}, str(e)


def predict_boq(input_data: Dict[str, Any]) -> tuple[bool, Dict[str, float], Optional[str]]:
    """
    Use ML model to predict BOQ quantities.
    
    Args:
        input_data: Structured input with all required fields
        
    Returns:
        Tuple of (success, boq_dict, error_message)
    """
    try:
        import numpy as np
        
        # Prepare features for model
        df = FeatureEngineer.prepare_for_model(input_data, AppState.model_features)
        
        logger.info(f"Input features for model: {df.to_dict('records')[0]}")
        
        # Make prediction (in scaled space)
        prediction = AppState.model.predict(df)[0]
        
        logger.info(f"Raw model predictions (scaled): {prediction}")
        
        # Inverse scale predictions using saved scalers
        if AppState.target_scalers:
            prediction_unscaled = []
            for i, target in enumerate(AppState.model_targets):
                if target in AppState.target_scalers:
                    scaler = AppState.target_scalers[target]
                    # Clip scaled prediction to [0, 1]
                    scaled_val = np.clip(prediction[i], 0, 1)
                    # Inverse transform
                    unscaled = scaler.inverse_transform([[scaled_val]])[0][0]
                    prediction_unscaled.append(max(0, unscaled))  # Ensure non-negative
                else:
                    prediction_unscaled.append(max(0, prediction[i]))
            prediction = np.array(prediction_unscaled)
            logger.info(f"Model predictions (unscaled): {prediction}")
        
        # Create BOQ dictionary
        boq = dict(zip(AppState.model_targets, prediction))
        
        logger.info(f"BOQ before cleanup: {boq}")
        
        # Ensure non-negative values and round to whole numbers
        boq = {k: int(round(max(0, v))) for k, v in boq.items()}
        
        # Remove labor_cost from BOQ (it's handled separately in costing)
        boq.pop("labor_cost", None)
        
        logger.info(f"BOQ after cleanup: {boq}")
        logger.info(f"BOQ prediction successful: {len(boq)} items")
        return True, boq, None
        
    except Exception as e:
        logger.error(f"BOQ prediction error: {str(e)}")
        return False, {}, str(e)


def calculate_costs(
    boq: Dict[str, float],
    area_sqft: float,
    quality: str,
    location: str,
    contractor_margin: bool = True,
) -> tuple[bool, Dict[str, Any], Optional[str]]:
    """
    Calculate costs using CPWD rates with hidden costs.
    
    Args:
        boq: Bill of Quantities
        area_sqft: Built-up area
        quality: Quality tier
        location: Location tier
        contractor_margin: Include contractor margin
        
    Returns:
        Tuple of (success, cost_dict, error_message)
    """
    try:
        calculator = CostCalculator(
            quality=quality,
            location=location,
            contractor_margin=contractor_margin,
        )
        
        cost_data = calculator.calculate(boq, area_sqft)
        
        logger.info(f"Cost calculation successful: ₹{cost_data['total_cost']:,.2f}")
        return True, cost_data, None
        
    except Exception as e:
        logger.error(f"Cost calculation error: {str(e)}")
        return False, {}, str(e)


# =========================================
# API ENDPOINTS
# =========================================
@app.on_event("startup")
async def startup_event():
    """Initialize app on startup."""
    try:
        AppState.initialize()
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="operational" if AppState.model else "degraded",
        model_loaded=AppState.model is not None,
        api_key_configured=bool(os.getenv("OPENROUTER_API_KEY")),
    )


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest, background_tasks: BackgroundTasks):
    """
    Predict BOQ and costs from natural language input.
    
    Args:
        request: PredictRequest with query and options
        background_tasks: Background task manager for logging
        
    Returns:
        PredictResponse with predictions, costs, and floor plan
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Parse query to structured input
    parse_success, parsed_input, parse_error = parse_query_to_input(
        request.query,
        use_nlp=request.use_nlp,
    )
    
    if not parse_success:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse query: {parse_error}",
        )
    
    # Add quality if not in parsed input
    if "quality" not in parsed_input:
        parsed_input["quality"] = request.quality
    
    # Predict BOQ
    boq_success, boq, boq_error = predict_boq(parsed_input)
    
    if not boq_success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to predict BOQ: {boq_error}",
        )
    
    # Calculate costs
    quality_str = parse_quality(request.quality)
    cost_success, cost_data, cost_error = calculate_costs(
        boq,
        parsed_input.get("area_sqft", 1000),
        quality_str,
        request.location,
        request.contractor_margin,
    )
    
    if not cost_success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate costs: {cost_error}",
        )
    
    # Generate floor plan
    floor_plan_prompt = create_floor_plan_prompt(parsed_input)
    fp_success, floor_plan_url, fp_error = generate_floor_plan(floor_plan_prompt)
    
    if not fp_success:
        logger.warning(f"Floor plan generation failed: {fp_error}")
        floor_plan_url = None
    
    # Log prediction for analytics
    background_tasks.add_task(
        logger.info,
        f"Prediction completed: query='{request.query[:50]}...' | "
        f"cost=₹{cost_data['total_cost']:,.0f} | "
        f"floor_plan={'✓' if floor_plan_url else '✗'}"
    )
    
    return PredictResponse(
        success=True,
        input=parsed_input,
        boq=boq,
        cost=cost_data,
        floor_plan=floor_plan_url,
        metadata={
            "quality": quality_str,
            "location": request.location,
            "parser": "nlp" if request.use_nlp and AppState.nlp_parser else "fallback",
        },
    )


@app.post("/predict-with-input")
async def predict_with_input(input_data: Dict[str, Any]):
    """
    Predict BOQ and costs from pre-structured input.
    
    Useful for programmatic clients that already have structured data.
    
    Args:
        input_data: Dictionary with area_sqft, floors, bedrooms, etc.
        
    Returns:
        PredictResponse with predictions
    """
    # Extract quality and location
    quality = parse_quality(input_data.get("quality", 1))
    location = input_data.get("location", "tier2")
    
    # Predict BOQ
    boq_success, boq, boq_error = predict_boq(input_data)
    
    if not boq_success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to predict BOQ: {boq_error}",
        )
    
    # Calculate costs
    cost_success, cost_data, cost_error = calculate_costs(
        boq,
        input_data.get("area_sqft", 1000),
        quality,
        location,
    )
    
    if not cost_success:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate costs: {cost_error}",
        )
    
    return PredictResponse(
        success=True,
        input=input_data,
        boq=boq,
        cost=cost_data,
        metadata={
            "quality": quality,
            "location": location,
            "parser": "direct",
        },
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "BOQ Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "predict_with_input": "/predict-with-input (POST)",
            "docs": "/docs",
        },
        "status": "operational" if AppState.model else "model_not_loaded",
    }


# =========================================
# EXCEPTION HANDLERS
# =========================================
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") else "An error occurred",
        },
    )


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting BOQ API on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )

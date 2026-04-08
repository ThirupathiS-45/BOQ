export interface FloorPlanRequest {
  query: string
  quality?: number  // 0=budget, 1=standard, 2=premium
  location?: string // tier1, tier2, tier3, metro
  contractor_margin?: boolean // Include contractor margin
}

export interface BOQItem {
  [key: string]: number | string
}

export interface MaterialBreakdown {
  quantity: number
  unit: string
  rate: number
  cost: number
}

export interface HiddenCosts {
  gst: number
  contingency: number
  contractor_margin: number
  subtotal: number
}

export interface CostBreakdown {
  material_cost: number
  labor_cost: number
  total_cost: number
  cost_per_sqft: number
  hidden_costs?: HiddenCosts
  breakdown?: {
    materials?: {
      [key: string]: MaterialBreakdown
    }
    labor?: {
      rate_per_sqft: number
      area_sqft: number
      multiplier: number
      total: number
    }
  }
}

export interface Metadata {
  parser?: string
  quality?: string
  location?: string
}

export interface FloorPlanResponse {
  success: boolean
  floor_plan: string // Base64 data URL
  boq: BOQItem
  cost: CostBreakdown
  metadata: Metadata
}

export interface AppContextType {
  floorPlan: FloorPlanResponse | null
  loading: boolean
  error: string | null
  setFloorPlan: (data: FloorPlanResponse) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  resetState: () => void
}

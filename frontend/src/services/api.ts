import axios, { AxiosInstance, AxiosError } from 'axios'
import type { FloorPlanRequest, FloorPlanResponse } from '@/types'

declare global {
  interface ImportMeta {
    env: Record<string, string>
  }
}

class APIClient {
  private client: AxiosInstance
  private baseURL: string

  constructor() {
    this.baseURL = (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000'
    
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 120000, // 2 minutes for AI generation
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.message)
        return Promise.reject(error)
      }
    )
  }

  async generateFloorPlan(request: FloorPlanRequest): Promise<FloorPlanResponse> {
    try {
      // Map UI values to backend format
      const qualityMap: Record<string | number, number> = { budget: 0, standard: 1, premium: 2, low: 0, medium: 1, high: 2 }
      const locationMap: Record<string, string> = { default: 'tier2', urban: 'metro', suburban: 'tier2', commercial: 'tier1' }
      
      const quality = typeof request.quality === 'number' ? request.quality : qualityMap[request.quality || 'standard'] ?? 1
      const location = locationMap[request.location || 'default'] ?? 'tier2'
      
      const response = await this.client.post<FloorPlanResponse>('/predict', {
        query: request.query,
        quality: quality,
        location: location,
        use_nlp: true,  // Enable NLP parser to test new model
      })

      if (!response.data.success) {
        throw new Error('Generation failed: ' + (response.data as any).message || 'Unknown error')
      }

      return response.data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          throw new Error('Request timeout. The AI model is taking longer than expected.')
        }
        if (error.response?.status === 404) {
          throw new Error('API endpoint not found. Check backend connection.')
        }
        if (error.response?.status === 500) {
          throw new Error('Server error. Please try again later.')
        }
        throw new Error(error.response?.data?.message || error.message)
      }
      throw error
    }
  }

  getBaseURL(): string {
    return this.baseURL
  }
}

export const apiClient = new APIClient()

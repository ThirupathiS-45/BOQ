import { useCallback } from 'react'
import { useAppStore } from '@/context/AppContext'
import { apiClient } from '@/services/api'
import type { FloorPlanRequest } from '@/types'

export const useGenerateFloorPlan = () => {
  const { setFloorPlan, setLoading, setError, addToHistory } = useAppStore()

  const generate = useCallback(
    async (request: FloorPlanRequest) => {
      try {
        setLoading(true)
        setError(null)

        const response = await apiClient.generateFloorPlan(request)
        setFloorPlan(response)
        addToHistory(response)

        return response
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to generate floor plan'
        setError(errorMessage)
        throw err
      } finally {
        setLoading(false)
      }
    },
    [setFloorPlan, setLoading, setError, addToHistory]
  )

  return { generate }
}

export const useFloorPlan = () => {
  const { floorPlan, loading, error, resetState } = useAppStore()
  return { floorPlan, loading, error, resetState }
}

import { createContext, useContext, type ReactNode } from 'react'
import { create } from 'zustand'
import type { FloorPlanResponse } from '@/types'

interface AppStore {
  floorPlan: FloorPlanResponse | null
  loading: boolean
  error: string | null
  history: FloorPlanResponse[]
  setFloorPlan: (data: FloorPlanResponse) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  addToHistory: (data: FloorPlanResponse) => void
  clearHistory: () => void
  resetState: () => void
}

export const useAppStore = create<AppStore>((set) => ({
  floorPlan: null,
  loading: false,
  error: null,
  history: [],
  
  setFloorPlan: (data) => set({ floorPlan: data }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  addToHistory: (data) => set((state) => ({
    history: [data, ...state.history].slice(0, 10), // Keep last 10
  })),
  clearHistory: () => set({ history: [] }),
  resetState: () => set({
    floorPlan: null,
    loading: false,
    error: null,
  }),
}))

// Legacy context for compatibility
const AppContext = createContext<AppStore | null>(null)

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const store = useAppStore()
  return <AppContext.Provider value={store}>{children}</AppContext.Provider>
}

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    return useAppStore()
  }
  return context
}

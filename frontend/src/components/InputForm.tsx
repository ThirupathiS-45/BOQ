import React, { useState } from 'react'
import { Button } from './Button'
import { Alert } from './Alert'
import type { FloorPlanRequest } from '@/types'

interface InputFormProps {
  onSubmit: (data: FloorPlanRequest) => Promise<void>
  isLoading: boolean
}

export const InputForm: React.FC<InputFormProps> = ({ onSubmit, isLoading }): JSX.Element => {
  const [formData, setFormData] = useState<FloorPlanRequest>({
    query: '',
    quality: 1,  // 0=budget, 1=standard, 2=premium
    location: 'default',
  })
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!formData.query.trim()) {
      setError('Please describe the floor plan requirements')
      return
    }

    try {
      await onSubmit(formData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate floor plan')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
      <h2 className="text-2xl font-bold mb-6 text-slate-900">Generate Floor Plan</h2>

      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      <div className="space-y-4">
        {/* Query Input */}
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-slate-700 mb-2">
            Project Description <span className="text-red-500">*</span>
          </label>
          <textarea
            id="query"
            name="query"
            value={formData.query}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                query: e.target.value,
              }))
            }
            placeholder="e.g., 2 BHK apartment, modern design with open kitchen, north-facing"
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            rows={4}
            disabled={isLoading}
          />
          <p className="text-xs text-slate-500 mt-1">Describe your floor plan requirements in detail</p>
        </div>

        {/* Quality Select */}
        <div>
          <label htmlFor="quality" className="block text-sm font-medium text-slate-700 mb-2">
            Quality Level
          </label>
          <select
            id="quality"
            name="quality"
            value={formData.quality}
            onChange={(e) => setFormData((prev) => ({ ...prev, quality: parseInt(e.target.value) }))}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="0">Low (Budget)</option>
            <option value="1">Medium (Standard)</option>
            <option value="2">High (Premium)</option>
          </select>
        </div>

        {/* Location Select */}
        <div>
          <label htmlFor="location" className="block text-sm font-medium text-slate-700 mb-2">
            Location
          </label>
          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="default">Default</option>
            <option value="urban">Urban</option>
            <option value="suburban">Suburban</option>
            <option value="commercial">Commercial</option>
          </select>
        </div>

        {/* Submit Button */}
        <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full">
          Generate Floor Plan & Estimate
        </Button>
      </div>
    </form>
  )
}

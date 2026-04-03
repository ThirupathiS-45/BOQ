import React, { useState } from 'react'
import { Sparkles } from 'lucide-react'
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
    <form onSubmit={handleSubmit} className="bg-gradient-to-br from-white to-blue-50 p-8 rounded-xl shadow-lg border border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
          <Sparkles size={24} className="text-white" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">Generate Floor Plan</h2>
      </div>

      {error && <Alert type="error" message={error} onClose={() => setError(null)} />}

      <div className="space-y-6">
        {/* Query Input */}
        <div>
          <label htmlFor="query" className="block text-sm font-semibold text-slate-700 mb-3">
            Project Description <span className="text-red-500 font-bold">*</span>
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
            placeholder="e.g., A luxurious 2 BHK apartment with 1200 sq ft, modern open kitchen, spacious living room, north-facing with natural light..."
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none bg-white hover:border-blue-300 transition-colors"
            rows={5}
            disabled={isLoading}
          />
          <p className="text-xs text-slate-500 mt-2">💡 Provide detailed specifications for better results</p>
        </div>

        {/* Quality Select */}
        <div>
          <label htmlFor="quality" className="block text-sm font-semibold text-slate-700 mb-3">
            Quality Level
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[
              { value: 0, label: 'Budget', desc: 'Cost-effective' },
              { value: 1, label: 'Standard', desc: 'Recommended' },
              { value: 2, label: 'Premium', desc: 'Luxury' },
            ].map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setFormData((prev) => ({ ...prev, quality: option.value }))}
                disabled={isLoading}
                className={`p-3 rounded-lg border-2 transition-all ${
                  formData.quality === option.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-slate-200 bg-white hover:border-blue-300'
                }`}
              >
                <div className="font-semibold text-slate-900">{option.label}</div>
                <div className="text-xs text-slate-500">{option.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Location Select */}
        <div>
          <label htmlFor="location" className="block text-sm font-semibold text-slate-700 mb-3">
            Location Type
          </label>
          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white hover:border-blue-300 transition-colors font-medium"
            disabled={isLoading}
          >
            <option value="default">Default Rates</option>
            <option value="urban">Urban Area</option>
            <option value="suburban">Suburban Area</option>
            <option value="commercial">Commercial Zone</option>
          </select>
        </div>

        {/* Submit Button */}
        <Button 
          type="submit" 
          disabled={isLoading}
          className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/30 transition-all duration-300 disabled:opacity-50"
        >
          {isLoading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Generating...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <Sparkles size={18} />
              Generate Floor Plan & Estimate
            </span>
          )}
        </Button>
      </div>
    </form>
  )
}

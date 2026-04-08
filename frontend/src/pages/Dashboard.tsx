import { FC } from 'react'
import { InputForm } from '@/components/InputForm'
import { ImageViewer } from '@/components/ImageViewer'
import { BOQTable } from '@/components/BOQTable'
import { CostBreakdown } from '@/components/CostBreakdown'
import { LoadingSpinner } from '@/components/LoadingSpinner'
import { Alert } from '@/components/Alert'
import { useGenerateFloorPlan, useFloorPlan } from '@/hooks/useFloorPlan'
import type { FloorPlanRequest } from '@/types'

export const Dashboard: FC = (): JSX.Element => {
  const { generate } = useGenerateFloorPlan()
  const { floorPlan, loading, error, resetState } = useFloorPlan()

  const handleGenerate = async (request: FloorPlanRequest) => {
    await generate(request)
  }

  return (
    <div className="space-y-8">
      {/* Error Alert */}
      {error && (
        <Alert
          type="error"
          message={error}
          onClose={() => {
            resetState()
          }}
        />
      )}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Column - Form */}
        <div>
          <InputForm onSubmit={handleGenerate} isLoading={loading} />
        </div>

        {/* Right Column - Results */}
        <div>
          {loading ? (
            <div className="bg-gradient-to-br from-white to-blue-50 p-6 rounded-xl shadow-lg border border-blue-100">
              <LoadingSpinner />
            </div>
          ) : floorPlan ? (
            <ImageViewer imageUrl={floorPlan.floor_plan} />
          ) : (
            <div className="bg-gradient-to-br from-white to-blue-50 p-12 rounded-xl shadow-lg border border-blue-100 text-center">
              <div className="space-y-3">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-slate-600 font-medium">Your floor plan will appear here</p>
                <p className="text-slate-500 text-sm">Describe your project and click "Generate" to get started</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Full Width Results */}
      {floorPlan && (
        <>
          {/* BOQ and Cost Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <BOQTable data={floorPlan.boq} cost={floorPlan.cost} />
            <CostBreakdown cost={floorPlan.cost} />
          </div>

          {/* Metadata */}
          {floorPlan.metadata && (
            <div className="bg-gradient-to-br from-white to-blue-50 p-6 rounded-xl shadow-lg border border-blue-100">
              <h3 className="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2">
                <span className="w-1 h-6 bg-gradient-to-b from-blue-500 to-cyan-500 rounded"></span>
                Generation Details
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-4 rounded-lg border border-blue-100">
                  <p className="text-xs text-slate-600 font-semibold uppercase tracking-wide">Parser Method</p>
                  <p className="text-base font-bold text-slate-900 mt-2">{floorPlan.metadata.parser || 'N/A'}</p>
                </div>
                <div className="bg-gradient-to-br from-cyan-50 to-blue-50 p-4 rounded-lg border border-cyan-100">
                  <p className="text-xs text-slate-600 font-semibold uppercase tracking-wide">Quality Tier</p>
                  <p className="text-base font-bold text-slate-900 mt-2">{floorPlan.metadata.quality || 'Standard'}</p>
                </div>
                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 p-4 rounded-lg border border-blue-100">
                  <p className="text-xs text-slate-600 font-semibold uppercase tracking-wide">Location</p>
                  <p className="text-base font-bold text-slate-900 mt-2">{floorPlan.metadata.location || 'N/A'}</p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

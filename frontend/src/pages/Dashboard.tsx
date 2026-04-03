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
            <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
              <LoadingSpinner />
            </div>
          ) : floorPlan ? (
            <ImageViewer imageUrl={floorPlan.floor_plan} />
          ) : (
            <div className="bg-white p-12 rounded-lg shadow-sm border border-slate-200 text-center">
              <p className="text-slate-500">Your floor plan will appear here</p>
            </div>
          )}
        </div>
      </div>

      {/* Full Width Results */}
      {floorPlan && (
        <>
          {/* BOQ and Cost Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <BOQTable data={floorPlan.boq} />
            <CostBreakdown cost={floorPlan.cost} />
          </div>

          {/* Metadata */}
          {floorPlan.metadata && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
              <h3 className="text-lg font-bold text-slate-900 mb-4">Generation Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-sm text-slate-500 font-medium">Parser Method</p>
                  <p className="text-base font-semibold text-slate-900">{floorPlan.metadata.parser || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Quality Tier</p>
                  <p className="text-base font-semibold text-slate-900">{floorPlan.metadata.quality || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500 font-medium">Location</p>
                  <p className="text-base font-semibold text-slate-900">{floorPlan.metadata.location || 'N/A'}</p>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}

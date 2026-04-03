import React from 'react'
import type { CostBreakdown as CostBreakdownData } from '@/types'

interface CostBreakdownProps {
  cost: CostBreakdownData
  currency?: string
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({ cost, currency = '₹' }): JSX.Element => {
  const formatCurrency = (amount: number) => {
    return `${currency} ${amount.toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
      <h3 className="text-xl font-bold text-slate-900 mb-6">Cost Breakdown</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Material Cost */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-700 font-medium mb-1">Material Cost</p>
          <p className="text-2xl font-bold text-blue-900">{formatCurrency(cost.material_cost)}</p>
        </div>

        {/* Labor Cost */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
          <p className="text-sm text-green-700 font-medium mb-1">Labor Cost</p>
          <p className="text-2xl font-bold text-green-900">{formatCurrency(cost.labor_cost)}</p>
        </div>

        {/* Cost per Sqft */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
          <p className="text-sm text-purple-700 font-medium mb-1">Cost per Sqft</p>
          <p className="text-2xl font-bold text-purple-900">{formatCurrency(cost.cost_per_sqft)}</p>
        </div>

        {/* Total Cost */}
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 p-4 rounded-lg border border-amber-300">
          <p className="text-sm text-amber-700 font-medium mb-1">Total Cost</p>
          <p className="text-2xl font-bold text-amber-900">{formatCurrency(cost.total_cost)}</p>
        </div>
      </div>

      {/* Summary */}
      <div className="mt-6 pt-6 border-t border-slate-200">
        <div className="flex items-center justify-between text-lg">
          <span className="font-semibold text-slate-900">Project Total:</span>
          <span className="text-2xl font-bold text-blue-600">{formatCurrency(cost.total_cost)}</span>
        </div>
      </div>
    </div>
  )
}

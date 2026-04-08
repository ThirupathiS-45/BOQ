import React from 'react'
import { TrendingUp, DollarSign } from 'lucide-react'
import type { CostBreakdown as CostBreakdownData } from '@/types'

interface CostBreakdownProps {
  cost: CostBreakdownData
  currency?: string
}

export const CostBreakdown: React.FC<CostBreakdownProps> = ({ cost, currency = '₹' }): JSX.Element => {
  const formatCurrency = (amount: number) => {
    return `${currency} ${amount.toLocaleString('en-IN', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    })}`
  }

  const formatCurrencyDetailed = (amount: number) => {
    const inLakhs = amount / 100000
    if (inLakhs >= 1) {
      return `${currency} ${inLakhs.toFixed(2)} L`
    }
    return formatCurrency(amount)
  }

  return (
    <div className="bg-gradient-to-br from-white to-blue-50 p-6 rounded-xl shadow-lg border border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
          <TrendingUp size={24} className="text-white" />
        </div>
        <h3 className="text-xl font-bold text-slate-900">Cost Breakdown & Estimates</h3>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
        {/* Material Cost */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-5 rounded-xl border border-blue-400/30 text-white shadow-lg hover:shadow-xl transition-shadow">
          <p className="text-sm text-blue-100 font-semibold mb-2">Material Cost</p>
          <p className="text-3xl font-bold">{formatCurrencyDetailed(cost.material_cost)}</p>
          <p className="text-xs text-blue-200 mt-1">Raw materials & supplies</p>
        </div>

        {/* Labor Cost */}
        <div className="bg-gradient-to-br from-cyan-500 to-cyan-600 p-5 rounded-xl border border-cyan-400/30 text-white shadow-lg hover:shadow-xl transition-shadow">
          <p className="text-sm text-cyan-100 font-semibold mb-2">Labor Cost</p>
          <p className="text-3xl font-bold">{formatCurrencyDetailed(cost.labor_cost)}</p>
          <p className="text-xs text-cyan-200 mt-1">Professional workforce</p>
        </div>

        {/* Cost per Sqft */}
        <div className="bg-gradient-to-br from-indigo-500 to-indigo-600 p-5 rounded-xl border border-indigo-400/30 text-white shadow-lg hover:shadow-xl transition-shadow">
          <p className="text-sm text-indigo-100 font-semibold mb-2">Cost per Sqft</p>
          <p className="text-3xl font-bold">{formatCurrency(cost.cost_per_sqft)}</p>
          <p className="text-xs text-indigo-200 mt-1">Unit rate</p>
        </div>

        {/* Total Cost - Highlighted */}
        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 p-5 rounded-xl border border-emerald-400/30 text-white shadow-lg hover:shadow-xl transition-shadow">
          <p className="text-sm text-emerald-100 font-semibold mb-2">Project Total</p>
          <p className="text-3xl font-bold">{formatCurrencyDetailed(cost.total_cost)}</p>
          <p className="text-xs text-emerald-200 mt-1">Complete estimate</p>
        </div>
      </div>

      {/* Summary Bar */}
      <div className="bg-gradient-to-r from-slate-900 to-blue-900 rounded-xl p-6 text-white border border-blue-500/20">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-white/10 rounded-lg flex items-center justify-center border border-white/20">
              <DollarSign size={24} className="text-white" />
            </div>
            <div>
              <p className="text-sm text-blue-200 font-semibold">Total Project Investment</p>
              <p className="text-lg text-white/80">All inclusive estimate for your building</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-4xl font-bold">{formatCurrencyDetailed(cost.total_cost)}</p>
          </div>
        </div>
      </div>

      {/* Cost Distribution */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="text-sm font-semibold text-slate-900 mb-3">Cost Distribution</h4>
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-700">Materials</span>
            <div className="flex items-center gap-2">
              <div className="w-24 h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-500 rounded-full"
                  style={{
                    width: `${(cost.material_cost / cost.total_cost) * 100}%`,
                  }}
                />
              </div>
              <span className="text-slate-600 font-semibold w-12 text-right">
                {Math.round((cost.material_cost / cost.total_cost) * 100)}%
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-700">Labor</span>
            <div className="flex items-center gap-2">
              <div className="w-24 h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-cyan-500 rounded-full"
                  style={{
                    width: `${(cost.labor_cost / cost.total_cost) * 100}%`,
                  }}
                />
              </div>
              <span className="text-slate-600 font-semibold w-12 text-right">
                {Math.round((cost.labor_cost / cost.total_cost) * 100)}%
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Costs Section */}
      {cost.hidden_costs && (
        <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <h4 className="text-sm font-semibold text-slate-900 mb-3 flex items-center gap-2">
            <span className="text-amber-600">⚠️</span> Additional Costs
          </h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-700">GST (18% on materials)</span>
              <span className="text-slate-900 font-semibold">
                ₹ {formatCurrency(cost.hidden_costs.gst)}
              </span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-700">Contingency (10%)</span>
              <span className="text-slate-900 font-semibold">
                ₹ {formatCurrency(cost.hidden_costs.contingency)}
              </span>
            </div>
            {cost.hidden_costs.contractor_margin > 0 && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-700">Contractor Margin (12%)</span>
                <span className="text-slate-900 font-semibold">
                  ₹ {formatCurrency(cost.hidden_costs.contractor_margin)}
                </span>
              </div>
            )}
            <div className="border-t border-amber-300 pt-2 mt-2 flex items-center justify-between text-sm">
              <span className="text-slate-700 font-semibold">Subtotal</span>
              <span className="text-slate-900 font-bold">
                ₹ {formatCurrency(cost.hidden_costs.subtotal)}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}


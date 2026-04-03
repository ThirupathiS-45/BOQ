import React from 'react'
import { Package } from 'lucide-react'
import type { BOQItem } from '@/types'

interface BOQTableProps {
  data: BOQItem
}

export const BOQTable: React.FC<BOQTableProps> = ({ data }): JSX.Element => {
  const items = Object.entries(data).map(([key, value]) => ({
    item: key,
    quantity: value,
  }))

  return (
    <div className="bg-gradient-to-br from-white to-blue-50 p-6 rounded-xl shadow-lg border border-blue-100">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
          <Package size={24} className="text-white" />
        </div>
        <h3 className="text-xl font-bold text-slate-900">Bill of Quantities</h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-blue-200 bg-gradient-to-r from-blue-50 to-cyan-50">
              <th className="text-left px-4 py-4 font-semibold text-slate-800">Material Item</th>
              <th className="text-right px-4 py-4 font-semibold text-slate-800">Quantity</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => (
              <tr
                key={idx}
                className={`border-b border-blue-100 transition-colors hover:bg-blue-50 ${
                  idx % 2 === 0 ? 'bg-white' : 'bg-blue-50/40'
                }`}
              >
                <td className="px-4 py-4 text-slate-900 font-medium capitalize">
                  {item.item.replace(/_/g, ' ')}
                </td>
                <td className="px-4 py-4 text-right text-slate-700 font-bold text-blue-600">
                  {typeof item.quantity === 'number' ? item.quantity.toFixed(2) : item.quantity}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {items.length === 0 && (
        <div className="text-center py-12">
          <Package size={48} className="mx-auto text-slate-300 mb-3" />
          <p className="text-slate-500 font-medium">No items in BOQ</p>
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-slate-600">
          <span className="font-semibold">Total Items:</span> {items.length} material categories
        </p>
      </div>
    </div>
  )
}


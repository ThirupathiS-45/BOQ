import React from 'react'
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
    <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
      <h3 className="text-xl font-bold text-slate-900 mb-4">Bill of Quantities</h3>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-slate-200 bg-slate-50">
              <th className="text-left px-4 py-3 font-semibold text-slate-700">Item</th>
              <th className="text-right px-4 py-3 font-semibold text-slate-700">Quantity</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, idx) => (
              <tr
                key={idx}
                className={`border-b border-slate-100 ${idx % 2 === 0 ? 'bg-slate-50' : 'bg-white'} hover:bg-blue-50 transition-colors`}
              >
                <td className="px-4 py-3 text-slate-900">{item.item}</td>
                <td className="px-4 py-3 text-right text-slate-700 font-medium">
                  {typeof item.quantity === 'number' ? item.quantity.toFixed(2) : item.quantity}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {items.length === 0 && (
        <p className="text-center text-slate-500 py-8">No items in BOQ</p>
      )}
    </div>
  )
}

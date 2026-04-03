import React from 'react'

export const LoadingSpinner: React.FC = (): JSX.Element => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-slate-200"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 border-r-blue-600 animate-spin"></div>
      </div>
      <p className="mt-4 text-slate-600 font-medium text-center">
        Generating floor plan and estimates...
        <br />
        <span className="text-sm text-slate-500">This may take a few moments</span>
      </p>
    </div>
  )
}

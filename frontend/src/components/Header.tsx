import React from 'react'

export const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">BOQ Generator</h1>
            <p className="text-blue-100 text-sm mt-1">AI-Powered Floor Plan & Cost Estimation</p>
          </div>
          <div className="hidden md:block text-right">
            <p className="text-blue-100 text-sm">Generate detailed floor plans and estimates instantly</p>
          </div>
        </div>
      </div>
    </header>
  )
}

import React from 'react'
import { ArrowLeft, Home } from 'lucide-react'

interface HeaderProps {
  onBackToHome?: () => void
}

export const Header: React.FC<HeaderProps> = ({ onBackToHome }) => {
  return (
    <header className="sticky top-0 z-50 bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 text-white shadow-2xl border-b border-blue-500/20 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {onBackToHome && (
              <button
                onClick={onBackToHome}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition-all duration-300 text-blue-200 hover:text-white"
              >
                <ArrowLeft size={18} />
                <span className="hidden sm:inline text-sm font-medium">Home</span>
              </button>
            )}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center">
                <Home size={22} className="text-white" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-black bg-gradient-to-r from-emerald-400 to-cyan-300 bg-clip-text text-transparent">
                  ArchAI
                </h1>
                <p className="text-blue-200 text-xs sm:text-sm mt-0.5">Smart Design & Estimation</p>
              </div>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-4 text-right">
            <div>
              <p className="text-blue-100 text-sm font-semibold">Professional Design Tools</p>
              <p className="text-blue-300 text-xs">Instant generation in seconds</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

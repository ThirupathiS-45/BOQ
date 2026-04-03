import React from 'react'

interface LayoutProps {
  children: React.ReactNode
  header?: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children, header }) => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {header}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
      <footer className="bg-slate-900 text-slate-400 text-center py-4 text-sm mt-12">
        <p>© 2024 BOQ Generator. Powered by AI</p>
      </footer>
    </div>
  )
}

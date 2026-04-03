import React from 'react'

interface LayoutProps {
  children: React.ReactNode
  header?: React.ReactNode
}

export const Layout: React.FC<LayoutProps> = ({ children, header }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-slate-50 flex flex-col">
      {header}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
      <footer className="bg-gradient-to-r from-slate-900 to-blue-900 text-slate-300 py-8 mt-16 border-t border-blue-500/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <h4 className="font-semibold text-white mb-2">Product</h4>
              <ul className="space-y-1 text-sm">
                <li><a href="#" className="hover:text-white transition">Features</a></li>
                <li><a href="#" className="hover:text-white transition">Pricing</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Support</h4>
              <ul className="space-y-1 text-sm">
                <li><a href="#" className="hover:text-white transition">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-2">Legal</h4>
              <ul className="space-y-1 text-sm">
                <li><a href="#" className="hover:text-white transition">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition">Terms</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-blue-500/20 pt-8 text-center text-sm">
            <p>© 2024 BOQ Generator. Transforming Building Design with AI.</p>
            <p className="text-slate-500 mt-2">Advanced floor planning and cost estimation technology</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

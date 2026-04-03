import React, { useState } from 'react'
import { AppProvider } from '@/context/AppContext'
import { Layout } from '@/components/Layout'
import { Header } from '@/components/Header'
import { Dashboard } from '@/pages/Dashboard'
import { HomePage } from '@/pages/HomePage'

type Page = 'home' | 'app'

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>('home')

  const handleGetStarted = () => {
    setCurrentPage('app')
  }

  const handleBackToHome = () => {
    setCurrentPage('home')
  }

  return (
    <AppProvider>
      {currentPage === 'home' ? (
        <HomePage onGetStarted={handleGetStarted} />
      ) : (
        <Layout header={<Header onBackToHome={handleBackToHome} />}>
          <Dashboard />
        </Layout>
      )}
    </AppProvider>
  )
}

export default App

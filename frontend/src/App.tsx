import React from 'react'
import { AppProvider } from '@/context/AppContext'
import { Layout } from '@/components/Layout'
import { Header } from '@/components/Header'
import { Dashboard } from '@/pages/Dashboard'

const App: React.FC = () => {
  return (
    <AppProvider>
      <Layout header={<Header />}>
        <Dashboard />
      </Layout>
    </AppProvider>
  )
}

export default App

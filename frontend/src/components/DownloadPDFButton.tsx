import React, { useState } from 'react'
import { Download, Loader } from 'lucide-react'
import { apiClient } from '@/services/api'
import type { FloorPlanResponse } from '@/types'

interface DownloadPDFButtonProps {
  floorPlan: FloorPlanResponse
  projectDescription?: string
  isLoading?: boolean
}

export const DownloadPDFButton: React.FC<DownloadPDFButtonProps> = ({
  floorPlan,
  projectDescription = 'Building Project Report',
  isLoading = false,
}): JSX.Element => {
  const [loading, setLoading] = useState(false)

  const handleDownloadPDF = async () => {
    if (!floorPlan) return

    try {
      setLoading(true)

      // Prepare PDF export data
      const pdfRequest = {
        project_description: projectDescription,
        floor_plan: floorPlan.floor_plan,
        boq: floorPlan.boq,
        cost: floorPlan.cost,
        metadata: floorPlan.metadata,
      }

      // Request PDF from backend
      const pdfBlob = await apiClient.downloadPDF(pdfRequest)

      // Create download link and trigger download
      const url = URL.createObjectURL(pdfBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `boq_report_${new Date().getTime()}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('PDF download error:', error)
      alert('Failed to download PDF. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <button
      onClick={handleDownloadPDF}
      disabled={loading || isLoading}
      className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 disabled:cursor-not-allowed"
      title="Download as PDF including floor plan"
    >
      {loading || isLoading ? (
        <>
          <Loader size={20} className="animate-spin" />
          <span>Generating PDF...</span>
        </>
      ) : (
        <>
          <Download size={20} />
          <span>Download PDF</span>
        </>
      )}
    </button>
  )
}

import React, { useState } from 'react'
import { Download, ZoomIn, Eye } from 'lucide-react'
import { Button } from './Button'

interface ImageViewerProps {
  imageUrl: string
  fileName?: string
}

export const ImageViewer: React.FC<ImageViewerProps> = ({ imageUrl, fileName = 'floor_plan' }) => {
  const [isFullScreen, setIsFullScreen] = useState(false)

  const handleDownload = async () => {
    try {
      const link = document.createElement('a')
      link.href = imageUrl
      link.download = `${fileName}.png`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (err) {
      console.error('Download failed:', err)
    }
  }

  return (
    <>
      <div className="bg-gradient-to-br from-white to-blue-50 p-6 rounded-xl shadow-lg border border-blue-100">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
              <Eye size={24} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Generated Floor Plan</h3>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsFullScreen(true)}
              className="p-2 hover:bg-blue-100 rounded-lg transition-colors text-slate-600 hover:text-blue-600"
              title="Expand view"
            >
              <ZoomIn size={20} />
            </button>
            <Button 
              onClick={handleDownload}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg hover:shadow-lg transition-all"
            >
              <Download size={18} />
              <span className="hidden sm:inline">Download</span>
            </Button>
          </div>
        </div>

        <div className="bg-gradient-to-br from-slate-100 to-slate-50 rounded-xl p-4 flex items-center justify-center min-h-96 border border-blue-100">
          <div className="relative">
            <img
              src={imageUrl}
              alt="Generated floor plan"
              className="max-w-full max-h-96 rounded-lg object-contain shadow-lg cursor-pointer hover:shadow-xl transition-shadow"
              onClick={() => setIsFullScreen(true)}
            />
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg flex items-start gap-3">
          <div className="flex-shrink-0 mt-0.5">
            <svg className="h-5 w-5 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zm-11-1a1 1 0 11-2 0 1 1 0 012 0z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-900">Floor Plan Generated Successfully</h4>
            <p className="text-sm text-slate-600 mt-1">Your floor plan has been generated based on the specifications provided. Download the image or view it in full screen mode.</p>
          </div>
        </div>
      </div>

      {/* Full Screen Modal */}
      {isFullScreen && (
        <div className="fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4">
          <div className="relative max-w-5xl max-h-[90vh] w-full">
            <button
              onClick={() => setIsFullScreen(false)}
              className="absolute top-4 right-4 bg-white/10 hover:bg-white/20 text-white p-2 rounded-lg transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <img
              src={imageUrl}
              alt="Floor plan full screen"
              className="w-full h-full object-contain rounded-lg"
            />
          </div>
        </div>
      )}
    </>
  )
}


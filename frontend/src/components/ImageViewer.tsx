import React from 'react'
import { Button } from './Button'

interface ImageViewerProps {
  imageUrl: string
  fileName?: string
}

export const ImageViewer: React.FC<ImageViewerProps> = ({ imageUrl, fileName = 'floor_plan' }) => {
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
    <div className="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-slate-900">Floor Plan</h3>
        <Button variant="secondary" size="sm" onClick={handleDownload}>
          ↓ Download
        </Button>
      </div>

      <div className="bg-slate-50 rounded-lg p-4 flex items-center justify-center min-h-96">
        <img src={imageUrl} alt="Generated floor plan" className="max-w-full max-h-96 rounded-lg object-contain" />
      </div>
    </div>
  )
}

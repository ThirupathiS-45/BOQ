import React, { ReactNode } from 'react'

interface AlertProps {
  type: 'success' | 'error' | 'warning' | 'info'
  message: string | ReactNode
  onClose?: () => void
}

const typeClasses = {
  success: 'bg-green-50 border-green-200 text-green-800',
  error: 'bg-red-50 border-red-200 text-red-800',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
  info: 'bg-blue-50 border-blue-200 text-blue-800',
}

const iconClasses = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ',
}

export const Alert: React.FC<AlertProps> = ({ type, message, onClose }): JSX.Element => {
  return (
    <div className={`border-l-4 p-4 rounded mb-4 ${typeClasses[type]} flex items-start justify-between`}>
      <div className="flex items-start gap-3">
        <span className={`text-lg font-bold flex-shrink-0`}>{iconClasses[type]}</span>
        <p className="text-sm leading-relaxed">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-lg opacity-50 hover:opacity-100 transition-opacity flex-shrink-0 ml-4"
        >
          ×
        </button>
      )}
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useDocumentStore } from '../lib/store/documentStore'
import { useThemeStore } from '../lib/store/themeStore'
import { documentApi } from '../lib/api/documentApi'
import './Sidebar.css'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

export const Sidebar = ({ isOpen, onToggle }: SidebarProps) => {
  const { content, documentId, lastSavedAt } = useDocumentStore()
  const { isDarkMode, fontSize, showLineNumbers, toggleTheme, setFontSize, toggleLineNumbers } = useThemeStore()
  const [isSharing, setIsSharing] = useState(false)
  const [fontSizeInput, setFontSizeInput] = useState(fontSize.toString())

  useEffect(() => {
    setFontSizeInput(fontSize.toString())
  }, [fontSize])

  const handleShare = async () => {
    if (!content.trim()) {
      alert('Please add some content before sharing')
      return
    }

    setIsSharing(true)

    try {
      if (documentId) {
        // Document already exists, copy URL to clipboard
        const url = `${window.location.origin}/edit/${documentId}`
        await navigator.clipboard.writeText(url)
        alert('Document link copied to clipboard!')
      } else {
        // Create new document
        const response = await documentApi.createDocument(content)
        const url = `${window.location.origin}/edit/${response.share_id}`
        
        // Update URL
        window.history.replaceState(null, '', `/edit/${response.share_id}`)
        
        // Copy to clipboard
        await navigator.clipboard.writeText(url)
        alert('Document created and link copied to clipboard!')
      }
    } catch (error: any) {
      console.error('Failed to share document:', error)
      
      let errorMessage = 'Failed to share document. Please try again.'
      
      if (error.response) {
        const status = error.response.status
        const statusText = error.response.statusText
        
        if (status === 404) {
          errorMessage = 'Document not found. It may have been deleted.'
        } else if (status === 400) {
          errorMessage = 'Invalid document data. Please check your content.'
        } else if (status === 500) {
          errorMessage = 'Server error. Please try again later.'
        } else {
          errorMessage = `Server error (${status}): ${statusText}`
        }
      } else if (error.request) {
        errorMessage = 'Network error. Please check your connection and try again.'
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timeout. Please try again.'
      } else if (error.name === 'NotAllowedError') {
        errorMessage = 'Clipboard access denied. Please copy the link manually.'
      } else {
        errorMessage = `Unexpected error: ${error.message || 'Unknown error'}`
      }
      
      alert(errorMessage)
    } finally {
      setIsSharing(false)
    }
  }

  const handleFontSizeChange = (value: string) => {
    setFontSizeInput(value)
    const numValue = parseInt(value, 10)
    if (!isNaN(numValue) && numValue >= 8 && numValue <= 32) {
      setFontSize(numValue)
    }
  }

  const formatLastSaved = (date: Date | null) => {
    if (!date) return 'Never'
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    
    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}h ago`
    const days = Math.floor(hours / 24)
    return `${days}d ago`
  }

  return (
    <>
      {/* Toggle Arrow Button */}
      <button 
        className={`sidebar-toggle ${isOpen ? 'open' : ''}`}
        onClick={onToggle}
        aria-label="Toggle sidebar"
      >
        <span className="arrow">›</span>
      </button>

      {/* Sidebar Content */}
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-content">
          <div className="sidebar-section">
            <h3>Settings</h3>
            <div className="font-size-control">
              <label htmlFor="font-size-input">Font Size (8-32px)</label>
              <input
                id="font-size-input"
                type="number"
                min="8"
                max="32"
                value={fontSizeInput}
                onChange={(e) => handleFontSizeChange(e.target.value)}
                className="font-size-input"
                placeholder="14"
              />
            </div>
            <div className="line-numbers-control">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={showLineNumbers}
                  onChange={toggleLineNumbers}
                  className="line-numbers-checkbox"
                />
                <span className="checkbox-text">Show Line Numbers</span>
              </label>
            </div>
          </div>
          
          <div className="sidebar-section">
            <h3>Theme</h3>
            <button 
              className="theme-toggle-button"
              onClick={toggleTheme}
              aria-label={`Switch to ${isDarkMode ? 'light' : 'dark'} mode`}
            >
              {isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
            </button>
          </div>
          
          <div className="sidebar-section">
            <h3>Share</h3>
            <button 
              className="share-button"
              onClick={handleShare}
              disabled={isSharing || !content.trim()}
            >
              {isSharing ? 'Sharing...' : (documentId ? 'Copy Link' : 'Save & Share')}
            </button>
          </div>
          
          <div className="sidebar-section">
            <h3>Last Saved</h3>
            <div className="last-saved">
              {formatLastSaved(lastSavedAt)}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

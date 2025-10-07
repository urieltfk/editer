import { useState } from 'react'
import { useDocumentStore } from '../lib/store/documentStore'
import { documentApi } from '../lib/api/documentApi'
import './Sidebar.css'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

export const Sidebar = ({ isOpen, onToggle }: SidebarProps) => {
  const { content, documentId, lastSavedAt } = useDocumentStore()
  const [isSharing, setIsSharing] = useState(false)

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
    } catch (error) {
      console.error('Failed to share document:', error)
      alert('Failed to share document. Please try again.')
    } finally {
      setIsSharing(false)
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
            <div className="placeholder">Settings placeholder</div>
          </div>
          
          <div className="sidebar-section">
            <h3>Night Mode</h3>
            <div className="placeholder">Night mode toggle placeholder</div>
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

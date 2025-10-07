import { useState, ChangeEvent } from 'react'
import { useParams } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { useDocumentStore } from '../lib/store/documentStore'
import { useAutosave } from '../lib/hooks/useAutosave'
import { useDocumentLoader } from '../lib/hooks/useDocumentLoader'
import './TextEditor.css'

export const TextEditor = () => {
  const { id: documentId } = useParams<{ id: string }>()
  const { content, setContent } = useDocumentStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { isSaving } = useAutosave()
  const { isLoading, error } = useDocumentLoader(documentId || null)

  const handleTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setContent(event.target.value)
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  if (error) {
    return (
      <div className="text-editor-container">
        <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
        <div className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
          <div className="error-message">
            <h2>Document not found</h2>
            <p>The document you're looking for doesn't exist or has been deleted.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="text-editor-container">
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
      
      <div className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
        {/* Gray vertical line separator */}
        <div className="page-edge-line"></div>
        
        <div className="text-editor-content">
          <textarea
            value={content}
            onChange={handleTextChange}
            placeholder={isLoading ? "Loading document..." : "Start typing here..."}
            className="text-editor-textarea"
            autoFocus
            disabled={isLoading}
          />
        </div>
        
        {/* Loading indicator */}
        {isSaving && (
          <div className="saving-indicator">
            💾 Saving...
          </div>
        )}
      </div>
    </div>
  )
}

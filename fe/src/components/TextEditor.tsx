import { useState, ChangeEvent, KeyboardEvent, useRef, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { useDocumentStore } from '../lib/store/documentStore'
import { useThemeStore } from '../lib/store/themeStore'
import { useAutosave } from '../lib/hooks/useAutosave'
import { useDocumentLoader } from '../lib/hooks/useDocumentLoader'
import './TextEditor.css'

export const TextEditor = () => {
  const { id: documentId } = useParams<{ id: string }>()
  const { content, setContent, storageError } = useDocumentStore()
  const { showLineNumbers } = useThemeStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { isSaving } = useAutosave()
  const { isLoading, error } = useDocumentLoader(documentId || null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const lineNumbersRef = useRef<HTMLDivElement>(null)

  const handleTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setContent(event.target.value)
  }

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Tab') {
      event.preventDefault()
      
      const textarea = textareaRef.current
      if (!textarea) return
      
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const spaces = '  ' // 2 spaces for tab
      
      const newContent = content.slice(0, start) + spaces + content.slice(end)
      setContent(newContent)
      
      // Update cursor position after the inserted spaces
      setTimeout(() => {
        const newCursorPos = start + spaces.length
        textarea.setSelectionRange(newCursorPos, newCursorPos)
      }, 0)
    }
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  // Generate line numbers
  const generateLineNumbers = () => {
    const lines = content.split('\n')
    return lines.map((_, index) => index + 1)
  }

  // Sync line numbers scroll with textarea scroll
  useEffect(() => {
    const textarea = textareaRef.current
    const lineNumbers = lineNumbersRef.current
    
    if (!textarea || !lineNumbers) return

    const syncScroll = () => {
      lineNumbers.scrollTop = textarea.scrollTop
    }

    textarea.addEventListener('scroll', syncScroll)
    return () => textarea.removeEventListener('scroll', syncScroll)
  }, [])

  if (error) {
    return (
      <div className="text-editor-container">
        <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
        <div className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
          <div className="error-message">
            <h2>Error Loading Document</h2>
            <p>{error}</p>
            <button 
              onClick={() => window.location.reload()} 
              style={{ marginTop: '10px', padding: '8px 16px' }}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (storageError) {
    return (
      <div className="text-editor-container">
        <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
        <div className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
          <div className="error-message">
            <h2>Storage Error</h2>
            <p>{storageError}</p>
            <p style={{ fontSize: '14px', color: '#666', marginTop: '10px' }}>
              Your content will be saved in memory but may be lost when you refresh the page.
            </p>
            <button 
              onClick={() => window.location.reload()} 
              style={{ marginTop: '10px', padding: '8px 16px' }}
            >
              Continue Anyway
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="text-editor-container">
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} />
      
      <div className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="text-editor-content">
          <div className={`line-numbers ${showLineNumbers ? 'with-numbers' : 'without-numbers'}`} ref={lineNumbersRef}>
            {showLineNumbers && generateLineNumbers().map((lineNumber) => (
              <div key={lineNumber} className="line-number">
                {lineNumber}
              </div>
            ))}
          </div>
          <textarea
            ref={textareaRef}
            value={content}
            onChange={handleTextChange}
            onKeyDown={handleKeyDown}
            placeholder={isLoading ? "Loading document..." : "Start typing here..."}
            className={`text-editor-textarea ${showLineNumbers ? 'with-line-numbers' : ''}`}
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

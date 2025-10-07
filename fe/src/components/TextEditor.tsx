import { useState, ChangeEvent } from 'react'
import { Sidebar } from './Sidebar'
import './TextEditor.css'

export const TextEditor = () => {
  const [content, setContent] = useState('')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const handleTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setContent(event.target.value)
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
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
            placeholder="Start typing here..."
            className="text-editor-textarea"
            autoFocus
          />
        </div>
      </div>
    </div>
  )
}

import { useState, ChangeEvent } from 'react'
import './TextEditor.css'

export const TextEditor = () => {
  const [content, setContent] = useState('')

  const handleTextChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setContent(event.target.value)
  }

  return (
    <div className="text-editor-container">
      <div className="text-editor-header">
        <h1>Editer</h1>
      </div>
      <div className="text-editor-content">
        <textarea
          value={content}
          onChange={handleTextChange}
          placeholder="Start typing your text here..."
          className="text-editor-textarea"
          autoFocus
        />
      </div>
    </div>
  )
}

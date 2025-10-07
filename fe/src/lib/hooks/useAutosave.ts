import { useEffect, useRef } from 'react'
import { useDocumentStore } from '../store/documentStore'
import { documentApi } from '../api/documentApi'

export const useAutosave = () => {
  const {
    content,
    lastSavedContent,
    isSaving,
    documentId,
    setLastSavedContent,
    setIsSaving,
    setDocumentId,
    setLastSavedAt
  } = useDocumentStore()

  const timeoutRef = useRef<NodeJS.Timeout | null>(null)

  const saveDocument = async (contentToSave: string) => {
    if (contentToSave === lastSavedContent || isSaving) {
      return
    }

    setIsSaving(true)

    try {
      if (documentId) {
        // Update existing document
        await documentApi.updateDocument(documentId, contentToSave)
      } else {
        // Create new document
        const response = await documentApi.createDocument(contentToSave)
        setDocumentId(response.share_id)
        // Update URL with new document ID
        window.history.replaceState(null, '', `/edit/${response.share_id}`)
      }

      setLastSavedContent(contentToSave)
      setLastSavedAt(new Date())
    } catch (error) {
      console.error('Failed to save document:', error)
      // TODO: Show user-friendly error message
      alert('Failed to save document. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  useEffect(() => {
    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }

    // Don't save if content hasn't changed
    if (content === lastSavedContent) {
      return
    }

    // Set new timeout for debounced save
    timeoutRef.current = setTimeout(() => {
      saveDocument(content)
    }, 700)

    // Cleanup timeout on unmount
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [content, lastSavedContent, isSaving, documentId])

  return {
    isSaving,
    lastSavedAt: useDocumentStore.getState().lastSavedAt
  }
}

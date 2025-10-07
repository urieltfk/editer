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
    } catch (error: any) {
      console.error('Failed to save document:', error)
      
      let errorMessage = 'Failed to save document. Please try again.'
      
      if (error.response) {
        // Server responded with error status
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
        // Network error
        errorMessage = 'Network error. Please check your connection and try again.'
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timeout. Please try again.'
      } else {
        errorMessage = `Unexpected error: ${error.message || 'Unknown error'}`
      }
      
      alert(errorMessage)
    } finally {
      setIsSaving(false)
    }
  }

  // Manual save function with debouncing
  const manualSave = async () => {
    if (content === lastSavedContent || isSaving) {
      return
    }

    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }

    // Set new timeout for debounced save
    timeoutRef.current = setTimeout(async () => {
      await saveDocument(content)
    }, 700)
  }

  // Auto save for existing documents
  useEffect(() => {
    // Only auto-save if we have an existing document ID
    if (!documentId) {
      return
    }

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
  }, [content, lastSavedContent, documentId])

  return {
    isSaving,
    lastSavedAt: useDocumentStore.getState().lastSavedAt,
    manualSave
  }
}

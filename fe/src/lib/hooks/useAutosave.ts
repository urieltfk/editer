import { useEffect, useRef } from 'react'
import { useDocumentStore } from '../store/documentStore'
import { documentApi } from '../api/documentApi'
import { useToast } from './useToast'

export const useAutosave = () => {
  const {
    content,
    isSaving,
    documentId,
    isTemporaryDocument,
    hasUnsavedChanges,
    setIsSaving,
    setDocumentId,
    setLastSavedAt,
    setHasUnsavedChanges
  } = useDocumentStore()

  const toast = useToast()
  const timeoutRef = useRef<number | null>(null)

  const saveDocument = async (contentToSave: string) => {
    if (isSaving) {
      return
    }

    setIsSaving(true)

    try {
      const loadingToastId = toast.loading('Saving...')
      if (documentId && !isTemporaryDocument) {
        await documentApi.updateDocument(documentId, contentToSave)
        setLastSavedAt(new Date())
        setHasUnsavedChanges(false)
      } else if (isTemporaryDocument) {
        setLastSavedAt(new Date())
        setHasUnsavedChanges(false)
      }
      toast.dismiss(loadingToastId)
      toast.success(`Saved ${isTemporaryDocument ? 'locally' : 'to cloud'}`)
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
      
      toast.error(errorMessage)
    } finally {
      setIsSaving(false)
    }
  }

  // Create online document from temporary document
  const createOnlineDocument = async () => {
    if (isSaving) {
      return
    }

    setIsSaving(true)

    try {
      const response = await documentApi.createDocument(content)
      setDocumentId(response.share_id)
      setLastSavedAt(new Date())
      setHasUnsavedChanges(false)
      // Update URL with new document ID
      window.history.replaceState(null, '', `/edit/${response.share_id}`)
    } catch (error: any) {
      console.error('Failed to create online document:', error)
      
      let errorMessage = 'Failed to create online document. Please try again.'
      
      if (error.response) {
        const status = error.response.status
        const statusText = error.response.statusText
        
        if (status === 400) {
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
    if (!hasUnsavedChanges || isSaving) {
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

  // Auto save for documents with changes
  useEffect(() => {
    // Only auto-save if there are unsaved changes
    if (!hasUnsavedChanges || isSaving) {
      return
    }

    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
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
  }, [content, hasUnsavedChanges, isSaving])

  return {
    isSaving,
    lastSavedAt: useDocumentStore.getState().lastSavedAt,
    hasUnsavedChanges,
    manualSave,
    createOnlineDocument
  }
}

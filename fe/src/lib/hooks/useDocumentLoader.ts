import { useEffect, useState } from 'react'
import { useDocumentStore } from '../store/documentStore'
import { documentApi } from '../api/documentApi'

export const useDocumentLoader = (documentId: string | null) => {
  const { loadSavedDocument, createTemporaryDocument, reset } = useDocumentStore()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadDocument = async () => {
      if (!documentId) {
        // No document ID, create a temporary document
        createTemporaryDocument()
        return
      }

      setIsLoading(true)
      setError(null)

      try {
        const response = await documentApi.getDocument(documentId)
        // Load saved document with proper state management
        loadSavedDocument(
          response.content,
          response.share_id,
          new Date(response.updated_at)
        )
      } catch (error: any) {
        console.error('Failed to load document:', error)
        
        let errorMessage = 'Failed to load document'
        
        if (error.response) {
          const status = error.response.status
          if (status === 404) {
            errorMessage = 'Document not found. It may have been deleted or the link is incorrect.'
          } else if (status === 400) {
            errorMessage = 'Invalid document ID. Please check the URL.'
          } else if (status === 500) {
            errorMessage = 'Server error while loading document. Please try again later.'
          } else {
            errorMessage = `Server error (${status}): ${error.response.statusText}`
          }
        } else if (error.request) {
          errorMessage = 'Network error. Please check your connection and try again.'
        } else if (error.code === 'ECONNABORTED') {
          errorMessage = 'Request timeout. Please try again.'
        } else {
          errorMessage = `Unexpected error: ${error.message || 'Unknown error'}`
        }
        
        setError(errorMessage)
        // Reset to temporary document on error
        createTemporaryDocument()
      } finally {
        setIsLoading(false)
      }
    }

    loadDocument()
  }, [documentId, loadSavedDocument, createTemporaryDocument])

  return { isLoading, error }
}

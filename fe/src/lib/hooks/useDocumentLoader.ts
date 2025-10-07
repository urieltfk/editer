import { useEffect, useState } from 'react'
import { useDocumentStore } from '../store/documentStore'
import { documentApi } from '../api/documentApi'

export const useDocumentLoader = (documentId: string | null) => {
  const { setContent, setLastSavedContent, setDocumentId, setLastSavedAt, reset } = useDocumentStore()
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadDocument = async () => {
      if (!documentId) {
        // No document ID, load from local storage (handled by Zustand persist)
        return
      }

      setIsLoading(true)
      setError(null)

      try {
        const response = await documentApi.getDocument(documentId)
        setContent(response.content)
        setLastSavedContent(response.content)
        setDocumentId(response.share_id)
        setLastSavedAt(new Date(response.updated_at))
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
        // Reset to local content on error
        reset()
      } finally {
        setIsLoading(false)
      }
    }

    loadDocument()
  }, [documentId, setContent, setLastSavedContent, setDocumentId, setLastSavedAt, reset])

  return { isLoading, error }
}

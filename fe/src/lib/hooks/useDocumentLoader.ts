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
        if (error.response?.status === 404) {
          setError('Document not found')
        } else {
          setError('Failed to load document')
        }
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

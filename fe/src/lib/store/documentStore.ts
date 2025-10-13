import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { createVersionedStorage, documentMigrations } from '../utils/storageVersion'

interface DocumentState {
  content: string
  lastSavedContent: string
  isSaving: boolean
  documentId: string | null
  lastSavedAt: Date | null
  storageError: string | null
  setContent: (content: string) => void
  setLastSavedContent: (content: string) => void
  setIsSaving: (isSaving: boolean) => void
  setDocumentId: (documentId: string | null) => void
  setLastSavedAt: (date: Date | null) => void
  setStorageError: (error: string | null) => void
  reset: () => void
}

// Safe storage wrapper to handle storage errors
const createSafeStorage = () => {
  try {
    // Test if storage is available
    const testKey = '__storage_test__'
    sessionStorage.setItem(testKey, 'test')
    sessionStorage.removeItem(testKey)
    return sessionStorage
  } catch (error) {
    console.warn('Session storage not available, using memory fallback:', error)
    return null
  }
}

// Create versioned storage for document store
const createVersionedDocumentStorage = () => {
  const baseStorage = createSafeStorage()
  if (!baseStorage) return undefined
  
  return createVersionedStorage('editer-document-storage', documentMigrations)
}

export const useDocumentStore = create<DocumentState>()(
  persist(
    (set) => ({
      content: '',
      lastSavedContent: '',
      isSaving: false,
      documentId: null,
      lastSavedAt: null,
      storageError: null,
      
      setContent: (content: string) => set({ content }),
      setLastSavedContent: (lastSavedContent: string) => set({ lastSavedContent }),
      setIsSaving: (isSaving: boolean) => set({ isSaving }),
      setDocumentId: (documentId: string | null) => set({ documentId }),
      setLastSavedAt: (lastSavedAt: Date | null) => set({ lastSavedAt }),
      setStorageError: (storageError: string | null) => set({ storageError }),
      
      reset: () => set({
        content: '',
        lastSavedContent: '',
        isSaving: false,
        documentId: null,
        lastSavedAt: null,
        storageError: null
      })
    }),
    {
      name: 'editer-document-storage',
      storage: createVersionedDocumentStorage(),
      partialize: (state) => ({
        content: state.content,
        lastSavedContent: state.lastSavedContent,
        documentId: state.documentId,
        lastSavedAt: state.lastSavedAt
      }),
      onRehydrateStorage: () => (state, error) => {
        if (error) {
          console.error('Failed to rehydrate storage:', error)
          state?.setStorageError(`Storage error: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }
    }
  )
)

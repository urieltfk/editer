import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface DocumentState {
  // Current document state
  content: string
  isSaving: boolean
  documentId: string | null
  lastSavedAt: Date | null
  storageError: string | null
  
  // Document type tracking
  isTemporaryDocument: boolean
  hasUnsavedChanges: boolean
  
  // Actions
  setContent: (content: string) => void
  setIsSaving: (isSaving: boolean) => void
  setDocumentId: (documentId: string | null) => void
  setLastSavedAt: (date: Date | null) => void
  setStorageError: (error: string | null) => void
  setTemporaryDocument: (isTemporary: boolean) => void
  setHasUnsavedChanges: (hasChanges: boolean) => void
  
  // Document management
  loadSavedDocument: (content: string, documentId: string, lastSavedAt: Date) => void
  createTemporaryDocument: () => void
  reset: () => void
  
  // Cross-tab synchronization
  syncFromStorage: (newContent: string, newHasUnsavedChanges: boolean) => void
}

export const useDocumentStore = create<DocumentState>()(
  persist(
    (set, get) => ({
      // Current document state
      content: '',
      isSaving: false,
      documentId: null,
      lastSavedAt: null,
      storageError: null,
      
      // Document type tracking
      isTemporaryDocument: true,
      hasUnsavedChanges: false,
      
      // Actions
      setContent: (content: string) => {
        const currentContent = get().content
        set({ 
          content,
          hasUnsavedChanges: content !== currentContent
        })
      },
      
      setIsSaving: (isSaving: boolean) => set({ isSaving }),
      setDocumentId: (documentId: string | null) => set({ documentId }),
      setLastSavedAt: (lastSavedAt: Date | null) => set({ lastSavedAt }),
      setStorageError: (storageError: string | null) => set({ storageError }),
      setTemporaryDocument: (isTemporary: boolean) => set({ isTemporaryDocument: isTemporary }),
      setHasUnsavedChanges: (hasChanges: boolean) => set({ hasUnsavedChanges: hasChanges }),
      
      // Document management
      loadSavedDocument: (content: string, documentId: string, lastSavedAt: Date) => {
        set({
          content,
          documentId,
          lastSavedAt,
          isTemporaryDocument: false,
          hasUnsavedChanges: false,
          storageError: null
        })
      },
      
      createTemporaryDocument: () => {
        set({
          content: '',
          documentId: null,
          lastSavedAt: null,
          isTemporaryDocument: true,
          hasUnsavedChanges: false,
          storageError: null
        })
      },
      
      reset: () => set({
        content: '',
        isSaving: false,
        documentId: null,
        lastSavedAt: null,
        storageError: null,
        isTemporaryDocument: true,
        hasUnsavedChanges: false
      }),
      
      // Cross-tab synchronization
      syncFromStorage: (newContent: string, newHasUnsavedChanges: boolean) => {
        const currentState = get()
        // Only sync if we're dealing with a temporary document
        if (currentState.isTemporaryDocument) {
          set({
            content: newContent,
            hasUnsavedChanges: newHasUnsavedChanges
          })
        }
      }
    }),
    {
      name: 'editer-document-storage',
      // Only persist temporary documents, not saved documents
      partialize: (state) => {
        // Only persist if it's a temporary document
        if (state.isTemporaryDocument) {
          return {
            content: state.content,
            isTemporaryDocument: state.isTemporaryDocument,
            hasUnsavedChanges: state.hasUnsavedChanges
          }
        }
        // Don't persist saved documents - they should be fetched from server
        return {}
      },
      onRehydrateStorage: () => (state, error) => {
        if (error) {
          console.error('Failed to rehydrate storage:', error)
          state?.setStorageError(`Storage error: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }
    }
  )
)

// Set up cross-tab synchronization for temporary documents
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (event) => {
    // Only handle changes to our document storage
    if (event.key === 'editer-document-storage' && event.newValue) {
      try {
        const newData = JSON.parse(event.newValue)
        const { state } = newData
        
        // Only sync if it's a temporary document with content
        if (state && state.isTemporaryDocument && state.content !== undefined) {
          useDocumentStore.getState().syncFromStorage(
            state.content,
            state.hasUnsavedChanges || false
          )
        }
      } catch (error) {
        console.warn('Failed to parse storage event data:', error)
      }
    }
  })
}

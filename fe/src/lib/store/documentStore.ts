import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface DocumentState {
  content: string
  lastSavedContent: string
  isSaving: boolean
  documentId: string | null
  lastSavedAt: Date | null
  setContent: (content: string) => void
  setLastSavedContent: (content: string) => void
  setIsSaving: (isSaving: boolean) => void
  setDocumentId: (documentId: string | null) => void
  setLastSavedAt: (date: Date | null) => void
  reset: () => void
}

export const useDocumentStore = create<DocumentState>()(
  persist(
    (set) => ({
      content: '',
      lastSavedContent: '',
      isSaving: false,
      documentId: null,
      lastSavedAt: null,
      
      setContent: (content: string) => set({ content }),
      setLastSavedContent: (lastSavedContent: string) => set({ lastSavedContent }),
      setIsSaving: (isSaving: boolean) => set({ isSaving }),
      setDocumentId: (documentId: string | null) => set({ documentId }),
      setLastSavedAt: (lastSavedAt: Date | null) => set({ lastSavedAt }),
      
      reset: () => set({
        content: '',
        lastSavedContent: '',
        isSaving: false,
        documentId: null,
        lastSavedAt: null
      })
    }),
    {
      name: 'editer-document-storage',
      partialize: (state) => ({
        content: state.content,
        lastSavedContent: state.lastSavedContent,
        documentId: state.documentId,
        lastSavedAt: state.lastSavedAt
      })
    }
  )
)

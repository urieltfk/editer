import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ThemeState {
  isDarkMode: boolean
  fontSize: number
  showLineNumbers: boolean
  toggleTheme: () => void
  setTheme: (isDark: boolean) => void
  setFontSize: (fontSize: number) => void
  setShowLineNumbers: (show: boolean) => void
  toggleLineNumbers: () => void
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      isDarkMode: false,
      fontSize: 14,
      showLineNumbers: false,
      toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
      setTheme: (isDark: boolean) => set({ isDarkMode: isDark }),
      setFontSize: (fontSize: number) => set({ fontSize }),
      setShowLineNumbers: (show: boolean) => set({ showLineNumbers: show }),
      toggleLineNumbers: () => set((state) => ({ showLineNumbers: !state.showLineNumbers })),
    }),
    {
      name: 'theme-storage',
      partialize: (state) => ({
        isDarkMode: state.isDarkMode,
        fontSize: state.fontSize,
        showLineNumbers: state.showLineNumbers
      })
    }
  )
)

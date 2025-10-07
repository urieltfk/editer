import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ThemeState {
  isDarkMode: boolean
  fontSize: number
  toggleTheme: () => void
  setTheme: (isDark: boolean) => void
  setFontSize: (fontSize: number) => void
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set) => ({
      isDarkMode: false,
      fontSize: 14,
      toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
      setTheme: (isDark: boolean) => set({ isDarkMode: isDark }),
      setFontSize: (fontSize: number) => set({ fontSize }),
    }),
    {
      name: 'theme-storage',
    }
  )
)

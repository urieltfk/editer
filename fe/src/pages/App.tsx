import { useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import { TextEditor } from '@components/TextEditor'
import { useThemeStore } from '../lib/store/themeStore'

function App() {
  const { isDarkMode, fontSize } = useThemeStore()

  useEffect(() => {
    const root = document.documentElement
    if (isDarkMode) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }, [isDarkMode])

  useEffect(() => {
    const root = document.documentElement
    root.style.setProperty('--font-size', `${fontSize}px`)
  }, [fontSize])

  return (
    <>
      <TextEditor />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: isDarkMode ? '#2a2a2a' : '#fff',
            color: isDarkMode ? '#fff' : '#333',
            border: isDarkMode ? '1px solid #444' : '1px solid #ddd',
            borderRadius: '8px',
            fontSize: '14px',
            maxWidth: '500px',
          },
          success: {
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </>
  )
}

export default App

import { useEffect } from 'react'
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

  return <TextEditor />
}

export default App

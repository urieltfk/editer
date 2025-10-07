import { useEffect } from 'react'
import { TextEditor } from '@components/TextEditor'
import { useThemeStore } from '../lib/store/themeStore'

function App() {
  const { isDarkMode } = useThemeStore()

  useEffect(() => {
    const root = document.documentElement
    if (isDarkMode) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
  }, [isDarkMode])

  return <TextEditor />
}

export default App

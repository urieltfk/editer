import { Link } from 'react-router-dom'
import { useEffect } from 'react'
import { useThemeStore } from '../lib/store/themeStore'
import './About.css'

const About = (): JSX.Element => {
    const { isDarkMode } = useThemeStore()

    useEffect(() => {
        const root = document.documentElement
        if (isDarkMode) {
            root.classList.add('dark')
        } else {
            root.classList.remove('dark')
        }
    }, [isDarkMode])

    return (
        <div className="about-page">
            <Link to="/" className="back-button">
                ← Back to Editor
            </Link>
            <div className="about-content">
                <p>
                    <span className="app-name">Editer</span> is a minimal, no-auth, shareable text editor designed to be comfortable 
                    and useful for basic text editing and handling on day to day tasks.
                </p>
                <div className="about-buttons">
                    <button className="about-button" disabled>
                        Report a Bug
                    </button>
                    <button className="about-button" disabled>
                        Contact the Maintainer
                    </button>
                </div>
            </div>
        </div>
    )
}

export {About};
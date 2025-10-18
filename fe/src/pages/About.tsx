import { Link } from 'react-router-dom'
import './About.css'

const About = (): JSX.Element => {
    return (
        <div className="about-page">
            <Link to="/" className="back-button">
                ← Back to Editor
            </Link>
            <div className="about-content">
                <h1>About Editer</h1>
                <p>
                    This site is a minimal, no-auth, shareable text editor designed to be comfortable 
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
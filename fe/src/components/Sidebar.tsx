import { useState } from 'react'
import './Sidebar.css'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

export const Sidebar = ({ isOpen, onToggle }: SidebarProps) => {
  return (
    <>
      {/* Toggle Arrow Button */}
      <button 
        className={`sidebar-toggle ${isOpen ? 'open' : ''}`}
        onClick={onToggle}
        aria-label="Toggle sidebar"
      >
        <span className="arrow">›</span>
      </button>

      {/* Sidebar Content */}
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-content">
          <div className="sidebar-section">
            <h3>Settings</h3>
            <div className="placeholder">Settings placeholder</div>
          </div>
          
          <div className="sidebar-section">
            <h3>Night Mode</h3>
            <div className="placeholder">Night mode toggle placeholder</div>
          </div>
          
          <div className="sidebar-section">
            <h3>Share</h3>
            <div className="placeholder">Share functionality placeholder</div>
          </div>
        </div>
      </div>
    </>
  )
}

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LogOut, Menu } from 'lucide-react';
import { canAccessPage, getRoleInfo } from '../utils/roleAccess';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = React.useState(false);
  const roleInfo = getRoleInfo(user?.role);

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  // Déterminer les pages accessibles
  const pages = [
    { path: '/dashboard', label: 'Tableau de bord', key: 'dashboard' },
    { path: '/assets', label: 'Actifs', key: 'assets' },
    { path: '/maintenance', label: 'Maintenance', key: 'maintenance' },
    { path: '/users', label: 'Utilisateurs', key: 'users', adminOnly: true },
    { path: '/reports', label: 'Rapports', key: 'reports' },
    { path: '/search-assets', label: '🔍 Recherche', key: 'search-assets' },
    { path: '/messenger', label: '💬 Messenger', key: 'messenger' },
    { path: '/qr-gallery', label: '🎨 QR Codes', key: 'qr-gallery' },
    { path: '/chatbot', label: '🤖 Chatbot', key: 'chatbot' }
  ];

  const accessiblePages = pages.filter(page => {
    if (page.adminOnly) {
      return user?.role === 'admin';
    }
    return canAccessPage(user?.role, page.key);
  });

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-logo">
          <span className="flag">🇹🇳</span>
          Patrimoine Municipal
        </Link>

        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          <Menu size={24} />
        </button>

        <ul className={`nav-menu ${menuOpen ? 'active' : ''}`}>
          {accessiblePages.map(page => (
            <li key={page.key}>
              <Link to={page.path} className="nav-link">
                {page.label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="navbar-right">
          <Link to="/profile" className="profile-link" title="Mon Profil">
            👤
          </Link>
          <span className="user-info">
            <span className="user-name">{user?.full_name || user?.username}</span>
            <span className="role-badge" style={{ backgroundColor: roleInfo.color }}>
              {roleInfo.name}
            </span>
          </span>
          <button className="btn-logout" onClick={handleLogout} title="Déconnexion">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

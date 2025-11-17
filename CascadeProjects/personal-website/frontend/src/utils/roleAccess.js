/**
 * Utilitaires de contrôle d'accès basé sur les rôles
 */

// Définition des permissions par rôle
const rolePermissions = {
  admin: {
    name: 'Administrateur',
    color: '#667eea',
    permissions: [
      'view_dashboard',
      'view_assets',
      'create_asset',
      'edit_asset',
      'delete_asset',
      'view_maintenance',
      'create_maintenance',
      'edit_maintenance',
      'delete_maintenance',
      'view_users',
      'create_user',
      'edit_user',
      'delete_user',
      'view_reports',
      'export_reports',
      'view_movements',
      'create_movement',
      'view_alerts'
    ],
    pages: ['dashboard', 'assets', 'maintenance', 'users', 'reports', 'search-assets', 'messenger', 'messages', 'chatbot']
  },
  
  responsable_patrimoine: {
    name: 'Responsable Patrimoine',
    color: '#764ba2',
    permissions: [
      'view_dashboard',
      'view_assets',
      'create_asset',
      'edit_asset',
      'view_maintenance',
      'create_maintenance',
      'edit_maintenance',
      'view_reports',
      'export_reports',
      'view_movements',
      'create_movement',
      'view_alerts'
    ],
    pages: ['dashboard', 'assets', 'maintenance', 'reports', 'search-assets', 'messenger', 'messages', 'chatbot']
  },
  
  responsable_service: {
    name: 'Responsable Service',
    color: '#f093fb',
    permissions: [
      'view_dashboard',
      'view_assets',
      'view_maintenance',
      'view_movements',
      'create_movement',
      'view_alerts'
    ],
    pages: ['dashboard', 'assets', 'maintenance', 'search-assets', 'messenger', 'messages', 'chatbot']
  },
  
  agent_maintenance: {
    name: 'Agent Maintenance',
    color: '#4facfe',
    permissions: [
      'view_dashboard',
      'view_assets',
      'view_maintenance',
      'edit_maintenance',
      'view_alerts'
    ],
    pages: ['dashboard', 'maintenance', 'search-assets', 'messenger', 'messages', 'chatbot']
  },
  
  auditeur: {
    name: 'Auditeur',
    color: '#43e97b',
    permissions: [
      'view_dashboard',
      'view_assets',
      'view_maintenance',
      'view_reports',
      'export_reports',
      'view_alerts'
    ],
    pages: ['dashboard', 'reports', 'search-assets', 'messenger', 'messages', 'chatbot']
  }
};

/**
 * Vérifier si un utilisateur a une permission
 */
export const hasPermission = (userRole, permission) => {
  const permissions = rolePermissions[userRole]?.permissions || [];
  return permissions.includes(permission);
};

/**
 * Vérifier si un utilisateur peut accéder à une page
 */
export const canAccessPage = (userRole, page) => {
  const pages = rolePermissions[userRole]?.pages || [];
  return pages.includes(page);
};

/**
 * Obtenir les informations du rôle
 */
export const getRoleInfo = (role) => {
  return rolePermissions[role] || {
    name: 'Utilisateur',
    color: '#999',
    permissions: [],
    pages: []
  };
};

/**
 * Obtenir la liste des pages accessibles
 */
export const getAccessiblePages = (userRole) => {
  return rolePermissions[userRole]?.pages || [];
};

/**
 * Vérifier si l'utilisateur est admin
 */
export const isAdmin = (userRole) => {
  return userRole === 'admin';
};

/**
 * Vérifier si l'utilisateur est responsable patrimoine
 */
export const isResponsablePatrimoine = (userRole) => {
  return userRole === 'responsable_patrimoine';
};

/**
 * Vérifier si l'utilisateur peut créer des utilisateurs
 */
export const canManageUsers = (userRole) => {
  return hasPermission(userRole, 'create_user');
};

/**
 * Vérifier si l'utilisateur peut créer des actifs
 */
export const canManageAssets = (userRole) => {
  return hasPermission(userRole, 'create_asset');
};

/**
 * Vérifier si l'utilisateur peut créer des maintenances
 */
export const canManageMaintenances = (userRole) => {
  return hasPermission(userRole, 'create_maintenance');
};

/**
 * Vérifier si l'utilisateur peut voir les rapports
 */
export const canViewReports = (userRole) => {
  return hasPermission(userRole, 'view_reports');
};

export default rolePermissions;

from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import time
import os
import random
import string
import qrcode
import base64
from dotenv import load_dotenv
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

load_dotenv()

app = Flask(__name__)

# Configuration pour les uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
QR_CODES_FOLDER = os.path.join(os.path.dirname(__file__), 'qr_codes')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Créer les dossiers s'ils n'existent pas
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(QR_CODES_FOLDER).mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False,
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///patrimoine.db')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ==================== HELPER FUNCTIONS ====================

def generate_unique_qr_code():
    """Génère un code QR unique de 8 caractères"""
    # Générer un code aléatoire de 8 caractères (lettres majuscules + chiffres)
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return code

def create_qr_code_image(username, qr_code, full_name=''):
    """Crée l'image QR code pour un utilisateur"""
    try:
        # Créer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Données du QR code
        qr_data = qr_code
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder l'image
        filename = f"qr_{username}_{qr_code}.png"
        filepath = os.path.join(QR_CODES_FOLDER, filename)
        img.save(filepath)
        
        print(f"✅ QR Code créé: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Erreur création QR code: {e}")
        return None

# ==================== MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin, responsable_patrimoine, responsable_service, agent_maintenance, auditeur
    full_name = db.Column(db.String(120))
    qr_code = db.Column(db.String(255))  # QR code unique pour l'utilisateur
    profile_image = db.Column(db.Text)  # Image de profil en Base64
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # bâtiment, véhicule, équipement, mobilier, terrain
    description = db.Column(db.Text)
    acquisition_date = db.Column(db.Date)
    acquisition_value = db.Column(db.Float)
    current_value = db.Column(db.Float)
    location = db.Column(db.String(200))
    status = db.Column(db.String(50), default='actif')  # actif, maintenance, hors_service, déclassé
    qr_code = db.Column(db.String(255))
    assigned_to = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class Maintenance(db.Model):
    __tablename__ = 'maintenances'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    maintenance_type = db.Column(db.String(50))  # préventive, corrective
    scheduled_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    description = db.Column(db.Text)
    cost = db.Column(db.Float)
    status = db.Column(db.String(50), default='planifiée')  # planifiée, en_cours, complétée
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movement(db.Model):
    __tablename__ = 'movements'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    from_location = db.Column(db.String(200))
    to_location = db.Column(db.String(200))
    movement_date = db.Column(db.Date, default=datetime.utcnow)
    reason = db.Column(db.Text)
    created_by = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenances.id'), nullable=True)
    alert_type = db.Column(db.String(50), nullable=False)  # MAINTENANCE_URGENT, MAINTENANCE_LATE, ASSET_MAINTENANCE_REQUIRED
    priority = db.Column(db.String(20), default='MEDIUM')  # HIGH, CRITICAL, MEDIUM
    message = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    days_count = db.Column(db.Integer, nullable=True)  # Jours restants ou jours de retard
    is_read = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)  # Permet de désactiver sans supprimer
    is_dismissed = db.Column(db.Boolean, default=False)  # Ignorée définitivement par l'utilisateur
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    asset = db.relationship('Asset', backref='alerts', foreign_keys=[asset_id])
    maintenance = db.relationship('Maintenance', backref='alerts', foreign_keys=[maintenance_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'maintenance_id': self.maintenance_id,
            'alert_type': self.alert_type,
            'priority': self.priority,
            'message': self.message,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'days_count': self.days_count,
            'is_read': self.is_read,
            'is_active': self.is_active,
            'is_dismissed': self.is_dismissed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_bot_response = db.Column(db.Boolean, default=False)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='chat_messages')

# Association table pour les groupes et les utilisateurs
group_members = db.Table('group_members',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    members = db.relationship('User', secondary=group_members, backref='groups')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_groups')

# ==================== AUTHENTICATION ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Créer un nouvel utilisateur (Admin uniquement)"""
    data = request.get_json()
    
    # Validation des champs obligatoires
    required_fields = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Champs obligatoires manquants'}), 400
    
    # Vérifier que l'utilisateur n'existe pas
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nom d\'utilisateur existe déjà'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email existe déjà'}), 400
    
    # Valider le rôle
    valid_roles = ['admin', 'responsable_patrimoine', 'responsable_service', 'agent_maintenance', 'auditeur']
    if data['role'] not in valid_roles:
        return jsonify({'error': f'Rôle invalide. Rôles valides: {", ".join(valid_roles)}'}), 400
    
    # Générer un QR code unique
    qr_code = generate_unique_qr_code()
    print(f"🎫 QR Code généré pour {data['username']}: {qr_code}")
    
    # Créer l'utilisateur
    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name', ''),
        role=data['role'],
        qr_code=qr_code
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Créer l'image QR code
        qr_filename = create_qr_code_image(
            username=user.username,
            qr_code=qr_code,
            full_name=user.full_name
        )
        
        print(f"✅ Utilisateur {user.username} créé avec QR code: {qr_code}")
        
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'full_name': user.full_name,
                'qr_code': qr_code,
                'qr_image': f'/qr_codes/{qr_filename}' if qr_filename else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur création utilisateur: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Nom d\'utilisateur et mot de passe requis'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Identifiants invalides'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name,
            'qr_code': user.qr_code,
            'profile_image': user.profile_image,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    }), 200

# ==================== USERS MANAGEMENT ====================

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    """Récupérer tous les utilisateurs"""
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role,
        'full_name': u.full_name,
        'qr_code': u.qr_code,
        'profile_image': u.profile_image,
        'created_at': u.created_at.isoformat()
    } for u in users]), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    
    # Mise à jour des champs modifiables
    if 'role' in data:
        user.role = data['role']
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        # Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400
        user.email = data['email']
    
    try:
        db.session.commit()
        print(f"✅ Utilisateur {user.username} mis à jour: {user.full_name} / {user.email}")
        return jsonify({
            'message': 'Utilisateur mis à jour avec succès',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'qr_code': user.qr_code,
                'profile_image': user.profile_image,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur mise à jour utilisateur {user_id}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    try:
        # Supprimer les messages envoyés par l'utilisateur
        Message.query.filter_by(sender_id=user_id).delete()
        
        # Supprimer les messages reçus par l'utilisateur
        Message.query.filter_by(recipient_id=user_id).delete()
        
        # Supprimer les messages de chat de l'utilisateur
        ChatMessage.query.filter_by(user_id=user_id).delete()
        
        # Supprimer l'utilisateur des groupes (table d'association group_members)
        db.session.execute(
            group_members.delete().where(group_members.c.user_id == user_id)
        )
        
        # Supprimer les groupes créés par l'utilisateur
        Group.query.filter_by(created_by=user_id).delete()
        
        # Supprimer l'utilisateur
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'Utilisateur supprimé'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500

# ==================== ASSETS MANAGEMENT ====================

@app.route('/api/assets/test', methods=['GET'])
def get_assets_test():
    """Récupérer tous les actifs (TEST - sans JWT)"""
    try:
        assets = Asset.query.all()
        return jsonify([{
            'id': a.id,
            'name': a.name,
            'category': a.category,
            'description': a.description,
            'acquisition_date': a.acquisition_date.isoformat() if a.acquisition_date else None,
            'acquisition_value': a.acquisition_value,
            'current_value': a.current_value,
            'location': a.location,
            'status': a.status,
            'qr_code': a.qr_code,
            'assigned_to': a.assigned_to,
            'created_at': a.created_at.isoformat()
        } for a in assets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assets', methods=['GET'])
@jwt_required()
def get_assets():
    assets = Asset.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'category': a.category,
        'description': a.description,
        'acquisition_date': a.acquisition_date.isoformat() if a.acquisition_date else None,
        'acquisition_value': a.acquisition_value,
        'current_value': a.current_value,
        'location': a.location,
        'status': a.status,
        'assigned_to': a.assigned_to,
        'qr_code': a.qr_code,
        'created_at': a.created_at.isoformat()
    } for a in assets]), 200

def generate_qr_code_for_asset(asset):
    """Génère un QR code unique pour un actif"""
    # Générer un code unique
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Créer le QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"ASSET_{asset.id}_{qr_code}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarder l'image
    filename = f"qr_asset_{asset.id}_{qr_code}.png"
    filepath = os.path.join(QR_CODES_FOLDER, filename)
    img.save(filepath)
    
    print(f"🎫 QR Code généré pour actif {asset.id}: {qr_code}")
    
    return qr_code

@app.route('/api/assets', methods=['POST'])
@jwt_required()
def create_asset():
    data = request.get_json()
    
    asset = Asset(
        name=data['name'],
        category=data['category'],
        description=data.get('description', ''),
        acquisition_date=datetime.strptime(data.get('acquisition_date', ''), '%Y-%m-%d').date() if data.get('acquisition_date') else None,
        acquisition_value=data.get('acquisition_value', 0),
        current_value=data.get('current_value', 0),
        location=data.get('location', ''),
        status=data.get('status', 'actif'),
        assigned_to=data.get('assigned_to', '')
    )
    
    db.session.add(asset)
    db.session.flush()  # Pour obtenir l'ID avant commit
    
    # ✅ Générer le QR code automatiquement
    qr_code = generate_qr_code_for_asset(asset)
    asset.qr_code = qr_code
    
    db.session.commit()
    
    print(f"✅ Actif créé: {asset.name} avec QR code: {qr_code}")
    
    return jsonify({
        'id': asset.id,
        'qr_code': qr_code,
        'message': 'Actif créé avec succès'
    }), 201

@app.route('/api/assets/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return jsonify({'error': 'Actif non trouvé'}), 404
    
    return jsonify({
        'id': asset.id,
        'name': asset.name,
        'category': asset.category,
        'description': asset.description,
        'acquisition_date': asset.acquisition_date.isoformat() if asset.acquisition_date else None,
        'acquisition_value': asset.acquisition_value,
        'current_value': asset.current_value,
        'location': asset.location,
        'status': asset.status,
        'assigned_to': asset.assigned_to,
        'qr_code': asset.qr_code,
        'created_at': asset.created_at.isoformat()
    }), 200

@app.route('/api/assets/<int:asset_id>', methods=['PUT'])
@jwt_required()
def update_asset(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return jsonify({'error': 'Actif non trouvé'}), 404
    
    data = request.get_json()
    asset.name = data.get('name', asset.name)
    asset.category = data.get('category', asset.category)
    asset.description = data.get('description', asset.description)
    asset.location = data.get('location', asset.location)
    asset.status = data.get('status', asset.status)
    asset.assigned_to = data.get('assigned_to', asset.assigned_to)
    asset.current_value = data.get('current_value', asset.current_value)
    
    db.session.commit()
    return jsonify({'message': 'Actif mis à jour'}), 200

@app.route('/api/assets/<int:asset_id>', methods=['DELETE'])
@jwt_required()
def delete_asset(asset_id):
    asset = db.session.get(Asset, asset_id)
    if not asset:
        return jsonify({'error': 'Actif non trouvé'}), 404
    
    # Supprimer en cascade tous les éléments liés
    # 1. Supprimer les maintenances associées
    Maintenance.query.filter_by(asset_id=asset_id).delete()
    
    # 2. Supprimer les mouvements associés
    Movement.query.filter_by(asset_id=asset_id).delete()
    
    # 3. Supprimer les alertes associées
    Alert.query.filter_by(asset_id=asset_id).delete()
    
    # 4. Supprimer l'actif lui-même
    db.session.delete(asset)
    db.session.commit()
    
    return jsonify({'message': 'Actif et données associées supprimés'}), 200

# ==================== MAINTENANCE ====================

@app.route('/api/maintenances/test', methods=['GET'])
def get_maintenances_test():
    """Récupérer toutes les maintenances (TEST - sans JWT)"""
    try:
        maintenances = Maintenance.query.all()
        return jsonify([{
            'id': m.id,
            'asset_id': m.asset_id,
            'maintenance_type': m.maintenance_type,
            'scheduled_date': m.scheduled_date.isoformat() if m.scheduled_date else None,
            'completed_date': m.completed_date.isoformat() if m.completed_date else None,
            'description': m.description,
            'cost': m.cost,
            'status': m.status,
            'created_at': m.created_at.isoformat()
        } for m in maintenances]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/maintenances', methods=['GET'])
@jwt_required()
def get_maintenances():
    maintenances = Maintenance.query.all()
    return jsonify([{
        'id': m.id,
        'asset_id': m.asset_id,
        'maintenance_type': m.maintenance_type,
        'scheduled_date': m.scheduled_date.isoformat() if m.scheduled_date else None,
        'completed_date': m.completed_date.isoformat() if m.completed_date else None,
        'description': m.description,
        'cost': m.cost,
        'status': m.status,
        'created_at': m.created_at.isoformat()
    } for m in maintenances]), 200

def generate_qr_code_for_maintenance(maintenance):
    """Génère un QR code unique pour une maintenance"""
    # Générer un code unique
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Créer le QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"MAINT_{maintenance.id}_{qr_code}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Sauvegarder l'image
    filename = f"qr_maintenance_{maintenance.id}_{qr_code}.png"
    filepath = os.path.join(QR_CODES_FOLDER, filename)
    img.save(filepath)
    
    print(f"🔧 QR Code généré pour maintenance {maintenance.id}: {qr_code}")
    
    return qr_code

@app.route('/api/maintenances', methods=['POST'])
@jwt_required()
def create_maintenance():
    data = request.get_json()
    
    maintenance = Maintenance(
        asset_id=data['asset_id'],
        maintenance_type=data.get('maintenance_type', 'préventive'),
        scheduled_date=datetime.strptime(data.get('scheduled_date', ''), '%Y-%m-%d').date() if data.get('scheduled_date') else None,
        description=data.get('description', ''),
        cost=data.get('cost', 0),
        status=data.get('status', 'planifiée')
    )
    
    db.session.add(maintenance)
    db.session.flush()  # Pour obtenir l'ID avant commit
    
    # ✅ Générer le QR code automatiquement
    qr_code = generate_qr_code_for_maintenance(maintenance)
    maintenance.qr_code = qr_code
    
    db.session.commit()
    
    print(f"✅ Maintenance créée avec QR code: {qr_code}")
    
    return jsonify({
        'id': maintenance.id,
        'qr_code': qr_code,
        'message': 'Maintenance créée'
    }), 201

@app.route('/api/maintenances/<int:maintenance_id>', methods=['PUT'])
@jwt_required()
def update_maintenance(maintenance_id):
    maintenance = db.session.get(Maintenance, maintenance_id)
    if not maintenance:
        return jsonify({'error': 'Maintenance non trouvée'}), 404
    
    try:
        data = request.get_json()
        print(f"📝 Mise à jour maintenance {maintenance_id}")
        print(f"   Données reçues: {data}")
        
        # Mettre à jour tous les champs
        if 'asset_id' in data:
            maintenance.asset_id = data['asset_id']
        if 'maintenance_type' in data:
            maintenance.maintenance_type = data['maintenance_type']
        if 'scheduled_date' in data:
            maintenance.scheduled_date = datetime.strptime(data['scheduled_date'], '%Y-%m-%d').date()
        if 'description' in data:
            maintenance.description = data['description']
        if 'cost' in data:
            maintenance.cost = float(data['cost']) if data['cost'] else None
        if 'status' in data:
            maintenance.status = data['status']
        if 'completed_date' in data and data['completed_date']:
            maintenance.completed_date = datetime.strptime(data['completed_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        print(f"✅ Maintenance {maintenance_id} mise à jour")
        
        return jsonify({
            'message': 'Maintenance mise à jour',
            'id': maintenance.id,
            'asset_id': maintenance.asset_id,
            'maintenance_type': maintenance.maintenance_type,
            'scheduled_date': maintenance.scheduled_date.isoformat(),
            'description': maintenance.description,
            'cost': maintenance.cost,
            'status': maintenance.status
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur mise à jour maintenance: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/maintenances/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance(maintenance_id):
    """Supprimer une maintenance"""
    try:
        maintenance = db.session.get(Maintenance, maintenance_id)
        if not maintenance:
            return jsonify({'error': 'Maintenance non trouvée'}), 404
        
        print(f"🗑️ Suppression maintenance {maintenance_id}")
        
        # Supprimer d'abord les alertes associées
        Alert.query.filter_by(maintenance_id=maintenance_id).delete()
        
        # Puis supprimer la maintenance
        db.session.delete(maintenance)
        db.session.commit()
        
        print(f"✅ Maintenance {maintenance_id} et alertes associées supprimées")
        
        return jsonify({'message': 'Maintenance supprimée'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur suppression maintenance: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== MOVEMENTS ====================

@app.route('/api/movements', methods=['GET'])
@jwt_required()
def get_movements():
    movements = Movement.query.all()
    return jsonify([{
        'id': m.id,
        'asset_id': m.asset_id,
        'from_location': m.from_location,
        'to_location': m.to_location,
        'movement_date': m.movement_date.isoformat(),
        'reason': m.reason,
        'created_by': m.created_by,
        'created_at': m.created_at.isoformat()
    } for m in movements]), 200

@app.route('/api/movements', methods=['POST'])
@jwt_required()
def create_movement():
    data = request.get_json()
    
    movement = Movement(
        asset_id=data['asset_id'],
        from_location=data.get('from_location', ''),
        to_location=data.get('to_location', ''),
        reason=data.get('reason', ''),
        created_by=data.get('created_by', '')
    )
    
    db.session.add(movement)
    db.session.commit()
    
    return jsonify({'id': movement.id, 'message': 'Mouvement enregistré'}), 201

# ==================== ALERTS ====================

def generate_and_update_alerts():
    """
    Fonction de génération/mise à jour des alertes stockées en base de données
    À appeler régulièrement (via scheduler ou manuellement)
    """
    try:
        from datetime import date, timedelta
        today = date.today()
        next_week = today + timedelta(days=7)
        
        print("🔄 Début génération alertes...")
        
        # Désactiver toutes les alertes existantes (on va les recréer ou réactiver)
        Alert.query.update({'is_active': False})
        
        alerts_created = 0
        alerts_updated = 0
        
        # ==================== TYPE 1: Maintenances Urgentes (< 7 jours) ====================
        urgent_maintenances = Maintenance.query.filter(
            Maintenance.status == 'planifié',
            Maintenance.scheduled_date <= next_week,
            Maintenance.scheduled_date >= today
        ).all()
        
        for m in urgent_maintenances:
            asset = db.session.get(Asset, m.asset_id) if m.asset_id else None
            days_left = (m.scheduled_date - today).days
            
            message = f"Maintenance prévue: {asset.name if asset else 'Actif'} dans {days_left} jour(s)"
            
            # Vérifier si l'utilisateur a ignoré cette alerte
            dismissed_alert = Alert.query.filter_by(
                maintenance_id=m.id,
                alert_type='MAINTENANCE_URGENT',
                is_dismissed=True
            ).first()
            
            if dismissed_alert:
                # Ne pas recréer une alerte ignorée par l'utilisateur
                continue
            
            # Vérifier si l'alerte existe déjà (inactive et non-dismissed)
            existing_alert = Alert.query.filter_by(
                maintenance_id=m.id,
                alert_type='MAINTENANCE_URGENT'
            ).filter(Alert.is_active == False, Alert.is_dismissed == False).first()
            
            if existing_alert:
                # Mise à jour
                existing_alert.message = message
                existing_alert.days_count = days_left
                existing_alert.due_date = m.scheduled_date
                existing_alert.is_active = True
                existing_alert.updated_at = datetime.utcnow()
                alerts_updated += 1
            else:
                # Création
                new_alert = Alert(
                    asset_id=m.asset_id,
                    maintenance_id=m.id,
                    alert_type='MAINTENANCE_URGENT',
                    priority='HIGH',
                    message=message,
                    due_date=m.scheduled_date,
                    days_count=days_left,
                    is_active=True
                )
                db.session.add(new_alert)
                alerts_created += 1
        
        # ==================== TYPE 2: Maintenances en Retard ====================
        overdue_maintenances = Maintenance.query.filter(
            Maintenance.status.in_(['planifié', 'en_cours']),
            Maintenance.scheduled_date < today
        ).all()
        
        for m in overdue_maintenances:
            asset = db.session.get(Asset, m.asset_id) if m.asset_id else None
            days_late = (today - m.scheduled_date).days
            
            message = f"⚠️ Maintenance en retard: {asset.name if asset else 'Actif'} ({days_late} jour(s) de retard)"
            
            # Vérifier si l'utilisateur a ignoré cette alerte
            dismissed_alert = Alert.query.filter_by(
                maintenance_id=m.id,
                alert_type='MAINTENANCE_LATE',
                is_dismissed=True
            ).first()
            
            if dismissed_alert:
                # Ne pas recréer une alerte ignorée par l'utilisateur
                continue
            
            # Vérifier si l'alerte existe déjà (inactive et non-dismissed)
            existing_alert = Alert.query.filter_by(
                maintenance_id=m.id,
                alert_type='MAINTENANCE_LATE'
            ).filter(Alert.is_active == False, Alert.is_dismissed == False).first()
            
            if existing_alert:
                # Mise à jour
                existing_alert.message = message
                existing_alert.days_count = days_late
                existing_alert.due_date = m.scheduled_date
                existing_alert.is_active = True
                existing_alert.updated_at = datetime.utcnow()
                alerts_updated += 1
            else:
                # Création
                new_alert = Alert(
                    asset_id=m.asset_id,
                    maintenance_id=m.id,
                    alert_type='MAINTENANCE_LATE',
                    priority='CRITICAL',
                    message=message,
                    due_date=m.scheduled_date,
                    days_count=days_late,
                    is_active=True
                )
                db.session.add(new_alert)
                alerts_created += 1
        
        # TYPE 3 (ASSET_MAINTENANCE_REQUIRED) supprimé - alertes 100% dynamiques basées sur maintenances uniquement
        
        # Commit toutes les modifications
        db.session.commit()
        
        # Supprimer les alertes inactives (mais conserver les dismissed pour historique)
        Alert.query.filter_by(is_active=False, is_dismissed=False).delete()
        db.session.commit()
        
        print(f"✅ Génération alertes terminée: {alerts_created} créées, {alerts_updated} mises à jour")
        return alerts_created, alerts_updated
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur génération alertes: {e}")
        raise e

@app.route('/api/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Récupère les alertes stockées en base de données (gérées par scheduler automatique)"""
    try:
        # Les alertes sont maintenant générées automatiquement toutes les 5 minutes par le scheduler
        # Pas besoin de régénérer à chaque requête = meilleures performances! 🚀
        
        # Récupérer toutes les alertes actives ET non-ignorées depuis la base de données
        alerts = Alert.query.filter_by(is_active=True, is_dismissed=False).order_by(Alert.priority.desc(), Alert.created_at.desc()).all()
        
        # Convertir en JSON
        alerts_list = [alert.to_dict() for alert in alerts]
        
        print(f"📊 Alertes récupérées depuis BDD: {len(alerts_list)} alertes actives (scheduler automatique)")
        
        return jsonify(alerts_list), 200
    except Exception as e:
        print(f"❌ Erreur get_alerts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/<int:alert_id>/read', methods=['PUT'])
@jwt_required()
def mark_alert_read(alert_id):
    """Marquer une alerte comme lue (stockée en BDD)"""
    try:
        # Récupérer l'alerte depuis la base de données
        alert = db.session.get(Alert, alert_id)
        if not alert:
            return jsonify({'error': 'Alerte non trouvée'}), 404
        
        # Marquer comme lue
        alert.is_read = True
        alert.updated_at = datetime.utcnow()
        db.session.commit()
        
        print(f"✅ Alerte {alert_id} marquée comme lue")
        return jsonify({
            'message': 'Alerte marquée comme lue',
            'alert': alert.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur mark_alert_read: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/generate', methods=['POST'])
@jwt_required()
def regenerate_alerts():
    """Endpoint pour régénérer manuellement toutes les alertes"""
    try:
        alerts_created, alerts_updated = generate_and_update_alerts()
        
        return jsonify({
            'message': 'Alertes régénérées avec succès',
            'alerts_created': alerts_created,
            'alerts_updated': alerts_updated
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
@jwt_required()
def delete_alert(alert_id):
    """Ignorer définitivement une alerte (dismissed)"""
    try:
        alert = db.session.get(Alert, alert_id)
        if not alert:
            return jsonify({'error': 'Alerte non trouvée'}), 404
        
        # Marquer comme ignorée définitivement par l'utilisateur
        # L'alerte ne sera plus recréée par le scheduler
        alert.is_dismissed = True
        alert.is_active = False
        alert.updated_at = datetime.utcnow()
        db.session.commit()
        
        print(f"✅ Alerte {alert_id} ignorée définitivement (dismissed)")
        return jsonify({'message': 'Alerte ignorée définitivement'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== MESSAGING ====================

@app.route('/api/messages/test', methods=['GET'])
@jwt_required()
def get_messages_test():
    """Récupérer les messages de l'utilisateur connecté uniquement"""
    try:
        current_user_id = get_jwt_identity()
        
        # Récupérer uniquement les messages où l'utilisateur est sender OU recipient
        messages = Message.query.filter(
            (Message.sender_id == current_user_id) | 
            (Message.recipient_id == current_user_id)
        ).order_by(Message.created_at.desc()).all()
        
        result = []
        
        for m in messages:
            # Récupérer les vrais noms des utilisateurs
            sender = db.session.get(User, m.sender_id)
            recipient = db.session.get(User, m.recipient_id)
            
            sender_name = sender.full_name if sender and sender.full_name else f'User {m.sender_id}'
            recipient_name = recipient.full_name if recipient and recipient.full_name else f'User {m.recipient_id}'
            
            result.append({
                'id': m.id,
                'sender_id': m.sender_id,
                'recipient_id': m.recipient_id,
                'sender_name': sender_name,
                'recipient_name': recipient_name,
                'subject': m.subject,
                'content': m.content,
                'is_read': m.is_read,
                'created_at': m.created_at.isoformat()
            })
        
        print(f"👤 Messages pour utilisateur {current_user_id}: {len(result)} message(s)")
        
        return jsonify(result), 200
    except Exception as e:
        print(f"❌ Erreur get_messages_test: {e}")
        return jsonify({'error': str(e)}), 500

# Stockage des appels en attente
pending_calls = {}

@app.route('/api/calls/initiate', methods=['POST'])
def initiate_call():
    """Initier un appel"""
    try:
        data = request.get_json()
        call_id = f"{data['caller_id']}-{data['recipient_id']}-{int(time.time())}"
        
        pending_calls[call_id] = {
            'caller_id': data['caller_id'],
            'caller_name': data['caller_name'],
            'recipient_id': data['recipient_id'],
            'type': data['type'],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'call_id': call_id,
            'status': 'initiated'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls/check/<int:user_id>', methods=['GET'])
def check_calls(user_id):
    """Vérifier les appels entrants"""
    try:
        incoming = []
        for call_id, call_data in list(pending_calls.items()):
            if call_data['recipient_id'] == user_id:
                incoming.append({
                    'call_id': call_id,
                    **call_data
                })
        
        return jsonify(incoming), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls/accept/<call_id>', methods=['POST'])
def accept_call(call_id):
    """Accepter un appel"""
    try:
        if call_id in pending_calls:
            del pending_calls[call_id]
        return jsonify({'status': 'accepted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls/reject/<call_id>', methods=['POST'])
def reject_call(call_id):
    """Refuser un appel"""
    try:
        if call_id in pending_calls:
            del pending_calls[call_id]
        return jsonify({'status': 'rejected'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Vérifier si le fichier est autorisé"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload un fichier"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Pas de fichier'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Fichier vide'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
        filename = secure_filename(file.filename)
        # Ajouter un timestamp pour éviter les doublons
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'filename': filename,
            'url': f'/api/uploads/{filename}',
            'size': os.path.getsize(filepath)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>/profile-image', methods=['POST'])
@jwt_required()
def upload_profile_image(user_id):
    """Upload une image de profil pour un utilisateur (stockée en Base64)"""
    try:
        # Vérifier que l'utilisateur existe
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        if 'file' not in request.files:
            return jsonify({'error': 'Pas de fichier'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Fichier vide'}), 400
        
        # Vérifier que c'est une image
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            return jsonify({'error': 'Seules les images sont autorisées (PNG, JPG, JPEG, GIF, WEBP)'}), 400
        
        # Lire le fichier et le convertir en Base64
        file_content = file.read()
        
        # Vérifier la taille (max 5MB)
        if len(file_content) > 5 * 1024 * 1024:
            return jsonify({'error': 'L\'image ne doit pas dépasser 5MB'}), 400
        
        # Encoder en Base64
        base64_encoded = base64.b64encode(file_content).decode('utf-8')
        
        # Déterminer le type MIME
        ext = file.filename.rsplit('.', 1)[1].lower()
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        # Format Data URL
        image_data_url = f"data:{mime_type};base64,{base64_encoded}"
        
        # Mettre à jour le profil de l'utilisateur avec le Base64
        user.profile_image = image_data_url
        db.session.commit()
        
        print(f"✅ Image de profil (Base64) sauvegardée pour {user.username}")
        print(f"   Taille: {len(file_content)} bytes ({len(base64_encoded)} chars Base64)")
        
        return jsonify({
            'message': 'Image de profil uploadée et sauvegardée en Base64',
            'image_size': len(file_content),
            'base64_size': len(base64_encoded),
            'profile_image': image_data_url,  # Image complète en Base64
            'user': {
                'id': user.id,
                'username': user.username,
                'profile_image': image_data_url  # Image complète
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur upload image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """Télécharger un fichier uploadé"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'error': 'Fichier non trouvé'}), 404

@app.route('/api/calls/log', methods=['POST'])
def log_call():
    """Enregistrer un appel dans les messages"""
    try:
        data = request.get_json()
        
        # Créer un message pour l'appel
        message = Message(
            sender_id=data['caller_id'],
            recipient_id=data['recipient_id'],
            subject='Appel',
            content=f"📞 Appel {data['type']} - {data.get('duration', 0)}s",
            is_read=False
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'id': message.id,
            'status': 'logged'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages', methods=['GET'])
@jwt_required()
def get_messages():
    """Récupérer les messages reçus"""
    current_user_id = get_jwt_identity()
    messages = Message.query.filter_by(recipient_id=current_user_id).order_by(Message.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'sender_name': m.sender.full_name or m.sender.username,
        'subject': m.subject,
        'content': m.content,
        'is_read': m.is_read,
        'created_at': m.created_at.isoformat()
    } for m in messages]), 200


@app.route('/api/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_read(message_id):
    """Marquer un message comme lu"""
    message = db.session.get(Message, message_id)
    if not message:
        return jsonify({'error': 'Message non trouvé'}), 404
    
    message.is_read = True
    db.session.commit()
    return jsonify({'message': 'Message marqué comme lu'}), 200

# ==================== CHATBOT ====================

def get_chatbot_response(user_message, user_role):
    """Générer une réponse détaillée du chatbot avec guide étape par étape"""
    message_lower = user_message.lower()
    
    # GUIDES DÉTAILLÉS POUR CHAQUE QUESTION
    
    # Guide: Comment créer un actif
    if 'créer' in message_lower and 'actif' in message_lower:
        return """📝 **GUIDE COMPLET: Créer un Actif**

**Étape 1: Accéder à la page Actifs**
- Cliquez sur "Actifs" dans le menu de navigation
- Vous verrez la liste de tous les actifs existants

**Étape 2: Ouvrir le formulaire**
- Cliquez sur le bouton "+ Ajouter un actif" (en haut à droite)
- Un formulaire s'ouvrira

**Étape 3: Remplir les informations**
✓ Nom: Nom de l'actif (ex: "Ordinateur Bureau 101")
✓ Catégorie: Sélectionnez dans la liste (Bâtiment, Véhicule, Équipement, etc.)
✓ Valeur: Prix d'achat en euros
✓ Localisation: Où se trouve l'actif (ex: "Bureau 101, Étage 2")
✓ Numéro de série: Identifiant unique (optionnel)
✓ Date d'acquisition: Date d'achat
✓ État: Actif, En maintenance, Retiré
✓ Description: Détails supplémentaires (optionnel)

**Étape 4: Valider**
- Cliquez sur "Enregistrer"
- L'actif apparaîtra dans la liste!

✅ **Astuce:** Vous pouvez uploader une photo de l'actif pour le reconnaître facilement!"""

    # Guide: Comment planifier une maintenance
    if 'planifier' in message_lower and 'maintenance' in message_lower:
        return """🔧 **GUIDE COMPLET: Planifier une Maintenance**

**Étape 1: Accéder à la page Maintenance**
- Cliquez sur "Maintenance" dans le menu
- Vous verrez toutes les maintenances planifiées

**Étape 2: Choisir l'actif**
- Cliquez sur "+ Planifier une maintenance"
- OU depuis la page d'un actif, cliquez sur "Planifier maintenance"

**Étape 3: Remplir les détails**
✓ Actif concerné: Sélectionnez l'actif (si pas déjà sélectionné)
✓ Type de maintenance:
  • Préventive: Maintenance régulière planifiée
  • Corrective: Réparation d'une panne
  • Inspection: Vérification de l'état
✓ Date planifiée: Quand effectuer la maintenance
✓ Description: Détails de l'intervention à faire
✓ Coût estimé: Budget prévu (optionnel)
✓ Technicien: Qui effectuera la maintenance (optionnel)

**Étape 4: Enregistrer**
- Cliquez sur "Planifier"
- La maintenance apparaîtra dans le calendrier!

**Étape 5: Suivi**
- Quand la maintenance est effectuée, changez le statut à "Terminée"
- Vous pouvez ajouter des notes et le coût réel

✅ **Important:** Les maintenances urgentes (dans 7 jours) génèrent automatiquement une alerte!"""

    # Guide: Comment générer un rapport
    if 'générer' in message_lower and 'rapport' in message_lower:
        return """📊 **GUIDE COMPLET: Générer un Rapport**

**Étape 1: Accéder à la page Rapports**
- Cliquez sur "Rapports" dans le menu
- Interface de génération s'affiche

**Étape 2: Choisir le type de rapport**
📈 **Rapport d'actifs:**
  - Liste complète des actifs
  - Filtrable par catégorie, localisation, état
  
📈 **Rapport de maintenances:**
  - Historique des maintenances effectuées
  - Coûts par période
  - Maintenances à venir
  
📈 **Rapport financier:**
  - Coûts de maintenance par catégorie
  - Évolution des dépenses
  - Budget vs Réel

**Étape 3: Définir les paramètres**
✓ Période: Date de début et date de fin
✓ Catégorie: Filtrer par type d'actif (optionnel)
✓ Localisation: Filtrer par lieu (optionnel)
✓ Format: PDF ou Excel

**Étape 4: Aperçu**
- Cliquez sur "Aperçu" pour voir le résultat
- Vérifiez que les données sont correctes

**Étape 5: Télécharger**
- Cliquez sur "Télécharger PDF" ou "Télécharger Excel"
- Le fichier se télécharge automatiquement!

✅ **Astuce:** Les rapports incluent automatiquement des graphiques et statistiques!"""

    # Guide général "Aide"
    if message_lower == 'aide' or message_lower == 'help':
        guide_text = """🤖 **ASSISTANT VIRTUEL - GUIDE COMPLET**

Je peux vous aider avec les questions suivantes:

**📝 Gestion des Actifs:**
- "Comment créer un actif?"
- "Comment modifier un actif?"
- "Comment rechercher un actif?"
- "Comment supprimer un actif?"

**🔧 Gestion des Maintenances:**
- "Comment planifier une maintenance?"
- "Comment suivre une maintenance?"
- "Comment marquer une maintenance terminée?"

**📊 Rapports et Statistiques:**
- "Comment générer un rapport?"
- "Comment consulter les statistiques?"
- "Comment voir les coûts?"

**🔔 Alertes:**
- "Comment consulter les alertes?"
- "Quelles sont les alertes urgentes?"

**💬 Messagerie:**
- "Comment envoyer un message?"
- "Comment créer un groupe?"
"""
        
        if user_role == 'admin':
            guide_text += """
**👥 Administration (votre rôle):**
- "Comment créer un utilisateur?"
- "Comment gérer les rôles?"
- "Comment gérer les permissions?"
"""
        
        guide_text += """
**💡 Posez votre question en français naturel!**
Exemple: "Comment puis-je ajouter un nouveau véhicule?"
"""
        return guide_text

    # Salutations
    if any(word in message_lower for word in ['bonjour', 'salut', 'hello', 'hi']):
        return f"""👋 Bonjour! Je suis votre assistant virtuel.

Je peux vous guider dans l'utilisation du système de gestion du patrimoine municipal.

**Questions fréquentes:**
• Comment créer un actif?
• Comment planifier une maintenance?
• Comment générer un rapport?

**Tapez "aide" pour voir toutes les possibilités!**

Comment puis-je vous aider aujourd'hui?"""

    # Remerciements
    if 'merci' in message_lower or 'thank' in message_lower:
        return "De rien! 😊 N'hésitez pas si vous avez d'autres questions. Tapez 'aide' pour voir ce que je peux faire!"

    # Questions sur les actifs
    if 'actif' in message_lower:
        return """📝 **GESTION DES ACTIFS**

**Actions disponibles:**

1️⃣ **Créer un actif:** "Comment créer un actif?"
2️⃣ **Modifier un actif:** Cliquez sur l'actif → Bouton "Modifier"
3️⃣ **Supprimer un actif:** Cliquez sur l'actif → Bouton "Supprimer" (confirmation requise)
4️⃣ **Rechercher:** Utilisez la barre de recherche en haut de la page Actifs
5️⃣ **Filtrer:** Filtrez par catégorie ou localisation

**Informations d'un actif:**
- Nom, catégorie, valeur
- Localisation actuelle
- Historique des mouvements
- Maintenances associées
- Documents et photos

Posez-moi une question plus spécifique!"""

    # Questions sur les maintenances
    if 'maintenance' in message_lower:
        return """🔧 **GESTION DES MAINTENANCES**

**Actions disponibles:**

1️⃣ **Planifier:** "Comment planifier une maintenance?"
2️⃣ **Consulter:** Page Maintenance → Liste de toutes les maintenances
3️⃣ **Modifier:** Cliquez sur une maintenance → Bouton "Modifier"
4️⃣ **Changer le statut:** 
   - Planifiée → En cours → Terminée
5️⃣ **Voir l'historique:** Page Maintenance → Onglet "Historique"

**Types de maintenance:**
• **Préventive:** Planifiée régulièrement
• **Corrective:** Réparation d'une panne
• **Inspection:** Vérification de l'état

**Alertes automatiques:**
✅ Les maintenances urgentes (< 7 jours) génèrent une alerte
✅ Les maintenances en retard sont signalées
✅ Actualisation automatique toutes les 30 secondes

Posez-moi une question plus spécifique!"""

    # Questions sur les rapports
    if 'rapport' in message_lower or 'statistique' in message_lower:
        return """📊 **RAPPORTS ET STATISTIQUES**

**Dashboard (Tableau de bord):**
- Statistiques en temps réel
- Graphiques interactifs
- Alertes actives
- Coûts du mois

**Générer un rapport:** "Comment générer un rapport?"

**Types de rapports disponibles:**
1️⃣ Rapport d'inventaire (liste actifs)
2️⃣ Rapport de maintenances
3️⃣ Rapport financier (coûts)
4️⃣ Rapport par catégorie
5️⃣ Rapport par localisation

**Formats d'export:**
📄 PDF (pour impression)
📊 Excel (pour analyse)

Les rapports incluent automatiquement:
- Tableaux détaillés
- Graphiques
- Statistiques clés
- Période sélectionnée

Tapez "comment générer un rapport" pour le guide détaillé!"""

    # Questions sur les alertes
    if 'alerte' in message_lower:
        return """🔔 **SYSTÈME D'ALERTES DYNAMIQUES**

**Types d'alertes:**
1️⃣ **Maintenances urgentes** (dans 7 jours)
2️⃣ **Maintenances en retard**
3️⃣ **Actifs nécessitant maintenance**

**Comment consulter:**
- Dashboard → Section "Alertes" (en haut)
- Icône de notification dans le menu

**Fonctionnalités:**
✅ Génération automatique 100% dynamique
✅ Actualisation toutes les 30 secondes
✅ Compteur d'alertes non lues
✅ Clic sur une alerte → Accès direct à l'actif/maintenance

**Innovation:**
Les alertes ne sont PAS stockées en base de données.
Elles sont calculées en temps réel à partir des données actuelles!

Vous voyez toujours les alertes les plus à jour! 🎯"""

    # Questions sur la messagerie
    if 'message' in message_lower or 'messagerie' in message_lower:
        return """💬 **MESSAGERIE INSTANTANÉE**

**Comment envoyer un message:**
1️⃣ Cliquez sur "Messagerie" dans le menu
2️⃣ Cliquez sur "+ Nouveau message"
3️⃣ Sélectionnez le destinataire
4️⃣ Tapez votre message
5️⃣ Appuyez sur Envoyer ✉️

**Groupes de discussion:**
- Créer un groupe: "+ Nouveau groupe"
- Nommez le groupe
- Ajoutez des membres
- Discutez en équipe!

**Fonctionnalités:**
✅ Chat 1-1 et groupes
✅ Notifications en temps réel
✅ Historique complet
✅ Recherche de messages
✅ Indicateur "en ligne"
✅ Messages non lus marqués

**Icônes:**
👤 Chat individuel
👥 Groupe de discussion

Tapez votre message et communiquez avec votre équipe!"""

    # Questions pour l'admin
    if user_role == 'admin':
        if 'utilisateur' in message_lower or 'user' in message_lower:
            return """👥 **GESTION DES UTILISATEURS (Admin)**

**Comment créer un utilisateur:**
1️⃣ Page "Utilisateurs" → "+ Ajouter un utilisateur"
2️⃣ Remplir les informations:
   - Nom complet
   - Email (sera l'identifiant)
   - Rôle (voir ci-dessous)
   - Téléphone
3️⃣ Mot de passe généré automatiquement
4️⃣ Enregistrer

**Rôles disponibles:**
🔑 **Admin:** Accès complet au système
📋 **Responsable Patrimoine:** Gestion actifs + maintenances + rapports
👔 **Responsable Service:** Consultation + création maintenances
🔧 **Agent Maintenance:** Exécution maintenances
📊 **Auditeur:** Consultation seule (rapports + statistiques)

**Gestion:**
- Modifier: Cliquez sur l'utilisateur → "Modifier"
- Désactiver: Cliquez sur l'utilisateur → "Désactiver"
- Réactiver: Cliquez sur l'utilisateur → "Activer"
- Supprimer: Cliquez sur l'utilisateur → "Supprimer" (attention!)

**Permissions:**
Chaque rôle a des permissions spécifiques.
Consultez la documentation pour les détails complets."""

    # Réponse par défaut
    return """❓ Je n'ai pas tout à fait compris votre question.

**Essayez de poser une question comme:**
• "Comment créer un actif?"
• "Comment planifier une maintenance?"
• "Comment générer un rapport?"

**Ou tapez simplement:**
• "Aide" → Pour voir toutes les possibilités
• "Actifs" → Pour l'aide sur les actifs
• "Maintenance" → Pour l'aide sur les maintenances
• "Rapport" → Pour l'aide sur les rapports

Je suis là pour vous guider! 🤖"""

@app.route('/api/chatbot', methods=['POST'])
@jwt_required()
def chatbot():
    """Endpoint du chatbot"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    data = request.get_json()
    
    user_message = data.get('message', '')
    bot_response = get_chatbot_response(user_message, user.role)
    
    # Enregistrer le message
    chat_msg = ChatMessage(
        user_id=int(current_user_id),
        message=user_message,
        is_bot_response=True,
        response=bot_response
    )
    
    db.session.add(chat_msg)
    db.session.commit()
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/chatbot/history', methods=['GET'])
@jwt_required()
def get_chatbot_history():
    """Récupérer l'historique du chatbot"""
    current_user_id = get_jwt_identity()
    messages = ChatMessage.query.filter_by(user_id=int(current_user_id)).order_by(ChatMessage.created_at).all()
    
    return jsonify([{
        'id': m.id,
        'message': m.message,
        'response': m.response,
        'created_at': m.created_at.isoformat()
    } for m in messages]), 200

# ==================== MOBILE - QR CODE ====================

@app.route('/api/assets/qr/<qr_code>', methods=['GET'])
def get_asset_by_qr(qr_code):
    """Récupérer un actif par QR Code (sans authentification)"""
    asset = Asset.query.filter_by(qr_code=qr_code).first()
    
    if not asset:
        return jsonify({'error': 'Actif non trouvé'}), 404
    
    return jsonify({
        'id': asset.id,
        'name': asset.name,
        'category': asset.category,
        'description': asset.description,
        'acquisition_date': asset.acquisition_date.isoformat() if asset.acquisition_date else None,
        'acquisition_value': asset.acquisition_value,
        'current_value': asset.current_value,
        'location': asset.location,
        'status': asset.status,
        'assigned_to': asset.assigned_to,
        'qr_code': asset.qr_code,
        'created_at': asset.created_at.isoformat()
    }), 200

@app.route('/api/users/qr/<qr_code>', methods=['GET'])
def get_user_by_qr(qr_code):
    """Récupérer un utilisateur par QR Code (sans authentification)"""
    user = User.query.filter_by(qr_code=qr_code).first()
    
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'full_name': user.full_name,
        'email': user.email,
        'role': user.role,
        'qr_code': user.qr_code,
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/qr-codes', methods=['GET'])
def get_all_qr_codes():
    """Récupérer tous les QR codes des utilisateurs"""
    try:
        users = User.query.filter(User.qr_code.isnot(None)).all()
        qr_codes = []
        
        for user in users:
            qr_codes.append({
                'username': user.username,
                'full_name': user.full_name,
                'qr_code': user.qr_code,
                'qr_image_url': f'/qr_codes/qr_{user.username}_{user.qr_code}.png',
                'scan_url': f'http://localhost:3000/qr-scanner?code={user.qr_code}'
            })
        
        return jsonify(qr_codes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/qr_codes/<filename>')
def serve_qr_code(filename):
    """Servir les images QR codes"""
    return send_from_directory(QR_CODES_FOLDER, filename)

# ==================== GROUPS MANAGEMENT ====================

@app.route('/api/groups/test', methods=['GET'])
def get_groups_test():
    """Récupérer tous les groupes (TEST - sans JWT)"""
    try:
        groups = Group.query.all()
        return jsonify([{
            'id': g.id,
            'name': g.name,
            'description': g.description,
            'created_by': g.created_by,
            'members_count': len(g.members),
            'created_at': g.created_at.isoformat()
        } for g in groups]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups', methods=['GET'])
@jwt_required()
def get_groups():
    """Récupérer les groupes dont l'utilisateur est membre"""
    try:
        current_user_id = get_jwt_identity()
        user = db.session.get(User, int(current_user_id))
        
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        # Retourner SEULEMENT les groupes dont l'utilisateur est membre
        user_groups = user.groups  # Relation many-to-many définie dans le modèle
        
        print(f"👥 Groupes de l'utilisateur {user.full_name} (ID:{current_user_id}): {len(user_groups)} groupe(s)")
        
        return jsonify([{
            'id': g.id,
            'name': g.name,
            'description': g.description,
            'created_by': g.created_by,
            'members_count': len(g.members),
            'created_at': g.created_at.isoformat()
        } for g in user_groups]), 200
    except Exception as e:
        print(f"❌ Erreur get_groups: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    """Récupérer un groupe spécifique"""
    try:
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        return jsonify({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'created_by': group.created_by,
            'members': [{
                'id': m.id, 
                'username': m.username, 
                'full_name': m.full_name,
                'profile_image': m.profile_image,
                'role': m.role
            } for m in group.members],
            'created_at': group.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['PUT'])
@jwt_required()
def update_group(group_id):
    """Modifier un groupe"""
    try:
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        data = request.get_json()
        group.name = data.get('name', group.name)
        group.description = data.get('description', group.description)
        
        db.session.commit()
        return jsonify({'message': 'Groupe mis à jour'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
@jwt_required()
def delete_group(group_id):
    """Supprimer un groupe (seul le créateur ou un admin peut supprimer)"""
    try:
        current_user_id = get_jwt_identity()
        group = db.session.get(Group, group_id)
        
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        user = db.session.get(User, int(current_user_id))
        
        # Vérifier si l'utilisateur est le créateur ou un admin
        is_creator = group.created_by == int(current_user_id)
        is_admin = user and user.role == 'admin'
        
        if not (is_creator or is_admin):
            return jsonify({'error': 'Vous n\'avez pas la permission de supprimer ce groupe'}), 403
        
        print(f"🗑️ Suppression groupe ID:{group_id} par utilisateur:{current_user_id}")
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({'message': 'Groupe supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur suppression groupe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>/leave', methods=['POST'])
@jwt_required()
def leave_group(group_id):
    """Quitter un groupe"""
    try:
        current_user_id = get_jwt_identity()
        group = db.session.get(Group, group_id)
        
        if not group:
            print(f"❌ Groupe {group_id} non trouvé")
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        user = db.session.get(User, int(current_user_id))
        if user not in group.members:
            print(f"❌ Utilisateur {current_user_id} n'est pas membre du groupe {group_id}")
            return jsonify({'error': 'Vous n\'êtes pas membre de ce groupe'}), 400
        
        print(f"👋 Utilisateur {user.full_name} (ID:{current_user_id}) quitte le groupe '{group.name}' (ID:{group_id})")
        group.members.remove(user)
        db.session.commit()
        
        return jsonify({'message': 'Vous avez quitté le groupe avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur quitter groupe: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== MESSAGES MANAGEMENT ====================

@app.route('/api/messages', methods=['POST'])
@jwt_required()
def create_message():
    """Envoyer un nouveau message"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        message = Message(
            sender_id=int(current_user_id),
            recipient_id=data['recipient_id'],
            content=data['content'],
            subject=data.get('subject', '')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'id': message.id,
            'sender_id': message.sender_id,
            'recipient_id': message.recipient_id,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'is_read': message.is_read
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Supprimer un message"""
    try:
        current_user_id = get_jwt_identity()
        message = db.session.get(Message, message_id)
        
        if not message:
            return jsonify({'error': 'Message non trouvé'}), 404
        
        # Vérifier que l'utilisateur est l'expéditeur
        if message.sender_id != int(current_user_id):
            return jsonify({'error': 'Non autorisé'}), 403
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({'message': 'Message supprimé'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
@jwt_required()
def delete_conversation(conversation_id):
    """Supprimer une conversation (tous les messages entre deux utilisateurs)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Parser l'ID de conversation (format: "user1-user2")
        if '-' in conversation_id:
            user_ids = conversation_id.split('-')
            user1_id, user2_id = int(user_ids[0]), int(user_ids[1])
            
            # Vérifier que l'utilisateur actuel fait partie de la conversation
            if int(current_user_id) not in [user1_id, user2_id]:
                return jsonify({'error': 'Non autorisé'}), 403
            
            # Supprimer tous les messages entre ces deux utilisateurs
            messages = Message.query.filter(
                ((Message.sender_id == user1_id) & (Message.recipient_id == user2_id)) |
                ((Message.sender_id == user2_id) & (Message.recipient_id == user1_id))
            ).all()
            
            for message in messages:
                db.session.delete(message)
            
            db.session.commit()
            return jsonify({'message': f'Conversation supprimée ({len(messages)} messages)'}), 200
        else:
            return jsonify({'error': 'Format de conversation invalide'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups', methods=['POST'])
@jwt_required()
def create_group():
    """Créer un nouveau groupe"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        group = Group(
            name=data['name'],
            description=data.get('description', ''),
            created_by=int(current_user_id)
        )
        
        # Ajouter le créateur comme membre
        creator = db.session.get(User, int(current_user_id))
        group.members.append(creator)
        
        # Ajouter les autres membres
        if 'member_ids' in data:
            for member_id in data['member_ids']:
                member = db.session.get(User, member_id)
                if member and member not in group.members:
                    group.members.append(member)
        
        db.session.add(group)
        db.session.commit()
        
        return jsonify({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'members_count': len(group.members),
            'created_at': group.created_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>/messages', methods=['POST'])
@jwt_required()
def send_group_message(group_id):
    """Envoyer un message à un groupe"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Vérifier que le groupe existe
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        # Vérifier que l'utilisateur est membre du groupe
        user = db.session.get(User, int(current_user_id))
        if user not in group.members:
            return jsonify({'error': 'Vous n\'êtes pas membre de ce groupe'}), 403
        
        # Créer le message (note: actuellement les messages sont 1-à-1)
        # Pour les groupes, on pourrait créer un message pour chaque membre
        # Ou créer une nouvelle table GroupMessage
        # Pour l'instant, on simule en créant un message marqué comme groupe
        
        message = Message(
            sender_id=int(current_user_id),
            recipient_id=group_id,  # Utiliser l'ID du groupe comme recipient
            subject=f'Message groupe: {group.name}',
            content=data['content']
        )
        
        db.session.add(message)
        db.session.commit()
        
        print(f"✅ Message groupe envoyé: groupe_id={group_id}, sender={current_user_id}, sender_name={user.full_name}")
        
        return jsonify({
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_name': user.full_name,  # Ajouter le nom de l'expéditeur
            'group_id': group_id,
            'content': message.content,
            'created_at': message.created_at.isoformat(),
            'message': 'Message envoyé au groupe'
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur envoi message groupe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>/messages', methods=['GET'])
@jwt_required()
def get_group_messages(group_id):
    """Récupérer les messages d'un groupe"""
    try:
        current_user_id = get_jwt_identity()
        
        # Vérifier que le groupe existe
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        # Vérifier que l'utilisateur est membre
        user = db.session.get(User, int(current_user_id))
        if user not in group.members:
            return jsonify({'error': 'Vous n\'êtes pas membre de ce groupe'}), 403
        
        # Récupérer les messages du groupe
        messages = Message.query.filter_by(recipient_id=group_id).order_by(Message.created_at.desc()).all()
        
        result = []
        for msg in messages:
            sender = db.session.get(User, msg.sender_id)
            result.append({
                'id': msg.id,
                'sender_id': msg.sender_id,
                'sender_name': sender.full_name if sender else 'Utilisateur',
                'content': msg.content,
                'created_at': msg.created_at.isoformat()
            })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"❌ Erreur récupération messages groupe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>/members', methods=['POST'])
@jwt_required()
def add_group_member(group_id):
    """Ajouter un membre à un groupe"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        # Vérifier que l'utilisateur actuel est membre ou créateur
        user = db.session.get(User, int(current_user_id))
        if user not in group.members:
            return jsonify({'error': 'Vous n\'êtes pas membre de ce groupe'}), 403
        
        # Ajouter le nouveau membre
        new_member_id = data.get('user_id')
        new_member = db.session.get(User, new_member_id)
        
        if not new_member:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        
        if new_member in group.members:
            return jsonify({'error': 'Cet utilisateur est déjà membre'}), 400
        
        group.members.append(new_member)
        db.session.commit()
        
        return jsonify({
            'message': f'{new_member.full_name} ajouté au groupe',
            'members_count': len(group.members)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== STATISTICS ====================

@app.route('/api/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    total_assets = Asset.query.count()
    active_assets = Asset.query.filter_by(status='actif').count()
    total_value = db.session.query(db.func.sum(Asset.current_value)).scalar() or 0
    
    categories = db.session.query(Asset.category, db.func.count(Asset.id)).group_by(Asset.category).all()
    
    return jsonify({
        'total_assets': total_assets,
        'active_assets': active_assets,
        'total_value': total_value,
        'by_category': [{'category': c[0], 'count': c[1]} for c in categories]
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Ressource non trouvée'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur serveur'}), 500

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({'error': 'Token invalide ou manquant'}), 401

# JWT Error Handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({'error': 'Token expiré'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Token invalide'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Token manquant'}), 401

# ==================== SCHEDULER AUTOMATIQUE POUR ALERTES ====================

def scheduled_alert_generation():
    """
    Fonction appelée périodiquement par le scheduler pour générer les alertes
    """
    with app.app_context():
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Génération automatique des alertes...")
            alerts_created, alerts_updated = generate_and_update_alerts()
            print(f"✅ Scheduler: {alerts_created} créées, {alerts_updated} mises à jour\n")
        except Exception as e:
            print(f"❌ Erreur scheduler alertes: {e}\n")

# Créer et configurer le scheduler
scheduler = BackgroundScheduler()

# Générer les alertes toutes les 5 minutes
scheduler.add_job(
    func=scheduled_alert_generation,
    trigger="interval",
    minutes=5,
    id='alert_generation_job',
    name='Génération automatique des alertes',
    replace_existing=True
)

# Démarrer le scheduler
scheduler.start()
print("\n🤖 SCHEDULER AUTOMATIQUE DÉMARRÉ!")
print("📋 Configuration:")
print("   - Génération des alertes: toutes les 5 minutes")
print("   - Première exécution: dans 5 minutes")
print("   - Mode: Arrière-plan (non-bloquant)\n")

# Générer les alertes immédiatement au démarrage
with app.app_context():
    try:
        print("🚀 Génération initiale des alertes au démarrage...")
        alerts_created, alerts_updated = generate_and_update_alerts()
        print(f"✅ Démarrage: {alerts_created} créées, {alerts_updated} mises à jour\n")
    except Exception as e:
        print(f"❌ Erreur génération initiale: {e}\n")

# Arrêter le scheduler proprement à la fermeture de l'application
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

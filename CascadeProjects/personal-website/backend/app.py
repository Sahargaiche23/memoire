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
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    alert_type = db.Column(db.String(50))  # maintenance, garantie, amortissement
    message = db.Column(db.Text)
    due_date = db.Column(db.Date)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Actif supprimé'}), 200

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
        
        db.session.delete(maintenance)
        db.session.commit()
        
        print(f"✅ Maintenance {maintenance_id} supprimée")
        
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

@app.route('/api/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    alerts = Alert.query.all()
    return jsonify([{
        'id': a.id,
        'asset_id': a.asset_id,
        'alert_type': a.alert_type,
        'message': a.message,
        'due_date': a.due_date.isoformat() if a.due_date else None,
        'is_read': a.is_read,
        'created_at': a.created_at.isoformat()
    } for a in alerts]), 200

@app.route('/api/alerts/<int:alert_id>/read', methods=['PUT'])
@jwt_required()
def mark_alert_read(alert_id):
    alert = db.session.get(Alert, alert_id)
    if not alert:
        return jsonify({'error': 'Alerte non trouvée'}), 404
    
    alert.is_read = True
    db.session.commit()
    return jsonify({'message': 'Alerte marquée comme lue'}), 200

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
    """Générer une réponse du chatbot"""
    message_lower = user_message.lower()
    
    # Réponses du chatbot selon le rôle
    responses = {
        'admin': {
            'utilisateur': 'Pour gérer les utilisateurs, allez à la page Utilisateurs et cliquez sur "+ Ajouter un utilisateur".',
            'rôle': 'Les rôles disponibles sont: Admin, Responsable Patrimoine, Responsable Service, Agent Maintenance, Auditeur.',
            'permission': 'Les permissions dépendent du rôle de l\'utilisateur. Consultez ROLE_MANAGEMENT.md pour plus de détails.',
            'aide': 'Je peux vous aider avec: utilisateurs, rôles, permissions, actifs, maintenances, rapports.'
        },
        'responsable_patrimoine': {
            'actif': 'Pour créer un actif, allez à la page Actifs et cliquez sur "+ Ajouter un actif".',
            'maintenance': 'Pour planifier une maintenance, allez à la page Maintenance et cliquez sur "+ Planifier".',
            'rapport': 'Pour générer un rapport, allez à la page Rapports et sélectionnez les paramètres.',
            'aide': 'Je peux vous aider avec: actifs, maintenances, rapports, mouvements.'
        },
        'agent_maintenance': {
            'intervention': 'Pour enregistrer une intervention, allez à la page Maintenance et mettez à jour le statut.',
            'maintenance': 'Consultez la liste des maintenances planifiées pour vous.',
            'aide': 'Je peux vous aider avec: interventions, maintenances, actifs.'
        },
        'auditeur': {
            'rapport': 'Pour consulter les rapports, allez à la page Rapports.',
            'statistique': 'Les statistiques sont disponibles sur le Tableau de Bord.',
            'aide': 'Je peux vous aider avec: rapports, statistiques, alertes.'
        }
    }
    
    # Réponses générales
    general_responses = {
        'bonjour': 'Bonjour! Comment puis-je vous aider?',
        'salut': 'Salut! Que puis-je faire pour vous?',
        'aide': 'Je suis un assistant virtuel. Je peux vous aider avec les fonctionnalités du système.',
        'merci': 'De rien! N\'hésitez pas à me poser d\'autres questions.',
        'comment': 'Pouvez-vous être plus spécifique? Que voulez-vous faire?',
        'quoi': 'Je peux vous aider avec les fonctionnalités du système. Que voulez-vous savoir?'
    }
    
    # Chercher une réponse spécifique au rôle
    role_responses = responses.get(user_role, {})
    for keyword, response in role_responses.items():
        if keyword in message_lower:
            return response
    
    # Chercher une réponse générale
    for keyword, response in general_responses.items():
        if keyword in message_lower:
            return response
    
    # Réponse par défaut
    return 'Je n\'ai pas compris votre question. Pouvez-vous reformuler? Tapez "aide" pour voir ce que je peux faire.'

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
    """Récupérer tous les groupes"""
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
            'members': [{'id': m.id, 'username': m.username, 'full_name': m.full_name} for m in group.members],
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
    """Supprimer un groupe"""
    try:
        group = db.session.get(Group, group_id)
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': 'Groupe supprimé'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/groups/<int:group_id>/leave', methods=['POST'])
@jwt_required()
def leave_group(group_id):
    """Quitter un groupe"""
    try:
        current_user_id = get_jwt_identity()
        group = db.session.get(Group, group_id)
        
        if not group:
            return jsonify({'error': 'Groupe non trouvé'}), 404
        
        user = db.session.get(User, int(current_user_id))
        if user not in group.members:
            return jsonify({'error': 'Vous n\'êtes pas membre de ce groupe'}), 400
        
        group.members.remove(user)
        db.session.commit()
        
        return jsonify({'message': 'Vous avez quitté le groupe'}), 200
    except Exception as e:
        db.session.rollback()
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

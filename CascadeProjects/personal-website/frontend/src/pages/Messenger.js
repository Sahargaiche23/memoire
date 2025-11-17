import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import CallModal from './CallModal';
import { Send, Search, Plus, Phone, Video, MoreVertical, Smile, X, Users, Heart, Share2, Paperclip, Image as ImageIcon, Download, Eye } from 'lucide-react';
import './Messenger.css';

function Messenger({ user, onLogout }) {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showNewChat, setShowNewChat] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [showGroupCreate, setShowGroupCreate] = useState(false);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [groupName, setGroupName] = useState('');
  const [groups, setGroups] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [contextMenu, setContextMenu] = useState(null);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const [activeCall, setActiveCall] = useState(null);
  const [callType, setCallType] = useState(null);
  const [callHistory, setCallHistory] = useState([]);
  const [incomingCall, setIncomingCall] = useState(null);
  const imageInputRef = useRef(null);
  const fileInputRef = useRef(null);
  const callCheckInterval = useRef(null);  // ✅ Pour gérer le polling des appels
  const token = localStorage.getItem('token');

  const emojis = ['😀', '😂', '❤️', '👍', '🎉', '🔥', '✨', '👏', '🙌', '💯', '😍', '🤔', '😢', '😡', '🤮', '😎'];

  useEffect(() => {
    // Charger les données une seule fois au montage
    fetchConversations();
    fetchUsers();
    fetchGroups();
    
    // Vérifier les appels entrants via le serveur
    const checkIncomingCalls = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/calls/check/${user.id}`);
        if (response.data && response.data.length > 0) {
          const call = response.data[0];
          setIncomingCall({
            from: call.caller_name,
            fromId: call.caller_id,  // ✅ Ajout de l'ID de l'appelant
            type: call.type,
            timestamp: new Date().toLocaleTimeString(),
            callId: call.call_id
          });
          
          console.log('📞 Appel entrant de:', call.caller_name, 'ID:', call.caller_id);
          
          // Notification système
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`Appel ${call.type === 'video' ? 'vidéo' : 'vocal'} de ${call.caller_name}`, {
              icon: '📞',
              badge: '📞',
              tag: 'incoming-call',
              requireInteraction: true
            });
            
            // Son de notification
            const audio = new Audio('data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAA==');
            audio.play().catch(e => console.log('Son non disponible'));
          }
        }
      } catch (e) {
        console.error('Erreur vérification appels:', e);
      }
    };
    
    // Demander la permission de notification
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
    
    // Vérifier les appels toutes les 2 secondes
    callCheckInterval.current = setInterval(checkIncomingCalls, 2000);
    
    return () => {
      if (callCheckInterval.current) {
        clearInterval(callCheckInterval.current);
      }
    };
  }, [user.id]);

  useEffect(() => {
    if (selectedConversation || selectedUser) {
      fetchMessages();
    }
  }, [selectedConversation, selectedUser]);

  const fetchConversations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/messages/test');
      
      if (!response.data || !Array.isArray(response.data) || response.data.length === 0) {
        setConversations([]);
        setLoading(false);
        return;
      }

      const grouped = {};
      response.data.forEach(msg => {
        try {
          // Créer une clé unique pour chaque paire d'utilisateurs
          const otherUserId = msg.sender_id === user.id ? msg.recipient_id : msg.sender_id;
          const key = `${Math.min(user.id, otherUserId)}-${Math.max(user.id, otherUserId)}`;
          
          if (!grouped[key]) {
            // Déterminer le nom de l'autre utilisateur
            const otherUserName = msg.sender_id === user.id ? 
              (msg.recipient_name || 'Utilisateur') : 
              (msg.sender_name || 'Utilisateur');
            
            grouped[key] = {
              id: key,
              lastMessage: msg,
              messages: [msg],
              otherUserId: otherUserId,
              otherUserName: otherUserName,
              type: 'direct'
            };
          } else {
            grouped[key].messages.push(msg);
            // Mettre à jour le dernier message si plus récent
            if (new Date(msg.created_at) > new Date(grouped[key].lastMessage.created_at)) {
              grouped[key].lastMessage = msg;
            }
          }
        } catch (e) {
          console.error('Erreur traitement message:', e);
        }
      });

      const sortedConversations = Object.values(grouped).sort((a, b) => 
        new Date(b.lastMessage.created_at) - new Date(a.lastMessage.created_at)
      );

      setConversations(sortedConversations);
    } catch (err) {
      console.error('Erreur fetchConversations:', err.message);
      setConversations([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async () => {
    try {
      if (!selectedConversation && !selectedUser) {
        setMessages([]);
        return;
      }

      const response = await axios.get('http://localhost:5000/api/messages/test');
      if (Array.isArray(response.data)) {
        // Filtrer les messages pour la conversation sélectionnée
        let filteredMessages = response.data;
        
        if (selectedUser) {
          const userId1 = Math.min(user.id, selectedUser.id);
          const userId2 = Math.max(user.id, selectedUser.id);
          filteredMessages = response.data.filter(m => {
            const msgUserId1 = Math.min(m.sender_id, m.recipient_id);
            const msgUserId2 = Math.max(m.sender_id, m.recipient_id);
            return msgUserId1 === userId1 && msgUserId2 === userId2;
          });
        }
        
        setMessages(filteredMessages);
      } else {
        setMessages([]);
      }
    } catch (err) {
      console.error('Erreur fetchMessages:', err.message);
      setMessages([]);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (Array.isArray(response.data)) {
        setUsers(response.data.filter(u => u.id !== user.id));
      } else {
        setUsers([]);
      }
    } catch (err) {
      console.error('Erreur fetchUsers:', err.message);
      setUsers([]);
    }
  };

  const fetchGroups = async () => {
    try {
      if (!token) {
        console.warn('Pas de token JWT, utilisation des données de démonstration');
        setGroups([
          { id: 1, name: 'Équipe Patrimoine', members: 5, avatar: 'E' },
          { id: 2, name: 'Maintenance', members: 3, avatar: 'M' },
          { id: 3, name: 'Direction', members: 2, avatar: 'D' }
        ]);
        return;
      }

      // Appeler le backend pour récupérer les groupes
      const response = await axios.get('http://localhost:5000/api/groups');
      
      // Vérifier si la réponse contient des données
      if (response.data && Array.isArray(response.data)) {
        // Transformer les données pour le frontend
        const groupsData = response.data.map(g => ({
          id: g.id,
          name: g.name || 'Groupe sans nom',
          members: g.members_count || 0,
          avatar: (g.name || 'G').charAt(0).toUpperCase()
        }));
        
        setGroups(groupsData);
        console.log('✅ Groupes chargés depuis le backend:', groupsData);
      } else {
        throw new Error('Réponse invalide du serveur');
      }
    } catch (e) {
      console.error('Erreur fetchGroups:', e.response?.data || e.message);
      // Données de démonstration en cas d'erreur
      setGroups([
        { id: 1, name: 'Équipe Patrimoine', members: 5, avatar: 'E' },
        { id: 2, name: 'Maintenance', members: 3, avatar: 'M' },
        { id: 3, name: 'Direction', members: 2, avatar: 'D' }
      ]);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    // Pour les groupes
    if (selectedConversation?.type === 'group') {
      const newMsg = {
        id: messages.length + 1,
        sender_id: user.id,
        recipient_id: selectedConversation.group.id,
        content: newMessage,
        created_at: new Date().toISOString(),
        sender_name: user.full_name || 'Vous'
      };
      setMessages([...messages, newMsg]);
      setNewMessage('');
      setShowEmojiPicker(false);
      return;
    }

    // Pour les conversations directes
    const recipientId = selectedUser?.id || (selectedConversation?.lastMessage.sender_id === user.id ?
      selectedConversation.lastMessage.recipient_id :
      selectedConversation.lastMessage.sender_id);

    if (!recipientId) return;

    try {
      const messageData = {
        recipient_id: recipientId,
        subject: 'Message',
        content: newMessage
      };

      await axios.post('http://localhost:5000/api/messages', messageData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setNewMessage('');
      setShowEmojiPicker(false);
      await fetchConversations();
      await fetchMessages();
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const startNewChat = (selectedUser) => {
    setSelectedUser(selectedUser);
    setSelectedConversation(null);
    setShowNewChat(false);
    setSearchTerm('');
  };

  const createGroup = async () => {
    if (!groupName.trim()) {
      alert('Veuillez entrer un nom de groupe');
      return;
    }
    if (selectedUsers.length === 0) {
      alert('Veuillez sélectionner au moins un membre');
      return;
    }

    try {
      // Appeler l'endpoint backend
      const response = await axios.post('http://localhost:5000/api/groups', {
        name: groupName,
        description: `Groupe créé par ${user.full_name}`,
        member_ids: selectedUsers
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      // Ajouter le nouveau groupe à la liste
      const newGroup = {
        id: response.data.id,
        name: response.data.name,
        members: response.data.members_count,
        avatar: response.data.name.charAt(0).toUpperCase()
      };

      setGroups([...groups, newGroup]);
      setConversations([...conversations, {
        id: `group-${newGroup.id}`,
        lastMessage: {
          sender_id: user.id,
          sender_name: 'Vous',
          content: `Groupe "${groupName}" créé`,
          created_at: new Date().toISOString()
        },
        type: 'group',
        group: newGroup
      }]);
      setGroupName('');
      setSelectedUsers([]);
      setShowGroupCreate(false);
      alert('✅ Groupe créé avec succès!');
    } catch (e) {
      console.error('Erreur création groupe:', e);
      alert('❌ Erreur lors de la création du groupe');
    }
  };

  const deleteConversation = async (convId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer cette conversation?')) {
      try {
        // Si c'est un groupe, utiliser l'endpoint DELETE group
        if (convId.toString().startsWith('group-')) {
          const groupId = convId.replace('group-', '');
          await axios.delete(`http://localhost:5000/api/groups/${groupId}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          // Supprimer le groupe de la liste
          setGroups(prevGroups => prevGroups.filter(g => g.id !== parseInt(groupId)));
        } else {
          // Pour les conversations privées, utiliser l'endpoint DELETE conversation
          await axios.delete(`http://localhost:5000/api/conversations/${convId}`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
        }
        
        // Supprimer la conversation de la liste
        setConversations(prevConversations => {
          return prevConversations.filter(c => c.id !== convId);
        });
        
        // Fermer le chat si c'est la conversation sélectionnée
        if (selectedConversation?.id === convId) {
          setSelectedConversation(null);
          setSelectedUser(null);
        }
        
        // Rafraîchir les messages
        await fetchMessages();
        
        alert('✅ Conversation supprimée avec succès!');
      } catch (e) {
        console.error('Erreur suppression conversation:', e);
        alert('❌ Erreur lors de la suppression');
      }
    }
  };

  const deleteMessage = async (messageId) => {
    if (window.confirm('Êtes-vous sûr de vouloir supprimer ce message?')) {
      try {
        // Appeler l'endpoint backend
        await axios.delete(`http://localhost:5000/api/messages/${messageId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Supprimer le message de la liste locale
        const updated = messages.filter(m => m.id !== messageId);
        setMessages(updated);
        
        alert('✅ Message supprimé avec succès!');
      } catch (e) {
        console.error('Erreur suppression message:', e);
        alert('❌ Erreur lors de la suppression du message');
      }
    }
  };

  const leaveGroup = async (groupId) => {
    if (window.confirm('Êtes-vous sûr de vouloir quitter ce groupe?')) {
      try {
        // Appeler l'endpoint backend
        await axios.post(`http://localhost:5000/api/groups/${groupId}/leave`, {}, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Supprimer le groupe de la liste
        setGroups(prevGroups => prevGroups.filter(g => g.id !== groupId));
        
        // Supprimer la conversation du groupe
        setConversations(prevConversations => {
          return prevConversations.filter(c => c.id !== `group-${groupId}`);
        });
        
        // Fermer le chat
        setSelectedConversation(null);
        setSelectedUser(null);
        
        alert('✅ Vous avez quitté le groupe!');
      } catch (e) {
        console.error('Erreur quitter groupe:', e);
        alert('❌ Erreur lors de la suppression du groupe');
      }
    }
  };

  const initiateCall = async (type) => {
    if (!currentRecipient) {
      alert('Veuillez sélectionner une conversation');
      return;
    }
    
    const callType = type === 'video' ? 'Appel vidéo' : 'Appel vocal';
    const timestamp = new Date().toLocaleTimeString();
    
    // Enregistrer dans l'historique
    const callRecord = {
      id: callHistory.length + 1,
      caller: user.full_name,
      recipient: currentRecipient.full_name,
      type: type,
      duration: 0,
      timestamp: timestamp,
      date: new Date().toLocaleDateString(),
      status: 'incoming'
    };
    
    setCallHistory([...callHistory, callRecord]);
    
    // Notifier le destinataire avec notification native
    if ('Notification' in window && Notification.permission === 'granted') {
      const notification = new Notification(`${callType} de ${user.full_name}`, {
        icon: '📞',
        badge: '📞',
        tag: 'incoming-call',
        requireInteraction: true,
        actions: [
          { action: 'accept', title: '✅ Accepter' },
          { action: 'reject', title: '❌ Refuser' }
        ]
      });
      
      // Jouer un son de notification
      const audio = new Audio('data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAA==');
      audio.play().catch(e => console.log('Son non disponible'));
      
      notification.onclick = () => {
        setCallType(type);
        setActiveCall(currentRecipient.full_name);
        setIncomingCall(null);
        notification.close();
      };
    } else if ('Notification' in window && Notification.permission !== 'denied') {
      // Demander la permission
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          new Notification(`${callType} de ${user.full_name}`, {
            icon: '📞',
            requireInteraction: true
          });
        }
      });
    }
    
    // Envoyer l'appel au destinataire via le serveur
    try {
      await axios.post('http://localhost:5000/api/calls/initiate', {
        caller_id: user.id,
        caller_name: user.full_name,
        recipient_id: currentRecipient.id,
        type: type
      });
    } catch (e) {
      console.error('Erreur envoi appel:', e);
    }
    
    // Notifier le destinataire dans l'app (même navigateur)
    setIncomingCall({
      from: user.full_name,
      fromId: user.id,  // ✅ Ajout de l'ID pour cohérence
      type: type,
      timestamp: timestamp,
      callId: callRecord.id
    });
    
    // Simuler la notification pour le destinataire après 2 secondes
    setTimeout(() => {
      setCallType(type);
      setActiveCall(currentRecipient.full_name);
      setIncomingCall(null);
    }, 2000);
  };

  const logCallInMessages = async (duration, isMissed = false, type = 'audio', specificRecipientId = null) => {
    // Enregistrer l'appel dans les messages
    try {
      const typeCall = type || 'audio';
      const status = isMissed ? 'manqué' : '';
      const callText = `📞 Appel ${typeCall === 'video' ? 'vidéo' : 'vocal'} ${status} - ${duration}s`;
      
      // Utiliser le destinataire spécifique ou le destinataire actuel
      const recipientId = specificRecipientId || (currentRecipient ? currentRecipient.id : null);
      
      if (!recipientId) {
        console.error('Pas de destinataire pour enregistrer l\'appel');
        return;
      }
      
      // Créer un message local d'abord
      const newMsg = {
        id: messages.length + 1,
        sender_id: user.id,
        recipient_id: recipientId,
        content: callText,
        created_at: new Date().toISOString(),
        is_read: false
      };
      
      // Mettre à jour les messages seulement si c'est la conversation actuelle
      if (currentRecipient && currentRecipient.id === recipientId) {
        setMessages([...messages, newMsg]);
      }
      
      // Envoyer au serveur
      await axios.post('http://localhost:5000/api/calls/log', {
        caller_id: user.id,
        recipient_id: recipientId,
        type: typeCall,
        duration: duration,
        status: isMissed ? 'missed' : 'completed'
      });
      
      console.log(`✅ Appel enregistré avec destinataire ID: ${recipientId}`);
    } catch (e) {
      console.error('Erreur enregistrement appel:', e);
    }
  };

  // Exposer la fonction globalement pour CallModal
  React.useEffect(() => {
    window.logCallInMessages = logCallInMessages;
  }, [logCallInMessages]);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type.startsWith('image/')) {
      try {
        // Convertir l'image en Base64
        const reader = new FileReader();
        reader.onload = () => {
          const base64String = reader.result;
          // Ajouter l'image Base64 au message
          setNewMessage(newMessage + `\n[IMAGE:${base64String}]`);
          console.log('✅ Image convertie en Base64');
        };
        reader.onerror = (error) => {
          console.error('❌ Erreur lecture fichier:', error);
          alert('❌ Erreur lors de la lecture de l\'image');
        };
        reader.readAsDataURL(file);
      } catch (error) {
        console.error('❌ Erreur upload image:', error);
        alert('❌ Erreur lors de l\'upload de l\'image');
      }
    } else {
      // Si ce n'est pas une image, suggérer d'utiliser le bouton fichier
      alert(`❌ "${file.name}" n'est pas une image.\n\n💡 Pour envoyer des fichiers (PDF, Word, etc.), utilisez le bouton 📎 (trombone) à gauche.`);
      e.target.value = ''; // Reset input
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        // Vérifier la taille (limite à 10 MB)
        const maxSize = 10 * 1024 * 1024; // 10 MB
        if (file.size > maxSize) {
          alert('❌ Fichier trop volumineux! Maximum 10 MB');
          return;
        }

        // Convertir le fichier en Base64
        const reader = new FileReader();
        reader.onload = () => {
          const base64String = reader.result;
          // Stocker le fichier avec nom, type et contenu Base64
          setNewMessage(newMessage + `\n[FILE:${file.name}|${file.type}|${base64String}]`);
          console.log('✅ Fichier converti en Base64:', file.name, 'Type:', file.type, 'Taille:', (file.size/1024).toFixed(2), 'KB');
        };
        reader.onerror = (error) => {
          console.error('❌ Erreur lecture fichier:', error);
          alert('❌ Erreur lors de la lecture du fichier');
        };
        reader.readAsDataURL(file);
      } catch (error) {
        console.error('❌ Erreur upload fichier:', error);
        alert('❌ Erreur lors de l\'upload du fichier');
      }
    }
  };

  const handleUserSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    if (term) {
      setFilteredUsers(users.filter(u => 
        u.full_name.toLowerCase().includes(term) ||
        u.email.toLowerCase().includes(term)
      ));
    } else {
      setFilteredUsers(users);
    }
  };

  const getOtherUserName = (conv) => {
    if (!conv) return 'Utilisateur';
    if (conv.type === 'group') return conv.group?.name || 'Groupe';
    
    // Utiliser la nouvelle structure avec otherUserName
    if (conv.otherUserName) {
      return conv.otherUserName;
    }
    
    // Fallback pour l'ancienne structure
    if (conv.lastMessage) {
      const otherName = conv.lastMessage.sender_id === user.id ? 
        (conv.lastMessage.recipient_name || 'Utilisateur') : 
        (conv.lastMessage.sender_name || 'Utilisateur');
      
      // Chercher l'utilisateur dans la liste pour obtenir le nom complet
      const otherUserId = conv.lastMessage.sender_id === user.id ? 
        conv.lastMessage.recipient_id : 
        conv.lastMessage.sender_id;
      const otherUser = users.find(u => u.id === otherUserId);
      
      return otherUser?.full_name || otherName;
    }
    
    return 'Utilisateur';
  };

  const filteredConversations = conversations.filter(conv => {
    try {
      const name = getOtherUserName(conv);
      if (!name) return true;
      return name.toLowerCase().includes(searchTerm.toLowerCase());
    } catch (e) {
      return true;
    }
  });

  const currentRecipient = selectedUser || (selectedConversation && {
    full_name: getOtherUserName(selectedConversation),
    id: selectedConversation.otherUserId || (
      selectedConversation.lastMessage ? (
        selectedConversation.lastMessage.sender_id === user.id ?
          selectedConversation.lastMessage.recipient_id :
          selectedConversation.lastMessage.sender_id
      ) : null
    )
  });

  const getConversationMessages = () => {
    return messages.filter(msg => {
      const isRelevant = (msg.sender_id === user.id && msg.recipient_id === currentRecipient.id) ||
                        (msg.sender_id === currentRecipient.id && msg.recipient_id === user.id);
      return isRelevant;
    });
  };

  const isFileMessage = (content) => {
    return content.includes('📎 Fichier:') || content.includes('📁') || content.includes('[FILE:');
  };

  const extractFileFromContent = (content) => {
    // Nouveau format: [FILE:nom|type|base64]
    let match = content.match(/\[FILE:([^|]+)\|([^|]+)\|([^\]]+)\]/);
    if (match) {
      return {
        name: match[1],
        type: match[2],
        data: match[3]
      };
    }
    
    // Ancien format: [FILE:nom|base64] (sans type)
    match = content.match(/\[FILE:([^|]+)\|([^\]]+)\]/);
    if (match) {
      return {
        name: match[1],
        type: 'application/octet-stream',
        data: match[2]
      };
    }
    
    // Format très ancien: 📎 Fichier: nom
    if (content.includes('📎 Fichier:')) {
      const name = content.replace('📎 Fichier:', '').trim();
      return { name, type: null, data: null };
    }
    
    return null;
  };

  const getFileIcon = (filename, type) => {
    const ext = filename?.split('.').pop()?.toLowerCase();
    
    // Icônes selon l'extension
    if (['pdf'].includes(ext)) return '📄';
    if (['doc', 'docx'].includes(ext)) return '📝';
    if (['xls', 'xlsx'].includes(ext)) return '📊';
    if (['ppt', 'pptx'].includes(ext)) return '📊';
    if (['txt', 'md'].includes(ext)) return '📃';
    if (['zip', 'rar', '7z'].includes(ext)) return '📦';
    if (['mp3', 'wav', 'ogg'].includes(ext)) return '🎵';
    if (['mp4', 'avi', 'mkv'].includes(ext)) return '🎬';
    
    // Icônes selon le type MIME
    if (type?.startsWith('application/pdf')) return '📄';
    if (type?.includes('word') || type?.includes('document')) return '📝';
    if (type?.includes('sheet') || type?.includes('excel')) return '📊';
    if (type?.includes('text')) return '📃';
    if (type?.includes('audio')) return '🎵';
    if (type?.includes('video')) return '🎬';
    
    return '📎'; // Icône par défaut
  };

  const isImageContent = (content) => {
    return content.includes('[IMAGE:') || 
           content.includes('data:image') || 
           content.includes('/api/uploads/') ||
           /\.(jpg|jpeg|png|gif|webp)$/i.test(content);
  };

  const extractImageFromContent = (content) => {
    // Chercher [IMAGE:data:image...] (Base64)
    let match = content.match(/\[IMAGE:(data:image[^\]]+)\]/);
    if (match) {
      console.log('🖼️ Image Base64 trouvée (taille:', match[1].length, 'chars)');
      return match[1];
    }
    
    // Chercher [IMAGE: http://...] (avec espace)
    match = content.match(/\[IMAGE: (.*?)\]/);
    if (match) {
      console.log('🖼️ Image URL trouvée:', match[1].substring(0, 50));
      return match[1];
    }
    
    // Chercher data:image directement
    match = content.match(/(data:image[^,\s]*[^,]*)/);
    if (match) {
      console.log('🖼️ Image data: trouvée');
      return match[1];
    }
    
    // Chercher URL d'image (http://localhost:5000/api/uploads/...)
    match = content.match(/(http:\/\/localhost:5000\/api\/uploads\/[^\s]+\.(jpg|jpeg|png|gif|webp))/i);
    if (match) {
      console.log('🖼️ Image upload trouvée');
      return match[1];
    }
    
    // Chercher URL d'image générale
    match = content.match(/(https?:\/\/[^\s]+\.(jpg|jpeg|png|gif|webp))/i);
    if (match) {
      console.log('🖼️ Image URL générale trouvée');
      return match[1];
    }
    
    return null;
  };

  if (loading) return <div className="loading">Chargement...</div>;

  return (
    <div className="messenger-page">
      <Navbar user={user} onLogout={onLogout} />

      <div className="messenger-main">
        {/* Sidebar */}
        <div className="messenger-sidebar">
          <div className="sidebar-header">
            <h1>💬 Messenger</h1>
            <button className="btn-new-chat" onClick={() => setShowNewChat(!showNewChat)} title="Nouvelle conversation">
              <Plus size={24} />
            </button>
          </div>

          {/* Barre de recherche */}
          <div className="search-box">
            <Search size={18} />
            <input
              type="text"
              placeholder="Rechercher..."
              value={searchTerm}
              onChange={handleUserSearch}
            />
          </div>

          {/* Onglets */}
          <div className="messenger-tabs">
            <button className="tab active">Messages</button>
            <button className="tab" onClick={() => setShowGroupCreate(!showGroupCreate)}>
              👥 Groupes ({groups.length})
            </button>
          </div>

          {/* Nouveau chat */}
          {showNewChat && (
            <div className="new-chat-panel">
              <h3>Nouvelle conversation</h3>
              <div className="users-list">
                {filteredUsers.length === 0 ? (
                  <div className="no-users">Aucun utilisateur trouvé</div>
                ) : (
                  filteredUsers.map(u => (
                    <div
                      key={u.id}
                      className="user-item"
                      onClick={() => startNewChat(u)}
                    >
                      <div className="user-avatar">
                        {u.full_name.charAt(0).toUpperCase()}
                      </div>
                      <div className="user-info">
                        <p className="user-name">{u.full_name}</p>
                        <p className="user-role">{u.role}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Créer groupe */}
          {showGroupCreate && (
            <div className="new-chat-panel">
              <h3>Créer un groupe</h3>
              <input
                type="text"
                placeholder="Nom du groupe"
                value={groupName}
                onChange={(e) => setGroupName(e.target.value)}
                className="group-input"
              />
              <div className="users-list">
                {users.map(u => (
                  <div
                    key={u.id}
                    className={`user-item ${selectedUsers.includes(u.id) ? 'selected' : ''}`}
                    onClick={() => {
                      if (selectedUsers.includes(u.id)) {
                        setSelectedUsers(selectedUsers.filter(id => id !== u.id));
                      } else {
                        setSelectedUsers([...selectedUsers, u.id]);
                      }
                    }}
                  >
                    <div className="user-avatar">
                      {u.full_name.charAt(0).toUpperCase()}
                    </div>
                    <div className="user-info">
                      <p className="user-name">{u.full_name}</p>
                    </div>
                    {selectedUsers.includes(u.id) && <span className="checkmark">✓</span>}
                  </div>
                ))}
              </div>
              <button className="btn-create-group" onClick={createGroup}>
                Créer le groupe
              </button>
            </div>
          )}

          {/* Groupes */}
          {!showNewChat && !showGroupCreate && (
            <div className="groups-section">
              <h3>Groupes</h3>
              {groups.map(group => (
                <div 
                  key={group.id} 
                  className="group-item"
                  onClick={() => {
                    setSelectedConversation({
                      id: `group-${group.id}`,
                      type: 'group',
                      group: group,
                      lastMessage: {
                        sender_id: user.id,
                        sender_name: 'Vous',
                        content: `Groupe "${group.name}"`,
                        created_at: new Date().toISOString()
                      }
                    });
                    setSelectedUser(null);
                  }}
                  onContextMenu={(e) => {
                    e.preventDefault();
                    const rect = e.currentTarget.getBoundingClientRect();
                    setMenuPosition({ x: rect.right, y: rect.bottom });
                    setContextMenu({ id: group.id, type: 'group' });
                  }}
                >
                  <div className="group-avatar">{group.avatar}</div>
                  <div className="group-info">
                    <p className="group-name">{group.name}</p>
                    <p className="group-members">{group.members} membres</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Liste des conversations */}
          <div className="conversations-list">
            {filteredConversations.length === 0 ? (
              <div className="no-conversations">
                <p>Aucune conversation</p>
              </div>
            ) : (
              filteredConversations.map(conv => (
                <div
                  className={`conversation-item ${selectedConversation?.id === conv.id && !selectedUser ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedConversation(conv);
                    setSelectedUser(null);
                  }}
                  onContextMenu={(e) => {
                    e.preventDefault();
                    deleteConversation(conv.id);
                  }}
                >
                  <div className="conversation-avatar">
                    {getOtherUserName(conv).charAt(0).toUpperCase()}
                  </div>
                  <div className="conversation-content">
                    <h4>{getOtherUserName(conv)}</h4>
                    <p>{conv.lastMessage.content.substring(0, 40)}...</p>
                  </div>
                  <span className="conversation-time">
                    {new Date(conv.lastMessage.created_at).toLocaleTimeString()}
                  </span>
                  <button 
                    className="conv-menu-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      if (contextMenu?.id === conv.id) {
                        setContextMenu(null);
                      } else {
                        const rect = e.currentTarget.getBoundingClientRect();
                        setMenuPosition({ x: rect.right, y: rect.bottom });
                        setContextMenu({ id: conv.id });
                      }
                    }}
                  >
                    ⋮
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="messenger-chat">
          {currentRecipient ? (
            <>
              {/* Chat Header */}
              <div className="chat-header">
                <div className="chat-header-info">
                  <div className="recipient-selector">
                    <div className="recipient-avatar">
                      {currentRecipient.full_name.charAt(0).toUpperCase()}
                    </div>
                    <div>
                      <h3>{currentRecipient.full_name}</h3>
                      <p>Actif maintenant</p>
                    </div>
                  </div>
                </div>
                <div className="chat-header-actions">
                  <button className="icon-btn" title="Appel audio" onClick={() => initiateCall('audio')}>
                    <Phone size={20} />
                  </button>
                  <button className="icon-btn" title="Appel vidéo" onClick={() => initiateCall('video')}>
                    <Video size={20} />
                  </button>
                  <button className="icon-btn">
                    <MoreVertical size={20} />
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="chat-messages">
                {getConversationMessages().map(msg => {
                  const imageUrl = extractImageFromContent(msg.content);
                  const isImage = isImageContent(msg.content);
                  const isCall = msg.content.includes('📞 Appel');
                  const isOwnMessage = msg.sender_id === user.id;
                  const senderName = isOwnMessage ? user.full_name : currentRecipient?.full_name || 'Utilisateur';
                  const senderInitial = senderName.charAt(0).toUpperCase();
                  
                  return (
                    <div key={msg.id} className={`message-group ${isOwnMessage ? 'own' : 'other'}`}>
                      {/* Avatar et Nom - Style Facebook (sauf pour appels) */}
                      {!isOwnMessage && !isCall && (
                        <div className="message-header">
                          <div className="avatar" style={{
                            background: '#667eea',
                            color: 'white'
                          }}>
                            {senderInitial}
                          </div>
                          <div className="sender-info">
                            <div className="sender-name">{senderName}</div>
                            <div className="message-time">
                              {new Date(msg.created_at).toLocaleTimeString()}
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {isCall ? (
                        <div className={`call-message-wrapper ${msg.content.includes('manqué') ? 'missed' : ''}`}>
                          <div className={`call-message ${msg.content.includes('manqué') ? 'missed' : ''}`}>
                            <div className={`call-icon ${msg.content.includes('manqué') ? 'missed' : ''}`}>📞</div>
                            <div className="call-content">
                              <p className="call-title">{msg.content}</p>
                              <button className="call-btn">📞 Rappeler</button>
                            </div>
                          </div>
                          <div className="call-meta">
                            <span className="call-sender">{senderName}</span>
                            <span className="call-time">{new Date(msg.created_at).toLocaleTimeString()}</span>
                          </div>
                        </div>
                      ) : (
                        <div
                          className={`message-bubble ${isOwnMessage ? 'sent' : 'received'}`}
                          onMouseEnter={(e) => e.currentTarget.querySelector('.message-actions')?.style.display === 'none' && (e.currentTarget.querySelector('.message-actions').style.display = 'flex')}
                          onMouseLeave={(e) => e.currentTarget.querySelector('.message-actions')?.style.display === 'flex' && (e.currentTarget.querySelector('.message-actions').style.display = 'none')}
                        >
                          {isFileMessage(msg.content) && !isImage ? (
                          <div className="file-message">
                            <span className="file-icon">
                              {getFileIcon(extractFileFromContent(msg.content)?.name, extractFileFromContent(msg.content)?.type)}
                            </span>
                            <div className="file-info">
                              <span className="file-name">{extractFileFromContent(msg.content)?.name || msg.content.replace('📎 Fichier: ', '')}</span>
                              {extractFileFromContent(msg.content)?.type && (
                                <span className="file-type">
                                  {extractFileFromContent(msg.content).type.split('/')[1]?.toUpperCase() || 'Fichier'}
                                </span>
                              )}
                            </div>
                            <button 
                              className="file-btn" 
                              title="Télécharger"
                              onClick={(e) => {
                                e.stopPropagation();
                                const fileInfo = extractFileFromContent(msg.content);
                                if (fileInfo && fileInfo.data) {
                                  const link = document.createElement('a');
                                  link.href = fileInfo.data;
                                  link.download = fileInfo.name;
                                  link.click();
                                  console.log('📥 Téléchargement:', fileInfo.name, 'Type:', fileInfo.type);
                                } else {
                                  alert('⚠️ Fichier non disponible (ancien format)');
                                }
                              }}
                            >
                              <Download size={14} />
                            </button>
                          </div>
                        ) : isImage && imageUrl ? (
                          <div className="image-message">
                            <img 
                              src={imageUrl} 
                              alt="Message image" 
                              onClick={() => setSelectedImage(imageUrl)}
                              onError={(e) => {
                                console.error('❌ Erreur chargement image:', e);
                                console.log('URL:', imageUrl.substring(0, 100));
                              }}
                              onLoad={() => {
                                console.log('✅ Image chargée');
                              }}
                            />
                            <button 
                              className="image-download-btn" 
                              onClick={(e) => {
                                e.stopPropagation();
                                // Télécharger l'image
                                const link = document.createElement('a');
                                link.href = imageUrl;
                                link.download = `image_${Date.now()}.png`;
                                link.click();
                                console.log('📥 Téléchargement image');
                              }}
                              title="Télécharger l'image"
                            >
                              <Download size={14} /> Télécharger
                            </button>
                          </div>
                        ) : (
                          <p>{msg.content}</p>
                          )}
                          
                          {isOwnMessage && (
                            <div className="message-actions" style={{ display: 'none', gap: '8px', marginTop: '4px' }}>
                              <button 
                                className="message-action-btn"
                                onClick={() => {
                                  const newContent = prompt('Modifier le message:', msg.content);
                                  if (newContent) {
                                    setMessages(messages.map(m => m.id === msg.id ? {...m, content: newContent} : m));
                                  }
                                }}
                                title="Modifier"
                              >
                                ✏️
                              </button>
                              <button 
                                className="message-action-btn danger"
                                onClick={() => deleteMessage(msg.id)}
                                title="Supprimer"
                              >
                                🗑️
                              </button>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Input Area */}
              <div className="chat-input-area">
                {showEmojiPicker && (
                  <div className="emoji-picker">
                    {emojis.map(emoji => (
                      <button
                        key={emoji}
                        className="emoji-btn"
                        onClick={() => {
                          setNewMessage(newMessage + emoji);
                        }}
                      >
                        {emoji}
                      </button>
                    ))}
                  </div>
                )}
                <form onSubmit={handleSendMessage} className="message-form">
                  {/* Input pour les images */}
                  <input
                    type="file"
                    ref={imageInputRef}
                    onChange={handleImageUpload}
                    style={{ display: 'none' }}
                    accept="image/*"
                  />
                  <button 
                    type="button" 
                    className="icon-btn" 
                    title="Ajouter une image"
                    onClick={() => imageInputRef.current?.click()}
                  >
                    <Plus size={20} />
                  </button>
                  
                  {/* Input pour tous types de fichiers */}
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    style={{ display: 'none' }}
                    accept="*"
                  />
                  <button 
                    type="button" 
                    className="icon-btn" 
                    title="Partager un fichier (PDF, Word, Excel, TXT...)"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Paperclip size={20} />
                  </button>
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Aa"
                    autoFocus
                  />
                  <button
                    type="button"
                    className="icon-btn"
                    onClick={() => setShowEmojiPicker(!showEmojiPicker)}
                    title="Emoji"
                  >
                    <Smile size={20} />
                  </button>
                  <button type="submit" className="btn-send" title="Envoyer">
                    <Send size={20} />
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div className="chat-empty">
              <div style={{ fontSize: '64px', marginBottom: '15px', opacity: 0.3 }}>💬</div>
              <p>Sélectionnez une conversation ou créez une nouvelle</p>
            </div>
          )}
        </div>
      </div>

      {/* Image Viewer Modal */}
      {selectedImage && (
        <div className="image-modal" onClick={() => setSelectedImage(null)}>
          <div className="image-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedImage(null)}>
              <X size={24} />
            </button>
            <img src={selectedImage} alt="Full screen message image" />
          </div>
        </div>
      )}

      {/* Notification d'appel entrant */}
      {incomingCall && (
        <div className="incoming-call-notification">
          <div className="notification-content">
            <h3>📞 Appel entrant</h3>
            <p>De: <strong>{incomingCall.from}</strong></p>
            <p>Type: <strong>{incomingCall.type === 'video' ? '📹 Vidéo' : '📞 Audio'}</strong></p>
            <p className="notification-time">{incomingCall.timestamp}</p>
            <div className="notification-actions">
              <button className="accept-btn" onClick={async () => {
                console.log('✅ Acceptation d\'appel de:', incomingCall.from);
                
                try {
                  // Supprimer l'appel du backend
                  if (incomingCall.callId) {
                    await axios.post(`http://localhost:5000/api/calls/accept/${incomingCall.callId}`);
                    console.log('🗑️ Appel accepté et supprimé du backend');
                  }
                  
                  // Ouvrir le modal d'appel
                  setCallType(incomingCall.type);
                  setActiveCall(incomingCall.from);
                  setIncomingCall(null);
                } catch (error) {
                  console.error('❌ Erreur lors de l\'acceptation:', error);
                  // Ouvrir quand même le modal
                  setCallType(incomingCall.type);
                  setActiveCall(incomingCall.from);
                  setIncomingCall(null);
                }
              }}>
                ✅ Accepter
              </button>
              <button className="reject-btn" onClick={async () => {
                console.log('❌ Refus d\'appel de:', incomingCall.from, 'ID:', incomingCall.fromId);
                
                try {
                  // 1. Supprimer l'appel du backend pour arrêter les notifications
                  if (incomingCall.callId) {
                    await axios.post(`http://localhost:5000/api/calls/reject/${incomingCall.callId}`);
                    console.log('🗑️ Appel supprimé du backend:', incomingCall.callId);
                  }
                  
                  // 2. Enregistrer le refus comme appel manqué avec le BON destinataire
                  await logCallInMessages(0, true, incomingCall.type, incomingCall.fromId);
                  
                  // 3. Fermer la notification
                  setIncomingCall(null);
                  
                  console.log('✅ Appel refusé et notification fermée');
                } catch (error) {
                  console.error('❌ Erreur lors du refus:', error);
                  // Fermer quand même la notification
                  setIncomingCall(null);
                }
              }}>
                ❌ Refuser
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Call Modal */}
      <CallModal
        isOpen={!!activeCall}
        onClose={() => {
          setActiveCall(null);
          setCallType(null);
        }}
        recipientName={activeCall}
        callType={callType}
        userId={user.id}
      />

      {/* Historique des appels */}
      {callHistory.length > 0 && (
        <div className="call-history-panel">
          <h3>📞 Historique des appels</h3>
          <div className="call-history-list">
            {callHistory.map(call => (
              <div key={call.id} className="call-history-item">
                <div className="call-icon">
                  {call.type === 'video' ? '📹' : '📞'}
                </div>
                <div className="call-details">
                  <p><strong>{call.caller}</strong> → <strong>{call.recipient}</strong></p>
                  <p className="call-time">{call.date} à {call.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Context Menu */}
      {contextMenu && (
        <>
          <div className="context-menu-overlay" onClick={() => setContextMenu(null)} />
          <div 
            className="context-menu-popup" 
            style={{ 
              top: `${menuPosition.y}px`, 
              left: `${menuPosition.x}px`,
              position: 'fixed'
            }}
          >
            {contextMenu.type === 'group' ? (
              <>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); leaveGroup(contextMenu.id); setContextMenu(null); }} 
                  className="danger"
                >
                  <span>👋</span> Quitter le groupe
                </button>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); deleteConversation(contextMenu.id); setContextMenu(null); }} 
                  className="danger"
                >
                  <span>🗑️</span> Supprimer le groupe
                </button>
              </>
            ) : (
              <>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); initiateCall('audio'); setContextMenu(null); }}
                >
                  <span>📞</span> Appel vocal
                </button>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); initiateCall('video'); setContextMenu(null); }}
                >
                  <span>📹</span> Discussion vidéo
                </button>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); alert('Conversation archivée'); setContextMenu(null); }}
                >
                  <span>📦</span> Archiver la discussion
                </button>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); deleteConversation(contextMenu.id); setContextMenu(null); }} 
                  className="danger"
                >
                  <span>🗑️</span> Supprimer la discussion
                </button>
                <button 
                  onMouseDown={(e) => { e.preventDefault(); alert('Conversation signalée'); setContextMenu(null); }} 
                  className="danger"
                >
                  <span>⚠️</span> Signaler
                </button>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default Messenger;

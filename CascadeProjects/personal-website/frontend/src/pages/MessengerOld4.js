import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Send, Search, Plus, Phone, Video, MoreVertical, Smile, X, Users, Heart, Share2, Paperclip, Image as ImageIcon, Phone as PhoneIcon, Video as VideoIcon } from 'lucide-react';
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
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [replyingTo, setReplyingTo] = useState(null);
  const [showCallModal, setShowCallModal] = useState(false);
  const [callType, setCallType] = useState(null);
  const fileInputRef = useRef(null);
  const token = localStorage.getItem('token');

  const emojis = ['😀', '😂', '❤️', '👍', '🎉', '🔥', '✨', '👏', '🙌', '💯', '😍', '🤔', '😢', '😡', '🤮', '😎'];

  useEffect(() => {
    fetchConversations();
    fetchUsers();
    const interval = setInterval(() => {
      fetchConversations();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedConversation || selectedUser) {
      fetchMessages();
    }
  }, [selectedConversation, selectedUser]);

  useEffect(() => {
    if (showNewChat) {
      setFilteredUsers(users);
    }
  }, [showNewChat, users]);

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
          const key = msg.sender_id < msg.recipient_id ? 
            `${msg.sender_id}-${msg.recipient_id}` : 
            `${msg.recipient_id}-${msg.sender_id}`;
          
          if (!grouped[key]) {
            grouped[key] = {
              id: key,
              lastMessage: msg,
              messages: [msg],
              sender_id: msg.sender_id,
              recipient_id: msg.recipient_id,
              sender_name: msg.sender_id === user.id ? (msg.recipient_name || 'Utilisateur') : (msg.sender_name || 'Utilisateur'),
              recipient_name: msg.sender_id === user.id ? (msg.recipient_name || 'Utilisateur') : (msg.sender_name || 'Utilisateur')
            };
          } else {
            grouped[key].messages.push(msg);
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
      const response = await axios.get('http://localhost:5000/api/messages/test');
      if (Array.isArray(response.data)) {
        setMessages(response.data);
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

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

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

      if (replyingTo) {
        messageData.content = `[Réponse à ${replyingTo.sender_name}]\n${replyingTo.content}\n\n${newMessage}`;
      }

      await axios.post('http://localhost:5000/api/messages', messageData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setNewMessage('');
      setShowEmojiPicker(false);
      setReplyingTo(null);
      await fetchConversations();
      await fetchMessages();
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const startNewChat = (user) => {
    setSelectedUser(user);
    setSelectedConversation(null);
    setShowNewChat(false);
    setSearchTerm('');
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
    return conv.sender_id === user.id ? conv.recipient_name : conv.sender_name;
  };

  const filteredConversations = conversations.filter(conv => {
    const name = getOtherUserName(conv);
    return name.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const currentRecipient = selectedUser || (selectedConversation && {
    full_name: getOtherUserName(selectedConversation),
    id: selectedConversation.lastMessage.sender_id === user.id ?
      selectedConversation.lastMessage.recipient_id :
      selectedConversation.lastMessage.sender_id
  });

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const fileName = file.name;
      setNewMessage(newMessage + `\n📎 Fichier: ${fileName}`);
    }
  };

  const handleCall = (type) => {
    setCallType(type);
    setShowCallModal(true);
    setTimeout(() => {
      alert(`Appel ${type === 'video' ? 'vidéo' : 'audio'} avec ${currentRecipient.full_name}\n\nFonctionnalité à implémenter avec WebRTC`);
      setShowCallModal(false);
    }, 2000);
  };

  const getConversationMessages = () => {
    return messages.filter(msg => {
      const isRelevant = (msg.sender_id === user.id && msg.recipient_id === currentRecipient.id) ||
                        (msg.sender_id === currentRecipient.id && msg.recipient_id === user.id);
      return isRelevant;
    });
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

          {/* Liste des conversations */}
          <div className="conversations-list">
            {filteredConversations.length === 0 ? (
              <div className="no-conversations">
                <p>Aucune conversation</p>
              </div>
            ) : (
              filteredConversations.map(conv => (
                <div
                  key={conv.id}
                  className={`conversation-item ${selectedConversation?.id === conv.id && !selectedUser ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedConversation(conv);
                    setSelectedUser(null);
                  }}
                >
                  <div className="conversation-avatar">
                    {getOtherUserName(conv).charAt(0).toUpperCase()}
                  </div>
                  <div className="conversation-content">
                    <h4>{getOtherUserName(conv)}</h4>
                    <p>{conv.lastMessage.content.substring(0, 50)}...</p>
                  </div>
                  <span className="conversation-time">
                    {new Date(conv.lastMessage.created_at).toLocaleTimeString()}
                  </span>
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
                  <button className="icon-btn" title="Appel audio" onClick={() => handleCall('audio')}>
                    <Phone size={20} />
                  </button>
                  <button className="icon-btn" title="Appel vidéo" onClick={() => handleCall('video')}>
                    <Video size={20} />
                  </button>
                  <button className="icon-btn">
                    <MoreVertical size={20} />
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="chat-messages">
                {getConversationMessages().map(msg => (
                  <div key={msg.id} className="message-group">
                    <div
                      className={`message-bubble ${msg.sender_id === user.id ? 'sent' : 'received'}`}
                    >
                      <p>{msg.content}</p>
                      <span className="message-time">
                        {new Date(msg.created_at).toLocaleTimeString()}
                      </span>
                    </div>
                    {msg.sender_id !== user.id && (
                      <button 
                        className="reply-btn"
                        onClick={() => setReplyingTo(msg)}
                        title="Répondre"
                      >
                        ↩️
                      </button>
                    )}
                  </div>
                ))}
              </div>

              {/* Reply Preview */}
              {replyingTo && (
                <div className="reply-preview">
                  <div className="reply-content">
                    <strong>Réponse à {replyingTo.sender_name}:</strong>
                    <p>{replyingTo.content.substring(0, 100)}...</p>
                  </div>
                  <button onClick={() => setReplyingTo(null)} className="reply-close">
                    <X size={16} />
                  </button>
                </div>
              )}

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
                  <button type="button" className="icon-btn" title="Ajouter">
                    <Plus size={20} />
                  </button>
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileUpload}
                    style={{ display: 'none' }}
                  />
                  <button 
                    type="button" 
                    className="icon-btn" 
                    title="Partager un fichier"
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

      {/* Call Modal */}
      {showCallModal && (
        <div className="call-modal">
          <div className="call-content">
            <div className="call-avatar">
              {currentRecipient?.full_name.charAt(0).toUpperCase()}
            </div>
            <h2>Appel {callType === 'video' ? 'vidéo' : 'audio'}</h2>
            <p>{currentRecipient?.full_name}</p>
            <div className="call-status">En cours de connexion...</div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Messenger;

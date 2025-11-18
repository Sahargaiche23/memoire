import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Send, Search, Plus, Phone, Video, MoreVertical, Smile, X } from 'lucide-react';
import './Messenger.css';

function Messenger({ user, onLogout }) {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showNewChat, setShowNewChat] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  const emojis = ['😀', '😂', '❤️', '👍', '🎉', '🔥', '✨', '👏', '🙌', '💯', '😍', '🤔'];

  useEffect(() => {
    fetchConversations();
    fetchUsers();
    // Rafraîchir toutes les 3 secondes
    const interval = setInterval(() => {
      fetchConversations();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      fetchMessages(selectedConversation.id);
    }
  }, [selectedConversation]);

  const fetchConversations = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/messages', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const grouped = {};
      response.data.forEach(msg => {
        const key = msg.sender_id < msg.recipient_id ? 
          `${msg.sender_id}-${msg.recipient_id}` : 
          `${msg.recipient_id}-${msg.sender_id}`;
        
        if (!grouped[key]) {
          grouped[key] = {
            id: key,
            lastMessage: msg,
            messages: [msg]
          };
        } else {
          grouped[key].messages.push(msg);
          if (new Date(msg.created_at) > new Date(grouped[key].lastMessage.created_at)) {
            grouped[key].lastMessage = msg;
          }
        }
      });

      setConversations(Object.values(grouped).sort((a, b) => 
        new Date(b.lastMessage.created_at) - new Date(a.lastMessage.created_at)
      ));
    } catch (err) {
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (conversationId) => {
    try {
      const response = await axios.get('http://localhost:5000/api/messages', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(response.data);
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/users', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data.filter(u => u.id !== user.id));
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConversation) return;

    try {
      const recipientId = selectedConversation.lastMessage.sender_id === user.id ?
        selectedConversation.lastMessage.recipient_id :
        selectedConversation.lastMessage.sender_id;

      await axios.post('http://localhost:5000/api/messages', {
        recipient_id: recipientId,
        subject: 'Message',
        content: newMessage
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setNewMessage('');
      setShowEmojiPicker(false);
      await fetchConversations();
      await fetchMessages(selectedConversation.id);
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const startNewChat = async (selectedUser) => {
    try {
      await axios.post('http://localhost:5000/api/messages', {
        recipient_id: selectedUser.id,
        subject: 'Message',
        content: 'Salut!'
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setShowNewChat(false);
      await fetchConversations();
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const filteredConversations = conversations.filter(conv => {
    const otherUser = conv.lastMessage.sender_id === user.id ?
      conv.lastMessage.sender_name :
      conv.lastMessage.sender_name;
    return otherUser.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const getOtherUser = (conv) => {
    return conv.lastMessage.sender_id === user.id ?
      conv.lastMessage.sender_name :
      conv.lastMessage.sender_name;
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
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          {/* Nouveau chat */}
          {showNewChat && (
            <div className="new-chat-panel">
              <h3>Nouvelle conversation</h3>
              <div className="users-list">
                {users.map(u => (
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
                ))}
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
                  className={`conversation-item ${selectedConversation?.id === conv.id ? 'active' : ''}`}
                  onClick={() => setSelectedConversation(conv)}
                >
                  <div className="conversation-avatar">
                    {getOtherUser(conv).charAt(0).toUpperCase()}
                  </div>
                  <div className="conversation-content">
                    <h4>{getOtherUser(conv)}</h4>
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
          {selectedConversation ? (
            <>
              {/* Chat Header */}
              <div className="chat-header">
                <div className="chat-header-info">
                  <h3>{getOtherUser(selectedConversation)}</h3>
                  <p>Actif maintenant</p>
                </div>
                <div className="chat-header-actions">
                  <button className="icon-btn" title="Appel">
                    <Phone size={20} />
                  </button>
                  <button className="icon-btn" title="Vidéo">
                    <Video size={20} />
                  </button>
                  <button className="icon-btn">
                    <MoreVertical size={20} />
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="chat-messages">
                {messages.map(msg => (
                  <div
                    key={msg.id}
                    className={`message-bubble ${msg.sender_id === user.id ? 'sent' : 'received'}`}
                  >
                    <p>{msg.content}</p>
                    <span className="message-time">
                      {new Date(msg.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
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
                  <button type="button" className="icon-btn" title="Ajouter">
                    <Plus size={20} />
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
              <p>Sélectionnez une conversation</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Messenger;

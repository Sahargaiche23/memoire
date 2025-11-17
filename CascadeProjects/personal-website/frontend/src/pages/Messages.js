import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Send, Mail, Check, X, Search, MessageCircle, Reply } from 'lucide-react';
import './Messages.css';

function Messages({ user, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [loading, setLoading] = useState(true);
  const [replyContent, setReplyContent] = useState('');
  const token = localStorage.getItem('token');

  const [formData, setFormData] = useState({
    recipient_id: '',
    subject: '',
    content: ''
  });

  useEffect(() => {
    fetchMessages();
    fetchUsers();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/messages', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessages(response.data);
    } catch (err) {
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/api/messages', formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Message envoyé avec succès!');
      setFormData({ recipient_id: '', subject: '', content: '' });
      fetchMessages();
    } catch (err) {
      alert('Erreur lors de l\'envoi du message');
      console.error('Erreur:', err);
    }
  };

  const handleReply = async (e) => {
    e.preventDefault();
    if (!replyContent.trim()) return;

    try {
      await axios.post('http://localhost:5000/api/messages', {
        recipient_id: selectedMessage.sender_id,
        subject: `RE: ${selectedMessage.subject}`,
        content: replyContent
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Réponse envoyée avec succès!');
      setReplyContent('');
      fetchMessages();
      setSelectedMessage(null);
    } catch (err) {
      alert('Erreur lors de l\'envoi de la réponse');
      console.error('Erreur:', err);
    }
  };

  const markAsRead = async (messageId) => {
    try {
      await axios.put(`http://localhost:5000/api/messages/${messageId}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchMessages();
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  // Filtrer les messages
  const filteredMessages = messages.filter(msg => {
    const matchesSearch = msg.sender_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         msg.subject.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || 
                         (filterStatus === 'unread' && !msg.is_read) ||
                         (filterStatus === 'read' && msg.is_read);
    return matchesSearch && matchesFilter;
  });

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="messages-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="messenger-container">
        {/* Sidebar */}
        <div className="messenger-sidebar">
          <div className="sidebar-header">
            <h2>💬 Messages</h2>
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

          {/* Filtres */}
          <div className="filters">
            <button 
              className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
              onClick={() => setFilterStatus('all')}
            >
              Tous ({messages.length})
            </button>
            <button 
              className={`filter-btn ${filterStatus === 'unread' ? 'active' : ''}`}
              onClick={() => setFilterStatus('unread')}
            >
              Non lus ({messages.filter(m => !m.is_read).length})
            </button>
            <button 
              className={`filter-btn ${filterStatus === 'read' ? 'active' : ''}`}
              onClick={() => setFilterStatus('read')}
            >
              Lus ({messages.filter(m => m.is_read).length})
            </button>
          </div>

          {/* Liste des messages */}
          <div className="messages-list-sidebar">
            {filteredMessages.length === 0 ? (
              <div className="no-messages">
                <Mail size={32} />
                <p>Aucun message</p>
              </div>
            ) : (
              filteredMessages.map(msg => (
                <div 
                  key={msg.id}
                  className={`message-item ${selectedMessage?.id === msg.id ? 'active' : ''} ${!msg.is_read ? 'unread' : ''}`}
                  onClick={() => {
                    setSelectedMessage(msg);
                    if (!msg.is_read) markAsRead(msg.id);
                  }}
                >
                  <div className="message-item-avatar">
                    {msg.sender_name.charAt(0).toUpperCase()}
                  </div>
                  <div className="message-item-content">
                    <h4>{msg.sender_name}</h4>
                    <p>{msg.subject}</p>
                    <span className="time">
                      {new Date(msg.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  {!msg.is_read && <div className="unread-dot"></div>}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Chat Area */}
        <div className="messenger-chat">
          {selectedMessage ? (
            <>
              {/* Header du message */}
              <div className="chat-header">
                <div className="chat-header-info">
                  <h3>{selectedMessage.sender_name}</h3>
                  <p>{new Date(selectedMessage.created_at).toLocaleString()}</p>
                </div>
              </div>

              {/* Contenu du message */}
              <div className="chat-messages">
                <div className="message-bubble received">
                  <div className="message-subject">{selectedMessage.subject}</div>
                  <div className="message-text">{selectedMessage.content}</div>
                  <div className="message-time">
                    {new Date(selectedMessage.created_at).toLocaleTimeString()}
                  </div>
                </div>
                
                {/* Afficher les réponses si elles existent */}
                {messages
                  .filter(msg => 
                    msg.subject.includes(`RE: ${selectedMessage.subject}`) ||
                    msg.subject === `RE: ${selectedMessage.subject}`
                  )
                  .map(reply => (
                    <div key={reply.id} className="message-bubble sent">
                      <div className="message-text">{reply.content}</div>
                      <div className="message-time">
                        {new Date(reply.created_at).toLocaleTimeString()}
                      </div>
                    </div>
                  ))
                }
              </div>

              {/* Zone de réponse */}
              <div className="chat-input-area">
                <form onSubmit={handleReply} className="reply-form">
                  <textarea
                    value={replyContent}
                    onChange={(e) => setReplyContent(e.target.value)}
                    placeholder="Écrivez votre réponse..."
                    rows="3"
                  ></textarea>
                  <button type="submit" className="btn-reply" disabled={!replyContent.trim()}>
                    <Reply size={18} /> Répondre
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div className="chat-empty">
              <MessageCircle size={64} />
              <p>Sélectionnez un message pour le lire</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Messages;

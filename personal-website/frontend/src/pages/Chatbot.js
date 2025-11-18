import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { Send, MessageCircle, RotateCcw } from 'lucide-react';
import './Chatbot.css';

function Chatbot({ user, onLogout }) {
  const [messages, setMessages] = useState([
    {
      id: 0,
      message: 'Bonjour! Je suis votre assistant virtuel. Comment puis-je vous aider?',
      response: null,
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchHistory();
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchHistory = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/chatbot/history', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setHistory(response.data);
    } catch (err) {
      console.error('Erreur:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setLoading(true);

    // Ajouter le message utilisateur
    const newUserMessage = {
      id: messages.length,
      message: userMessage,
      response: null,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await axios.post('http://localhost:5000/api/chatbot', 
        { message: userMessage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Ajouter la réponse du bot
      const botMessage = {
        id: messages.length + 1,
        message: userMessage,
        response: response.data.bot_response,
        isBot: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      fetchHistory();
    } catch (err) {
      console.error('Erreur:', err);
      const errorMessage = {
        id: messages.length + 1,
        message: userMessage,
        response: 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
        isBot: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([
      {
        id: 0,
        message: 'Bonjour! Je suis votre assistant virtuel. Comment puis-je vous aider?',
        response: null,
        isBot: true,
        timestamp: new Date()
      }
    ]);
    setInput('');
  };

  const quickQuestions = [
    'Comment créer un actif?',
    'Comment planifier une maintenance?',
    'Comment générer un rapport?',
    'Aide'
  ];

  return (
    <div className="chatbot-page">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="chatbot-container">
        <div className="chatbot-header">
          <div className="header-content">
            <h1>🤖 Assistant Virtuel</h1>
            <p>Posez vos questions et je vous aiderai</p>
          </div>
          <button className="btn-reset" onClick={handleReset}>
            <RotateCcw size={18} /> Réinitialiser
          </button>
        </div>

        <div className="chatbot-main">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.isBot ? 'bot' : 'user'}`}>
                <div className="message-bubble">
                  {msg.isBot ? (
                    <>
                      <div className="bot-avatar">🤖</div>
                      <div className="message-content">
                        <p className="user-question">{msg.message}</p>
                        <p className="bot-response">{msg.response}</p>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="message-content">
                        <p className="user-message">{msg.message}</p>
                      </div>
                      <div className="user-avatar">👤</div>
                    </>
                  )}
                </div>
                <span className="message-time">
                  {msg.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </span>
              </div>
            ))}
            {loading && (
              <div className="message bot">
                <div className="message-bubble">
                  <div className="bot-avatar">🤖</div>
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-sidebar">
            <h3>Questions Rapides</h3>
            <div className="quick-questions">
              {quickQuestions.map((question, index) => (
                <button
                  key={index}
                  className="quick-question-btn"
                  onClick={() => {
                    setInput(question);
                  }}
                >
                  {question}
                </button>
              ))}
            </div>

            <h3 style={{ marginTop: '30px' }}>Historique</h3>
            <div className="history-list">
              {history.length === 0 ? (
                <p className="no-history">Aucun historique</p>
              ) : (
                history.slice(-5).reverse().map((item, index) => (
                  <div 
                    key={index} 
                    className="history-item"
                    onClick={() => setInput(item.message)}
                  >
                    <p className="history-question">{item.message}</p>
                    <p className="history-time">
                      {new Date(item.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Posez votre question..."
            disabled={loading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="btn-send-message"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chatbot;

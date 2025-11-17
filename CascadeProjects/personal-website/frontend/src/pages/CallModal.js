import React, { useState, useEffect, useRef } from 'react';
import { X, Mic, MicOff, Video, VideoOff, Phone, PhoneOff } from 'lucide-react';
import './CallModal.css';

function CallModal({ isOpen, onClose, recipientName, callType, userId }) {
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOn, setIsVideoOn] = useState(callType === 'video');
  const [callDuration, setCallDuration] = useState(0);
  const [callStatus, setCallStatus] = useState('connecting');
  const localVideoRef = useRef(null);
  const remoteVideoRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    // Simuler la connexion
    setTimeout(() => setCallStatus('connected'), 2000);

    // Démarrer le chronomètre
    const timer = setInterval(() => {
      setCallDuration(prev => prev + 1);
    }, 1000);

    // Demander l'accès à la caméra/micro
    if (callType === 'video') {
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
          if (localVideoRef.current) {
            localVideoRef.current.srcObject = stream;
          }
        })
        .catch(err => console.error('Erreur caméra:', err));
    } else {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          console.log('Micro activé');
        })
        .catch(err => console.error('Erreur micro:', err));
    }

    return () => {
      clearInterval(timer);
      if (localVideoRef.current?.srcObject) {
        localVideoRef.current.srcObject.getTracks().forEach(track => track.stop());
      }
    };
  }, [isOpen, callType]);

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleEndCall = () => {
    // Enregistrer l'appel dans les messages avant de fermer
    if (window.logCallInMessages) {
      window.logCallInMessages(callDuration, false, callType);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="call-modal-overlay">
      <div className="call-modal">
        {/* Vidéo distante */}
        {callType === 'video' && (
          <video
            ref={remoteVideoRef}
            className="remote-video"
            autoPlay
            playsInline
          />
        )}

        {/* Vidéo locale */}
        {callType === 'video' && (
          <video
            ref={localVideoRef}
            className="local-video"
            autoPlay
            playsInline
            muted
          />
        )}

        {/* Contenu de l'appel */}
        <div className="call-content">
          <div className="call-header">
            <h2>{recipientName}</h2>
            <p className={`call-status ${callStatus}`}>
              {callStatus === 'connecting' ? '⏳ Connexion...' : '✅ Connecté'}
            </p>
          </div>

          <div className="call-duration">
            {formatDuration(callDuration)}
          </div>

          {/* Contrôles */}
          <div className="call-controls">
            <button
              className={`control-btn ${isMuted ? 'muted' : ''}`}
              onClick={() => setIsMuted(!isMuted)}
              title={isMuted ? 'Activer le micro' : 'Désactiver le micro'}
            >
              {isMuted ? <MicOff size={24} /> : <Mic size={24} />}
            </button>

            {callType === 'video' && (
              <button
                className={`control-btn ${!isVideoOn ? 'off' : ''}`}
                onClick={() => setIsVideoOn(!isVideoOn)}
                title={isVideoOn ? 'Éteindre la caméra' : 'Allumer la caméra'}
              >
                {isVideoOn ? <Video size={24} /> : <VideoOff size={24} />}
              </button>
            )}

            <button
              className="control-btn end-call"
              onClick={handleEndCall}
              title="Terminer l'appel"
            >
              <PhoneOff size={24} />
            </button>
          </div>

          <button
            className="close-btn"
            onClick={onClose}
            title="Fermer"
          >
            <X size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default CallModal;

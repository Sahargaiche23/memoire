import { useEffect, useState } from 'react';

export function useCallNotification(userId, onIncomingCall) {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    if (!userId) return;

    // Simuler les notifications d'appel entrant
    // En production, utiliser WebSocket ou Server-Sent Events
    const handleIncomingCall = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'incoming_call') {
          onIncomingCall(data);
          
          // Notification système
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`Appel ${data.callType === 'video' ? 'vidéo' : 'vocal'} de ${data.from}`, {
              icon: '📞',
              badge: '📞',
              tag: 'incoming-call',
              requireInteraction: true
            });
          }
        }
      } catch (e) {
        console.error('Erreur parsing notification:', e);
      }
    };

    // Demander la permission de notification
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }

    setIsConnected(true);

    return () => {
      setIsConnected(false);
    };
  }, [userId, onIncomingCall]);

  return isConnected;
}

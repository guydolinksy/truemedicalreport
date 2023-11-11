import React, { useState } from 'react';

export const notificationsContext = React.createContext({});
export const NotificationsProvider = ({ children }) => {
  const [notifications, setNotifications] = useState(0);
  return (
    <notificationsContext.Provider value={{ notifications, setNotifications }}>
      {children}
    </notificationsContext.Provider>
  );
};

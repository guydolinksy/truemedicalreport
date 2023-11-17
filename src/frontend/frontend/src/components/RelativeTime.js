import React, { useContext, useEffect, useState } from 'react';
import Moment from 'react-moment';

export const relativeTime = React.createContext(true);

export const TimeContextProvider = ({ children }) => {
  const [isDown, setIsDown] = useState(true);

  useEffect(() => {
    const listener = (e) => {
      if (e.key === 'Control') setIsDown((prevState) => !prevState);
    };
    document.addEventListener('keydown', listener);
    return () => document.removeEventListener('keydown', listener);
  }, []);

  return <relativeTime.Provider value={{ showRelativeTime: isDown }}>{children}</relativeTime.Provider>;
};

export const RelativeTime = (props) => {
  const { showRelativeTime } = useContext(relativeTime);
  return (
    <Moment
      interval={1000}
      durationFromNow={showRelativeTime}
      format={showRelativeTime ? 'H[h]mm[m]' : 'H:mm'}
      {...props}
    />
  );
};

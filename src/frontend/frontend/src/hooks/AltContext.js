import React, {useEffect, useState} from "react";

export const altContext = React.createContext(false);

export const AltContextProvider = ({children}) => {
    const [isDown, setIsDown] = useState(false);

    useEffect(() => {
        const listener = (e) => {
            if (e.key === 'Alt') setIsDown(prevState => !prevState);
        }
        document.addEventListener('keydown', listener)
        return () => document.removeEventListener('keydown', listener);
    }, []);

    return <altContext.Provider value={{isAltDown: isDown}}>
        {children}
    </altContext.Provider>
}

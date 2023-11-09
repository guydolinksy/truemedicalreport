import React, {useEffect, useState} from "react";

export const modeContext = React.createContext({});
const getWindowDimensions = () => {
    const {innerWidth: width, innerHeight: height} = window;
    return {
        width,
        height
    };
}
export const useWindowDimensions = () => {
    const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());

    useEffect(() => {
        const handleResize = () => setWindowDimensions(getWindowDimensions());
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return windowDimensions;
}
export const ModeProvider = ({children}) => {
    const [mode, setMode] = useState({isTablet: false});
    const {width, height} = useWindowDimensions();

    useEffect(() => {
        console.log(navigator.userAgent.toLowerCase())
        setMode({
            isLandscape: width > height,
            isFullSize: width > 1700,
            isLarge: width < 1200,
            isMedium: width < 1000,
            isSmall: width < 800,
            isTiny: width < 660,
            isTablet: /ipad|tablet|(android(?!.*mobile))/.test(navigator.userAgent.toLowerCase()),
            isFullScreen: !!document.fullscreenElement,
        })
    }, [document.fullscreenElement, width, height, setMode, navigator.userAgent]);

    return <modeContext.Provider value={{
        ...mode,
    }}>
        {children}
    </modeContext.Provider>
}

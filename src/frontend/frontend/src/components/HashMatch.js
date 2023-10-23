import {useLocation} from "react-router";

import React, {useMemo} from "react";

export const hashMatchContext = React.createContext({
    matched: () => false,
    matching:  () => [],
});

export const HashMatch = ({children}) => {
    const {hash} = useLocation();

    const [matched, matching] = useMemo(() => {
        let parts = hash.split('#').slice(1);
        return [
            match => parts.length >= match.length && !match.some((m, i) => m !== null && parts[i] !== m),
            match => parts.length >= match.length && !match.some((m, i) =>  m !== null && parts[i] !== m) ? parts.slice(match.length) : [],
        ]
    }, [hash])

    return <hashMatchContext.Provider value={{matched: matched, matching: matching}}>
        {children}
    </hashMatchContext.Provider>;
}
import React, {lazy, Suspense, useContext, useEffect, useState} from "react";
import {loginContext} from "../components/LoginContext";

export const LightTheme = lazy(() => import("./LightTheme"));
export const DarkTheme = lazy(() => import("./DarkTheme"));

export const UserTheme = (props) => {
    const {userSettings} = useContext(loginContext);
    const [counter, setCounter] = useState(0);

    useEffect(() => {
        setCounter(i => {console.log(i); return i + 1});
    }, [userSettings.theme]);

    return <div key={counter} className={userSettings.theme}>
        <Suspense fallback={<span/>}>
            {userSettings.theme === 'dark-theme' ? <DarkTheme/> : <LightTheme/>}
        </Suspense>
        {props.children}
    </div>
}

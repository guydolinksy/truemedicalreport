import {useEffect, useState} from "react";


export const useLocalStorage = (key, defaultValue) => {
    const [value, setValue] = useState(() => {
            const saved = localStorage.getItem(key);
            return ([null, undefined].includes(saved) && JSON.parse(saved)) || defaultValue;
        }
    );
    useEffect(() => {
        function storageEventHandler(event) {
            if (event.key === key) {
                setValue(JSON.parse(event.newValue));
            }
        }

        window.addEventListener("storage", storageEventHandler);
        window.addEventListener("stored", storageEventHandler);
        return () => {
            window.removeEventListener("storage", storageEventHandler);
            window.removeEventListener("stored", storageEventHandler);
        }
    }, [key, value]);
    const json = JSON.stringify(value);
    useEffect(() => {
        const event = new Event("stored");
        event.key = key;
        event.newValue = JSON.stringify(value);
        window.dispatchEvent(event);
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, json]);

    return [value, setValue];
};

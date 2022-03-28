import React, {useCallback, useEffect, useState} from "react";
import Axios from 'axios';
import useWebSocket from "react-use-websocket";
import {useNavigate} from "react-router";

export const createContext = (defaultValue) => {
    const context = React.createContext(defaultValue);

    const Provider = ({url, updateURL, socketURL, defaultValue = undefined, fetchOnMount = false, ...props}) => {

        const [{loadingData, value}, setValue] = useState({loading: false, value: defaultValue});
        const {lastMessage} = useWebSocket(`wss://${window.location.host}/api/ws`, {queryParams: {url: socketURL}});
        const navigate = useNavigate();

        useEffect(() => {
            if (!fetchOnMount) return;
            Axios.get(url).then(response => {
                setValue({loading: false, value: response.data});
            }).catch(error => {
                navigate('/');
                console.error(error)
            })
        }, [url, fetchOnMount, lastMessage]);

        const getData = useCallback((path) =>
                path.reduce((data, name) => data ? data[name] : undefined, value),
            [value]);

        const updateData = useCallback((path, newValue) => {
            const deepReplace = (path, data, value) => {
                if (!path.length) {
                    return value
                }
                const key = path.pop()
                return Object.assign({}, data, {[key]: deepReplace(path, data[key], value)});
            }
            setValue(prevState => {
                const newData = deepReplace(path.slice().reverse(), prevState.value, newValue)
                Axios.post(updateURL, {data: newData, path: path, value: newValue}).catch(error => {
                    console.error(error)
                });
                return {loading: prevState.loading, value: newData}
            });
        }, [updateURL]);

        return <context.Provider value={{getData: getData, updateData: updateData, loadingData: loadingData}}>
            {props.children({getData: getData, updateData: updateData, loadingData: loadingData, ...props})}
        </context.Provider>
    }

    const withData = Component => ({...props}) => {
        return <context.Consumer>{({getData, updateData, loadingData}) =>
            <Component loadingData={loadingData} getData={getData} updateData={updateData} {...props}/>
        }</context.Consumer>
    };

    return {withData: withData, Provider: Provider}
}

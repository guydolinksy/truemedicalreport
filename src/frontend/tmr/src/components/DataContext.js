import React, {useCallback, useEffect, useState} from "react";
import Axios from 'axios';
import useWebSocket from "react-use-websocket";
import {useNavigate} from "react-router";

export const createContext = (defaultValue) => {
    const context = React.createContext(defaultValue);

    const Provider = ({url, updateURL, socketURL, defaultValue = undefined, ...props}) => {

        const [{loadingData, value}, setValue] = useState({loading: false, value: defaultValue});
        const {lastMessage} = useWebSocket(`ws://${window.location.host}/api/sync/ws`, {queryParams: {key: socketURL || url}});
        const navigate = useNavigate();

        useEffect(() => {
            const s = Axios.CancelToken.source()
            Axios.get(url, {cancelToken: s.token}).then(response => {
                setValue({loading: false, value: response.data});
            }).catch(error => {
                if (Axios.isCancel(error))
                    return;
                navigate('/');
                console.error(error)
            })
            return () => s.cancel()
        }, [url, lastMessage, navigate]);

        const getData = useCallback((path, defaultValue) => path.reduce((data, name) =>
            (data === undefined || data[name] === undefined) ? defaultValue : data[name], value), [value]);

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
                Axios.post(updateURL || url, {data: newData, path: path, value: newValue}).catch(error => {
                    console.error("update error", error)
                });
                return {loading: prevState.loading, value: newData}
            });
        }, [url, updateURL]);

        return <context.Provider
            value={{getData: getData, updateData: updateData, loadingData: loadingData, lastMessage: lastMessage}}>
            {props.children({
                getData: getData,
                updateData: updateData,
                loadingData: loadingData,
                lastMessage: lastMessage, ...props
            })}
        </context.Provider>
    }

    const withData = Component => ({...props}) => {
        return <context.Consumer>{({getData, updateData, loadingData, lastMessage}) =>
            <Component loadingData={loadingData} getData={getData} updateData={updateData}
                       lastMessage={lastMessage} {...props}/>
        }</context.Consumer>
    };

    return {withData: withData, Provider: Provider, context: context}
}


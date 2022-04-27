import React, {useCallback, useEffect, useMemo, useState} from "react";
import Axios from 'axios';
import useWebSocket from "react-use-websocket";
import debounce from "lodash/debounce";
import {notification} from 'antd';

export const createContext = (defaultValue) => {
    const context = React.createContext(defaultValue);

    const Provider = ({url, updateURL, socketURL, defaultValue = undefined, onError, ...props}) => {
        console.log(url)
        const [{loadingData, value}, setValue] = useState({loading: false, value: defaultValue});
        const {lastMessage} = useWebSocket(`ws://${window.location.host}/api/sync/ws`,
            {
                queryParams: {key: socketURL || url},
                retryOnError: true,
                onReconnectStop: (e) => {
                    console.log('reconnect', e)
                    notification.error({
                        duration: 0,
                        message: 'שגיאה בעדכון נתונים',
                        description: 'המידע המוצג אינו מתעדכן עקב שגיאת חיבור, יש לרענן את העמוד.'
                    })
                },
            });

        const flushData = useMemo(() => debounce((token) => {
            Axios.get(url, {cancelToken: token}).then(response => {
                setValue({loading: false, value: response.data});
            }).catch(error => {
                if (Axios.isCancel(error))
                    return;
                if (onError)
                    onError(error);
                console.error(error);
            })
        }, 1000, {leading: true, trailing: true}), [url, onError]);

        useEffect(() => {
            return () => flushData.cancel();
        }, []);

        useEffect(() => {
            const s = Axios.CancelToken.source()
            flushData(s.token)
            return () => s.cancel()
        }, [url, lastMessage, flushData]);

        const getData = useCallback((path, defaultValue) => path.reduce((data, name) => {
            if ([undefined, null].includes(data) || [undefined, null].includes(data[name]))
                return defaultValue;
            return data[name];
        }, value), [value]);

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
            value={{
                getData: getData,
                updateData: updateData,
                loadingData: loadingData,
                flushData: flushData,
                lastMessage: lastMessage
            }}>
            {props.children({
                getData: getData,
                updateData: updateData,
                loadingData: loadingData,
                flushData: flushData,
                lastMessage: lastMessage, ...props
            })}
        </context.Provider>
    }

    const withData = Component => ({...props}) => {
        return <context.Consumer>{({getData, updateData, loadingData, flushData, lastMessage}) =>
            <Component loadingData={loadingData} getData={getData} updateData={updateData} flushData={flushData}
                       lastMessage={lastMessage} {...props}/>
        }</context.Consumer>
    };

    return {withData: withData, Provider: Provider, context: context}
}


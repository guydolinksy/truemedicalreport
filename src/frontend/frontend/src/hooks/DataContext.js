import React, {useCallback, useEffect, useMemo, useState} from "react";
import Axios from 'axios';
import useWebSocket from "react-use-websocket";
import debounce from "lodash/debounce";
import {notification} from 'antd';

export const createContext = (defaultValue) => {
    const context = React.createContext(defaultValue);

    const Provider = ({url, updateURL, socketURL, defaultValue = undefined, onError, ...props}) => {
        const [{loading, value}, setValue] = useState({loading: true, value: defaultValue});

        // When the website is served over HTTPs, the browser blocks non-TLS websocket connections.
        const websocketScheme = window.location.protocol.startsWith("https") ? "wss" : "ws";

        const {lastJsonMessage} = useWebSocket(`${websocketScheme}://${window.location.host}/api/sync/ws`,
            {
                share: true,
                shouldReconnect: () => true,
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

        const flush = useMemo(() => debounce(() => {
            const cancellationSource = Axios.CancelToken.source();
            Axios.get(url, {cancelToken: cancellationSource.token}).then(response => {
                setValue({loading: false, value: response.data});
            }).catch(error => {
                if (Axios.isCancel(error))
                    return;
                if (onError)
                    onError(error);
                console.error(error);
            })

            return () => cancellationSource.cancel();
        }, 1000, {leading: true, trailing: true}), [url, onError]);

        useEffect(() => {
            return flush()
        }, [url, flush]);

        useEffect(() => {
            if (lastJsonMessage && lastJsonMessage.keys.includes(url)) {
                flush()
            }
        }, [lastJsonMessage, url, flush]);

        const update = useCallback((path, newValue) => {
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

        return <context.Provider value={{
            value: value,
            update: update,
            loading: loading,
            flush: flush
        }}>
            {props.children({
                value: value,
                update: update,
                loading: loading,
                flush: flush,
                ...props
            })}
        </context.Provider>
    }

    const withData = Component => ({...props}) => {
        return <context.Consumer>{({value, update, loading, flush, lastMessage}) =>
            <Component loading={loading} value={value} update={update} flush={flush}
                       lastMessage={lastMessage} {...props}/>
        }</context.Consumer>
    };

    return {withData: withData, Provider: Provider, context: context}
}

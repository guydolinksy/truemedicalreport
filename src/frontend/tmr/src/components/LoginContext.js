import React, {useCallback, useEffect, useState, useContext} from "react";
import Axios from 'axios';
import useWebSocket from "react-use-websocket";
import {useNavigate} from "react-router";
import {Spin} from 'antd';

const context = React.createContext();

export const LoginProvider = ({...props}) => {

    const [user, setUser] = useState();
    const navigate = useNavigate();

    useEffect(() => {
        const s = Axios.CancelToken.source()
        Axios.get('/api/auth/user', {cancelToken: s.token}).then(response => {
            setUser(response.data);
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            navigate('/login');
            console.error(error)
        })
        return () => s.cancel()
    }, [navigate]);

    return <context.Provider value={{user: user}}>
        {props.children({user: user, ...props})}
    </context.Provider>
}

export const withLogin = Component => ({...props}) => {
    return <context.Consumer>{({user}) =>
        <Component user={user} {...props}/>
    }</context.Consumer>
};

export const LoginRequired = ({...props}) => {
    const {loading, user} = useContext(context);
    const navigate = useNavigate();

    if(loading)
        return <Spin/>

    if(!user)
        navigate('/login')

    return props.children;
};


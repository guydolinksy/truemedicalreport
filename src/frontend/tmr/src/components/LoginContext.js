import React, {useCallback, useContext, useEffect, useState} from "react";
import Axios from 'axios';
import {useLocation, useNavigate} from "react-router";
import {Navigate} from "react-router-dom";

import {Button, Form, Input, Spin} from 'antd';
import {LockOutlined, UserOutlined} from "@ant-design/icons";

export const loginContext = React.createContext(null);

export const LoginProvider = ({...props}) => {

    const [{loading, user}, setUser] = useState({loading: false, user: null});
    const {pathname} = useLocation();

    const checkUser = useCallback((token = null) => {
        setUser(prevState => ({loading: true, user: prevState.user}));
        Axios.get('/api/auth/user', {cancelToken: token}).then(response => {
            setUser({loading: false, user: response.data});
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setUser({loading: false, user: null});
            console.error(error)
        })
    }, []);

    useEffect(() => {
        const s = Axios.CancelToken.source()
        checkUser(s.token);
        return () => s.cancel()
    }, [pathname, checkUser]);

    return <loginContext.Provider value={{user: user, checkUser: checkUser, loadingUser: loading}}>
        {props.children({user: user, checkUser: checkUser, loadingUser: loading, ...props})}
    </loginContext.Provider>
}

export const withLogin = Component => ({...props}) => {
    return <loginContext.Consumer>{({user, checkUser, loadingUser}) =>
        <Component user={user} checkUser={checkUser} loadingUser={loadingUser} {...props}/>
    }</loginContext.Consumer>
};

export const LoginRequired = ({...props}) => {
    const {user, loadingUser} = useContext(loginContext);
    const {pathname, search, hash} = useLocation();
    if (loadingUser)
        return <Spin/>
    return user ? props.children :
        <Navigate to={`/login?next=${encodeURIComponent(pathname + search + hash)}`}/>;
};

export const LoginForm = () => {
    const navigate = useNavigate();
    const {search} = useLocation();
    const {user, checkUser, loadingUser} = useContext(loginContext);
    const [error, setError] = useState(false);

    const loginErrorProps = {hasFeedback: true, validateStatus: "error", help: "???? ???????????? ?????????????? ???????? ????????????."};

    const onFinish = useCallback((values) => {
        Axios.post('/api/auth/token', values).then(() => checkUser()).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });
    }, [checkUser]);

    useEffect(() => {
        if (!user)
            return;
        let next = (new URLSearchParams(search)).get('next');
        navigate(next ? decodeURIComponent(next) : '/');
    }, [user, search, navigate])

    return loadingUser ? <Spin/> :
        <Form name={"login"} onFinish={onFinish} onValuesChange={() => setError(false)}>
            <Form.Item name={"username"} label={"???? ??????????"} rules={[{required: true, message: '???????? ???? ??????????'}]}
                       {...(error ? loginErrorProps : {})}>
                <Input prefix={<UserOutlined/>} autoComplete={"username"}
                       placeholder={"???? ??????????"}/>
            </Form.Item>
            <Form.Item name={"password"} label={"??????????"} rules={[{required: true, message: '?????????? ??????????'}]}
                       {...(error ? loginErrorProps : {})}>
                <Input
                    prefix={<LockOutlined/>}
                    type={"password"} autoComplete={"current-password"}
                    placeholder={"??????????"}/>
            </Form.Item>
            <Form.Item>
                <Button type={"primary"} htmlType={"submit"}>
                    ??????????.??
                </Button>
            </Form.Item>
        </Form>
}
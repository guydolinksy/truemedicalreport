import React, {Suspense, useCallback, useContext, useEffect, useState} from "react";
import Axios from 'axios';
import {useLocation, useNavigate} from "react-router";
import {Navigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react'

import {Button, Form, Input, Spin} from 'antd';
import {LockOutlined, UserOutlined} from "@ant-design/icons";
import {LightTheme} from "../themes/ThemeContext";

export const loginContext = React.createContext({});

export const LoginProvider = ({...props}) => {

    const [{loading, user, userSettings}, setUser] = useState({loading: false, user: null, userSettings: {}});
    const {pathname} = useLocation();

    const checkUser = useCallback((token = null) => {
        setUser(prevState => ({loading: true, user: prevState.user, userSettings: prevState.userSettings}));
        Axios.get('/api/auth/user', {cancelToken: token}).then(response => {
            setUser({
                loading: false,
                user: response.data.user || false,
                userSettings: response.data.userSettings || {}
            });
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setUser({loading: false, user: null, userSettings: {}});
            console.error(error)
        })
    }, []);

    useEffect(() => {
        const s = Axios.CancelToken.source()
        checkUser(s.token);
        return () => s.cancel()
    }, [pathname, checkUser]);

    return <loginContext.Provider
        value={{user: user, userSettings: userSettings, checkUser: checkUser, loadingUser: loading}}>
        {props.children({user: user, userSettings: userSettings, checkUser: checkUser, loadingUser: loading, ...props})}
    </loginContext.Provider>
}

export const withLogin = Component => ({...props}) => {
    return <loginContext.Consumer>{({user, userSettings, checkUser, loadingUser}) =>
        <Component user={user} userSettings={userSettings} checkUser={checkUser} loadingUser={loadingUser} {...props}/>
    }</loginContext.Consumer>
};

export const LoginRequired = ({...props}) => {
    const {user, loadingUser} = useContext(loginContext);
    const {pathname, search, hash} = useLocation();
    const {pushInstruction} = useMatomo()

    if (loadingUser)
        return <Spin/>

    if (user) {
        pushInstruction('setUserId', user.user);
        return props.children;
    }

    return <Navigate to={`/login?next=${encodeURIComponent(pathname + search + hash)}`}/>;
};

export const LoginForm = () => {
    const navigate = useNavigate();
    const {search} = useLocation();
    const {user, checkUser, loadingUser} = useContext(loginContext);
    const [error, setError] = useState(false);

    const loginErrorProps = {hasFeedback: true, validateStatus: "error", help: "שם המשתמש והסיסמה אינם תואמים."};

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


    return <>
        <Suspense fallback={<span/>}>
            <LightTheme/>
        </Suspense>
        {loadingUser ? <Spin/> : <Form name={"login"} onFinish={onFinish} onValuesChange={() => setError(false)}>
            <Form.Item name={"username"} label={"שם משתמש"} rules={[{required: true, message: 'נדרש שם משתמש'}]}
                       {...(error ? loginErrorProps : {})}>
                <Input prefix={<UserOutlined/>} autoComplete={"username"}
                       placeholder={"שם משתמש"}/>
            </Form.Item>
            <Form.Item name={"password"} label={"סיסמה"} rules={[{required: true, message: 'נדרשת סיסמה'}]}
                       {...(error ? loginErrorProps : {})}>
                <Input
                    prefix={<LockOutlined/>}
                    type={"password"} autoComplete={"current-password"}
                    placeholder={"סיסמה"}/>
            </Form.Item>
            <Form.Item>
                <Button type={"primary"} htmlType={"submit"}>
                    התחבר.י
                </Button>
            </Form.Item>
        </Form>}
    </>
}
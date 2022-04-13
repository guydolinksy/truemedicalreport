import {Button, Card, Form, Input, Space, Switch} from "antd";
import React, {useCallback, useEffect, useRef, useState} from "react";
import Axios from "axios";

const LDAPAuthentication = () => {
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [initialValue, setInitialValue] = useState({});
    const form = useRef();
    useEffect(() => {
        const s = Axios.CancelToken.source();
        Axios.get('/api/auth/ldap', {cancelToken: s.token}).then(response => {
            setInitialValue(response.data);
            form.current.resetFields();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });
        return () => s.cancel();
    }, []);

    const onFinish = useCallback((values) => {
        Axios.post('/api/auth/ldap', values).then(() => setSuccess(true)).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });
    }, []);
    const onTest = useCallback((values) => {
        Axios.post('/api/auth/ldap/test', values).then(() => setSuccess(true)).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });
    }, []);

    return <Form ref={form} name={"ldap"} title={''} onFinish={onFinish} onValuesChange={() => setError(false)}
                 initialValues={initialValue}>
        <Form.Item name={"enabled"} label={"חיבור LDAP מאופשר"} valuePropName={"checked"}>
            <Switch/>
        </Form.Item>
        <Form.Item name={"connection"} label={"ניתוב שרת LDAP"} hasFeedback rules={[
            {required: true, message: 'יש להזין את הניתוב לשרת LDAP'},
            () => ({
                async validator(_, value) {
                    if (!value) {
                        return Promise.resolve();
                    }
                    try {
                        if ((await Axios.post('/api/auth/ldap/test', {connection: value})).data) {
                            return Promise.resolve();
                        }
                    } catch (error) {
                        console.log(error)
                    }
                    return Promise.reject(new Error('לא ניתן להתחבר לניתוב שהוזן!'));
                },
            })
        ]}>
            <Input placeholder={"הניתוב לשרת"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"user_dn"} label={"פורמט DN למשתמש"} rules={[
            {required: true, message: 'יש להזין פורמט DN למשתמש'}
        ]}>
            <Input placeholder={"פורמט DN למשתמש"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"bind_dn"} label={"מזהה DN לחיבור"} rules={[
            {required: true, message: 'יש להזין DN משתמש לחיבור'}
        ]}>
            <Input placeholder={"מזהה DN לחיבור"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"bind_password"} label={"סיסמה לחיבור"} rules={[
            {required: true, message: 'יש להזין סיסמה לחיבור'}
        ]}>
            <Input placeholder={"סיסמה לחיבור"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"admin_ou"} label={"קבוצת מנהלים"} rules={[
            {required: true, message: 'יש להזין DN לקבוצת מנהלים'}
        ]}>
            <Input placeholder={"מזהה DN לקבוצת מנהלים"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"users_ou"} label={"קבוצת משתמשים"} rules={[
            {required: true, message: 'יש להזין DN לקבוצת משתמשים'}
        ]}>
            <Input placeholder={"מזהה DN לקבוצת משתמשים"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"test_user"} label={"משתמש לבדיקה"}>
            <Input placeholder={"משתמש לבדיקה"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"test_password"} label={"סיסמה לבדיקה"}>
            <Input placeholder={"סיסמה לבדיקה"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item hasFeedback>
            <Button danger={error} onClick={() => onTest()}>בדיקת חיבור</Button>
        </Form.Item>
        <Form.Item>
            <Button type={"primary"} htmlType={"submit"}>שמירה</Button>
        </Form.Item>
    </Form>
}
const methods = {
    ldap: <LDAPAuthentication/>
}
export const AuthenticationCard = () => {
    const [activeTabKey, setActiveTabKey] = useState('ldap');
    return <Card title={'הגדרות מערכת'} tabList={[{key: 'ldap', tab: 'ldap'}]} activeTabKey={activeTabKey}
                 onTabChange={setActiveTabKey}>
        {methods[activeTabKey]}
    </Card>
}
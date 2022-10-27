import {Alert, Button, Card, Form, Input, Space, Switch} from "antd";
import React, {useCallback, useEffect, useRef, useState} from "react";
import merge from "lodash/merge";
import Axios from "axios";

const convertFormToLdapConfig = ({enabled, test_user, test_password, ...settings}) => {
    delete settings.settings
    return {
        enabled,
        test_user,
        test_password,
        settings
    }
}

const convertLdapConfigToForm = ({settings, ...rest}) => {
    return merge(settings, rest);
}

const toParagraphs = (items) => {
    return items.map((item, index) => <p key={index}>{item}</p>)
}

const formatError = (prefix, {status, data}) => {
    return toParagraphs([
        prefix,
        `סטטוס: ${status}`,
        data.detail ? data.detail : data
    ])
}

const LDAPAuthentication = () => {
    const [message, setMessage] = useState(null);
    const [isError, setIsError] = useState(false);
    const [initialFormValues, setInitialFormValues] = useState({});
    const form = useRef();

    const setInfo = (message) => {
        setMessage(message);
        setIsError(false);
    }

    const setError = (message) => {
        setMessage(message);
        setIsError(true);
    }

    useEffect(() => {
        const s = Axios.CancelToken.source();
        Axios.get('/api/auth/ldap', {cancelToken: s.token}).then(response => {
            setInitialFormValues(convertLdapConfigToForm(response.data));
            form.current.resetFields();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;

            setError(formatError("השליפה של ההגדרות הקיימות של התאמתות LDAP נכשלה", error.response));
        });
        return () => s.cancel();
    }, []);

    const saveLdapConfig = useCallback((values) => {
        let conf = convertFormToLdapConfig(values);

        // these are not stored; the API will refuse to store the LDAP config if these are passed.
        delete conf.test_user;
        delete conf.test_password;

        Axios.post('/api/auth/ldap', conf).then(() => setInfo("ההגדרות נשמרו!")).catch(error => {
            if (Axios.isCancel(error)) {
                return
            }
            setError(formatError("השמירה של ההגדרות נכשלה.", error.response));
        });
    }, []);

    const testLdapConfig = useCallback((values) => {
        Axios.post('/api/auth/ldap/test', convertFormToLdapConfig(values)).then((response) => {
            let groups = "המשתמש לא חבר באף קבוצה."
            if (response.data.groups) {
                groups = response.data.groups.join(" | ")
            }

            setInfo(toParagraphs([
                `ההתאמתות הצליחה!`,
                `משתמש: ${response.data.username}`,
                `מנהל: ${response.data.is_admin ? "כן" : "לא"}`,
                `קבוצות: ${groups}`
                ]))
        }).catch(error => {
            if (Axios.isCancel(error)) {
                return;
            }

            setError(formatError("המשתמש לא אומת בהצלחה.", error.response));
        });
    }, []);

    return <Form ref={form} name={"ldap"} title={''} onFinish={saveLdapConfig} onValuesChange={() => {
        setMessage(null)
    }}
                 initialValues={initialFormValues}>
        {message && <Alert message={message} type={isError ? "error" : "info"} style={{marginBottom: 24}}/>}
        <Form.Item name={"enabled"} label={"חיבור LDAP מאופשר"} valuePropName={"checked"}>
            <Switch/>
        </Form.Item>
        <Form.Item name={"uri"} label={"ניתוב שרת LDAP"} hasFeedback rules={[
            {required: true, message: 'יש להזין את הניתוב לשרת LDAP'}
        ]}>
            <Input placeholder={"ldap://..."} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"base"} label={"מזהה בסיסי"} rules={[
            {required: true, message: 'יש להזין מזהה בסיסי'}
        ]}>
            <Input placeholder={"ex. dc=example,dc=com"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"filter"} label={"פילטר משתמשים"} rules={[
            {required: true, message: 'יש להזין פילטר משתמשים'}
        ]}>
            <Input placeholder={"sAMAccounrName={username}"} autoComplete={"off"}/>
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
        <Form.Item name={"admin_group_dn"} label={"קבוצת מנהלים"} rules={[
            {required: true, message: 'יש להזין DN לקבוצת מנהלים'}
        ]}>
            <Input placeholder={"admin group name (OU)"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"user_group_dn"} label={"קבוצת משתמשים"} rules={[
            {required: true, message: 'יש להזין DN לקבוצת משתמשים'}
        ]}>
            <Input placeholder={"user group name (OU)"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"test_user"} label={"משתמש לבדיקה"}>
            <Input placeholder={"משתמש לבדיקה"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"test_password"} label={"סיסמה לבדיקה"}>
            <Input placeholder={"סיסמה לבדיקה"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item>
            <Space>
                <Form.Item>
                    <Button onClick={() => testLdapConfig(form.current.getFieldValue())}>בדיקת חיבור</Button>
                </Form.Item>
                <Form.Item>
                    <Button type={"primary"} htmlType={"submit"}>שמירה</Button>
                </Form.Item>
            </Space>
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

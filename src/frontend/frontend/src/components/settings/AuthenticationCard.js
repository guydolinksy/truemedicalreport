import {Alert, Button, Card, Form, Input, Space, Switch} from "antd";
import React, {useCallback, useEffect, useRef, useState} from "react";
import Axios from "axios";

const toParagraphs = (items) => {
    return items.map((item, index) => <p key={index}>{item}</p>)
}

const formatError = (prefix, {status, data}) => {
    return toParagraphs([
        prefix,
        `סטטוס: ${status}`,
        data.detail || data
    ])
}

const LDAPAuthentication = () => {
    const [message, _setMessage] = useState(null);
    const [isError, _setIsError] = useState(false);
    const [initialFormValues, setInitialFormValues] = useState({});
    const form = useRef();

    const setInfo = (message) => {
        _setMessage(message);
        _setIsError(false);
    }

    const setError = (message) => {
        _setMessage(message);
        _setIsError(true);
    }

    const showError = (prefix, error) => {
        if (Axios.isCancel(error)) {
            return;
        }

        setError(formatError(prefix, error.response));
    }

    useEffect(() => {
        const s = Axios.CancelToken.source();

        Axios.get('/api/auth/ldap', {cancelToken: s.token}).then(response => {
            // Previously, the actual values were in the 'settings' key.
            // Nowadays, it's flat, but we support the old style for easy upgrade.
            const { settings, ...rest } = response.data;
            setInitialFormValues({
                ...(settings || {}),
                ...rest
            });
            form.current.resetFields();
        }).catch(error => showError("השליפה של ההגדרות הקיימות של התאמתות LDAP נכשלה", error));

        return () => s.cancel();
    }, []);

    const saveLdapConfig = useCallback(({test_user, test_password, ...conf}) => {
        Axios.post('/api/auth/ldap', conf)
            .then(() => setInfo("ההגדרות נשמרו!"))
            .catch(error => showError("השמירה של ההגדרות נכשלה.", error))
    }, []);

    const [missingTestUser, setMissingTestUser] = useState(false);
    const [missingTestPassword, setMissingTestPassword] = useState(false);

    const testLdapConfig = useCallback(({test_user, test_password, ...conf}) => {
        let missingInput = false;

        if (!test_user) {
            setMissingTestUser(true);
            missingInput = true;
        }

        if (!test_password) {
            setMissingTestPassword(true);
            missingInput = true;
        }

        if (missingInput) {
            return;
        }

        Axios.post('/api/auth/ldap/test', {
            test_user,
            test_password,
            ...conf
        }).then((response) => {
            let groups = "המשתמש לא חבר באף קבוצה."
            if (response.data.groups) {
                groups = response.data.groups.join(" | ")
            }

            setInfo(toParagraphs([
                `ההתאמתות הצליחה!`,
                `משתמש: ${response.data.user.username}`,
                `מנהל: ${response.data.user.is_admin ? "כן" : "לא"}`,
                `קבוצות: ${groups}`
                ]))
        }).catch(error => showError("המשתמש לא אומת בהצלחה.", error));
    }, []);

    const testLdapConfigGroupsOnly = useCallback(({test_user, test_password, ...conf}) => {
        if (!test_user) {
            setMissingTestUser(true);
            return;
        }

        Axios.post('/api/auth/ldap/test_get_user_groups', {
            test_user,
            ...conf,
        }).then((response) => {
            if (response.data.groups) {
                setInfo(toParagraphs([`המשתמש חבר בקבוצות הבאות:`].concat(response.data.groups)))
            } else {
                setInfo("המשתמש לא חבר באף קבוצה.")
            }
        }).catch(error => showError("חלה תקלה בעת תשאול קבוצות המשתמש.", error));
    }, []);

    const testUserErrorProps = missingTestUser ? {hasFeedback: true, validateStatus: "error", help: "נדרש שם משתמש לבדיקה"}: {};
    const testPasswordErrorProps = missingTestPassword ? {hasFeedback: true, validateStatus: "error", help: "נדרשת סיסמה למשתמש הבדיקה"}: {};

    return <Form ref={form}
                 name={"ldap"}
                 title={''}
                 onFinish={saveLdapConfig}
                 onValuesChange={() => _setMessage(null)}
                 initialValues={initialFormValues}
    >
        {message && <Alert message={message} type={isError ? "error" : "info"} style={{marginBottom: 24}}/>}
        <Form.Item name={"enabled"} label={"חיבור LDAP מאופשר"} valuePropName={"checked"}>
            <Switch/>
        </Form.Item>
        <Form.Item name={"uri"} label={"ניתוב שרת LDAP"} hasFeedback rules={[
            {required: true, message: 'יש להזין את הניתוב לשרת LDAP'}
        ]}>
            <Input placeholder={"ldap://..."} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"users_base"} label={"מזהה בסיסי למשתמשים"} rules={[
            {required: true, message: 'יש להזין מזהה בסיסי למשתמשים'}
        ]}>
            <Input placeholder={"ex. ou=users,dc=example,dc=com"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"groups_base"} label={"מזהה בסיסי לקבוצות"} rules={[
            {required: true, message: 'יש להזין מזהה בסיסי לקבוצות'}
        ]}>
            <Input placeholder={"ex. ou=groups,dc=example,dc=com"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"use_ad_style_group_membership"} label={"מצב תאימות ל-Active Directory"} valuePropName={"checked"}>
            <Switch/>
        </Form.Item>
        <Form.Item name={"filter"} label={"פילטר משתמשים"} rules={[
            {required: true, message: 'יש להזין פילטר משתמשים'}
        ]}>
            <Input placeholder={"sAMAccountName={username}"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"bind_dn"} label={"מזהה DN לחיבור"} rules={[
            {required: true, message: 'יש להזין DN משתמש לחיבור'}
        ]}>
            <Input placeholder={"מזהה DN לחיבור"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"bind_password"} label={"סיסמה לחיבור"} rules={[
            {required: true, message: 'יש להזין סיסמה לחיבור'}
        ]}>
            <Input.Password placeholder={"סיסמה לחיבור"} autoComplete={"off"}/>
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
        <Form.Item name={"test_user"}
                   label={"משתמש לבדיקה"}
                   onChange={() => setMissingTestUser(false)}
                   {...testUserErrorProps}>
            <Input placeholder={"משתמש לבדיקה"} autoComplete={"off"}/>
        </Form.Item>
        <Form.Item name={"test_password"}
                   label={"סיסמה לבדיקה"}
                   onChange={() => setMissingTestPassword(false)}
                   {...testPasswordErrorProps}>
            <Input.Password placeholder={"סיסמה לבדיקה"} autoComplete={"off"} />
        </Form.Item>
        <Form.Item>
            <Space>
                <Form.Item>
                    <Button onClick={() => testLdapConfigGroupsOnly(form.current.getFieldValue())}>בדיקת קבוצות (ללא אימות)</Button>
                </Form.Item>
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
    return <Card title={'הגדרות מערכת'} tabList={[{key: 'ldap', tab: 'LDAP'}]} activeTabKey={activeTabKey}
                 onTabChange={setActiveTabKey}>
        {methods[activeTabKey]}
    </Card>
}

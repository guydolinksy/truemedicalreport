import React, {useCallback, useContext, useEffect, useRef, useState} from "react";
import Axios from "axios";
import {Alert, Button, Card, Form, Input, Radio} from "antd";
import {EyeInvisibleOutlined, UserOutlined} from "@ant-design/icons";
import {loginContext} from "../LoginContext";

export const DisplayCard = () => {
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [canSubmit, setCanSubmit] = useState(false);
    const [initialValue, setInitialValue] = useState({});

    const form = useRef();

    useEffect(() => {
        const s = Axios.CancelToken.source();
        Axios.get('/api/settings/display', {cancelToken: s.token}).then(response => {
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
        Axios.post('/api/settings/display', values).then(() => {
            setSuccess(true);
            document.location.reload();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });

    }, []);

    const onChange = useCallback((changedValues, allValues) => {
        setError(false);
        setCanSubmit(true);
    }, [setError, setCanSubmit]);

    return <Card title={'הגדרות תצוגה'}>
        {success ? <Alert message={'הגדרות התצוגה נשמרו בהצלחה'} type={"success"} closable
                          afterClose={() => setSuccess(false)}/> :
            <Form ref={form} name={"display"} title={'הגדרות תצוגה'} onFinish={onFinish} onValuesChange={onChange}
                  initialValues={initialValue}>
                <Form.Item name={"theme"} label={"סכמת צבעים"} rules={[(() => ({
                    validator(_, value) {
                        if (!value || !error)
                            return Promise.resolve();
                        return Promise.reject(new Error('שגיאת נתונים , יש לנסות שנית!'));
                    }
                }))]}>
                    <Radio.Group>
                        <Radio.Button value="dark-theme">מצב לילה</Radio.Button>
                        <Radio.Button value="light-theme">מצב יום</Radio.Button>
                    </Radio.Group>
                </Form.Item>
                <Form.Item>
                    <Button disabled={!canSubmit} type={"primary"} htmlType={"submit"}>שמירה</Button>
                </Form.Item>
            </Form>}
    </Card>
}
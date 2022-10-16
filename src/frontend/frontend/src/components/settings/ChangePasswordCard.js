import React, {useCallback, useState} from "react";
import Axios from "axios";
import {Alert, Button, Card, Form, Input} from "antd";
import {EyeInvisibleOutlined, UserOutlined} from "@ant-design/icons";

export const ChangePasswordCard = () => {
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [canSubmit, setCanSubmit] = useState(false);

    const onFinish = useCallback((values) => {
        Axios.post('/api/auth/change-password', values).then(() => setSuccess(true)).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });

    }, []);

    const onChange = useCallback((changedValues, allValues) => {
        setError(false);
        setCanSubmit(allValues.previous && allValues.password && allValues.confirm);
    }, [setError, setCanSubmit]);

    return <Card title={'הגדרות משתמש'}>
        {success ? <Alert message={'הסיסמה הוחלפה בהצלחה'} type={"success"} closable
                         afterClose={() => setSuccess(false)}/> :
            <Form name={"change-password"} title={'החלפת סיסמה'} onFinish={onFinish}
                  onValuesChange={onChange}>
                <Form.Item name={"username"} hidden>
                    <Input prefix={<UserOutlined/>} autoComplete={"username"}
                           placeholder={"שם משתמש"}/>
                </Form.Item>
                <Form.Item name={"previous"} label={"סיסמה נוכחית"} hasFeedback rules={[
                    {required: true, message: 'יש להזין את הסיסמה הנוכחית'},
                    (() => ({
                        validator(_, value) {
                            if (!value || !error)
                                return Promise.resolve();
                            return Promise.reject(new Error('הסיסמה שגויה, יש לנסות שנית!'));
                        }
                    }))
                ]}>
                    <Input prefix={<EyeInvisibleOutlined/>} type={"password"} autoComplete={"current-password"}
                           placeholder={"סיסמה נוכחית"}/>
                </Form.Item>
                <Form.Item name={"password"} label={"סיסמה חדשה"} rules={[
                    {required: true, message: 'נדרשת סיסמה חדשה'},
                    ({getFieldValue}) => ({
                        validator(_, value) {
                            if (!value || getFieldValue('previous') !== value) {
                                return Promise.resolve();
                            }
                            return Promise.reject(new Error('הסיסמה החדשה לא יכולה להיות זהה לסיסמה הישנה!'));
                        },
                    }),
                ]}>
                    <Input prefix={<EyeInvisibleOutlined/>} type={"password"} autoComplete={"new-password"}
                           placeholder={"סיסמה חדשה"}/>
                </Form.Item>
                <Form.Item name={"confirm"} label={"אימות סיסמה"} hasFeedback dependencies={['password']} rules={[
                    {required: true, message: 'יש להזין את הסיסמה החדשה שנית!'},
                    ({getFieldValue}) => ({
                        validator(_, value) {
                            if (!value || getFieldValue('password') === value) {
                                return Promise.resolve();
                            }
                            return Promise.reject(new Error('הסיסמה אינה תואמת!'));
                        },
                    }),
                ]}>
                    <Input prefix={<EyeInvisibleOutlined/>} type={"password"} autoComplete={"confirm-password"}
                           placeholder={"וידוא סיסמה"}/>
                </Form.Item>
                <Form.Item>
                    <Button disabled={!canSubmit} type={"primary"} htmlType={"submit"}>שמירה</Button>
                </Form.Item>
            </Form>}
    </Card>
}
import React, {useCallback, useEffect, useRef, useState} from "react";
import Axios from "axios";
import {Alert, Button, Card, Checkbox, Form, Radio} from "antd";

export const DepartmentItemsCard = () => {
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [canSubmit, setCanSubmit] = useState(false);
    const [initialValue, setInitialValue] = useState({});

    const form = useRef();

    useEffect(() => {
        const s = Axios.CancelToken.source();
        Axios.get('/api/settings/department-items', {cancelToken: s.token}).then(response => {
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
        Axios.post('/api/settings/statistics', values).then(() => {
            setSuccess(true);
            document.location.reload();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });

    }, []);

    const renderValue = (departmentItem) => <Checkbox.Item>
        {departmentItem}
    </Checkbox.Item>

    const onChange = useCallback((changedValues, allValues) => {
        setError(false);
        setCanSubmit(true);
    }, [setError, setCanSubmit]);

    return <Card title={'הגדרות הצגת פרטי מחלקה'}>
        {success ? <Alert message={'הגדרות התצוגה נשמרו בהצלחה'} type={"success"} closable
                          afterClose={() => setSuccess(false)}/> :
            <Form ref={form} name={"display"} title={'הגדרות הצגת פרטי מחלקה'} onFinish={onFinish} onValuesChange={onChange}
                  initialValues={initialValue}>
                <Form.Item name={"items"} label={"לא להציג:"} rules={[(() => ({
                    validator(_, value) {
                        if (!value || !error)
                            return Promise.resolve();
                        return Promise.reject(new Error('שגיאת נתונים , יש לנסות שנית!'));
                    }
                }))]}>
                    <Checkbox.Group>
                        {!!initialValue?.length && initialValue.map(value=>renderValue(value))}
                    </Checkbox.Group>
                </Form.Item>
                <Form.Item>
                    <Button disabled={!canSubmit} type={"primary"} htmlType={"submit"}>מחיקה</Button>
                </Form.Item>
            </Form>}
    </Card>
}
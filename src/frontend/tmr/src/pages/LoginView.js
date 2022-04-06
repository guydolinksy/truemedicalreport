import React from 'react';
import {Card, Col, Row, Spin, Tooltip,Form, Input, Button, Checkbox} from "antd";
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import {useNavigate} from "react-router";

export const LOGIN_URL = '/login'

export const LoginView = () => {
    const navigate = useNavigate();

    const onFinish = (values: any) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(values)
        };
        fetch('/api/auth/token', requestOptions)
        .then(response => {
            if(response.ok)
                navigate('/');
        });
    };

    return  <div style={{padding: 16}}>
                <Row>
                    <Col offset={9} span={6}>
                        <Form
                          name="login"
                          className="login-form"
                          onFinish={onFinish}>
                            <Form.Item
                                name="username"
                                rules={[{ required: true, message: 'נדרש שם משתמש' }]}>
                                <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="שם משתמש" />
                            </Form.Item>
                            <Form.Item
                                name="password"
                                rules={[{ required: true, message: 'נדרשת סיסמא' }]}>
                                <Input
                                    prefix={<LockOutlined className="site-form-item-icon" />}
                                    type="password"
                                    placeholder="סיסמא" />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit" className="login-form-button">
                                  התחבר/י
                                </Button>
                            </Form.Item>
                        </Form>
                    </Col>
                </Row>
            </div>
}
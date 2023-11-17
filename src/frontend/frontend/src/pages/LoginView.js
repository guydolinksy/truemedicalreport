import React from 'react';
import { Col, Row } from 'antd';
import { LoginForm } from '../components/LoginContext';

export const LOGIN_URL = '/login';

export const LoginView = () => {
  return (
    <div style={{ padding: 16 }}>
      <Row style={{ marginTop: 200 }}>
        <Col offset={9} span={6}>
          <LoginForm />
        </Col>
      </Row>
    </div>
  );
};

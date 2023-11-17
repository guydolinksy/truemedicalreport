import React, { Suspense, useCallback, useContext, useEffect, useState, createContext } from 'react';
import Axios from 'axios';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useMatomo } from '@datapunt/matomo-tracker-react';

import { Button, Checkbox, Form, Input, Space, Spin } from 'antd';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { LightTheme } from '../themes/ThemeContext';

export const loginContext = createContext({});

export const LoginProvider = ({ ...props }) => {
  const [{ loading, user, userSettings }, setUser] = useState({ loading: false, user: null, userSettings: {} });
  const { pathname } = useLocation();

  const checkUser = useCallback((token = null) => {
    setUser((prevState) => ({ loading: true, user: prevState.user, userSettings: prevState.userSettings }));
    Axios.get('/api/auth/user', { cancelToken: token })
      .then((response) => {
        setUser({
          loading: false,
          user: response.data.user || false,
          userSettings: response.data.userSettings || {},
        });
      })
      .catch((error) => {
        if (Axios.isCancel(error)) return;
        setUser({ loading: false, user: null, userSettings: {} });
        console.error(error);
      });
  }, []);

  useEffect(() => {
    const s = Axios.CancelToken.source();
    checkUser(s.token);
    return () => s.cancel();
  }, [pathname, checkUser]);

  return (
    <loginContext.Provider
      value={{ user: user, userSettings: userSettings, checkUser: checkUser, loadingUser: loading }}
    >
      {props.children({ user: user, userSettings: userSettings, checkUser: checkUser, loadingUser: loading, ...props })}
    </loginContext.Provider>
  );
};

export const LoginRequired = ({ ...props }) => {
  const { user, loadingUser } = useContext(loginContext);
  const { pathname, search, hash } = useLocation();
  const { pushInstruction } = useMatomo();

  if (loadingUser) return <Spin />;

  if (user) {
    pushInstruction('setUserId', user.user);
    return props.children;
  }

  return <Navigate to={`/login?next=${encodeURIComponent(pathname + search + hash)}`} />;
};

export const LoginForm = () => {
  const navigate = useNavigate();
  const { search } = useLocation();
  const { user, checkUser, loadingUser } = useContext(loginContext);
  const [error, setError] = useState(null);

  const [checkingLdapAvailability, setCheckingLdapAvailability] = useState(true);
  const [usingLdapAuth, setUsingLdapAuth] = useState(true);
  const [isLdapEnabled, setLdapEnabled] = useState(true);

  useEffect(() => {
    Axios.get('/api/auth/ldap-status').then((response) => {
      setLdapEnabled(response.data.enabled);
      setCheckingLdapAvailability(false);
    });
  });

  const onFinish = useCallback(
    (values) => {
      Axios.post('/api/auth/token', {
        ...values,
        authProviderName: usingLdapAuth ? 'ldap' : 'local',
      })
        .then(() => checkUser())
        .catch((error) => {
          if (Axios.isCancel(error)) {
            return;
          }

          let message = 'חלה תקלה לא צפויה בזמן ניסיון ההתחברות';
          let incorrectCredentials = false;

          if (error.response.status === 504) {
            message = 'השרת אינו זמין';
          } else if (error.response.status === 403) {
            message = 'אינך חבר.ה בקבוצה מורשי הגישה למערכת, נא צרו קשר עימנו';
          } else if (error.response.status === 401) {
            message = 'שם המשתמש או הסיסמא לא נכונים';
            incorrectCredentials = true;
          }
          setError({
            message,
            incorrectCredentials,
          });
        });
    },
    [checkUser, usingLdapAuth],
  );

  useEffect(() => {
    if (!user) {
      return;
    }

    let next = new URLSearchParams(search).get('next');
    console.log('REDIRECT');
    navigate(next ? decodeURIComponent(next) : '/');
  }, [user, search, navigate]);

  const credsErrorProps = error && error.incorrectCredentials ? { hasFeedback: true, validateStatus: 'error' } : {};
  const errorMsgProps =
    error && error.message
      ? {
          hasFeedback: true,
          validateStatus: 'error',
          help: error.message,
        }
      : {};

  return (
    <>
      <Suspense fallback={<span />}>
        <LightTheme />
      </Suspense>
      {loadingUser || checkingLdapAvailability ? (
        <Spin />
      ) : (
        <Form layout="vertical" name="login" onFinish={onFinish} onValuesChange={() => setError(null)}>
          <Form.Item
            name="username"
            label="שם משתמש"
            rules={[{ required: true, message: 'נדרש שם משתמש' }]}
            {...credsErrorProps}
          >
            <Input
              prefix={<UserOutlined />}
              autoComplete={'username'}
              placeholder={'שם משתמש'}
              onChange={(e) => {
                if (e.target.value === 'admin') {
                  // Disable LDAP when logging in as admin.
                  // Just helps the user a bit...
                  setUsingLdapAuth(false);
                }
              }}
            />
          </Form.Item>
          <Form.Item
            name={'password'}
            label={'סיסמה'}
            rules={[{ required: true, message: 'נדרשת סיסמה' }]}
            {...credsErrorProps}
          >
            <Input.Password prefix={<LockOutlined />} autoComplete={'current-password'} placeholder={'סיסמה'} />
          </Form.Item>
          <Form.Item {...errorMsgProps}>
            <Space direction="horizontal" size={15}>
              <Button type={'primary'} htmlType={'submit'}>
                התחבר.י
              </Button>
              <Space direction="horizontal" size={0}>
                <Checkbox
                  checked={usingLdapAuth && isLdapEnabled}
                  disabled={!isLdapEnabled}
                  onChange={(e) => setUsingLdapAuth(e.target.checked)}
                >
                  משתמש ארגוני
                </Checkbox>
              </Space>
            </Space>
          </Form.Item>
        </Form>
      )}
    </>
  );
};

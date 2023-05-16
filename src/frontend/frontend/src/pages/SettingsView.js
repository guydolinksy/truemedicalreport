import React, {useContext} from 'react';
import {Col, Layout} from 'antd';
import {MainMenu} from "../components/MainMenu";
import {loginContext, LoginRequired} from "../components/LoginContext";
import {ChangePasswordCard} from "../components/settings/ChangePasswordCard";
import {AuthenticationCard} from "../components/settings/AuthenticationCard";
import {DisplayCard} from "../components/settings/DisplayCard";

const {Header, Content} = Layout;


export const SETTINGS_URL = '/settings'
export const SettingsView = () => {
    const {user} = useContext(loginContext);
    return <LoginRequired>
        <Layout>
            <Header>
                <MainMenu/>
            </Header>
            <Content style={{overflowY: "auto"}}>
                <Col style={{
                    display: "flex",
                    flexFlow: 'column nowrap',
                    height: '100%',
                    padding: "50px 350px",
                    rowGap: 50
                }}>
                    {user && user.canChangePassword && <ChangePasswordCard/>}
                    {user && <DisplayCard/>}
                    {user && user.is_admin && <AuthenticationCard/>}
                </Col>
            </Content>
        </Layout>
    </LoginRequired>
}
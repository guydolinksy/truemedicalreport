import React, {useContext} from 'react';
import {Layout} from 'antd';
import {MainMenu} from "../components/MainMenu";
import {loginContext, LoginRequired} from "../components/LoginContext";
import {ChangePasswordCard} from "../components/settings/ChangePasswordCard";
import {AuthenticationCard} from "../components/settings/AuthenticationCard";

const {Header, Content} = Layout;


export const SETTINGS_URL = '/settings'
export const SettingsView = () => {
    const {user} = useContext(loginContext);
    return <LoginRequired>
        <Layout>
            <Header>
                <MainMenu/>
            </Header>
            <Content style={{display: "flex", flexDirection: "column", padding: "50px 350px", rowGap: 50}}>
                {user && user.canChangePassword && <ChangePasswordCard/>}
                {user && user.admin && <AuthenticationCard/>}
            </Content>
        </Layout>
    </LoginRequired>
}


import React from 'react';
import {Department} from "../components/Department";
import {Layout} from 'antd';
import {MainMenu} from "../components/MainMenu";
import {LoginRequired} from "../components/LoginContext";

const {Header, Content} = Layout;


export const DEPARTMENT_URL = '/'
export const DepartmentView = () => {
    return <LoginRequired>
        <Layout>
            <Header>
                <MainMenu/>
            </Header>
            <Content>
                <Department/>
            </Content>
        </Layout>
    </LoginRequired>
}
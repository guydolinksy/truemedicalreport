import React from 'react';
import {Department} from "../components/Department";
import {Layout} from 'antd';
import {MainMenu} from "../components/MainMenu";
import {LoginRequired} from "../components/LoginContext";
import {useParams} from "react-router";

const {Header, Content} = Layout;


export const DEPARTMENT_URL = '/departments/:department'
export const DepartmentView = () => {
    const params = useParams()
    return <LoginRequired>
        <Layout>
            <Header>
                <MainMenu/>
            </Header>
            <Content style={{display: "flex", flexDirection: "column", padding: "50px 350px", rowGap: 50}}>
                <Department department={params.department}/>
            </Content>
        </Layout>
    </LoginRequired>
}
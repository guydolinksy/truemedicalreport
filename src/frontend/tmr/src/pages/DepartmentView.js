import React from 'react';
import {Department} from "../components/Department";
import { Layout } from 'antd';

const { Header, Footer, Sider, Content } = Layout;


export const DEPARTMENT_URL = '/'
export const DepartmentView = () => {
    return  <Layout>
      <Header></Header>
      <Content><Department/></Content>
    </Layout>

}
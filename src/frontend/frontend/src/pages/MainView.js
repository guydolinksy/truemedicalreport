import React, {useEffect, useState} from 'react';
import {Outlet, useLocation, useNavigate} from 'react-router-dom';
import {LoginRequired} from "../components/LoginContext";
import {Layout, Modal} from 'antd';
import {MainMenu} from "../components/MainMenu";
import axios from 'axios';
import {Settings} from "../components/settings/Settings";
import {hashMatchContext} from "../components/HashMatch";
import {createContext} from "../hooks/DataContext";

const {Header} = Layout;

export const MAIN_URL = '/'

export const menuContext = createContext({});

export const MainView = (() => {
    return <menuContext.Provider url={'/api/departments/'} defaultValue={[]}>
        {() => <Layout style={{height: '100vh', display: 'flex'}}>
            <Header>
                <MainMenu/>
            </Header>
            <LoginRequired>
                <Outlet/>
            </LoginRequired>
        </Layout>}
    </menuContext.Provider>
});


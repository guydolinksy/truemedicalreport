import React, {useContext, useEffect} from 'react';
import {Layout, Modal, Spin} from "antd";
import {LoginRequired} from "../components/LoginContext";
import {modeContext} from "../contexts/ModeContext";
import {MainMenu} from "../components/MainMenu";
import {Outlet} from 'react-router-dom';
import {viewsContext} from '../contexts/ViewsContext'
const {Header} = Layout;

export const MAIN_URL = '/'
export const MainView = () => {
    const {isTablet, isTiny, isFullScreen, setIsFullScreen} = useContext(modeContext);
    const [modal, modalContext] = Modal.useModal();

    useEffect(() => {
        if (isTablet && !isFullScreen) {
            modal.info({
                icon: null,
                width: "70%",
                okText: "עבור למסך מלא",
                centered: true,
                closeable: false,
                maskCloseable: true,
                content: <div>
                    שמנו לב שאת.ה כנראה גולש.ת מטאבלט. לחצ.י כאן כדי לעבור למסך מלא
                </div>,
                onOk: () => {
                    document.body.requestFullscreen().then(() => setIsFullScreen(true))
                }
            })
        }
    }, [modal, isTablet, isFullScreen, setIsFullScreen])

    return <LoginRequired>
        <viewsContext.Provider url={'/api/views/'} defaultValue={{views: []}}>
            {({loading}) => <Layout style={{height: '100vh', display: 'flex'}}>
                {modalContext}
                <Header style={isTiny ? {padding: "0 8px"} : {}}>
                    <MainMenu/>
                </Header>
                {loading ? <Spin/> : <Outlet/>}
            </Layout>}
        </viewsContext.Provider>
    </LoginRequired>
}
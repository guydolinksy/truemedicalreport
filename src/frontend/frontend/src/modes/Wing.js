import React, {useCallback, useContext, useEffect, useState} from 'react';
import {Button, Col, Drawer, Layout} from 'antd';
import {MIN_WIDTH} from "../components/card/Patient";
import {generatePath, useLocation} from "react-router-dom";
import {ArrowsAltOutlined} from "@ant-design/icons";
import {loginContext} from "../components/LoginContext";
import {WingNotifications} from "../components/WingNotifications";
import {wingDataContext} from "../contexts/WingContext";
import {hashMatchContext} from "../components/HashMatch";
import {modeContext} from "../contexts/ModeContext";
import {INFO_URL} from "../pages/InfoView";
import {InfoContext} from "../components/panel/Info";
import {ListMode} from "./ListMode";

const {Content} = Layout;

export const Wing = ({department, wing}) => {
    const {hash} = useLocation();

    const {user, userSettings} = useContext(loginContext);
    const {value, flush} = useContext(wingDataContext.context);

    const onInfoError = useCallback(() => {
        flush(true)
        navigate('#')
    }, [navigate, flush]);

    const {isFullSize, isTablet} = useContext(modeContext);




    const [{title, className}, setHeader] = useState({});
    const {matched, matching} = useContext(hashMatchContext);

    useEffect(() => {
        if (isTablet && matched(['info'])) {
            navigate(generatePath(INFO_URL, {department: department, wing: wing, patient: matching(['info'])[0]}))
        }
    }, [isTablet, matched, matching, navigate, wing, department]);
    return <>
        <Content className={'content'} style={{flex: 1, display: 'flex', overflowY: 'scroll', padding: '0 20px'}}>
            <Col style={{padding: 16, flex: 1, display: 'flex', flexFlow: 'column nowrap'}}>
                <ListMode patients={allPatients} onError={flush} style={{
                    display: "grid",
                    gridGap: 16,
                    gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
                }}/>
            </Col>
        </Content>
        <Drawer title={title} placement={"left"} open={matched(['info'])}
                extra={<Button type={'text'} icon={<ArrowsAltOutlined/>} onClick={() => {
                    navigate(generatePath(INFO_URL, {
                        department: department,
                        wing: wing,
                        patient: matching(['info'])[0]
                    }))
                }}/>}
                onClose={() => navigate('#')} className={className} size={500}>
            <InfoContext patient={matching(['info'])[0]} setHeader={setHeader} onError={onInfoError}/>
        </Drawer>
        <Drawer title={'עדכונים'} placement={"left"} open={matched(['notifications'])} onClose={() => navigate('#')}>
            <WingNotifications/>
        </Drawer>
    </>
};



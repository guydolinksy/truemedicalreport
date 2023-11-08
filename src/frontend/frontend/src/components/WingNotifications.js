import {useNavigate} from "react-router-dom";
import React, {useCallback, useContext, useState} from "react";
import {loginContext} from "./LoginContext";
import {Badge, Collapse, Empty, List, Space} from "antd";
import {PushpinOutlined, UserOutlined} from "@ant-design/icons";
import {RelativeTime} from "./RelativeTime";
import {Notification} from "./Notification";
import {wingDataContext} from "../contexts/WingContext";
import moment from "moment";

const {Panel} = Collapse;
const {Item} = List;
const badgeClass = {
    0: 'status-badge status-success',
    1: 'status-badge status-warn',
    2: 'status-badge status-error',
}

export const WingNotifications = () => {
    const navigate = useNavigate();
    const {user} = useContext(loginContext);
    const {value} = useContext(wingDataContext.context);
    const [openKeys, setOpenKeys] = useState([]);
    const [read, setRead] = useState({});

    const markRead = useCallback((oid, static_id) => {
        setRead(p => Object.assign({}, p, {[oid]: (p[oid] || []).concat(static_id)}));
    }, [setRead]);


    const openChange = useCallback(key => {
        let keys = Array.isArray(key) ? key : [key];

        setOpenKeys(prevState => {
            keys.filter(k => !prevState.includes(k)).forEach(k => navigate(`#notifications#${k}#open`));
            prevState.filter(k => !keys.includes(k)).forEach(k => navigate(`#notifications#${k}#close`));
            return keys;
        })
    }, [navigate]);


    return value.patients.length ?
        <div style={{display: "flex !important", flexDirection: "column", flex: "1"}}>
            <Collapse onChange={openChange} style={{flex: "1 0 10vh", minHeight: "10vh", overflowY: "overlay"}}>
                {value.patients.filter(({patient}) => patient.notifications.length).map(({oid, patient}) => {
                    const {patient: last} = patient.notifications.sort(
                        (k1, k2) => moment(k1.notification.at).isAfter(k2.notification.at) ? 1 : -1
                    ).pop();
                    const worst = patient.notifications.sort(
                        (k1, k2) => moment(k1.notification.level).isAfter(k2.notification.level) ? 1 : -1
                    ).pop();
                    const unread = patient.notifications.filter(m => (read[oid] || []).includes(m.key))
                    return <Panel key={oid} header={<>
                    <span className={`gender-${patient.info.gender}`}>
                        <UserOutlined/>{!user.anonymous && <span>&nbsp;{patient.info.name}</span>}
                    </span>
                        <br/>
                        <span style={{fontSize: "10px"}}>{last.message}</span>
                    </>} extra={<div style={{
                        display: "flex",
                        flexFlow: "column nowrap",
                        alignItems: "flex-end",
                    }}>
                        <RelativeTime style={{fontSize: 12}} date={last.at}/>
                        <Space>
                            {patient.flagged && <PushpinOutlined style={{marginLeft: 0}}/>}
                            {unread.length > 0 &&
                                <Badge className={badgeClass[worst]} count={unread.length} size={"small"}/>}
                        </Space>
                    </div>}>
                        <List>
                            {patient.notifications.length ? patient.notifications.sort(
                                (k1, k2) => moment(k1.notification.at).isAfter(k2.notification.at) ? 1 : -1
                            ).map(({key, message}, j) =>
                                <Item key={`${oid}-${j}`}>
                                    <Notification
                                        unread={unread.includes(message.static_id)}
                                        markRead={() => markRead(oid, message.static_id)}
                                        patient={oid} message={message}/>
                                </Item>
                            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין עדכונים זמינים'}/>}
                        </List>
                    </Panel>
                })}
            </Collapse>
        </div> : <div style={{display: "flex", flex: 1, flexDirection: "column"}}>
            <Empty style={{height: 'fit-content'}} description={'אין התרעות'} image={Empty.PRESENTED_IMAGE_SIMPLE}/>
        </div>
}
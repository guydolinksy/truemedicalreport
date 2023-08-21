import {useNavigate} from "react-router";
import React, {useCallback, useContext, useEffect, useState} from "react";
import {loginContext} from "./LoginContext";
import {Badge, Collapse, Empty, List, Space} from "antd";
import {PushpinOutlined, UserOutlined} from "@ant-design/icons";
import {RelativeTime} from "./RelativeTime";
import {Notification} from "./Notification";
import {wingDataContext} from "./Wing";

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
    const [unread, setUnread] = useState({});

    const appendUnread = useCallback((oid, messages) => {
        console.log('UNREAD', oid, messages)
        setUnread(p => Object.assign({}, p, {[oid]: (p[oid] || []).concat(messages)}));
    }, [setUnread]);
    const markRead = useCallback((oid, static_id) => {
        setUnread(p => Object.assign({}, p, {[oid]: (p[oid] || []).filter(s => s !== static_id)}));
    }, [setUnread]);

    const [notifications, setNotifications] = useState(null);
    useEffect(() => {
        setNotifications(prevState => Object.assign({}, ...value.notifications.map((n) => {
            let messages = n.notifications.map(m => m.static_id)
            if (prevState !== null)
                appendUnread(n.patient.oid, messages.filter(s => !(prevState[n.patient.oid] || []).includes(s)));
            return {[n.patient.oid]: messages};
        })));
    }, [appendUnread, value.notifications]);

    const openChange = useCallback(key => {
        let keys = Array.isArray(key) ? key : [key];

        setOpenKeys(prevState => {
            keys.filter(k => !prevState.includes(k)).forEach(k => navigate(`#highlight#${k}#open`));
            prevState.filter(k => !keys.includes(k)).forEach(k => navigate(`#highlight#${k}#close`));
            return keys;
        })
    }, [navigate]);
    if (!value.notifications.length)
        return <div style={{display: "flex", flex: 1, flexDirection: "column"}}>
            <Empty style={{height: 'fit-content'}} description={'אין התרעות'} image={Empty.PRESENTED_IMAGE_SIMPLE}/>
        </div>
    return <div style={{display: "flex !important", flexDirection: "column", flex: "1"}}>
        <Collapse onChange={openChange} style={{flex: "1 0 10vh", minHeight: "10vh", overflowY: "overlay"}}>
            {value.notifications.map((notification) => <Panel key={notification.patient.oid} header={
                <>
                    <span className={`gender-${notification.patient.info.gender}`}>
                        <UserOutlined/>{!user.anonymous && <span>&nbsp;{notification.patient.info.name}</span>}
                    </span>
                    <br/>
                    <span style={{fontSize: "10px"}}>{notification.preview}</span>
                </>
            } extra={
                <div style={{
                    display: "flex",
                    flexFlow: "column nowrap",
                    alignItems: "flex-end",
                }}>
                    <RelativeTime style={{fontSize: 12}} date={notification.at}/>
                    <Space>
                        {notification.patient.flagged && <PushpinOutlined style={{marginLeft: 0}}/>}
                        {(unread[notification.patient.oid] || []).length > 0 && <Badge
                            className={badgeClass[notification.level]}
                            count={unread[notification.patient.oid].length}
                            size={"small"}/>}
                    </Space>
                </div>
            }>
                {notification.notifications.length ? <List>
                    {notification.notifications.map((message, j) =>
                        <Item key={`${notification.patient.oid}-${j}`}>
                            <Notification unread={(unread[notification.patient.oid] || []).includes(message.static_id)}
                                          markRead={() => markRead(notification.patient.oid, message.static_id)}
                                          patient={notification.patient.oid} message={message}/>
                        </Item>
                    )}
                </List> : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין עדכונים זמינים'}/>}
            </Panel>)}
        </Collapse>
    </div>
}
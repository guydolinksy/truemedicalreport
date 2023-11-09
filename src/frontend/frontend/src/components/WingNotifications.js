import {useNavigate, useParams} from "react-router-dom";
import React, {useCallback, useContext, useState, useEffect} from "react";
import {loginContext} from "./LoginContext";
import {Badge, Collapse, Drawer, Empty, List, Space} from "antd";
import {PushpinOutlined, UserOutlined} from "@ant-design/icons";
import {RelativeTime} from "./RelativeTime";
import {Notification} from "./Notification";
import moment from "moment";
import {hashMatchContext} from "./HashMatch";
import {notificationsContext} from "../contexts/NotificationContext";
import {filtersDataContext} from "./PatientsFilter";

const {Panel} = Collapse;
const {Item} = List;
const badgeClass = {
    0: 'status-badge status-success',
    1: 'status-badge status-warn',
    2: 'status-badge status-error',
}


const PatientNotification = ({patient, markRead, read}) => {
    const {user} = useContext(loginContext);

    const last = patient.notifications.sort(
        (k1, k2) => moment(k1.at).isAfter(k2.at) ? 1 : -1
    ).slice().pop();
    const worst = patient.notifications.sort(
        (k1, k2) => moment(k1.level).isAfter(k2.level) ? 1 : -1
    ).slice().pop();
    const unread = patient.notifications.filter(m => (read[patient.oid] || []).includes(m.key))

    return <Panel key={patient.oid} header={<>
                    <span className={`gender-${patient.info.gender}`}>
                        <UserOutlined/>{!user.anonymous && <span>&nbsp;{patient.info.name}</span>}
                    </span>
        <br/>
        <span style={{fontSize: "10px"}}>{last.message}</span>
    </>}
                  extra={<div style={{
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
                (k1, k2) => moment(k1.at).isAfter(k2.at) ? 1 : -1
            ).map(({key, message}, j) =>
                <Item key={`${patient.oid}-${j}`}>
                    <Notification
                        unread={unread.includes(message.static_id)}
                        markRead={() => markRead(patient.oid, message.static_id)}
                        patient={patient.oid} message={message}/>
                </Item>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE}
                       description={'אין עדכונים זמינים'}/>}
        </List>
    </Panel>
}
export const WingNotifications = () => {
    const navigate = useNavigate();
    const {value} = useContext(filtersDataContext.context);
    const {setNotifications} = useContext(notificationsContext);
    useEffect(() => {
        setNotifications(value.getPatients.patients.length)
    }, [value]);
    const {matched} = useContext(hashMatchContext);
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


    return <Drawer title={'עדכונים'} placement={"left"} open={matched(['notifications'])}
                   onClose={() => navigate('#')}>
        {value.getPatients.patients.length ?
            <div style={{display: "flex !important", flexDirection: "column", flex: "1"}}>
                <Collapse onChange={openChange} style={{flex: "1 0 10vh", minHeight: "10vh", overflowY: "auto"}}>
                    {value.getPatients.patients.filter(patient => patient.notifications.length).map(patient =>
                        <PatientNotification key={patient.oid} patient={patient} markRead={markRead} read={read}/>
                    )}
                </Collapse>
            </div> : <div style={{display: "flex", flex: 1, flexDirection: "column"}}>
                <Empty style={{height: 'fit-content'}} description={'אין התרעות'} image={Empty.PRESENTED_IMAGE_SIMPLE}/>
            </div>}
    </Drawer>
}
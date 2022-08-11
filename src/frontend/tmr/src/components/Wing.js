import React, {useCallback, useContext, useEffect, useState} from 'react';
import {Badge, List, Space, Card, Col, Collapse, Empty, Input, Layout, Menu, Row, Spin} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "./DataContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import debounce from 'lodash/debounce';
import {Highlighter} from './Highlighter'
import {Bed} from "./Bed";

import {PushpinOutlined, SettingOutlined, UserOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";

import {useViewport} from "./UseViewPort";
import moment from 'moment';
import {loginContext} from "./LoginContext";

const {Search} = Input;
const {Content, Sider} = Layout;
const wingDataContext = createContext(null);
const notificationsDataContext = createContext(null);

const highlighter = new Highlighter('root');
const {Panel} = Collapse;
const {Item} = List;
const badgeClass = {
    1: 'status-badge status-error',
    2: 'status-badge status-warn',
    3: 'status-badge status-success',
}
const WingNotificationsInner = ({wingName}) => {
    const navigate = useNavigate();
    const [openKeys, setOpenKeys] = useState([]);
    const [search, setSearch] = useState('');
    const {value, lastMessage} = useContext(notificationsDataContext.context);
    const {userSettings} = useContext(loginContext);

    useEffect(() => {
        highlighter.apply(search)
    }, [search]);

    useEffect(() => {
        if (!lastMessage)
            return;
        setOpenKeys(prevState => prevState.concat(...JSON.parse(lastMessage.data).openKeys || []));
    }, [lastMessage]);

    const openChange = useCallback(key => {
        let keys = Array.isArray(key) ? key : [key];

        setOpenKeys(prevState => {
            keys.filter(k => !prevState.includes(k)).forEach(k => navigate(`#highlight#${k}#open`));
            prevState.filter(k => !keys.includes(k)).forEach(k => navigate(`#highlight#${k}#close`));
            return keys;
        })
    }, [openKeys, navigate]);

    return <div style={{
        display: "flex",
        flexDirection: "column",
        height: '100vh',
        overflowY: "hidden",
        justifyContent: "space-between",
    }}>
        <div style={{
            display: "flex",
            flexDirection: "column",
            flex: 1,
            overflowY: "hidden",
        }}>
            <Collapse>
                <Panel key={'basic'} showArrow={false} extra={<SettingOutlined/>} header={wingName}>
                </Panel>
            </Collapse>
            <Search key={'search'} allowClear onChange={debounce(e => setSearch(e.target.value), 300)}
                    placeholder={'חיפוש'}/>
            <Collapse style={{overflowY: "auto", flex: 1}} activeKey={openKeys} onChange={openChange}>
                {value.map((notification) =>
                    <Panel key={notification.patient.oid} showArrow={false} header={
                        <div style={{
                            display: "flex",
                            flexFlow: "column nowrap",
                            alignItems: "flex-start",
                        }}>
                            <div><UserOutlined/>&nbsp;{notification.patient.name}</div>
                            <div style={{
                                textOverflow: "ellipsis",
                                fontSize: "10px"
                            }}>{notification.preview}</div>
                        </div>
                    } extra={
                        <div style={{
                            display: "flex",
                            flexFlow: "column nowrap",
                            alignItems: "flex-end",
                        }}>
                            <Moment style={{display: "block"}}
                                    date={notification.at || notification.patient.arrival}
                                    format={'hh:mm'}/>
                            <Space>
                                {notification.patient.flagged &&
                                    <PushpinOutlined style={{marginLeft: 0}}/>}
                                {notification.notifications.length > 0 &&
                                    <Badge
                                        className={badgeClass[notification.level]}
                                        count={notification.notifications.length}
                                        size={"small"}/>}
                            </Space>
                        </div>
                    }>
                        <List>
                            {notification.notifications.map((message, j) =>
                                <Item><Link key={`${notification.patient.oid}-${j}`}
                                            to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
                                    <span className={message.danger ? 'warn-text' : undefined}>{message.message}</span>
                                </Link></Item>
                            )}
                        </List>
                    </Panel>
                )}
            </Collapse>
        </div>
        <Menu selectable={false} mode={"inline"} style={{userSelect: "none"}} items={[
            {key: 'exit', label: <span><FontAwesomeIcon icon={faRightFromBracket}/>&nbsp;חזרה למחלקה</span>}
        ]} onClick={() => navigate('/')}/>
    </div>
};
const WingNotifications = ({department, wing, wingName, onError}) => {
    const notificationsURI = `/api/departments/${department}/wings/${wing}/notifications`;

    return <notificationsDataContext.Provider url={notificationsURI} defaultValue={[]} onError={onError}>
        {({loading}) => loading ? <Spin/> : <WingNotificationsInner wingName={wingName}/>}
    </notificationsDataContext.Provider>;
}
const WingLayout = ({department, wing, details, onError}) => {
    return <Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
        {(details.rows || []).map((row, i) => <Row key={i} style={row} wrap={false}>
            {(details.columns || []).map((column, j) =>
                details.beds[i][j] === null ? <div key={`filler-${j}`} style={column}/> :
                    <Bed key={`bed-${details.beds[i][j]}`} style={column} admission={{
                        department: department,
                        wing: wing,
                        bed: details.beds[i][j]
                    }} onError={onError}/>
            )}
        </Row>)}
    </Card>
}
const Patients = ({patients, onError}) => {
    return <Card key={'overflow'} style={{width: '100%', flex: '1'}}>
        {patients.length ? <div style={{
            display: "grid",
            gridGap: 16,
            gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))"
        }}>
            {patients.map(patient => <Patient key={patient.oid} patient={patient.oid}
                                              style={{flex: '1', minWidth: 300}} onError={onError}/>)}
        </div> : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>}
    </Card>
}
const WingInner = ({department, wing, onError}) => {
    const navigate = useNavigate();
    const {value, flush} = useContext(wingDataContext.context);

    const onInfoError = useCallback(() => {
        flush(true)
        navigate('#')
    }, [navigate, flush]);

    const siderWidth = 350, totalWidth = useViewport();

    const forceTabletMode = useCallback(() => {
        const buffer = 100;
        if (!value || !value.details || !value.details.columns)
            return true
        return totalWidth - siderWidth - value.details.columns.reduce((s, c) => s + c.minWidth, 0) < buffer;
    }, [totalWidth, value, siderWidth]);

    const [tabletMode, setTabletMode] = useState({forced: forceTabletMode(), value: false})

    useEffect(() => {
        setTabletMode(({value}) => ({forced: forceTabletMode(), value: value}))
    }, [forceTabletMode, totalWidth, value, siderWidth]);

    const allPatients = value.patients.sort((i, j) => moment(i.arrival).isAfter(j.arrival) ? 1 : -1);
    const unassignedPatients = allPatients.filter(({oid, admission}) => !admission.bed);
    return <Layout>
        <Sider breakpoint={"lg"} width={siderWidth}>
            <WingNotifications department={department} wing={wing} wingName={value.details.name} onError={onError}/>
        </Sider>
        <Content className={'content'} style={{overflowY: "auto"}}>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {tabletMode.forced || tabletMode.value ?
                    <Patients key={'patients'} patients={allPatients} onError={flush}/> : [
                        <WingLayout key={'wing'} department={department} wing={wing} details={value.details}
                                    onError={flush}/>,
                        <Patients key={'patients'} patients={unassignedPatients} onError={flush}/>
                    ]}
            </Col>
        </Content>
        <PatientInfo onError={onInfoError}/>
    </Layout>
};

export const Wing = ({department, wing, onError}) => {
    const uri = `/api/departments/${department}/wings/${wing}`;

    return <wingDataContext.Provider url={uri} defaultValue={{patients: [], details: {}}} onError={onError}>
        {({loading}) => loading ? <Spin/> : <WingInner department={department} wing={wing} onError={onError}/>}
    </wingDataContext.Provider>
}

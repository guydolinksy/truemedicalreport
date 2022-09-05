import React, {useCallback, useContext, useEffect, useMemo, useState} from 'react';
import {
    Badge, Card, Col, Collapse, Divider, Empty, Input, Layout, List, Menu, Radio, Row, Select, Space, Spin, TreeSelect,
} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "../hooks/DataContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import debounce from 'lodash/debounce';
import {Highlighter} from './Highlighter'
import {Bed} from "./Bed";
import {PushpinOutlined, UserOutlined, FilterOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";

import {useViewport} from "./UseViewPort";
import moment from 'moment';
import {useLocalStorage} from "../hooks/localStorageHook";

const {Option} = Select;
const {Search} = Input;
const {Content, Sider} = Layout;
const wingDataContext = createContext(null);

const highlighter = new Highlighter('root');
const {SHOW_PARENT} = TreeSelect;
const {Panel} = Collapse;
const {Item} = List;
const badgeClass = {
    1: 'status-badge status-error',
    2: 'status-badge status-warn',
    3: 'status-badge status-success',
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
const WingStatus = () => {
    const navigate = useNavigate();
    const [openKeys, setOpenKeys] = useState([]);
    const [search, setSearch] = useState('');
    const {value, lastMessage} = useContext(wingDataContext.context);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'location');

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

    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
    const toTree = filter => ({
        value: filter.key,
        title: `(${filter.count}) ${filter.title}`,
        children: (filter.children || []).map(toTree)
    })
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
            <Collapse defaultActiveKey={['basic'].concat(openKeys)} onChange={openChange}
                      style={{overflowY: "auto", flex: 1}}>
                <Panel key={'basic'} header={value.details.name} extra={<FilterOutlined/>}>
                    <Search key={'search'} allowClear onChange={debounce(e => setSearch(e.target.value), 300)}
                            placeholder={'חיפוש:'}/>
                    <Divider/>
                    <Select showSearch allowClear mode={"multiple"} placeholder="סינון לפי רופא.ה מטפל.ת:"
                            style={{width: '100%'}} value={selectedDoctors} onChange={setSelectedDoctors}>
                        {value.filters.doctors.map(filter => <Option key={filter.key} value={filter.value}>
                            {filter.title}
                        </Option>)}
                    </Select>
                    <Divider/>
                    <TreeSelect treeData={value.filters.awaiting.map(toTree)} style={{width: '100%'}} showSearch allowClear
                                placeholder="סינון לפי המתנה עבור:" treeDefaultExpandAll onChange={setSelectedAwaiting}
                                value={selectedAwaiting} showCheckedStrategy={SHOW_PARENT} treeCheckable multiple/>
                    <Divider/>
                    <Radio.Group value={wingSortKey} onChange={e => setWingSortKey(e.target.value)}
                                 buttonStyle={"solid"}
                                 style={{width: '100%', flexDirection: "row", flexWrap: "nowrap", display: "flex"}}>
                        <Radio.Button value={"location"} style={{flex: "1 1 30px", textAlign: "center"}}>
                            מיקום
                        </Radio.Button>
                        <Radio.Button value={"arrival"} style={{flex: "1 1 40px", textAlign: "center"}}>
                            זמן קבלה
                        </Radio.Button>
                        <Radio.Button value={"name"} style={{flex: "1 1 40px", textAlign: "center"}}>
                            שם מלא
                        </Radio.Button>
                        <Radio.Button value={"severity"} style={{flex: "1 1 35px", textAlign: "center"}}>
                            דחיפות
                        </Radio.Button>
                    </Radio.Group>
                </Panel>
                {value.notifications.map((notification) =>
                    <Panel key={notification.patient.oid} showArrow={false} header={
                        <div style={{
                            display: "flex",
                            flexFlow: "column nowrap",
                            alignItems: "flex-start",
                        }}>
                            <div><UserOutlined/>&nbsp;{notification.patient.info.name}</div>
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
                                    date={notification.at || notification.patient.admission.arrival}
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
                        {notification.notifications.length ? <List>
                            {notification.notifications.map((message, j) =>
                                <Item key={`${notification.patient.oid}-${j}`}>
                                    <Link to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
                                        <span className={message.danger ? 'warn-text' : undefined}>
                                            {message.message}
                                        </span>
                                    </Link>
                                </Item>
                            )}
                        </List> : <Empty description={'אין התרעות חדשות'}/>}
                    </Panel>
                )}
            </Collapse>
        </div>
        <Menu selectable={false} mode={"inline"} style={{userSelect: "none"}} items={[
            {key: 'exit', label: <span><FontAwesomeIcon icon={faRightFromBracket}/>&nbsp;חזרה למחלקה</span>}
        ]} onClick={() => navigate('/')}/>
    </div>
};
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

const sortFunctions = {
    name: (i, j) => i.info.name.localeCompare(j.info.name),
    severity: (i, j) => i.severity.value - j.severity.value,
    arrival: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1,
    location: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1,
    [undefined]: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1
}
const WingInner = ({department, wing}) => {
    const navigate = useNavigate();
    const {value, flush} = useContext(wingDataContext.context);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'location');
    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);

    const onInfoError = useCallback(() => {
        flush(true)
        navigate('#')
    }, [navigate, flush]);

    const siderWidth = 350, totalWidth = useViewport();

    const isForceTabletMode = useMemo(() => {
        const buffer = 100;
        if (!value || !value.details || !value.details.columns)
            return true
        return totalWidth - siderWidth - value.details.columns.reduce((s, c) => s + c.minWidth, 0) < buffer;
    }, [totalWidth, value, siderWidth]);

    const allPatients = value.patients.filter(({oid}) => !selectedAwaiting.length || selectedAwaiting.find(
        filter => value.filters.mapping[filter].includes(oid)
    )).filter(({oid}) => !selectedDoctors.length || selectedDoctors.find(
        filter => value.filters.mapping[filter].includes(oid)
    )).sort(sortFunctions[wingSortKey]);
    const unassignedPatients = allPatients.filter(({admission}) => !admission.bed);
    return <Layout>
        <Sider breakpoint={"lg"} width={siderWidth}>
            <WingStatus/>
        </Sider>
        <Content className={'content'} style={{overflowY: "auto"}}>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {isForceTabletMode || wingSortKey !== 'location' || selectedDoctors.length || selectedAwaiting.length ?
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

    return <wingDataContext.Provider url={uri} defaultValue={
        {patients: [], details: {}, filters: {mapping: {}, filters: []}, notifications: []}
    } onError={onError}>
        {({loading}) => loading ? <Spin/> : <WingInner department={department} wing={wing} onError={onError}/>}
    </wingDataContext.Provider>
}

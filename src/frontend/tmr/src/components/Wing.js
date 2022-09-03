import React, {useCallback, useContext, useEffect, useMemo, useState} from 'react';
import {
    Badge, Card, Col, Collapse, Divider, Empty, Input, Layout, List, Menu, Radio, Row, Space, Spin, TreeSelect,
    Typography
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
import {PushpinOutlined, UserOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";

import {useViewport} from "./UseViewPort";
import moment from 'moment';
import {useLocalStorage} from "../hooks/localStorageHook";

const {Paragraph} = Typography;
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

    const [selectedFilters, setSelectedFilters] = useLocalStorage('selectedFilters', []);

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
                <Panel key={'basic'} header={value.details.name}>
                    <Paragraph>
                        סנן לפי:
                    </Paragraph>
                    <TreeSelect treeData={value.filters.tree} showSearch style={{width: '100%'}} value={selectedFilters}
                                dropdownStyle={{maxHeight: 400, overflow: 'auto'}} placeholder="סינון מטופלים.ות:"
                                allowClear multiple treeDefaultExpandAll onChange={setSelectedFilters} treeCheckable
                                showCheckedStrategy={SHOW_PARENT}/>
                    <Divider/>
                    <Paragraph>
                        מיין לפי:
                    </Paragraph>
                    <Radio.Group value={wingSortKey} onChange={e => setWingSortKey(e.target.value)}>
                        <Radio.Button value={"location"}>מיקום</Radio.Button>
                        <Radio.Button value={"arrival"}>זמן קבלה</Radio.Button>
                        <Radio.Button value={"name"}>שם מלא</Radio.Button>
                        <Radio.Button value={"severity"}>דחיפות</Radio.Button>
                    </Radio.Group>
                    <Divider/>
                    <Paragraph>
                        רופא מטפל:
                    </Paragraph>
                    <Radio.Group>
                        <Radio.Button value="doctor-1">דר שרון שושן</Radio.Button>
                        <Radio.Button value="doctor-2">דר נופרת נהוראי</Radio.Button>
                        <Radio.Button value="doctor-3">דר גבע הרמלין</Radio.Button>
                    </Radio.Group>
                </Panel>
            </Collapse>
            <Search key={'search'} allowClear onChange={debounce(e => setSearch(e.target.value), 300)}
                    placeholder={'חיפוש'}/>
            <Collapse style={{overflowY: "auto", flex: 1}} activeKey={openKeys} onChange={openChange}>
                {value.notifications.map((notification) =>
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
                                <Item key={`${notification.patient.oid}-${j}`}>
                                    <Link to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
                                        <span className={message.danger ? 'warn-text' : undefined}>
                                            {message.message}
                                        </span>
                                    </Link>
                                </Item>
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
    name: (i, j) => i.name.localeCompare(j.name),
    severity: (i, j) => i.severity.value - j.severity.value,
    arrival: (i, j) => moment(i.arrival).isAfter(j.arrival) ? 1 : -1,
    location: (i, j) => moment(i.arrival).isAfter(j.arrival) ? 1 : -1,
    [undefined]: (i, j) => moment(i.arrival).isAfter(j.arrival) ? 1 : -1
}
const WingInner = ({department, wing}) => {
    const navigate = useNavigate();
    const {value, flush} = useContext(wingDataContext.context);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'location');
    const [selectedFilters, setSelectedFilters] = useLocalStorage('selectedFilters', []);

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

    const allPatients = value.patients.filter(({oid}) => !selectedFilters.length || selectedFilters.find(
        filter => value.filters.mapping[filter].includes(oid)
    )).sort(sortFunctions[wingSortKey]);
    const unassignedPatients = allPatients.filter(({admission}) => !admission.bed);
    return <Layout>
        <Sider breakpoint={"lg"} width={siderWidth}>
            <WingStatus/>
        </Sider>
        <Content className={'content'} style={{overflowY: "auto"}}>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {isForceTabletMode || wingSortKey !== 'location' || selectedFilters.length ?
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

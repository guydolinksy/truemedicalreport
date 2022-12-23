import React, {useCallback, useContext, useEffect, useMemo, useState} from 'react';
import {
    Badge, Button,
    Card,
    Col,
    Collapse,
    Divider,
    Empty,
    Input,
    Layout,
    List,
    Menu, Popover,
    Radio,
    Row,
    Select,
    Space,
    Spin,
    Tag,
    Tree
} from 'antd';
import {MIN_WIDTH, Patient} from "./Patient";
import {createContext} from "../hooks/DataContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import debounce from 'lodash/debounce';
import {Highlighter} from './Highlighter'
import {Bed} from "./Bed";
import {FilterOutlined, PushpinOutlined, RightOutlined, UserOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";
import {useLocalStorage} from "../hooks/localStorageHook";
import moment from "moment";
import { useViewport } from "./UseViewPort";

const {Search} = Input;
const {Content, Sider} = Layout;
const {CheckableTag} = Tag;
const wingDataContext = createContext(null);

const highlighter = new Highlighter('root');
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
const WingNotification = ({oid, notification, message, unread, markRead}) => {
    useEffect(() => {
        let task = setTimeout(() => markRead(oid, message.static_id), 6000);
        return () => clearTimeout(task);
    }, [oid, notification, message, markRead]);
    return <>
        <Link to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
            {(unread[oid] || []).includes(message.static_id) && <Badge status={'processing'}/>}
            &nbsp;<span className={message.danger ? 'warn-text' : undefined}>{message.message}</span>
        </Link>
        <Moment style={{display: "block"}} date={message.at} format={'HH:mm'}/>
    </>
}
const WingNotifications = () => {
    const navigate = useNavigate();
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
        return <Empty description={'אין התרעות'} image={Empty.PRESENTED_IMAGE_SIMPLE}/>
    return <div style={{display: "flex", flexDirection: "column", flex: 1, overflowY: "hidden"}}>
        <Collapse onChange={openChange} style={{overflowY: "auto", flex: 1}}>
            {value.notifications.map((notification) => <Panel key={notification.patient.oid} header={
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
                    <Moment style={{display: "block"}} date={notification.at} format={'HH:mm'}/>
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
                            <WingNotification oid={notification.patient.oid} notification={notification}
                                              message={message} markRead={markRead} unread={unread}/>
                        </Item>
                    )}
                </List> : <Empty description={'אין התרעות חדשות'}/>}
            </Panel>)}
        </Collapse>
    </div>
}

const WingStatus = () => {
    const navigate = useNavigate();
    const [search, setSearch] = useState('');
    const {value} = useContext(wingDataContext.context);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'location');

    useEffect(() => {
        highlighter.apply(search)
    }, [search]);


    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
    const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);

    const toTree = filter => ({
        key: filter.key,
        title: `(${filter.count}) ${filter.title}`,
        children: (filter.children || []).map(toTree)
    })

    const handleDoctorFilterChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedDoctors, tag] : selectedDoctors.filter((t) => t !== tag);
        setSelectedDoctors(nextSelectedTags);
    };

    const handleDecisionStatusFilterChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTreatments, tag] : selectedTreatments.filter((t) => t !== tag);
        setSelectedTreatments(nextSelectedTags);
    };

    const filterTagsContainerStyle = {
        display: 'flex',
        flexWrap: "wrap",
        gap: '5px 0',
        justifyContent: "space-between",
    }

    return <div style={{
        display: "flex",
        flexDirection: "column",
        height: '100vh',
        overflowY: "hidden",
        justifyContent: "space-between",
    }}>
        <Collapse defaultActiveKey={['basic']}>
            <Panel key={'basic'} header={value.details.name} extra={<FilterOutlined/>}>
                <Search key={'search'} allowClear onChange={debounce(e => setSearch(e.target.value), 300)}
                        placeholder={'חיפוש:'}/>
                <Divider style={{marginTop: 10, marginBottom: 10}}/>
                <div style={filterTagsContainerStyle}>
                    <b style={{whiteSpace: "nowrap"}}>מטפל.ת:</b>
                    {value.filters.doctors.map(filter => <CheckableTag
                        key={filter.key}
                        checked={selectedDoctors.indexOf(filter.key) > -1}
                        onChange={(checked) => handleDoctorFilterChange(filter.key, checked)}
                    >
                        {filter.title}
                    </CheckableTag>)}
                </div>
                <Divider style={{marginTop: 10, marginBottom: 10}}/>
                <div style={filterTagsContainerStyle}>
                    <b style={{whiteSpace: "nowrap"}}>יעד:</b>
                    {value.filters.treatments.map(filter => <CheckableTag
                        key={filter.key}
                        checked={selectedTreatments.indexOf(filter.key) > -1}
                        onChange={(checked) => handleDecisionStatusFilterChange(filter.key, checked)}
                    >
                        {filter.title}
                    </CheckableTag>)}
                </div>
                <Divider style={{marginTop: 10, marginBottom: 10}}/>
                <Tree treeData={value.filters.awaiting.map(toTree)} style={{width: '100%'}} checkable multiple
                      defaultExpandedKeys={value.filters.awaiting.map(x => x.key)}
                      placeholder="סינון לפי המתנה עבור:" onCheck={setSelectedAwaiting}
                      checkedKeys={selectedAwaiting}/>
                <Divider style={{marginTop: 10, marginBottom: 10}}/>
                <Radio.Group value={wingSortKey} onChange={e => setWingSortKey(e.target.value)}
                             buttonStyle={"solid"}
                             style={{width: '100%', flexDirection: "row", flexWrap: "nowrap", display: "flex"}}>
                    <Radio.Button value={"location"} style={{flex: "1 1 30px", textAlign: "center"}}>
                        <span style={{whiteSpace: "nowrap"}}>מיקום</span>
                    </Radio.Button>
                    <Radio.Button value={"arrival"} style={{flex: "1 1 50px", textAlign: "center"}}>
                        <span style={{whiteSpace: "nowrap"}}>זמן קבלה</span>
                    </Radio.Button>
                    <Radio.Button value={"name"} style={{flex: "1 1 50px", textAlign: "center"}}>
                        <span style={{whiteSpace: "nowrap"}}>שם מלא</span>
                    </Radio.Button>
                    <Radio.Button value={"severity"} style={{flex: "1 1 35px", textAlign: "center"}}>
                        <span style={{whiteSpace: "nowrap"}}>דחיפות</span>
                    </Radio.Button>
                </Radio.Group>
            </Panel>
        </Collapse>
        <WingNotifications/>
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
            gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
        }}>
            {patients.map(patient => <Patient key={patient.oid} patient={patient.oid}
                                              style={{flex: '1', minWidth: MIN_WIDTH}} onError={onError}/>)}
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
    const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);

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
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(({oid}) => !selectedTreatments.length || selectedTreatments.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(({oid}) => !selectedDoctors.length || selectedDoctors.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).sort(sortFunctions[wingSortKey]);
    const unassignedPatients = allPatients.filter(({admission}) => !admission.bed);

    const patientList = <List>
        {value.patients.map((i, patient) => <List.Item key={i}>
            <Button onClick={() => navigate(`#highlight#${patient.oid}#open`)}>{patient.info.name}</Button></List.Item>)}
    </List>

    return <Layout>
        <Sider breakpoint={"lg"} width={siderWidth}>
            <WingStatus/>
        </Sider>
        <Content className={'content'} style={{overflowY: "auto"}}>
            <Popover placement={"bottomLeft"} content={patientList} title={"מטופלים.ות:"}>
                <Button type={"primary"} style={{position: "absolute", top: 0, left: 0}} icon={<RightOutlined />}/>
            </Popover>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {isForceTabletMode || wingSortKey !== 'location' || selectedDoctors.length || selectedTreatments.length || selectedAwaiting.length ?
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

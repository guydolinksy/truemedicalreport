import React, {Suspense, useCallback, useContext, useMemo, useState} from 'react';
import {Button, Card, Col, Collapse, Empty, Layout, Modal, Popover, Radio, Row, Spin, Tooltip} from 'antd';
import {MIN_WIDTH, Patient} from "./Patient";
import {createContext} from "../hooks/DataContext";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import {Bed} from "./Bed";
import {FilterOutlined, QuestionOutlined, SearchOutlined} from "@ant-design/icons";
import {useLocalStorage} from "../hooks/localStorageHook";
import moment from "moment";
import {useViewport} from "./UseViewPort";
import {Department} from "./Department";
import {loginContext} from "./LoginContext";
import {DarkTheme, LightTheme} from "../themes/ThemeContext";
import {WingNotifications} from "./WingNotifications";
import {PatientList} from "./PatientList";
import {Legend} from "./Legend";
import {SortPatients} from "./SortPatients";

const {Content, Sider} = Layout;
export const wingDataContext = createContext(null);

const {Panel} = Collapse;

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

const WingStatus = ({department}) => {
    const {value} = useContext(wingDataContext.context);
    const {userSettings} = useContext(loginContext);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'arrival');

    const [isDepartmentPeekModelOpen, setIsDepartmentPeekModelOpen] = useState(false);

    return <div style={{
        display: "flex",
        flexDirection: "column",
        height: '100vh',
        // overflowY: "hidden",
        justifyContent: "space-between",
    }}>
        <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
            <Card bodyStyle={{display: "flex", padding: '10px'}}>
                <div style={{display: 'flex', flex: 1, justifyContent: 'space-between'}}>
                    <span>{value.details.name} - <b>{value.patients.length}</b> מטופלים.ות</span>
                    <ul style={{display: 'flex', gap: '0 5px', margin: 0}}>
                        <li>
                            <Tooltip overlay='מחלקות'>
                                <FontAwesomeIcon onClick={(evt) => {
                                    evt.stopPropagation();
                                    setIsDepartmentPeekModelOpen(true);
                                }} icon={faRightFromBracket} style={{cursor: 'pointer'}}/>
                            </Tooltip>
                        </li>
                    </ul>
                </div>
            </Card>
            <Collapse defaultActiveKey={['1', '2']}
                      style={{height: '100%', display: "flex", flexDirection: "column", overflowY: "scroll"}}>
                <Panel header={"סינון"} key={1} extra={<FilterOutlined/>}>
                    <Radio.Group value={wingSortKey} onChange={e => setWingSortKey(e.target.value)}
                                 buttonStyle={"solid"}
                                 style={{width: '100%', flexDirection: "row", flexWrap: "nowrap", display: "flex"}}>
                        <Radio.Button value={"arrival"} style={{flex: "1 1 50px", textAlign: "center"}}>
                            <span style={{whiteSpace: "nowrap"}}>זמן קבלה</span>
                        </Radio.Button>
                        <Radio.Button value={"location"} style={{flex: "1 1 30px", textAlign: "center"}}>
                            <span style={{whiteSpace: "nowrap"}}>מיקום</span>
                        </Radio.Button>
                        <Radio.Button value={"name"} style={{flex: "1 1 50px", textAlign: "center"}}>
                            <span style={{whiteSpace: "nowrap"}}>שם מלא</span>
                        </Radio.Button>
                        <Radio.Button value={"severity"} style={{flex: "1 1 35px", textAlign: "center"}}>
                            <span style={{whiteSpace: "nowrap"}}>דחיפות</span>
                        </Radio.Button>
                    </Radio.Group>
                </Panel>
                <Panel className="collapseNotifications" header="עדכונים" key="2" collapsible={"disabled"}
                       showArrow={false} style={{display: "flex", flexDirection: "column", flex: 1}}>
                    <WingNotifications/>
                </Panel>
            </Collapse>
        </div>
        <Modal title="נתוני מחלקה"
               open={isDepartmentPeekModelOpen}
               onCancel={() => setIsDepartmentPeekModelOpen(false)}
               footer={null}
               width='fit-content'
        >
            <ul style={{display: 'flex', gap: '0 20px', margin: 0}} className={userSettings.theme}>
                <Suspense fallback={<span/>}>
                    {userSettings.theme === 'dark-theme' ? <DarkTheme/> : <LightTheme/>}
                </Suspense>
                <Department department={department}/>
            </ul>
        </Modal>
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
                                              style={{minWidth: MIN_WIDTH}} onError={onError}/>)}
        </div> : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>}
    </Card>
}

const sortFunctions = {
    name: (i, j) => i.info.name.localeCompare(j.info.name),
    severity: (i, j) => {
        if (![null, undefined].includes(i.severity.value) && ![null, undefined].includes(j.severity.value))
            return i.severity.value - j.severity.value;
        else if ([null, undefined].includes(i.severity.value))
            return [null, undefined].includes(j.severity.value) ? 0 : 1;
        return -1
    },
    arrival: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1,
    location: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1,
    [undefined]: (i, j) => moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1
}
const WingInner = ({department, wing}) => {
    const navigate = useNavigate();

    const {user, userSettings} = useContext(loginContext);
    const {value, flush} = useContext(wingDataContext.context);

    const [wingSortKey, setWingSortKey] = useLocalStorage('wingSortKey', 'arrival');
    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
    const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);
    const [selectedTime, setSelectedTime] = useLocalStorage('selectedTime', []);

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

    const allPatients = value.patients.filter(({oid}) => !selectedAwaiting.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedAwaiting.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(({oid}) => !selectedTreatments.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedTreatments.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(({oid}) => !selectedDoctors.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedDoctors.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(({oid}) => !selectedTime.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedTime.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).sort(sortFunctions[wingSortKey]);
    const unassignedPatients = allPatients.filter(({admission}) => !admission.bed);

    return <Layout>
        <Sider breakpoint={"lg"} width={siderWidth}>
            <WingStatus department={department}/>
        </Sider>
        <Content className={'content'} style={{height: '100vh', overflowY: 'scroll'}}>
            <Popover placement={"leftTop"}
                     content={<PatientList value={value} user={user} userSettings={userSettings}/>}
                     title={"מטופלים.ות:"}>
                <Button type={"primary"} style={{position: "absolute", top: 41, left: 0, width: 40, zIndex: 1000}}
                        icon={<SearchOutlined/>}/>
            </Popover>
            <Popover placement={"leftTop"}
                     content={<SortPatients value={value} user={user} userSettings={userSettings}/>} title={"סינון:"}>
                <Button type={"primary"} style={{position: "absolute", top: 80, left: 0, width: 40, zIndex: 1000}}
                        icon={<FilterOutlined/>}/>
            </Popover>
            <Popover placement={"leftTop"} content={<Legend userSettings={userSettings}/>} title={"מקרא:"}>
                <Button type={"primary"} style={{position: "absolute", top: 119, left: 0, width: 40, zIndex: 1000}}
                        icon={<QuestionOutlined/>}/>
            </Popover>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {isForceTabletMode || wingSortKey !== 'location' || selectedDoctors.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length || selectedTreatments.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length || selectedAwaiting.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length || selectedTime.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length ?
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

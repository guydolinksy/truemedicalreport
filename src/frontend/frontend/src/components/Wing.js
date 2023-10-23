import React, {useCallback, useContext, useEffect, useMemo, useState} from 'react';
import {Button, Card, Col, Collapse, Drawer, Empty, Layout, Popover, Radio, Row} from 'antd';
import {MIN_WIDTH, Patient} from "./Patient";
import {useLocation, useNavigate} from "react-router-dom";
import {PatientInfo} from "./PatientInfo";
import {Bed} from "./Bed";
import {FilterOutlined, SortAscendingOutlined} from "@ant-design/icons";
import {useLocalStorage} from "../hooks/localStorageHook";
import moment from "moment";
import {useViewport} from "./UseViewPort";
import {loginContext} from "./LoginContext";
import {WingNotifications} from "./WingNotifications";
import {Legend} from "./Legend";
import {FilterPatients} from "./FilterPatients";
import {wingDataContext} from "../pages/WingView";
import {hashMatchContext} from "./HashMatch";
import {MCIForm} from "./MCI/MCIForm";

const {Content} = Layout;

const {Panel} = Collapse;

const WingLayout = ({department, wing, mci, details, onError, unassignedPatients}) => {
    return [
        <Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
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
        </Card>,
        <Card key={'overflow'} style={{width: '100%', flex: '1 0 300px', overflowY: 'auto'}}>
            <Patients patients={unassignedPatients} mci={mci} style={{
                display: "grid",
                gridGap: 16,
                gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
            }}/>
        </Card>
    ]
}
const StatusLayout = ({patients, mci}) => {

    const {value} = useContext(wingDataContext.context);
    const needAttention = patients.filter(
        patient => Object.values(value.patients[patient].watching).find(watchKey => watchKey.triggered)
    )
    const unassigned = patients.filter(
        patient => !needAttention.includes(patient) && value.patients[patient].status === 'unassigned'
    )
    const undecided = patients.filter(
        patient => !needAttention.includes(patient) && value.patients[patient].status === 'undecided'
    )
    const decided = patients.filter(
        patient => !needAttention.includes(patient) && value.patients[patient].status === 'decided'
    )
    return [
        <Card size={'small'} key={'needAttention'} style={{width: '100%', marginBottom: 16}}
              title={`ממתינים עבורך (${needAttention.length})`}
              bodyStyle={!needAttention.length ? {display: 'none'} : {}}>
            {needAttention.length > 0 && <Patients patients={needAttention} mci={mci} style={{
                display: "grid",
                gridGap: 16,
                gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
            }} showAttention/>}
        </Card>,
        <Card size={'small'} key={'unassigned'} style={{width: '100%', marginBottom: 16}}
              title={`ללא שיוך לרופא.ה (${unassigned.length})`}
              bodyStyle={!unassigned.length ? {display: 'none'} : {}}>
            {unassigned.length > 0 && <Patients patients={unassigned} mci={mci} style={{
                display: "grid",
                gridGap: 16,
                gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
            }}/>}
        </Card>,
        <Card size={'small'} key={'undecided'} style={{width: '100%', marginBottom: 16}}
              title={`ללא החלטה על יעד (${undecided.length})`}
              bodyStyle={!undecided.length ? {display: 'none'} : {}}>
            {undecided.length > 0 && <Patients patients={undecided} mci={mci} style={{
                display: "grid",
                gridGap: 16,
                gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
            }}/>}
        </Card>,
        <Card size={'small'} key={'decided'} style={{width: '100%', marginBottom: 16}}
              title={`ממתין לאשפוז/שחרור (${decided.length})`}
              bodyStyle={!decided.length ? {display: 'none'} : {}}>
            {decided.length > 0 && <Patients patients={decided} mci={mci} style={{
                display: "grid",
                gridGap: 16,
                gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
            }}/>}
        </Card>,
    ]
}

const Patients = ({patients, onError, style, showAttention, mci}) => {
    return patients.length ? <div style={style}>
        {patients.map(oid => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}} onError={onError}
                                      showAttention={showAttention} mci={mci}/>)}
    </div> : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>


}

const sortFunctions = (patients, sortKey) => {
    return {
        name: (i, j) => patients[i].info.name.localeCompare(patients[j].info.name),
        severity: (i, j) => {
            if (![null, undefined].includes(patients[i].severity) && ![null, undefined].includes(patients[j].value))
                return patients[i].severity.value - patients[j].severity.value;
            else if ([null, undefined].includes(patients[i].value))
                return [null, undefined].includes(patients[j].value) ? 0 : 1;
            return -1
        },
        arrival: (i, j) => moment(patients[i].admission.arrival).isAfter(patients[j].admission.arrival) ? 1 : -1,
        status: (i, j) => moment(patients[i].admission.arrival).isAfter(patients[j].admission.arrival) ? 1 : -1,
        location: (i, j) => moment(patients[i].admission.arrival).isAfter(patients[j].admission.arrival) ? 1 : -1,
        [undefined]: (i, j) => moment(patients[i].admission.arrival).isAfter(patients[j].admission.arrival) ? 1 : -1
    }[sortKey]
}
export const Wing = ({department, wing}) => {
    const mci = department === 'mci';
    const navigate = useNavigate();
    const {hash} = useLocation();

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

    const allPatients = Object.keys(value.patients).filter(oid => !selectedAwaiting.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedAwaiting.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(oid => !selectedTreatments.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedTreatments.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(oid => !selectedDoctors.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedDoctors.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).filter(oid => !selectedTime.filter(
        filter => value.filters.mapping[filter] !== undefined
    ).length || selectedTime.find(
        filter => (value.filters.mapping[filter] || []).includes(oid)
    )).sort(sortFunctions(value.patients, wingSortKey));
    const unassignedPatients = allPatients.filter(oid => !value.patients[oid].admission.bed);


    const [{title, className}, setHeader] = useState({});
    const {matched} = useContext(hashMatchContext);

    return <>
        <Content className={'content'} style={{flex: 1, display: 'flex', overflowY: 'scroll', padding: '0 20px'}}>
            <Col style={{padding: 16, flex: 1, display: 'flex', flexFlow: 'column nowrap'}}>
                {!isForceTabletMode && wingSortKey === 'location' && !selectedDoctors.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length && !selectedTreatments.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length && !selectedAwaiting.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length && !selectedTime.filter(
                    filter => value.filters.mapping[filter] !== undefined
                ).length ? <WingLayout department={department} wing={wing} details={value.details}
                                       onError={flush} unassignedPatients={unassignedPatients} mci={mci}/> :
                    wingSortKey !== 'status' ? <Patients patients={allPatients} onError={flush} style={{
                            display: "grid",
                            gridGap: 16,
                            gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
                        }} mci={mci}/> :
                        <StatusLayout department={department} wing={wing} onError={flush} patients={allPatients}
                                      mci={mci}/>

                }
            </Col>
        </Content>
        <Popover placement={"leftTop"}
                 content={<FilterPatients value={value} user={user} userSettings={userSettings}/>}
                 title={"סינון תצוגת אגף"}>
            <Button type={"primary"} style={{position: "absolute", top: 80, left: 0, width: 40, zIndex: 1000}}
                    icon={<FilterOutlined/>}/>
        </Popover>
        <Popover placement={"leftTop"}
                 content={
                     <Radio.Group value={wingSortKey} onChange={e => setWingSortKey(e.target.value)}
                                  buttonStyle={"solid"}
                                  style={{width: '100%', flexDirection: "row", flexWrap: "nowrap", display: "flex"}}>
                         <Radio.Button value={"arrival"} style={{flex: "1 1 50px", textAlign: "center"}}>
                             <span style={{whiteSpace: "nowrap"}}>לפי זמן קבלה</span>
                         </Radio.Button>
                         <Radio.Button value={"location"} style={{flex: "1 1 30px", textAlign: "center"}}>
                             <span style={{whiteSpace: "nowrap"}}>לפי מיקום</span>
                         </Radio.Button>
                         <Radio.Button value={"name"} style={{flex: "1 1 50px", textAlign: "center"}}>
                             <span style={{whiteSpace: "nowrap"}}>לפי שם מלא</span>
                         </Radio.Button>
                         <Radio.Button value={"severity"} style={{flex: "1 1 35px", textAlign: "center"}}>
                             <span style={{whiteSpace: "nowrap"}}>לפי דחיפות</span>
                         </Radio.Button>
                         <Radio.Button value={"status"} style={{flex: "1 1 35px", textAlign: "center"}}>
                             <span style={{whiteSpace: "nowrap"}}>לפי סטטוס</span>
                         </Radio.Button>
                     </Radio.Group>
                 } title={"מיון תצוגת אגף"}>
            <Button type={"primary"} style={{position: "absolute", top: 121, left: 0, width: 40, zIndex: 1000}}
                    icon={<SortAscendingOutlined/>}/>
        </Popover>
        <Drawer title={title} placement={"left"} visible={matched(['info'])}
                onClose={() => navigate('#')} className={className} size={500}>
            {mci ? <MCIForm setHeader={setHeader} onError={onInfoError}/> :
                <PatientInfo setHeader={setHeader} onError={onInfoError}/>}
        </Drawer>
        <Drawer title={'מקרא'} placement={"left"} visible={hash === '#help'} onClose={() => navigate('#')}>
            <Legend userSettings={userSettings}/>
        </Drawer>
        <Drawer title={'עדכונים'} placement={"left"} visible={matched(['notifications'])} onClose={() => navigate('#')}>
            <WingNotifications/>
        </Drawer>
    </>
};



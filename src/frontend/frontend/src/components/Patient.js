import React, {useContext, useRef} from "react";
import {Badge, Card, Carousel, Spin, Tooltip, Button} from "antd";
import {FlagFilled, UserOutlined} from '@ant-design/icons';
import {useLocation, useNavigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react'

import {hashMatchContext} from "./HashMatch";
import {patientDataContext} from "./PatientBase";
import {PatientHeader} from "./PatientHeader";
import {PatientMeasures} from "./PatientMeasures";
import {PatientArrival, PatientStatus} from "./PatientStatus";
import {PatientFooter} from "./PatientFooter";
import {PatientAwaiting} from "./PatientAwaiting";
import {PatientWatching} from "./PatientWatching";
import {PatientWarning} from "./PatientWarning";

import "./Patient.css"
import {PatientContent} from "./PatientContent";
import {MCIFormItem} from "./MCI/MCIFormSection";

export const MIN_WIDTH = 280, MAX_WIDTH = 500;

const MCIPatientBody = () => {
    const {value} = useContext(patientDataContext.context);
    return <div style={{flex: 1, padding: '8px 12px'}}>
        <MCIFormItem option={{key: 'ct', name: 'ct', type: 'checkbox'}}/>
        <MCIFormItem option={{key: 'blood_type', name: 'דם לסוג והצלבה', type: 'checkbox'}}/>
        <div>יעד:&nbsp;{value.treatment.destination || '-'}</div>
        <div>הערות:&nbsp;{value.comment}</div>
    </div>
}
const DESTINATIONS = {
    intake: [
        {key: 'intake_red', name: 'אדום'},
        {key: 'intake_yellow', name: 'צהוב'},
        {key: 'intake_yellow', name: 'ירוק'},
    ],
    intake_red: [
        {key: 'operating_room', name: 'חדר ניתוח'},
        {key: 'er_imaging', name: 'דימות מלר"ד'},
        {key: 'imaging_department', name: 'אגף דימות'},
    ],
    intake_yellow: [
        {key: 'operating_room', name: 'חדר ניתוח'},
        {key: 'er_imaging', name: 'דימות מלר"ד'},
        {key: 'imaging_department', name: 'אגף דימות'},
    ],
    intake_green: [
        {key: 'operating_room', name: 'חדר ניתוח'},
        {key: 'er_imaging', name: 'דימות מלר"ד'},
        {key: 'imaging_department', name: 'אגף דימות'},
    ]
}
const mciPatientActions = (value, update, patient) => (DESTINATIONS[value.admission.wing_id] || []).map(destination =>
    <Button type={'text'} onClick={e => {
        update(['admission'], {
            arrival: value.admission.arrival,
            department_id: value.admission.department_id,
            wing_id: destination.key,
        }, 'Admission');
        e.stopPropagation();
    }}>{destination.name}</Button>
)


const PatientBody = ({showAttention, patient}) => {
    const {value} = useContext(patientDataContext.context);
    return <div style={{
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        overflowX: 'hidden',
        backgroundColor: '#f5f5f5'
    }}>
        <PatientStatus patient={patient}
                       style={{padding: "8px 12px", gap: 20,}}/>
        <div style={{flex: 1}}>
            <Carousel autoplay swipeToSlide draggable dotPosition={"top"}>
                {showAttention && <PatientWatching/>}
                <PatientContent patient={patient}/>
                {Object.entries(value.warnings).filter(
                    ([key, {acknowledge}], i) => !acknowledge
                ).map(([key, warning], i) => <div key={i}>
                    <PatientWarning patient={patient} warning={warning} index={i} style={{
                        direction: "rtl",
                        userSelect: "none",
                        cursor: "pointer",
                        padding: "8px 12px",
                        height: 82,
                        overflowY: "overlay"
                    }}/>
                </div>)}
            </Carousel>
        </div>
        <PatientFooter/>
    </div>
}

const PatientInner = ({patient, avatar, style, showAttention, mci}) => {
    const ref = useRef(null);
    const {hash} = useLocation();
    const navigate = useNavigate();
    const {value, update, loading} = useContext(patientDataContext.context);
    const {matched, matching} = useContext(hashMatchContext);
    const {trackEvent} = useMatomo();

    let text = Object.keys(value.warnings).length || <Tooltip overlay={'סימון דגל'}>
        {<FlagFilled onClick={e => {
            update(['flagged'], !value.flagged);
            trackEvent({category: 'patient-flagged', action: 'click-event'});
            e.stopPropagation();
        }}/>}
    </Tooltip>
    if (hash.split('#').length > 2 && hash.split('#')[2] === patient && ref.current)
        ref.current.scrollIntoViewIfNeeded(true);

    let content = <Card ref={ref} type={"inner"} size={"small"} style={{
        margin: 0,
        borderStyle: patient ? "solid" : "dotted",
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflowX: 'hidden'
    }} bodyStyle={{
        padding: 0, flex: 1
    }} headStyle={{
        paddingRight: -4, paddingLeft: -4,
        animation: matched(['notifications', patient]) ?
            `highlight-${matching([null, patient])[0]} 2s ease-out` : undefined
    }} title={<PatientHeader patient={patient} avatar={avatar}/>} hoverable onClick={() => {
        navigate(`#info#${patient}#basic`);
        trackEvent({category: 'patient', action: 'click-event'});
    }} className={`severity-border severity-${value.severity ? value.severity.value : 0}`} actions={mci ?
        mciPatientActions(value, update, patient) : null
    } extra={mci ? <PatientArrival/> : <PatientAwaiting/>}>
        <div style={{display: 'flex', flexDirection: 'row', height: '100%'}}>
            <PatientMeasures patient={patient}/>
            {mci ? <MCIPatientBody/> : <PatientBody showAttention={showAttention} patient={patient}/>}
        </div>
    </Card>
    return loading ? <Spin/> : <div className={`status-bar status-${value.status || 'unassigned'}`} style={{
        maxWidth: MAX_WIDTH, minWidth: MIN_WIDTH, display: 'flex', flexDirection: "column", ...style
    }}>
        {mci ? content : <Badge.Ribbon text={text}
                                       color={Object.keys(value.warnings).length ? "red" : value.flagged ? "blue" : "grey"}>
            {content}
        </Badge.Ribbon>}
    </div>
}
export const Patient = ({patient, loading, avatar, style, onError, showAttention, mci}) => {
    const placeholder = (content) => <Card type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
        paddingRight: -4, paddingLeft: -4
    }} title={<PatientHeader avatar={avatar || <UserOutlined/>}/>} style={{
        margin: 0,
        height: '100%',
        maxWidth: MAX_WIDTH,
        minWidth: MIN_WIDTH,
        borderStyle: patient ? "solid" : "dotted",
        borderColor: "#d9d9d9", ...style
    }}>
        <div style={style}>
            <div style={{
                userSelect: "none",
                padding: 20,
                textAlign: "center", ...style
            }} className={'severity-0 severity-background'}>
                {content}
            </div>
        </div>
    </Card>
    return patient ? <patientDataContext.Provider url={`/api/patients/${patient}`} defaultValue={{
        warnings: [], awaiting: [], severity: {value: 0, at: null}, flagged: null,
        id_: null, name: null, age: null, gender: null, birthdate: null, arrival: null,
        protocol: {title: null, attributes: {}}, treatment: {destination: null}, complaint: null,
        admission: {bed: null}, measures: {}
    }} onError={onError}>
        {data => data.loading || loading ? placeholder(<Spin size={"small"}/>) :
            <PatientInner patient={patient} avatar={avatar} style={style} showAttention={showAttention} mci={mci}/>}
    </patientDataContext.Provider> : placeholder(<>
        <div>מיטה</div>
        <div>פנוייה</div>
    </>)
};

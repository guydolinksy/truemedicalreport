import React, {useContext, useRef} from "react";
import {Badge, Button, Card, Carousel, Space, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faHeart, faHeartPulse, faPercent, faTemperatureHalf, faWarning,} from "@fortawesome/free-solid-svg-icons";
import {FlagFilled, UserOutlined} from '@ant-design/icons';
import {createContext} from "./DataContext";
import {useLocation, useNavigate} from "react-router";
import {HashMatch} from "./HashMatch";

import Moment from "react-moment";
import {value} from "lodash/seq";
import {CustomIcon} from "./CustomIcon";
import moment from "moment";

export const patientDataContext = createContext({
    data: {},
    update: () => null,
    loading: true,
});


const Measure = ({patient, measure, value, icon, title}) => {
    const navigate = useNavigate();
    return <div onClick={patient && value ? e => {
        navigate(`#info#${patient}#measures#${measure}`);
        e.stopPropagation();
    } : null}>
        <div style={{fontSize: 12}}>{title}&nbsp;<FontAwesomeIcon icon={icon}/></div>
        <div style={{userSelect: "none", fontSize: 14, color: value && !value.is_valid ? 'red' : undefined}}>
            {value ? value.value : '-'}
        </div>
    </div>
};


export const severityBorderColor = {
    1: "#d32029",
    2: "#d87a16",
    3: "#d8bd14",
    4: "#8bbb11",
    5: "#49aa19",
    [undefined]: "#d9d9d9",
}
export const severityColor = {
    1: "#431418",
    2: "#441d12",
    3: "#443b11",
    4: "#2e3c10",
    5: "#1d3712",
    [undefined]: "#1a1a1a",
}
const PatientAge = ({patient}) => {
    const {value, loading} = useContext(patientDataContext.context);
    const genderedAge = {
        male: 'בן',
        female: 'בת',
    }
    return !patient || loading ? null : <span>
        ,&nbsp;{genderedAge[value.gender]}&nbsp;
        <Tooltip overlay={<Moment date={value.birthdate} format={"DD/MM/YYYY"}/>}>
            {value.age}
        </Tooltip>
    </span>
}
export const PatientComplaint = ({patient, style}) => {
    const navigate = useNavigate();
    const {value, loading} = useContext(patientDataContext.context);
    const innerStyle = {
        userSelect: "none",
        padding: 20,
        backgroundColor: severityColor[value.severity.value],
        cursor: "pointer",
        textAlign: "center",
        ...style
    };

    return loading ? <Spin/> : <div
        style={innerStyle}
        onClick={e => {
            navigate(`#info#${patient}#basic#complaint`);
            e.stopPropagation();
        }}>
        <Tooltip overlay={'תלונה עיקרית'}>{value.complaint}</Tooltip>
        &nbsp;-&nbsp;
        <Tooltip overlay={'זמן מקבלה'}>
            <Moment durationFromNow format={'h:mm'} date={value.arrival}/>
        </Tooltip>
    </div>
}
export const PatientWarning = ({patient, warning, index, style}) => {
    const navigate = useNavigate();
    return <div
        style={{
            userSelect: "none",
            padding: 20,
            backgroundColor: severityColor[warning.severity.value],
            cursor: patient ? "pointer" : undefined,
            textAlign: "center",
            ...style
        }}
        onClick={patient ? e => {
            navigate(`#info#${patient}#basic#warning-${index}`);
            e.stopPropagation();
        } : null}>
        <FontAwesomeIcon icon={faWarning}/>&nbsp;{warning.content}
    </div>
}

const patientMeasures = (patient, measures) => {
    return [
        <Measure key={'temperature'} patient={patient} measure={'temperature'} icon={faTemperatureHalf}
                 value={measures && measures.temperature} title={'חום'}/>,
        <Measure key={'blood_pressure'} patient={patient} measure={'blood_pressure'} icon={faHeart}
                 value={measures && measures.blood_pressure} title={'לחץ דם'}/>,
        <Measure key={'pulse'} patient={patient} measure={'pulse'} icon={faHeartPulse}
                 value={measures && measures.pulse} title={'דופק'}/>,
        <Measure key={'saturation'} patient={patient} measure={'saturation'} icon={faPercent}
                 value={measures && measures.saturation} title={'סטורציה'}/>,
    ];
}

const PatientAwaiting = () => {
    const AWAITING = ['doctor', 'nurse', 'laboratory', 'imaging', 'consult']
    const {loading, value} = useContext(patientDataContext.context);

    if (loading)
        return <Spin/>
    return <Space>{AWAITING.filter(k => value.awaiting[k]).map((k, i) => {
        let status, awaitings = value.awaiting[k];
        if (Object.values(awaitings).some(({since, limit, completed}) =>
            !completed && moment().subtract(limit, "seconds").isAfter(since)))
            status = 'error'
        else if (!Object.values(awaitings).some(({completed}) => !completed))
            status = 'success'
        else
            status = 'processing'

        let completed = Object.values(awaitings).filter(({completed}) => completed),
            pending = Object.values(awaitings).filter(({completed}) => !completed);
        return <Tooltip key={i} overlay={<div>
            {pending.length > 0 && <b>ממתין.ה עבור (דקות):</b>}
            {pending.sort((a, b) => a.since > b.since ? 1 : -1).map(({awaiting, since}, i) =>
                <div key={i}>{awaiting} - <Moment durationFromNow format={'h:mm'} date={since}/></div>
            )}
            {pending.length > 0 && completed.length > 0 && <span><br/></span>}
            {completed.length > 0 && <b>הושלמו:</b>}
            {completed.sort((a, b) => a.since > b.since ? 1 : -1).map(({awaiting, since}, i) =>
                <div key={i}>{awaiting}</div>
            )}
        </div>}>
            <span><CustomIcon status={status} icon={k}/></span>
        </Tooltip>
    })}</Space>
}

const PatientHeader = ({patient, avatar}) => {
    const {value} = useContext(patientDataContext.context);
    if (!patient)
        return <Button shape={"circle"} type={"text"}>{avatar || <UserOutlined/>}</Button>
    return <span>
        {avatar || value.admission.bed || <UserOutlined/>}&nbsp;<Tooltip overlay={`ת.ז. ${value.id_ || 'לא ידוע'}`}>
            {value.name}
        </Tooltip><PatientAge patient={patient}/>
    </span>
}
const PatientInner = ({patient, avatar, style}) => {
    const ref = useRef(null);
    const {hash} = useLocation();
    const navigate = useNavigate();
    const {value, update, loading} = useContext(patientDataContext.context);

    let text = value.warnings.length || <Tooltip overlay={'סימון דגל'}>
        {<FlagFilled onClick={e => {
            update(['flagged'], !value.flagged);
            e.stopPropagation();
        }}/>}
    </Tooltip>
    if (hash.split('#').length > 2 && hash.split('#')[2] === patient && ref.current)
        ref.current.scrollIntoViewIfNeeded(true);
    return loading ? <Spin/> : <HashMatch match={['highlight', patient]}>{({matched, match}) =>
        <Card ref={ref} type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
            paddingRight: -4, paddingLeft: -4, animation: matched ? `highlight-${match[0]} 1s ease-out` : undefined
        }} title={<PatientHeader patient={patient} avatar={avatar}/>} style={{
            margin: 0, maxWidth: 400, minWidth: 300, borderStyle: patient ? "solid" : "dotted",
            borderColor: severityBorderColor[value.severity.value], ...style
        }} hoverable onClick={() => navigate(`#info#${patient}#basic`)}
              extra={<PatientAwaiting/>} actions={patientMeasures(patient, value.measures)}>
            <div style={style}>
                <Badge.Ribbon text={text}
                              color={value.warnings.length ? "red" : value.flagged ? "blue" : "grey"}>
                    <Carousel autoplay swipeToSlide draggable dotPosition={"top"}>
                        <div><PatientComplaint patient={patient} style={{direction: "rtl"}}/></div>
                        {value.warnings.map((warning, i) => <div key={i}>
                            <PatientWarning patient={patient} warning={warning} index={i} style={{direction: "rtl"}}/>
                        </div>)}
                    </Carousel>
                </Badge.Ribbon>
            </div>
        </Card>
    }</HashMatch>
}
export const Patient = ({patient, loading, avatar, style, onError}) => {
    const placeholder = (content) => <Card type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
        paddingRight: -4, paddingLeft: -4
    }} title={<PatientHeader avatar={avatar || <UserOutlined/>}/>} style={{
        margin: 0,
        maxWidth: 400,
        minWidth: 300,
        borderStyle: patient ? "solid" : "dotted",
        borderColor: "#d9d9d9", ...style
    }} actions={patientMeasures()}>
        <div style={style}>
            <div style={{
                userSelect: "none",
                padding: 20,
                backgroundColor: '#1a1a1a',
                textAlign: "center", ...style
            }}>
                {content}
            </div>
        </div>
    </Card>
    return patient ? <patientDataContext.Provider url={`/api/patients/${patient}`} defaultValue={{
        warnings: [], awaiting: [], severity: {value: 0, at: null}, flagged: null,
        id_: null, name: null, age: null, gender: null, birthdate: null, arrival: null,
        complaint: null, admission: {bed: null}, measures: {}
    }} onError={onError}>
        {data => data.loading || loading ? placeholder(<Spin size={"small"}/>) :
            <PatientInner patient={patient} avatar={avatar} style={style}/>}
    </patientDataContext.Provider> : placeholder('מיטה ריקה')
};
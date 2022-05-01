import React, {useCallback, useContext, useEffect, useRef, useState} from "react";
import {Badge, Button, Card, Carousel, Input, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faClock,
    faHeart,
    faHeartPulse,
    faPercent,
    faTemperatureHalf,
    faWarning,
} from "@fortawesome/free-solid-svg-icons";
import {CheckOutlined, FlagFilled, UserOutlined} from '@ant-design/icons';
import {createContext} from "./DataContext";
import {useLocation, useNavigate} from "react-router";
import {HashMatch} from "./HashMatch";
import debounce from 'lodash/debounce';

import Moment from "react-moment";

export const patientDataContext = createContext({
    getData: (_, defaultValue) => defaultValue,
    updateData: () => null
});

const PatientData = ({path, title, icon, size, editable, style, danger}) => {
    const {loadingData, getData, updateData} = useContext(patientDataContext.context);
    const [editing, setEditing] = useState(false)

    const [value, setValue] = useState(getData(path))
    useEffect(() => {
        setValue(getData(path));
        setEditing(false)
    }, [path, getData])

    const onSave = useCallback(() => {
        updateData(path, value);
        setEditing(false)
    }, [path, value, updateData])

    const content = <span
        style={{userSelect: "none", color: danger ? 'red' : undefined, overflowX: "hidden", width: "100%"}}>
            <FontAwesomeIcon icon={icon}/>&nbsp;{value}
        </span>;
    return loadingData ? <Spin/> : <Tooltip overlay={title}>
        {!editable ? <div style={{padding: 0, maxWidth: 150}}>{content}</div> :
            !editing ?
                <Button style={{paddingRight: 8, paddingLeft: 8, maxWidth: 150}} type={"text"} danger={danger}
                        onClick={e => {
                            setEditing(true);
                            e.stopPropagation();
                        }}>{content}</Button> :
                <Input.Group style={{paddingRight: 8, paddingLeft: 8, width: 150, display: "flex"}} compact>
                    <Input size={size} onClick={e => e.stopPropagation()} defaultValue={value}
                           onChange={debounce(e => setValue(e.target.value), 300)} onPressEnter={onSave}
                           onBlur={onSave} style={{flex: 1}}/>
                    <Button type={"primary"} size={size} onClick={e => {
                        onSave();
                        e.stopPropagation();
                    }} icon={<CheckOutlined/>}/>
                </Input.Group>}
    </Tooltip>
}

const Measure = ({patient, measure, path, icon, title}) => {
    const navigate = useNavigate();
    const {getData} = useContext(patientDataContext.context);
    return <div onClick={patient ? e => {
        navigate(`#info#${patient}#measures#${measure}`);
        e.stopPropagation();
    } : null}>
        <div style={{fontSize: 12}}>{title}&nbsp;<FontAwesomeIcon icon={icon}/></div>
        <div style={{
            userSelect: "none",
            fontSize: 14,
            color: !getData(path.concat('is_valid'), true) ? 'red' : undefined
        }}>
            {getData(path.concat('value'), '-')}
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
    const {getData, loadingData} = useContext(patientDataContext.context);
    const genderedAge = {
        male: 'בן',
        female: 'בת',
    }
    return !patient || loadingData ? null : <span>
        ,&nbsp;{genderedAge[getData(['gender'])]}&nbsp;
        <Tooltip overlay={<Moment date={getData(['birthdate'])} format={"DD/MM/YYYY"}/>}>
            {getData(['age'])}
        </Tooltip>
    </span>
}
export const PatientComplaint = ({patient, style}) => {
    const navigate = useNavigate();
    const {getData} = useContext(patientDataContext.context);
    const innerStyle = {
            userSelect: "none",
            padding: 20,
            backgroundColor: severityColor[getData(['severity', 'value'])],
            cursor: patient ? "pointer" : undefined,
            textAlign: "center",
            ...style
        }
    return patient ? <div
        style={innerStyle}
        onClick={e => {
            navigate(`#info#${patient}#basic#complaint`);
            e.stopPropagation();
        }}>
        <Tooltip overlay={'תלונה עיקרית'}>{getData(['complaint'])}</Tooltip>
        &nbsp;-&nbsp;
        <Tooltip overlay={'זמן מקבלה'}>
            <Moment durationFromNow format={'h:mm'}
                    date={getData(['arrival'])}/>
        </Tooltip>
    </div> : <div style={innerStyle}>מיטה ריקה</div>
}
export const PatientWarning = ({patient, warning, index, style}) => {
    const navigate = useNavigate();
    return <div
        style={{
            userSelect: "none",
            padding: 20,
            backgroundColor: severityColor[warning.severity],
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

const patientMeasures = (patient) => [
    {id: 'temperature', path: ['measures', 'temperature',], icon: faTemperatureHalf, title: 'חום'},
    {id: 'blood_pressure', path: ['measures', 'blood_pressure'], icon: faHeart, title: 'לחץ דם'},
    {id: 'pulse', path: ['measures', 'pulse'], icon: faHeartPulse, title: 'דופק'},
    {id: 'saturation', path: ['measures', 'saturation'], icon: faPercent, title: 'סטורציה'},
].map(({id, path, icon, title}, i) =>
    <Measure key={i} patient={patient} measure={id} icon={icon} path={path} title={title}/>)

const PatientAwaiting = ({patient}) => {
    return patient ?
        <PatientData editable size={"small"} icon={faClock} title={'ממתין.ה עבור'} path={["awaiting"]}/> : null
}

const PatientHeader = ({patient, avatar}) => {
    const {getData} = useContext(patientDataContext.context);
    if (!patient)
        return <Button shape={"circle"} type={"text"}>{avatar}</Button>
    return <span>
        {avatar}&nbsp;<Tooltip overlay={`ת.ז. ${getData(['id_'], 'לא ידוע')}`}>
            {getData(['name'])}
        </Tooltip><PatientAge patient={patient}/>
    </span>
}
const PatientInner = ({patient, avatar, style}) => {
    const ref = useRef(null);
    const {hash} = useLocation();
    const navigate = useNavigate();
    const {getData, updateData} = useContext(patientDataContext.context);

    const warnings = getData(['warnings'], []), severity = getData(['severity', 'value']);

    let content = <Carousel autoplay swipeToSlide draggable dotPosition={"top"}>
        <div><PatientComplaint patient={patient} style={{direction: "rtl"}}/></div>
        {warnings.map((warning, i) => <div key={i}>
            <PatientWarning patient={patient} warning={warning} index={i} style={{direction: "rtl"}}/>
        </div>)}</Carousel>
    if (patient)
        content = <Badge.Ribbon text={warnings.length || <Tooltip overlay={'סימון דגל'}>{<FlagFilled onClick={e => {
            updateData(['flagged'], !getData(['flagged'], false));
            e.stopPropagation();
        }}/>}</Tooltip>} color={warnings.length ? "red" : getData(['flagged'], false) ? "blue" : "grey"}>
            {content}
        </Badge.Ribbon>
    if (hash.split('#').length > 2 && hash.split('#')[2] === patient && ref.current)
        ref.current.scrollIntoViewIfNeeded(true);
    return <HashMatch match={['highlight', patient]}>{({matched, match}) =>
        <Card ref={ref} type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
            paddingRight: -4, paddingLeft: -4, animation: matched ? `highlight-${match[0]} 1s ease-out` : undefined
        }} title={<PatientHeader patient={patient} avatar={avatar || <UserOutlined/>}/>} style={{
            margin: 0, maxWidth: 400, minWidth: 300, borderStyle: patient? "solid": "dotted",
            borderColor: severityBorderColor[severity], ...style
        }} hoverable={patient} onClick={patient ? () => navigate(`#info#${patient}#basic`) : null}
              extra={<PatientAwaiting patient={patient}/>} actions={patientMeasures(patient)}>
            <div style={style}>{content}</div>
        </Card>
    }</HashMatch>
}
export const Patient = ({patient, avatar, style, onError}) => {
    return patient ? <patientDataContext.Provider url={`/api/patients/${patient}`} defaultValue={{}} onError={onError}>
        {({loadingData}) => loadingData ? <Spin/> : <PatientInner patient={patient} avatar={avatar} style={style}/>}
    </patientDataContext.Provider> : <PatientInner avatar={avatar} style={style}/>
};

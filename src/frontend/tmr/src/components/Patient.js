import React, {useCallback, useEffect, useRef, useState} from "react";
import {Badge, Button, Card, Carousel, Col, Input, Row, Skeleton, Spin, Statistic, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faBed,
    faClock,
    faHeart,
    faHeartPulse, faPercent,
    faTemperatureHalf,
    faUserNurse,
    faWarning,
} from "@fortawesome/free-solid-svg-icons";
import {AlertOutlined, CheckOutlined, FlagFilled, UserOutlined} from '@ant-design/icons';
import {createContext} from "./DataContext";
import {useLocation, useNavigate, useParams} from "react-router";
import {HashMatch} from "./HashMatch";
import debounce from 'lodash/debounce';

import Moment from "react-moment";

const patientDataContext = createContext(null);
const PatientData = patientDataContext.withData(
    ({path, title, icon, size, editable, danger, loadingData, getData, updateData}) => {
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

        const content = <span style={{userSelect: "none", color: danger ? 'red' : undefined}}>
            <FontAwesomeIcon icon={icon}/>&nbsp;{value}
        </span>;
        return loadingData ? <Spin/> : <Tooltip overlay={title}>
            {!editable ? content :
                !editing ? <Button style={{padding: 0}} type={"text"} danger={danger} onClick={e => {
                        setEditing(true);
                        e.stopPropagation();
                    }}>{content}</Button> :
                    <Input.Group compact>
                        <Input size={size} style={{width: 150}} onClick={e => e.stopPropagation()} defaultValue={value}
                               onChange={debounce(e => setValue(e.target.value), 300)} onPressEnter={onSave}
                               onBlur={onSave}/>
                        <Button type={"primary"} size={size} onClick={e => {
                            onSave();
                            e.stopPropagation();
                        }} icon={<CheckOutlined/>}/>
                    </Input.Group>}
        </Tooltip>
    }
);

const Measure = patientDataContext.withData(
    ({id, path, icon, title, loadingData, getData}) => {
        const navigate = useNavigate();
        const oid = getData(['oid']);
        return <div onClick={e => {
            navigate(`#info#${oid}#measures#${id}`);
            e.stopPropagation();
        }}>
            <div style={{fontSize: 12}}>{title}&nbsp;<FontAwesomeIcon icon={icon}/></div>
            <div style={{
                userSelect: "none",
                fontSize: 14,
                color: !getData(path.concat('is_valid')) ? 'red' : undefined
            }}>
                {loadingData ? <Skeleton/> : getData(path.concat('value'))}
            </div>
        </div>
    }
);

const dataItems = [
    {id: 'temperature', path: ['measures', 'temperature',], icon: faTemperatureHalf, title: 'חום'},
    {id: 'blood_pressure', path: ['measures', 'blood_pressure'], icon: faHeart, title: 'לחץ דם'},
    {id: 'pulse', path: ['measures', 'pulse'], icon: faHeartPulse, title: 'דופק'},
    {id: 'saturation', path: ['measures', 'saturation'], icon: faPercent, title: 'סטורציה'},
]

const {Meta} = Card;
const severityBorderColor = {
    1: "#d32029",
    2: "#d87a16",
    3: "#d8bd14",
    4: "#8bbb11",
    5: "#49aa19",
    [undefined]: "#d9d9d9",
}
export const severityColor = {
    1: "#58181c",
    2: "#593815",
    3: "#595014",
    4: "#3e4f13",
    5: "#274916",
    [undefined]: "#1a1a1a",
}
const genderedAge = {
    male: 'בן',
    female: 'בת',
}
export const Patient = ({bed, id, style}) => {
    const ref = useRef(null);
    const {hash} = useLocation();
    const navigate = useNavigate();
    const uri = bed ? `/api/patients/bed/${bed}` : `/api/patients/id/${id}`
    return <patientDataContext.Provider url={uri} updateURL={uri} socketURL={uri} defaultValue={{}}>
        {({loadingData, getData, updateData}) => {
            const oid = getData(['oid']);
            if (!oid)
                return <div style={{maxWidth: 400, minWidth: 300, ...style}}/>

            const flagged = getData(['flagged']), warnings = getData(['warnings'], []),
                severity = getData(['severity', 'value']);
            const avatar = <Tooltip overlay={'סימון דגל'}>
                <Button disabled={loadingData} shape={"circle"} type={"text"} onClick={e => {
                    updateData(['flagged'], !flagged);
                    e.stopPropagation();
                }}>{bed || <UserOutlined/>}</Button>
            </Tooltip>
            const name = <Tooltip overlay={`ת.ז. ${getData(['id'], 'לא ידוע')}`}>
                {getData(['name'])}
            </Tooltip>
            const age = <Tooltip overlay={<Moment date={getData(['birthdate'])} format={"DD/MM/YYYY"}/>}>
                {getData(['age'])}
            </Tooltip>
            const title = <span>{avatar}&nbsp;{name},&nbsp;{genderedAge[getData(['gender'], 'male')]}&nbsp;{age}</span>
            const actions = dataItems.map(({id, path, icon, title}) =>
                <Measure id={id} icon={icon} path={path} title={title}/>
            );
            const extra = <PatientData editable size={"small"} icon={faClock} title={'ממתין.ה עבור'}
                                       path={["awaiting"]}/>
            const carousel = <Carousel autoplay swipeToSlide draggable dotPosition={"top"}>
                <div>
                    <div style={{
                        userSelect: "none",
                        padding: 20,
                        backgroundColor: severityColor[severity],
                        textAlign: "center",
                    }}
                         onClick={e => {
                             navigate(`#info#${oid}#basic#complaint`);
                             e.stopPropagation();
                         }}>
                        <Tooltip overlay={'תלונה עיקרית'}>
                            {getData(['complaint'])}
                        </Tooltip>
                        &nbsp;-&nbsp;
                        <Tooltip overlay={'זמן מקבלה'}>
                            <Moment durationFromNow format={'h:mm'}
                                    date={getData(['arrival'], '2022-04-12T09:00:00Z')}/>
                        </Tooltip>
                    </div>
                </div>
                {warnings.map((warning, i) =>
                    <div key={i}>
                        <div
                            style={{
                                userSelect: "none",
                                padding: 20,
                                backgroundColor: severityColor[warning.severity],
                                textAlign: "center",
                                cursor: "pointer"
                            }}
                            onClick={e => {
                                navigate(`#info#${oid}#basic#warning-${i}`);
                                e.stopPropagation();
                            }}>
                            {warning.content}&nbsp;<FontAwesomeIcon icon={faWarning}/>
                        </div>
                    </div>)}
            </Carousel>
            let content = carousel;
            if (warnings.length)
                content = <div style={style}>
                    <Badge.Ribbon text={warnings.length} color={"red"}>{carousel}</Badge.Ribbon>
                </div>
            else if (flagged)
                content = <div style={style}><Badge.Ribbon text={<FlagFilled/>}>{carousel}</Badge.Ribbon></div>

            if (hash.split('#').length > 2 && hash.split('#')[2] === oid && ref.current)
                ref.current.scrollIntoViewIfNeeded(true);
            return <HashMatch match={['highlight', oid]}>{({matched, match}) =>
                <Card ref={ref} type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
                    marginRight: -4, animation: matched ? `highlight-${match[0]} 1s ease-out` : undefined
                }} title={title} actions={actions} extra={extra} hoverable style={{
                    margin: 0, maxWidth: 400, minWidth: 300, borderColor: severityBorderColor[severity], ...style
                }} onClick={() => navigate(`#info#${oid}#basic`)}>{content}</Card>}</HashMatch>
        }}
    </patientDataContext.Provider>
};

import React, {useContext, useEffect, useRef, useState} from "react";
import {Badge, Button, Card, Carousel, Empty, List, notification, Popover, Space, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheckCircle, faWarning,} from "@fortawesome/free-solid-svg-icons";
import {ArrowLeftOutlined, FlagFilled, UserOutlined} from '@ant-design/icons';
import {createContext} from "../hooks/DataContext";
import {useLocation, useNavigate} from "react-router";
import {useMatomo} from '@datapunt/matomo-tracker-react'

import Moment from "react-moment";
import {CustomIcon} from "./CustomIcon";
import moment from "moment";
import {useTime} from 'react-timer-hook';
import {hashMatchContext} from "./HashMatch";
import {RelativeTime} from "./RelativeTime"
import {Notification} from "./Notification";
import {loginContext} from "./LoginContext";
import "./Patient.css"
import {Watchable} from "./Watchable";

const {Item} = List;
export const patientDataContext = createContext({
    data: {},
    update: () => null,
    loading: true,
});

export const MIN_WIDTH = 250, MAX_WIDTH = 500;
export const GENDERED_COLOR = {
    male: '#096dd9',
    female: '#eb2f96',
}

const Measure = ({patient, measure, icon, title}) => {
    const navigate = useNavigate();
    const {trackEvent} = useMatomo()
    const {value} = useContext(patientDataContext.context);
    const data = value && value.measures ? value.measures[measure] : null;

    return <Popover style={{width: 100}} title={<>
        <div><CustomIcon icon={icon}/>&nbsp;{title}</div>
    </>} content={<div style={{textAlign: "center"}}>
        <div>
            <span className={(data && !data.is_valid) ? 'error-text' : undefined}
                  style={{userSelect: "none", fontSize: 14}}>
                <b>{(data && data.value) ? data.value : '-'}</b>
            </span>&nbsp;{(data && data.effect.kind) &&
            <CustomIcon status={data.is_valid ? 'processing' : 'error'} icon={data.effect.kind}/>}
        </div>
        <div>
            {(data && data.value) && <RelativeTime style={{fontSize: 12}} date={data.at}/>}
            {(data && data.value && data.effect.kind) && '|'}
            {(data && data.effect.kind) && <RelativeTime style={{fontSize: 12}} date={data.effect.at}/>}
            {(!data || (!data.value && !data.effect.kind)) && '-'}
        </div>
    </div>}>
        <span className={'measurement'} style={{userSelect: "none", whiteSpace: "nowrap"}} onClick={data ? e => {
            navigate(`#info#${patient}#measures#${measure}`);
            trackEvent({category: 'patient-' + measure, action: 'click-event'});
            e.stopPropagation();
        } : null}>
            <CustomIcon style={{fontSize: 12}} icon={icon}/>&nbsp;
            <span className={(data && !data.is_valid) ? 'error-text' : undefined}>
                <Watchable watchKey={`measure#${measure}`} updateAt={data ? data.at : null}>
                    {(data && data.value) ? data.value : '?'}
                </Watchable>
            </span>{(data && data.effect.kind) && <span>
                &nbsp;<CustomIcon style={{fontSize: 12}} status={data.is_valid ? 'processing' : 'error'}
                                  icon={data.effect.kind}/>
            </span>}
        </span>
    </Popover>
};


const PatientAge = ({patient}) => {
    const {value, loading} = useContext(patientDataContext.context);
    const genderedAge = {
        male: 'בן',
        female: 'בת',
    }
    return !patient || loading ? null : <span>
        {genderedAge[value.info.gender]}&nbsp;
        <Tooltip overlay={
            value.info.birthdate ? <Moment date={value.info.birthdate} format={"DD/MM/YYYY"}/> : "לא ידוע"
        }>
            {value.info.age || "(לא ידוע)"}
        </Tooltip>
    </span>
}

export const PatientStatus = ({patient, style}) => {
    const navigate = useNavigate();
    const {value, loading} = useContext(patientDataContext.context);
    const {minutes} = useTime({});
    const [arrivalClass, setArrivalClass] = useState(undefined);
    const {trackEvent} = useMatomo()


    useEffect(() => {
        if (moment().subtract(10, "hours").isAfter(value.admission.arrival))
            setArrivalClass('error-text')
        else if (moment().subtract(4, "hours").isAfter(value.admission.arrival))
            setArrivalClass('warn-text')
    }, [value.admission.arrival, minutes]);

    return loading ? <Spin/> : <div style={{display: "flex", justifyContent: "space-between", ...style}} onClick={e => {
        navigate(`#info#${patient}#basic#complaint`);
        trackEvent({category: 'patient-complaint', action: 'click-event'});
        e.stopPropagation();
    }}>
        <div style={{whiteSpace: "nowrap", display: "flex", alignItems: "center", overflowX: "hidden"}}>
            {!!value.severity.value && <span><Tooltip overlay='דחיפות'>
                <span>(<strong>{value.severity.value}</strong>)</span>
            </Tooltip>&nbsp;</span>}
            {value.protocol && value.protocol.active &&
                <Tooltip overlay={`מצב פרוטוקול - ${value.intake.complaint}`}>
                    <FontAwesomeIcon icon={faCheckCircle} style={{marginLeft: "0.3rem", color: "#40a9ff"}}/>
                </Tooltip>}
            <Tooltip overlay={value.intake.nurse_description}>
                <span style={{overflowX: "hidden", textOverflow: "ellipsis"}}>{value.intake.complaint}</span>
            </Tooltip>&nbsp;
            <span>
                <ArrowLeftOutlined/>&nbsp;
                {value.treatment.destination || <span className={'error-text'}>(לא הוחלט)</span>}
            </span>
        </div>
        <Tooltip overlay={'זמן מקבלה'}>
            <RelativeTime className={arrivalClass} date={value.admission.arrival}/>
        </Tooltip>
    </div>
}
export const ProtocolStatus = ({patient}) => {
    const {value, loading} = useContext(patientDataContext.context);
    const {trackEvent} = useMatomo()

    return loading ? <Spin/> : <div onClick={e => {
        trackEvent({category: 'patient-protocol', action: 'click-event'});
    }}>
        {value.protocol && value.protocol.items && value.protocol.items.length ? value.protocol.items.map(item => {
            let data = value.protocol.values[item.key];
            return <div style={{
                display: "flex",
                flexFlow: "row nowrap",
                justifyContent: "space-between",
                alignItems: "baseline"
            }}>
                <div style={{display: "flex", flexFlow: "row nowrap", whiteSpace: "nowrap", overflowX: "hidden"}}>
                    <div>{item.name}:&nbsp;</div>
                    <div style={{overflowX: "hidden", textOverflow: "ellipsis"}}>
                        {data !== undefined && data.value !== undefined ? data.value : item.default}
                    </div>
                </div>
                {data !== undefined && <RelativeTime style={{fontSize: 12}} date={data.at}/>}
            </div>
        }) : <Empty style={{margin: -2}} image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין מידע לפרוטוקול'}/>}
    </div>
}
export const NotificationPreview = ({patient}) => {
    const navigate = useNavigate();
    const {value, loading} = useContext(patientDataContext.context);
    const {trackEvent} = useMatomo()

    return loading ? <Spin/> : <div onClick={e => {
        navigate(`#info#${patient}#notifications`);
        trackEvent({category: 'patient-timeline', action: 'click-event'});
        e.stopPropagation();
    }}>
        {value.notifications && value.notifications.slice(0, 2).map(item =>
            <div style={{
                display: "flex",
                flexFlow: "row nowrap",
                justifyContent: "space-between",
                alignItems: "center"
            }}>
                <Notification patient={patient} message={item} className={'patient-card-clickable-content'}
                              style={{whiteSpace: "nowrap", textOverflow: "ellipsis", overflowX: "hidden"}}/>
            </div>
        )}
        {value.notifications && value.notifications.slice(2, 3).length > 0 && <div>
            <a className={'patient-card-clickable-content'} href={`#info#${patient}#notifications`}>
                ועוד {value.notifications.length - 2} עדכונים נוספים...
            </a>
        </div>}
        {(!value.notifications || !value.notifications.length) &&
            <Empty style={{margin: -2}} image={Empty.PRESENTED_IMAGE_SIMPLE}
                   description={'אין עדכונים זמינים'}/>}
    </div>
}
export const PatientWarning = ({patient, warning, index, style}) => {
    const navigate = useNavigate();
    const {trackEvent} = useMatomo()
    return <div className={`severity-background severity-${warning.severity.value || 0}`}
                style={{
                    textAlign: "center",
                    ...style
                }}
                onClick={patient ? e => {
                    navigate(`#info#${patient}#basic#warning-${index}`);
                    trackEvent({category: 'patient-alert', action: 'click-event'});
                    e.stopPropagation();
                } : null}>
        <FontAwesomeIcon icon={faWarning}/>&nbsp;{warning.content}
    </div>
}

const PatientFooter = ({patient}) => {
    const {value} = useContext(patientDataContext.context);
    const notes = value.discussion.notes || {},
        descMotes = Object.keys(notes).sort((a, b)=>
            moment(notes[a].at).isSame(notes[b].at) ? 0 : moment(notes[a].at).isAfter(notes[b].at) ? 1 : -1
        );
    const doctorNotes = Object.assign({}, ...value.treatment.doctors.map(doctor => ({
        [doctor]: descMotes.find(note => notes[note].by === doctor && !notes[note].subject) || undefined
    })));
    const subjectNotes = Object.assign({}, ...value.referrals.map(ref => ({
        [ref.to]: descMotes.find(note => notes[note].subject === ref.to) || undefined
    })));
    const unpairedNotes = descMotes.filter(note =>
        !Object.values(doctorNotes).includes(note) && Object.values(subjectNotes).includes(note)
    );
    return (
        <div style={{display: "flex", flexDirection: "column"}}>
            <div style={{display: "flex", justifyContent: "space-between", padding: "8px 12px"}}>
                <Measure patient={patient} measure={'temperature'} icon={'temperature'} title={'חום'}/>
                <Measure patient={patient} measure={'blood_pressure'} icon={'bloodPressure'} title={'לחץ דם'}/>
                <Measure patient={patient} measure={'pulse'} icon={'pulse'} title={'דופק'}/>
                <Measure patient={patient} measure={'saturation'} icon={'saturation'} title={'סטורציה'}/>
                <Measure patient={patient} measure={'pain'} icon={'pain'} title={'כאב'}/>
            </div>
            {(value.treatment.doctors.length > 0 || value.referrals.length > 0 || unpairedNotes.length > 0) &&
                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    padding: "0px 12px 8px 12px"
                }}>
                    {value.treatment.doctors.length > 0 &&
                        <div style={{
                            display: "flex",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap"
                        }}>
                            {value.treatment.doctors.map((doctor, index) =>
                                <Tooltip overlay={doctorNotes[doctor] ? <div>
                                    <div>{doctor} (<RelativeTime date={doctorNotes[doctor].at}/>):</div>
                                    <div>{subjectNotes[doctor].content}</div>
                                </div> : doctor}>
                                    <div style={{overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap"}}>
                                        {index !== 0 ? ',' : ''}{doctor}
                                    </div>
                                </Tooltip>)}
                        </div>}
                    {value.referrals.length > 0 &&
                        <div style={{
                            display: "flex",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                            whiteSpace: "nowrap"
                        }}>
                            {value.referrals.filter(ref => !ref.completed).map((ref, index) =>
                                <Tooltip overlay={subjectNotes[ref.to] ? <div>
                                    <div>{ref.to} (<RelativeTime date={subjectNotes[ref.to].at}/>):</div>
                                    <div>{subjectNotes[ref.to].content}</div>
                                </div> : ref.to}>
                                    <div style={{overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap"}}>
                                        {index !== 0 ? ',' : ''}{ref.to}
                                    </div>
                                </Tooltip>)}
                        </div>}
                    {unpairedNotes.length > 0 &&
                        <div>
                            <Tooltip overlay={<div style={{maxWidth: '50vw', maxHeight: '50vh'}}>
                                {unpairedNotes.map(note => <div>
                                    <div>{unpairedNotes[note].by} {unpairedNotes[note].subject ? `- ${unpairedNotes[note].subject}` : ''}
                                        (<RelativeTime date={unpairedNotes[note].at}/>):</div>
                                    <div>{unpairedNotes[note].content}</div>
                                </div>)}
                            </div>}>
                                <div>
                                    +
                                </div>
                            </Tooltip>
                        </div>}
                </div>}
        </div>)
}

const PatientAwaiting = () => {
    const AWAITING = [
        'laboratory',
        'imaging',
        'referral',
        'nurse',
        'doctor',
    ]
    const {loading, value} = useContext(patientDataContext.context);

    if (loading)
        return <Spin/>
    return <Space>{AWAITING.filter(k => value.awaiting[k]).map((k, i) => {
        return <PatientAwaitingIcon awaitings={value.awaiting[k]} type={k} key={k}/>
    })}</Space>
}
const PatientAwaitingIcon = ({awaitings, type}) => {
    const [status, setStatus] = useState();
    const {seconds} = useTime({});

    useEffect(() => {
        if (Object.values(awaitings).some(({since, limit, completed}) =>
            !completed && moment().subtract(limit, "seconds").isAfter(since)))
            setStatus('error')
        else if (!Object.values(awaitings).some(({completed}) => !completed))
            setStatus('success')
        else
            setStatus('processing')

    }, [awaitings, seconds])

    let completed = Object.values(awaitings).filter(({completed}) => completed),
        pending = Object.values(awaitings).filter(({completed}) => !completed);
    const AWAITING_TITLE = {
        laboratory: 'בדיקות מעבדה',
        imaging: 'בדיקות הדמיה',
        referral: 'הפניות וייעוצים',
        nurse: 'צוות סיעודי',
        doctor: 'צוות רפואי',
    }
    return <Tooltip key={type} overlay={<div>
        <div><b style={{textDecoration: "underline"}}>{AWAITING_TITLE[type]}</b></div>
        {pending.length > 0 && <div><b>ממתין.ה עבור (דקות):</b></div>}
        {pending.sort((a, b) => a.since > b.since ? 1 : -1).map(({name, status, since}, i) =>
            <div key={i}>
                {name} - {status} - <RelativeTime date={since}/>
            </div>
        )}
        {pending.length > 0 && completed.length > 0 && <div><br/></div>}
        {completed.length > 0 && <div><b>הושלמו:</b></div>}
        {completed.sort((a, b) => a.since > b.since ? 1 : -1).map(({name, status, since}, i) =>
            <div key={i}>{name} - {status}</div>
        )}
    </div>}>
        <span><CustomIcon status={status} icon={type}/></span>
    </Tooltip>
}
export const handleCopyToClipboard = (event, text) => {
    event.stopPropagation()
    try {
        navigator.clipboard.writeText(text);
        openNotification('success', 'תעודת הזהות הועתקה');
    } catch (err) {
        openNotification('error', 'קרתה תקלה בהעתקת תעודת הזהות');
    }
};

export const openNotification = (type, message) => {
    notification[type]({
        message: message,
        duration: 3, // Display duration in seconds
    });
}

const PatientHeader = ({patient, avatar}) => {
    const {value} = useContext(patientDataContext.context);
    const {user} = useContext(loginContext);
    if (!patient)
        return <Button shape={"circle"} type={"text"}>{avatar || <UserOutlined/>}</Button>
    return <span className={`gender-${value.info.gender}`}>
        {avatar || value.admission.bed || <UserOutlined/>}&nbsp;
        {!user.anonymous && <span>
            <Tooltip overlay={<div onClick={(event) => handleCopyToClipboard(event, value.info.id_)}>
                {`ת.ז. ${value.info.id_ || 'לא ידוע'}`}
            </div>}>
                {value.info.name}</Tooltip>,&nbsp;
        </span>}
        <PatientAge patient={patient}/>
    </span>
}
const PatientInner = ({patient, avatar, style}) => {
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
    return loading ? <Spin/> : <div className={`status-bar status-${value.status || 'unassigned'}`} style={{
        maxWidth: MAX_WIDTH, minWidth: MIN_WIDTH, display: 'flex', flexDirection: "column", ...style
    }}>
        <Card ref={ref} type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
            paddingRight: -4, paddingLeft: -4,
            animation: matched(['highlight', patient]) ?
                `highlight-${matching(['highlight', patient])[0]} 2s ease-out` :
                undefined
        }} title={<PatientHeader patient={patient} avatar={avatar}/>} style={{
            margin: 0, borderStyle: patient ? "solid" : "dotted", flex: 1,
        }} className={`severity-border severity-${value.severity.value || 0}`} hoverable onClick={() => {
            navigate(`#info#${patient}#basic`);
            trackEvent({category: 'patient', action: 'click-event'});
        }} extra={<PatientAwaiting/>}>
            <PatientStatus patient={patient} style={{padding: "8px 12px", gap: 20}}/>
            <div className={"patient-content"}>
                <Badge.Ribbon text={text}
                              color={Object.keys(value.warnings).length ? "red" : value.flagged ? "blue" : "grey"}>
                    {value.protocol && value.protocol.attributes && Object.keys(value.protocol.attributes).map((key) =>
                        <div>{key}:{value.protocol.attributes[key]}</div>)}
                    <Carousel autoplay swipeToSlide draggable dotPosition={"top"}>
                        <div>
                            <div className={'status-background'} style={{
                                direction: "rtl",
                                userSelect: "none",
                                padding: "8px 12px",
                                cursor: "pointer",
                                height: 82,
                                overflowY: "overlay"
                            }}>
                                {value.protocol && value.protocol.active ?
                                    <ProtocolStatus patient={patient}/> :
                                    <NotificationPreview patient={patient}/>}
                            </div>
                        </div>
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
                </Badge.Ribbon>
                <PatientFooter patient={patient}/>
            </div>
        </Card>
    </div>
}
export const Patient = ({patient, loading, avatar, style, onError}) => {
    const placeholder = (content) => <Card type={"inner"} size={"small"} bodyStyle={{padding: 0}} headStyle={{
        paddingRight: -4, paddingLeft: -4
    }} title={<PatientHeader avatar={avatar || <UserOutlined/>}/>} style={{
        margin: 0,
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
            <PatientInner patient={patient} avatar={avatar} style={style}/>}
    </patientDataContext.Provider> : placeholder(<>
        <div>מיטה</div>
        <div>פנוייה</div>
    </>)
};

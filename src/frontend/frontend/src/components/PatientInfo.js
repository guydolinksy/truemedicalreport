import {Badge, Button, Collapse, Drawer, Empty, List, Modal, Radio, Space, Spin} from "antd";
import React, {useContext, useEffect, useState} from "react";
import {useNavigate} from "react-router";
import Moment from "react-moment";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import highchartsMore from 'highcharts/highcharts-more';
import lightTheme from 'highcharts/themes/grid-light';
import darkTheme from 'highcharts/themes/dark-unica';
import {useMatomo} from '@datapunt/matomo-tracker-react';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faFileLines,
    faHeart,
    faHeartPulse,
    faPercent,
    faTemperatureHalf,
    faWindowRestore,
    faXRay
} from "@fortawesome/free-solid-svg-icons";
import {htmlModal, iframeModal} from "./modals";
import { patientDataContext, PatientStatus, PatientWarning} from "./Patient";
import {loginContext} from "./LoginContext";
import {UserTheme} from "../themes/ThemeContext";
import {hashMatchContext} from "./HashMatch";
import {Notification} from "./Notification";
import {RelativeTime} from "./RelativeTime";
import moment from "moment";

highchartsMore(Highcharts);
const themes = {'dark-theme': darkTheme, 'light-theme': lightTheme}

const {Panel} = Collapse;
const fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;";

const labStatuses = {
    1: ' - הוזמן',
    2: ' - שויכו דגימות',
    3: ' - בעבודה',
    4: ' - תוצאות',
}

const RANGE_CODE_TO_DESCRIPTION = {
    "H": "High",
    "L": "Low",
    "VH": "Very High",
    "VL": "Very Low",
    "HH": "Panic High",
    "LL": "Panic Low",
    "JESUS": "Call the nearby priest"
}

const EcgRecord = ({record}) => <div style={{display:"flex", justifyContent:"space-between"}} key={record.title}>
    <a style={{cursor:"pointer"}} href={record.link}>{record.title}</a>
    <RelativeTime style={{fontSize: 12}} date={record.date}/>
</div>

const displayLab = (lab, displayAllResults, matched, patient) => {

    const rangeToResults = {};
    Object.values(lab.results).forEach(result => {
        if (!rangeToResults.hasOwnProperty(result.range)) {
            rangeToResults[result.range] = []
        }

        rangeToResults[result.range].push(result);
    })

    const ranges = Object.keys(rangeToResults);

    let badgeColor = "#000000";
    if (ranges.some(range => ["HH", "LL"].includes(range)))
        badgeColor = "#FF0000";
    else if (ranges.some(range => ["VH", "VL"].includes(range)))
        badgeColor = "#FF00FF";
    else if (ranges.some(range => ["H", "L", "X"].includes(range)))
        badgeColor = "#FFA500";
    else if (lab.status === 4 && ranges.every(range => range === "N"))
        badgeColor = "#00FF00";

    const rangesToConsiderAsBad = ["HH", "LL", "VH", "VL"].concat(displayAllResults ? ["H", "L"] : []).map(
        status => rangeToResults[status] || []
    )

    let badgeText = '-';
    if (lab.status === 4) {
        const badResultsCount = rangesToConsiderAsBad.map(results => results.length).reduce((a, b) => a + b)
        if (badResultsCount)
            badgeText = badResultsCount.toString()
        else if (ranges.every(range => range === "N"))
            badgeText = "✓";
        else
            badgeText = "X";
    }

    return <p key={`${lab.category}-${lab.ordered_at}`} style={{
        animation: matched(['info', patient, 'labs', lab.patient_id, encodeURIComponent(lab.category), lab.ordered_at.replace(/:/g, '-').replace(/\+/g, '-')]) ? 'highlight 2s ease-out' : undefined,
        direction: "rtl"
    }}>
        <p>
            <span><Badge style={{backgroundColor: badgeColor}} count={badgeText}/>&nbsp;
                {lab.category_display_name} {labStatuses[lab.status]} {ranges.some(range => range === "X") && ' - פסול'}
                <RelativeTime style={{fontSize: 12, float: "left"}} date={lab.ordered_at}/>
            </span>
        </p>
        <p style={{marginRight: "2rem"}}>
            {rangesToConsiderAsBad.flat().map((result, i) => <p key={i}>
                <span>{RANGE_CODE_TO_DESCRIPTION[result.range]} {result.test_type_name}: {result.result} {result.units}</span>
            </p>)}
            {displayAllResults && (rangeToResults[null] || []).length > 0 && <p>
                הוזמנו: {rangeToResults[null].map(result => result.test_type_name).join(', ')}
            </p>}
        </p>
    </p>
}

const MeasureGraph = ({data, title, graphProps}) => {
    const {userSettings} = useContext(loginContext);
    (themes[userSettings.theme] || (x => x))(Highcharts);
    return <HighchartsReact highcharts={Highcharts} options={{
        title: null,
        xAxis: {type: "datetime", useHTML: true},
        yAxis: {opposite: true, title: {enabled: false}},
        chart: {height: 80, width: 200, spacingBottom: 5, style: {fontFamily: fontFamily}},
        legend: {enabled: false},
        credits: {enabled: false},
        tooltip: {outside: true},
        plotOptions: {series: {marker: {radius: 3}, lineWidth: 1}},
        series: [{data: data, name: title, ...graphProps}]
    }}/>
}
const PatientSeverity = () => {
    const {value, update} = useContext(patientDataContext.context);
    return <Radio.Group value={value.severity.value} size={"small"} buttonStyle={"solid"}
                        style={{flex: 1, display: "inline-flex", textAlign: "center"}}
                        onChange={e => update(['severity', 'value'], e.target.value)}>
        {[1, 2, 3, 4, 5].map(i => <Radio.Button key={i} value={i} style={{flex: 1}} className={
            `severity-${i} severity-` + (value.severity.value === i ? "background" : "color")
        }>{i}</Radio.Button>)}
    </Radio.Group>
}
export const PatientInfo = ({onError}) => {
    const navigate = useNavigate();

    const {matched, matching} = useContext(hashMatchContext);

    const [{title, className}, setHeader] = useState({});
    return <Drawer title={title} placement={"left"} visible={matched(['info'])} onClose={() => navigate('#')}
                   className={className} size={500}>
        <UserTheme>
            {matched(['info']) &&
                <patientDataContext.Provider url={`/api/patients/${matching(['info'])[0]}/info`} defaultValue={{
                    warnings: [], awaiting: {}, severity: {value: 0, at: null}, flagged: null,
                    id_: null, name: null, age: null, gender: null, birthdate: null, arrival: null,
                    treatment: {destination: null}, complaint: null, admission: {},
                    intake: {nurse_description: null}, measures: {
                        temperature: null,
                        blood_pressure: null,
                        saturation: null,
                        pulse: null
                    },
                    full_measures: {
                        temperature: [],
                        blood_pressure: [],
                        saturation: [],
                        pulse: []
                    }, visits: [], notifications: [], labs: [], imaging: [], referrals: []
                }} onError={onError}>
                    {() => <InternalPatientCard patient={matching(['info'])[0]} setHeader={setHeader}/>}
                </patientDataContext.Provider>}
        </UserTheme>
    </Drawer>
}

const FullMeasure = ({patient, measure, icon, latest, data, title, graphProps}) => {
    const {matched} = useContext(hashMatchContext);
    return <List.Item style={{
        padding: 5,
        display: "flex",
        animation: matched(['info', patient, 'measures', measure]) ? 'highlight 2s ease-out' : undefined
    }}>
        <div style={{textAlign: "center", flex: 1}}>
            <div style={{fontSize: 12}}><FontAwesomeIcon icon={icon}/> {title}</div>
            <div className={latest && !latest.is_valid ? 'error-text' : undefined} style={{
                userSelect: "none",
                fontSize: 14,
            }}>
                {(latest && latest.value) || '-'}
            </div>
        </div>
        <MeasureGraph data={data} title={title} graphProps={graphProps}/>
    </List.Item>
}
const InternalPatientCard = ({patient, setHeader}) => {
    const {user} = useContext(loginContext);
    const {value, loading} = useContext(patientDataContext.context);
    const {matched, matching} = useContext(hashMatchContext);
    const [displayAllResults, setDisplayAllResults] = useState(false)

    const [modal, modalContext] = Modal.useModal();

    const {trackEvent} = useMatomo()
    useEffect(() => {
        if (loading)
            setHeader({title: ''})
        else {
            let gender = {
                male: 'בן',
                female: 'בת',
            }[value.info.gender];
            setHeader({
                title: user.anonymous ? `${gender} (${value.info.age || 'גיל לא ידוע'})` :
                    `${value.info.name}, ${gender} (${value.info.age || 'גיל לא ידוע'})` +
                    (value.info.id_ ? `, ת.ז. ${value.info.id_}` : '') +
                    (value.info.phone ? `, טלפון : ${value.info.phone}` : ''),
                className: `gender-${value.info.gender}`
            });
        }
    }, [value, loading, setHeader]);
    if (loading)
        return <Spin/>
    return <Collapse defaultActiveKey={['basic'].concat(...matching(['info', patient]).slice(0, 1))}>
        <Panel key={'basic'} showArrow={false} collapsible={"disabled"} header={'מידע בסיסי'}>
            {Object.entries(value.warnings).map(([key, warning], i) =>
                <PatientWarning key={i} patient={patient} warning={warning} index={i} style={{
                    direction: "rtl",
                    userSelect: "none",
                    cursor: "pointer",
                    animation: matched(['info', patient, 'basic', `warning-${i}`]) ?
                        'highlight 2s ease-out' : undefined,
                    marginBottom: 18
                }}/>
            )}
            <PatientStatus patient={patient} style={{
                animation: matched(['info', patient, 'basic', 'complaint']) ? 'highlight 2s ease-out' : undefined,
                marginBottom: 18
            }}/>
            <div style={{display: "flex", width: '100%', marginBottom: 14}}>
                <span>דחיפות:&nbsp;</span><PatientSeverity/>

            </div>
            <p style={{
                animation: matched(['info', patient, 'basic', 'nurse-summary']) ? 'highlight 2s ease-out' : undefined
            }}>
                תיאור צוות סיעודי: {value.intake.nurse_description}
            </p>
        </Panel>
        <Panel key={'measures'} header={'מדדים'}>
            <FullMeasure key={'temperature'} patient={patient} measure={'temperature'} icon={faTemperatureHalf}
                         latest={value.measures.temperature} title={'חום'} graphProps={{type: 'line'}}
                         data={value.full_measures.temperature}/>
            <FullMeasure key={'blood_pressure'} patient={patient} measure={'blood_pressure'} icon={faHeart}
                         latest={value.measures.blood_pressure} title={'לחץ דם'} graphProps={{
                type: 'arearange', tooltip: {
                    pointFormat: '<span style="color:{series.color}">●' +
                        '</span> {series.name}: <b>{point.low}/{point.high}</b><br/>'
                }
            }} data={value.full_measures.blood_pressure}/>
            <FullMeasure key={'pulse'} patient={patient} measure={'pulse'} icon={faHeartPulse}
                         latest={value.measures.pulse} title={'דופק'} graphProps={{type: 'line'}}
                         data={value.full_measures.pulse}/>
            <FullMeasure key={'saturation'} patient={patient} measure={'saturation'} icon={faPercent}
                         latest={value.measures.saturation} title={'סטורציה'}
                         graphProps={{type: 'line'}} data={value.full_measures.saturation}/>
        </Panel>
        {value.visits.length > 0 && <Panel key={'visit'} header={'ביקורים קודמים'}>
            {value.visits.map((visit, i) => <p key={i}>{visit.title} ב<a href={'/'}><Moment
                date={visit.at}/></a>
            </p>)}
        </Panel>}
        <Panel key={'notifications'} header={'עדכונים'} style={{
            animation: matched(['info', patient, 'notifications']) ? 'highlight 2s ease-out' : undefined
        }}>
            {value.notifications.length > 0 ? value.notifications.map((notification, i) =>
                <div style={{display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                    <Notification key={i} patient={patient} message={notification} showExternalLink={true}/>
                </div>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין עדכונים זמינים'}/>}
        </Panel>
        <Panel key={'labs'} header={
            <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                <span>מעבדה</span>
                <Space align="center">
                    <Badge style={{backgroundColor: '#1890ff'}} count={value.labs.length} size={"small"}/>
                    {iframeModal(modal, faWindowRestore, "צפה.י בקמיליון", value.lab_link)}
                </Space>
            </div>
        }>
            {value.labs.length ? <>
                {value.labs.sort(
                    (a, b) => moment(a.ordered_at).isSame(b.ordered_at) ? 0 :
                        moment(a.ordered_at).isBefore(b.ordered_at) ? 1 : -1
                ).map(
                    lab => displayLab(lab, displayAllResults, matched, patient)
                )}
                <Button onClick={() => setDisplayAllResults(!displayAllResults)}>
                    <span>{displayAllResults ? "הסתר בדיקות" : "הצג בדיקות"}</span>
                </Button>
            </> : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו בדיקות מעבדה'}/>}
        </Panel>
        <Panel key={'imaging'} header={
            <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                <span>הדמיות</span>
                <div><Badge style={{backgroundColor: '#1890ff'}} count={value.imaging.length} size={"small"}/></div>
            </div>
        }>
            {value.imaging.length ? value.imaging.map((image, i) =>
                <p key={i} style={{
                    animation: matched(['info', patient, 'imaging', `${image.external_id}`]) ? 'highlight 2s ease-out' : undefined
                }}>
                    {image.title} - {image.status_text}
                    {iframeModal(modal, faXRay, "דימות", image.link)}
                    {htmlModal(modal, faFileLines, "פענוח", image.interpretation)}
                </p>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו הדמיות'}/>}
        </Panel>
        <Panel key={'referrals'} header={'ייעוץ'}>
            {value.referrals.length ? value.referrals.map((referral, i) => <p key={i}>
                {referral.to} - {referral.completed ? 'הושלם' : 'בהמתנה'} - <RelativeTime style={{fontSize: 12}}
                                                                                          date={referral.at}/>
            </p>) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא נרשמו הפניות'}/>}
        </Panel>
        <Panel key={'medicalSummary'} header={
            <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                <span>סיכום רפואי</span>
                <Space align="center">
                    {iframeModal(modal, faWindowRestore, "צפה.י בקמיליון", value.medical_summary_link)}
                </Space>
            </div>
        }>
            <p/>
        </Panel>
        <Panel key={'ECGs'} header={
            <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                <span>בדיקות א.ק.ג</span>
            </div>
        }>
            {!!value?.ecg_records?.length
                ? value.ecg_records.map((record,index) => <EcgRecord record={record} key={index} />)
                : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו בדיקות א.ק.ג'}/>
            }
        </Panel>
        {value.plugins.map(({key, title, url}) =>
            <Panel key={key} header={title}>
                <iframe style={{border: "none", width: "100%", height: "250px"}} title={title} src={url}/>
            </Panel>
        )}
        {modalContext}
    </Collapse>
}

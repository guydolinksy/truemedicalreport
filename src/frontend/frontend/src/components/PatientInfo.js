import {Badge, Collapse, Drawer, Empty, List, Radio, Spin, Timeline, Tooltip, Modal} from "antd";
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
import {faHeart, faHeartPulse, faPercent, faTemperatureHalf, faWindowRestore} from "@fortawesome/free-solid-svg-icons";
import {FlagFilled} from '@ant-design/icons';
import {patientDataContext, PatientStatus, PatientWarning} from "./Patient";
import {loginContext} from "./LoginContext";
import {UserTheme} from "../themes/ThemeContext";
import {hashMatchContext} from "./HashMatch";
import {Notification} from "./Notification";
import {RelativeTime} from "./RelativeTime";

highchartsMore(Highcharts);
const themes = {['dark-theme']: darkTheme, ['light-theme']: lightTheme}

const {Panel} = Collapse;
const fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;";
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
                title: user.anonymous ? `${gender} (${value.info.age || 'גיל לא ידוע'})`:
                    `${value.info.name}, ${gender} (${value.info.age || 'גיל לא ידוע'}), ת.ז. ${value.info.id_}:`,
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
                    <Notification key={i} patient={patient} message={notification}/>
                </div>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין עדכונים זמינים'}/>}
        </Panel>
        <Panel key={'labs'} header={
            <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                <span>מעבדה</span>
                <div><Badge style={{backgroundColor: '#1890ff'}} count={value.labs.length} size={"small"}/></div>
                {value.lab_link && <Tooltip overlay={"צפה.י בקמיליון"}>
                    <FontAwesomeIcon icon={faWindowRestore} onClick={e => {
                        modal.info({
                            icon: null,
                            width: "95%",
                            okText: "סגור",
                            centered: true,
                            bodyStyle: {
                                padding: "10px"
                            },
                            content: <iframe
                                style={{
                                    border: 0,
                                    width: "100%",
                                    height: 0.75 * window.document.documentElement.clientHeight
                                }}
                                src={value.lab_link}
                            />
                        })
                        trackEvent({category: 'external-lab', action: 'click-event'})
                        e.stopPropagation();
                    }}/>
                </Tooltip>}
            </div>
        }>
            {value.labs.length ? value.labs.map((lab, i) =>
                <p key={i} style={{
                    animation: matched(['info', patient, 'labs', `lab-${i}`]) ? 'highlight 2s ease-out' : undefined
                }}>
                    {lab.category} - {lab.status} - <RelativeTime style={{fontSize: 12}} date={lab.at}/>
                </p>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו בדיקות מעבדה'}/>}
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
                </p>
            ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו הדמיות'}/>}
        </Panel>
        <Panel key={'referrals'} header={'ייעוץ'}>
            {value.referrals.length ? value.referrals.map((referral, i) => <p key={i}>
                {referral.to} - {referral.completed ? 'בהמתנה' : 'הושלם'} - <RelativeTime style={{fontSize: 12}}
                                                                                          date={referral.at}/>
            </p>) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא נרשמו הפניות'}/>}
        </Panel>
        <Panel key={'story'} header={'סיפור מטופל'}>
            <Timeline reverse mode={"left"}>{value.events.map(event =>
                <Timeline.Item key={event.key} label={<Moment date={event.at} format={'HH:mm DD-MM-YYYY'}/>}>
                    {event.content}
                </Timeline.Item>
            )}</Timeline>
        </Panel>
        {value.plugins.map(({key, title, url}) =>
            <Panel key={key} header={title}>
                <iframe style={{border: "none", width: "100%", height: "250px"}} title={title} src={url}/>
            </Panel>
        )}
        {modalContext}
    </Collapse>
}

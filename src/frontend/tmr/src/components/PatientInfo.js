import {Badge, Collapse, Drawer, Empty, List, Radio, Spin, Timeline} from "antd";
import React, {useContext, useEffect, useState} from "react";
import {useNavigate} from "react-router";
import Moment from "react-moment";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import highchartsMore from 'highcharts/highcharts-more';
import theme from 'highcharts/themes/dark-unica';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faHeart, faHeartPulse, faPercent, faTemperatureHalf,} from "@fortawesome/free-solid-svg-icons";
import {HashMatch} from "./HashMatch";
import {PatientComplaint, patientDataContext, PatientWarning, severityBorderColor, severityColor} from "./Patient";

theme(Highcharts);
highchartsMore(Highcharts);

const {Panel} = Collapse;
const fontFamily = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;";
const MeasureGraph = ({data, title, graphProps}) => {
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
        {[1, 2, 3, 4, 5].map(i => <Radio.Button key={i} value={i} style={{
            flex: 1,
            color: value.severity.value === i ? undefined : severityBorderColor[i],
            backgroundColor: value.severity.value === i ? severityColor[i] : undefined,
        }}>{i}</Radio.Button>)}
    </Radio.Group>
}
export const PatientInfo = ({onError}) => {
    const navigate = useNavigate();

    const [title, setTitle] = useState();
    return <HashMatch match={['info']}>
        {({matched, match}) => <Drawer title={title} placement={"left"} visible={matched}
                                       onClose={() => navigate('#')}>
            {matched &&
                <patientDataContext.Provider url={`/api/patients/${match[0]}/info`} defaultValue={{
                    warnings: [], awaiting: null, severity: {value: 0, at: null}, flagged: null,
                    id_: null, name: null, age: null, gender: null, birthdate: null, arrival: null,
                    complaint: null, admission: {}, measures: {
                        temperature: null,
                        blood_pressure: null,
                        saturation: null,
                        pulse: null
                    }, secondary_complaint: null, nurse_summary: null,
                    full_measures: {
                        temperature: [],
                        blood_pressure: [],
                        saturation: [],
                        pulse: []
                    }, visits: [],
                    notifications: [], labs: [], imaging: [], referrals: []
                }} onError={onError}>
                    {() => <InternalPatientCard patient={match[0]} setTitle={setTitle}/>}
                </patientDataContext.Provider>}
        </Drawer>}
    </HashMatch>
}

const FullMeasure = ({patient, measure, icon, latest, data, title, graphProps}) => {
    return <HashMatch match={['info', patient, 'measures', measure]}>{({matched}) => <List.Item style={{
        padding: 5,
        display: "flex",
        animation: matched ? 'highlight 2s ease-out' : undefined
    }}>
        <div style={{textAlign: "center", flex: 1}}>
            <div style={{fontSize: 12}}>{title}&nbsp;<FontAwesomeIcon icon={icon}/></div>
            <div style={{
                userSelect: "none",
                fontSize: 14,
                color: latest && !latest.is_valid ? 'red' : undefined
            }}>
                {(latest && latest.value) || '-'}
            </div>
        </div>
        <MeasureGraph data={data} title={title} graphProps={graphProps}/>
    </List.Item>}</HashMatch>
}
const InternalPatientCard = ({patient, setTitle}) => {
    const {value, loading} = useContext(patientDataContext.context);
    useEffect(() => {
        if (loading)
            setTitle('')
        else {
            setTitle(`${value.name} (${value.age || 'גיל לא ידוע'})`);
        }
    }, [value, loading, setTitle]);
    if (loading)
        return <Spin/>
    return <HashMatch match={['info', patient]}>
        {({match}) => <Collapse defaultActiveKey={['basic'].concat(...match.slice(0, 1))}>
            <Panel key={'basic'} showArrow={false} collapsible={"disabled"} header={'מידע בסיסי'}>
                {value.warnings.map((warning, i) =>
                    <HashMatch key={i} match={['info', patient, 'basic', `warning-${i}`]}>{({matched}) =>
                        <PatientWarning patient={patient} warning={warning} index={i} style={{
                            animation: matched ? 'highlight 2s ease-out' : undefined, marginBottom: 18
                        }}/>
                    }</HashMatch>
                )}
                <HashMatch match={['info', patient, 'basic', 'complaint']}>{({matched}) =>
                    <PatientComplaint patient={patient} style={{
                        animation: matched ? 'highlight 2s ease-out' : undefined, marginBottom: 18
                    }}/>
                }</HashMatch>
                <div style={{display: "flex", width: '100%', marginBottom: 14}}>
                    <span>דחיפות:&nbsp;</span><PatientSeverity/>

                </div>

                <HashMatch match={['info', patient, 'basic', 'secondary-complaint']}>{({matched}) =>
                    <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                        תלונה משנית: {value.secondary_complaint}
                    </p>}
                </HashMatch>
                <HashMatch match={['info', patient, 'basic', 'nurse-summary']}>{({matched}) =>
                    <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                        תיאור צוות סיעודי: {value.nurse_summary}
                    </p>}
                </HashMatch>
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
            {value.notifications.length > 0 && <Panel key={'important'} header={'עדכונים חשובים'}>
                {value.notifications.map((notification, i) => <p
                    key={i}>{notification}</p>)}
            </Panel>}
            <Panel key={'labs'} header={
                <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                    <span>מעבדה</span>
                    <div><Badge style={{backgroundColor: '#1890ff'}} count={value.labs.length} size={"small"}/></div>
                </div>
            }>
                {value.labs.length ? value.labs.map((lab, i) =>
                    <HashMatch key={i} match={['info', patient, 'labs', `lab-${i}`]}>{({matched}) =>
                        <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                            {lab.category} - {lab.status} - <Moment date={lab.at} format={'hh:mm DD/MM'}/>
                        </p>
                    }</HashMatch>
                ) : <Empty description={'לא הוזמנו בדיקות מעבדה'}/>}
            </Panel>
            <Panel key={'imaging'} header={
                <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
                    <span>הדמיות</span>
                    <div><Badge style={{backgroundColor: '#1890ff'}} count={value.imaging.length} size={"small"}/></div>
                </div>
            }>
                {value.imaging.length ? value.imaging.map((image, i) =>
                    <HashMatch key={i} match={['info', patient, 'imaging', `${image.external_id}`]}>{({matched}) =>
                        <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                            {image.title} - {image.status_text}
                        </p>
                    }</HashMatch>
                ) : <Empty description={'לא הוזמנו הדמיות'}/>}
            </Panel>
            <Panel key={'referrals'} header={'ייעוץ'}>
                {value.referrals.length ? value.referrals.map((referral, i) => <p key={i}>{referral}</p>) :
                    <Empty description={'לא נרשמו הפניות'}/>}
            </Panel>
            <Panel key={'story'} header={'סיפור מטופל'}>
                <Timeline reverse mode={"left"}>{value.events.map(event =>
                    <Timeline.Item key={event.key} label={<Moment date={event.at} format={'hh:mm DD-MM-YYYY'}/>}>
                        {event.content}
                    </Timeline.Item>
                )}</Timeline>
            </Panel>
        </Collapse>}
    </HashMatch>
}
import {Collapse, Drawer, List, Radio, Spin, Timeline} from "antd";
import React, {useContext, useEffect, useState} from "react";
import {useNavigate} from "react-router";
import Moment from "react-moment";
import moment from "moment";
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
        xAxis: {type: "datetime", reversed: true, useHTML: true},
        yAxis: {opposite: true, title: {enabled: false}},
        chart: {height: 80, width: 200, spacingBottom: 5, style: {fontFamily: fontFamily}},
        legend: {enabled: false},
        credits: {enabled: false},
        tooltip: {outside: false},
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
            setTitle(`${value.name} (${value.age})`);
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
                             data={value.full_measures.temperature.data}/>
                <FullMeasure key={'blood_pressure'} patient={patient} measure={'blood_pressure'} icon={faHeart}
                             latest={value.measures.blood_pressure} title={'לחץ דם'} graphProps={{
                    type: 'arearange', tooltip: {
                        pointFormat: '<span style="color:{series.color}">●' +
                            '</span> {series.name}: <b>{point.low}/{point.high}</b><br/>'
                    }
                }} data={value.full_measures.blood_pressure.data}/>
                <FullMeasure key={'pulse'} patient={patient} measure={'pulse'} icon={faHeartPulse}
                             latest={value.measures.pulse} title={'דופק'} graphProps={{type: 'line'}}
                             data={value.full_measures.pulse.data}/>
                <FullMeasure key={'saturation'} patient={patient} measure={'saturation'} icon={faPercent}
                             latest={value.measures.saturation} title={'סטורציה'}
                             graphProps={{type: 'line'}} data={value.full_measures.saturation.data}/>
            </Panel>
            <Panel key={'visit'} header={'ביקורים קודמים'}>
                {value.visits.map((visit, i) => <p key={i}>{visit.title} ב<a href={'/'}><Moment
                    date={visit.at}/></a>
                </p>)}
            </Panel>
            <Panel key={'important'} header={'עדכונים חשובים'}>
                {value.notifications.map((notification, i) => <p
                    key={i}>{notification}</p>)}
            </Panel>
            <Panel key={'labs'} header={'מעבדה'}>
                {value.labs.map((lab, i) =>
                    <HashMatch key={i} match={['info', patient, 'labs', `lab-${i}`]}>{({matched}) =>
                        <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                            {lab}
                        </p>
                    }</HashMatch>
                )}
            </Panel>
            <Panel key={'imaging'} header={'הדמיות'}>
                {value.imaging.map((image, i) =>
                    <HashMatch key={i} match={['info', patient, 'imaging', `${image.external_id}`]}>{({matched}) =>
                        <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                            {image.description} - {image.status_text}
                        </p>
                    }</HashMatch>
                )}
            </Panel>
            <Panel key={'referrals'} header={'ייעוץ'}>
                {value.referrals.map((referral, i) => <p key={i}>{referral}</p>)}
            </Panel>
            <Panel key={'story'} header={'סיפור מטופל'}>
                <Timeline reverse>{value.events.map(event =>
                    <Timeline.Item key={event.key} label={<Moment date={event.at}/>}>{event.content}</Timeline.Item>
                )}</Timeline>
            </Panel>
        </Collapse>}
    </HashMatch>
}
const dummyMeasures = [{
    id: 'blood_pressure',
    icon: faHeart,
    latest: '130/50',
    isLatestValid: false,
    data: {
        type: 'arearange',
        name: 'לחץ דם',
        data: [
            [moment().subtract(5, "hour").startOf('second').valueOf(), 120, 80],
            [moment().subtract(4, "hour").startOf('second').valueOf(), 123, 81],
            [moment().subtract(3, "hour").startOf('second').valueOf(), 120, 79],
            [moment().subtract(2, "hour").startOf('second').valueOf(), 120, 77],
            [moment().subtract(1, "hour").startOf('second').valueOf(), 100, 70],
        ],
        tooltip: {
            pointFormat: '<span style="color:{series.color}">●</span> {series.name}: <b>{point.low}/{point.high}</b><br/>'
        },
    }
}, {
    id: 'saturation',
    icon: faPercent,
    latest: '98',
    isLatestValid: true,
    data: {

        type: 'line',
        name: 'סטורציה',
        data: [
            [moment().subtract(5, "hour").startOf('second').valueOf(), 98],
            [moment().subtract(4, "hour").startOf('second').valueOf(), 87],
            [moment().subtract(3, "hour").startOf('second').valueOf(), 96],
            [moment().subtract(2, "hour").startOf('second').valueOf(), 92],
            [moment().subtract(1, "hour").startOf('second').valueOf(), 94],
        ]
    }
}, {
    id: 'pulse',
    icon: faHeartPulse,
    latest: '66',
    isLatestValid: true,
    data: {
        type: 'line',
        name: 'דופק',
        data: [
            [moment().subtract(5, "hour").startOf('second').valueOf(), 65],
            [moment().subtract(4, "hour").startOf('second').valueOf(), 70],
            [moment().subtract(3, "hour").startOf('second').valueOf(), 79],
            [moment().subtract(2, "hour").startOf('second').valueOf(), 69],
            [moment().subtract(1, "hour").startOf('second').valueOf(), 68],
        ],
    }
}, {
    id: 'temperature',
    icon: faTemperatureHalf,
    latest: '37.2',
    isLatestValid: true,
    data: {
        type: 'line',
        name: 'חום',
        data: [
            [moment().subtract(5, "hour").startOf('second').valueOf(), 37.7],
            [moment().subtract(4, "hour").startOf('second').valueOf(), null],
            [moment().subtract(3, "hour").startOf('second').valueOf(), null],
            [moment().subtract(2, "hour").startOf('second').valueOf(), null],
            [moment().subtract(1, "hour").startOf('second').valueOf(), null],
        ]
    }
}]
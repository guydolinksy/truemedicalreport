import {Collapse, Drawer, List, Radio, Timeline} from "antd";
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
const MeasureGraph = ({measure}) => {
    return <HighchartsReact highcharts={Highcharts} options={{
        title: null,
        xAxis: {type: "datetime", reversed: true, useHTML: true},
        yAxis: {opposite: true, title: {enabled: false}},
        chart: {height: 80, width: 200, spacingBottom: 5, style: {fontFamily: fontFamily}},
        legend: {enabled: false},
        credits: {enabled: false},
        tooltip: {outside: false},
        plotOptions: {series: {marker: {radius: 3}, lineWidth: 1}},
        series: [measure]
    }}/>
}
const PatientSeverity = () => {
    const {getData, updateData} = useContext(patientDataContext.context);
    const value = getData(['severity', 'value']);
    return <Radio.Group value={value} size={"small"} buttonStyle={"solid"}
                        style={{flex: 1, display: "inline-flex", textAlign: "center"}}
                        onChange={e => updateData(['severity', 'value'], e.target.value)}>
        {[1, 2, 3, 4, 5].map(i => <Radio.Button key={i} value={i} style={{
            flex: 1,
            color: value === i ? undefined : severityBorderColor[i],
            backgroundColor: value === i ? severityColor[i] : undefined,
        }}>{i}</Radio.Button>)}
    </Radio.Group>
}
export const PatientInfo = () => {
    const navigate = useNavigate();

    const [title, setTitle] = useState();
    return <HashMatch match={['info']}>
        {({matched, match}) => <Drawer title={title} placement={"left"} visible={matched}
                                       onClose={() => navigate('#')}>
            {matched &&
                <patientDataContext.Provider url={`/api/patients/${match[0]}/info`} defaultValue={{}} onError={() => navigate('#')}>
                    {() => <InternalPatientCard patient={match[0]} setTitle={setTitle}/>}
                </patientDataContext.Provider>}
        </Drawer>}
    </HashMatch>
}
const InternalPatientCard = ({patient, setTitle}) => {
    const {getData, loadingData} = useContext(patientDataContext.context);
    useEffect(() => {
        if (loadingData)
            setTitle('')
        else {
            let name = getData(['name']), age = getData(['age']);
            setTitle(`${name} (${age})`);
        }
    }, [getData, loadingData, setTitle]);
    return <HashMatch match={['info', patient]}>
        {({match}) => <Collapse defaultActiveKey={['basic'].concat(...match.slice(0, 1))}>
            <Panel key={'basic'} showArrow={false} collapsible={"disabled"} header={'מידע בסיסי'}>
                {getData(['warnings'], ['פירוט התרעה 1']).map((warning, i) =>
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
                        תלונה משנית: {getData(['secondary-complaint'], 'תלונה משנית')}
                    </p>}
                </HashMatch>
                <HashMatch match={['info', patient, 'basic', 'nurse-summary']}>{({matched}) =>
                    <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                        תיאור צוות סיעודי: {getData(['nurse-summary'], 'תיאור צוות סיעודי')}
                    </p>}
                </HashMatch>
            </Panel>
            <Panel key={'measures'} header={'מדדים'}>
                <List dataSource={(getData(['measures'], dummyMeasures))}
                      renderItem={(measure, i) => <HashMatch match={['info', patient, 'measures', measure.id]}>
                          {({matched}) => <List.Item style={{
                              padding: 5,
                              display: "flex",
                              animation: matched ? 'highlight 2s ease-out' : undefined
                          }}>
                              <div style={{textAlign: "center", flex: 1}}>
                                  <div style={{fontSize: 12}}>{measure.data.name}&nbsp;<FontAwesomeIcon
                                      icon={measure.icon}/>
                                  </div>
                                  <div style={{
                                      userSelect: "none",
                                      fontSize: 14,
                                      color: !measure.isLatestValid ? 'red' : undefined
                                  }}>
                                      {measure.latest}
                                  </div>
                              </div>
                              <MeasureGraph key={i} measure={measure.data}/>
                          </List.Item>}
                      </HashMatch>}/>
            </Panel>
            <Panel key={'visit'} header={'ביקורים קודמים'}>
                {(getData(['visits']) || []).map((visit, i) => <p key={i}>{visit.title} ב<a href={'/'}><Moment date={visit.at}/></a>
                </p>)}
            </Panel>
            <Panel key={'important'} header={'עדכונים חשובים'}>
                {(getData(['notifications']) || []).map((notification, i) => <p key={i}>{notification}</p>)}
            </Panel>
            <Panel key={'labs'} header={'מעבדה'}>
                {getData(['labs'], ['פירוט מדבקה 1']).map((lab, i) =>
                    <HashMatch key={i} match={['info', patient, 'labs', `lab-${i}`]}>{({matched}) =>
                        <p style={{animation: matched ? 'highlight 2s ease-out' : undefined}}>
                            {lab}
                        </p>}
                    </HashMatch>
                )}
            </Panel>
            <Panel key={'imaging'} header={'הדמיות'}>
                {(getData(['image']) || []).map((image, i) => <p key={i}>{image}</p>)}
            </Panel>
            <Panel key={'referrals'} header={'ייעוץ'}>
                {(getData(['referrals']) || []).map((referral, i) => <p key={i}>{referral}</p>)}
            </Panel>
            <Panel key={'story'} header={'סיפור מטופל'}>
                <Timeline reverse>{(getData(['events']) || []).map(event =>
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
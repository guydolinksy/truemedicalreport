import {Radio} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';
import {PatientWarning} from "../card/PatientWarning";
import {PatientStatus} from "../card/PatientStatus";
import {useParams} from 'react-router-dom';
import {hashMatchContext} from "../HashMatch";
import moment from "moment";

const PatientSeverity = () => {
    const {value, update} = useContext(patientDataContext.context);
    return <Radio.Group value={value.severity && value.severity.value} size={"small"} buttonStyle={"solid"}
                        style={{flex: 1, display: "inline-flex", textAlign: "center"}}
                        onChange={e => update(['severity'], {
                            value: e.target.value,
                            at: moment().toISOString().replace('Z', '+00:00')
                        }, 'Severity')}>
        {[1, 2, 3, 4, 5].map(i => <Radio.Button key={i} value={i} style={{flex: 1}} className={
            `severity-${i} severity-` + (value.severity && value.severity.value === i ? "background" : "color")
        }>{i}</Radio.Button>)}
    </Radio.Group>
}
export const BasicInfo = (params) => {
    const {matched} = useContext(hashMatchContext);
    const {patient} = useParams()
    const {value} = useContext(patientDataContext.context);
    return <div {...params}>
        {Object.entries(value.warnings).map(([key, warning], i) => <div key={i}>
            <PatientWarning patient={patient} warning={warning} index={i} style={{
                direction: "rtl",
                userSelect: "none",
                cursor: "pointer",
                padding: "8px 12px",
                height: 82,
                overflowY: "auto"
            }}/>
        </div>)}
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
        </p></div>
}
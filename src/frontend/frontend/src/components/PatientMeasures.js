import React, {useContext, useState} from "react";
import {CustomIcon} from "./CustomIcon";
import {RelativeTime} from "./RelativeTime";
import {Watchable} from "./Watchable";
import {patientDataContext} from "./PatientBase";
import {useNavigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react';
import {Popover} from 'antd';

const Measure = ({patient, hover, measure, icon, title}) => {
    const navigate = useNavigate();
    const {trackEvent} = useMatomo()
    const {value} = useContext(patientDataContext.context);
    const data = value && value.measures ? value.measures[measure] : null;
    const dataValue = data && data.value !== null && (Array.isArray(data.value) ? data.value.join('/') : data.value);

    return <Popover style={{width: 100}} title={<>
        <div><CustomIcon icon={icon}/>&nbsp;{title}</div>
    </>} placement={"left"} content={<div style={{textAlign: "center"}}>
        <div>
            <span className={(!data || data.is_valid === null) ? undefined : data.is_valid ? 'ok-text' : 'error-text'}
                  style={{userSelect: "none", fontSize: 14}}>
                <b>{(data && data.value) ? dataValue : '-'}</b>
            </span>&nbsp;{(data && data.effect && data.effect.kind) &&
            <CustomIcon status={data.is_valid !== false ? 'processing' : 'error'} icon={data.effect.kind}/>}
        </div>
        <div>
            {(data && data.value !== null) && <RelativeTime style={{fontSize: 12}} date={data.at}/>}
            {(data && data.value !== null && data.effect && data.effect.kind) && '|'}
            {(data && data.effect && data.effect.kind) && <RelativeTime style={{fontSize: 12}} date={data.effect.at}/>}
            {(!data || (!data.value !== null && (!data.effect || !data.effect.kind))) && '-'}
        </div>
    </div>}>
        <div className={'measurement'} style={{userSelect: "none", flexWrap: "nowrap", display: 'flex'}}
             onClick={data ? e => {
                 navigate(`#info#${patient}#measures#${measure}`);
                 trackEvent({category: 'patient-' + measure, action: 'click-event'});
                 e.stopPropagation();
             } : null}>
            <div className={(!data || data.is_valid === null) ? undefined : data.is_valid ? 'ok-text' : 'error-text'}
                 style={{flexWrap: "nowrap", display: 'flex'}}>
                <div style={{textAlign: 'center', width: 12}}>
                    <CustomIcon style={{fontSize: 12}} icon={icon}/>
                </div>
                {hover && <div style={{
                    flexWrap: "nowrap",
                    display: 'flex'
                }}>&nbsp;<Watchable forceOpen={hover} watchKey={`measure#${measure}`} updateAt={data ? data.at : null}>
                    {(data && data.value !== null) ? dataValue : '?'}
                </Watchable></div>}
            </div>
            {(data && data.effect && data.effect.kind) && <span>
                &nbsp;<CustomIcon style={{fontSize: 12}} status={data.is_valid !== false ? 'processing' : 'error'}
                                  icon={data.effect.kind}/>
            </span>}
        </div>
    </Popover>
};

export const PatientMeasures = ({patient}) => {
    const [hover, setHover] = useState(false);

    return <div style={{
        display: "flex", flexDirection: 'column', justifyContent: "space-between", padding: "8px 12px",
        width: hover ? '100%' : 40, flex: 0
    }} onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}>
        <Measure patient={patient} hover={hover} measure={'temperature'} icon={'temperature'} title={'חום'}/>
        <Measure patient={patient} hover={hover} measure={'blood_pressure'} icon={'bloodPressure'} title={'לחץ דם'}/>
        <Measure patient={patient} hover={hover} measure={'pulse'} icon={'pulse'} title={'דופק'}/>
        <Measure patient={patient} hover={hover} measure={'saturation'} icon={'saturation'} title={'סטורציה'}/>
        <Measure patient={patient} hover={hover} measure={'pain'} icon={'pain'} title={'כאב'}/>
    </div>
}
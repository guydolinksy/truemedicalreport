import React, {useContext} from "react";
import {Empty, Spin} from "antd";
import {useNavigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react'
import {patientDataContext} from "./PatientBase";
import {RelativeTime} from "./RelativeTime";
import {Notification} from "./Notification";

export const ProtocolStatus = () => {
    const {value, loading} = useContext(patientDataContext.context);
    const {trackEvent} = useMatomo()

    return loading ? <Spin/> : <div onClick={e => {
        trackEvent({category: 'patient-protocol', action: 'click-event'});
    }}>
        {value.protocol && value.protocol.items && value.protocol.items.length ? value.protocol.items.map(item => {
            let data = value.protocol.values[item.key];
            return <div key={item.key} style={{
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
        {Object.entries(value.notifications).slice(0, 2).map(([key, item]) =>
            <div key={key} style={{
                display: "flex",
                flexFlow: "row nowrap",
                justifyContent: "space-between",
                alignItems: "center"
            }}>
                <Notification patient={patient} message={item} className={'patient-card-clickable-content'}
                              style={{whiteSpace: "nowrap", textOverflow: "ellipsis", overflowX: "hidden"}}/>
            </div>
        )}
        {Object.entries(value.notifications).slice(2, 3).length > 0 && <div>
            <a className={'patient-card-clickable-content'} href={`#info#${patient}#notifications`}>
                ועוד {Object.keys(value.notifications).length - 2} עדכונים נוספים...
            </a>
        </div>}
        {(!Object.keys(value.notifications).length) &&
            <Empty style={{margin: -2}} image={Empty.PRESENTED_IMAGE_SIMPLE}
                   description={'אין עדכונים זמינים'}/>}
    </div>
}
export const PatientContent = ({patient}) => {
    const {value} = useContext(patientDataContext.context);
    return <div>
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
}
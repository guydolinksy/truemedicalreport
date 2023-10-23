import React, {useContext, useEffect, useState} from "react";
import {patientDataContext} from "./PatientBase";
import {RelativeTime} from "./RelativeTime";
import {Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {useNavigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react'
import moment from "moment";
import {useTime} from 'react-timer-hook';
import {ArrowLeftOutlined} from '@ant-design/icons';
import {faCheckCircle} from "@fortawesome/free-solid-svg-icons";

export const PatientArrival = () => {
    const {value} = useContext(patientDataContext.context);
    const {minutes} = useTime({});
    const [arrivalClass, setArrivalClass] = useState(undefined);

    useEffect(() => {
        if (moment().subtract(10, "hours").isAfter(value.admission.arrival))
            setArrivalClass('error-text')
        else if (moment().subtract(4, "hours").isAfter(value.admission.arrival))
            setArrivalClass('warn-text')
    }, [value.admission.arrival, minutes]);

    return <Tooltip overlay={'זמן מקבלה'}>
        <RelativeTime className={arrivalClass} date={value.admission.arrival}/>
    </Tooltip>
}
export const PatientStatus = ({patient, style}) => {
    const navigate = useNavigate();
    const {value, loading} = useContext(patientDataContext.context);
    const {minutes} = useTime({});
    const {trackEvent} = useMatomo()


    return loading ? <Spin/> : <div style={{display: "flex", justifyContent: "space-between", ...style}} onClick={e => {
        navigate(`#info#${patient}#basic#complaint`);
        trackEvent({category: 'patient-complaint', action: 'click-event'});
        e.stopPropagation();
    }}>
        <div style={{whiteSpace: "nowrap", display: "flex", alignItems: "center", overflowX: "hidden"}}>
            {value.severity && <span><Tooltip overlay='דחיפות'>
                <span>(<strong>{value.severity.value}</strong>)</span>
            </Tooltip>&nbsp;</span>}
            {value.protocol && value.protocol.active &&
                <Tooltip overlay={`מצב פרוטוקול - ${value.intake.complaint}`}>
                    <FontAwesomeIcon icon={faCheckCircle} style={{marginLeft: "0.3rem", color: "#40a9ff"}}/>
                </Tooltip>}
            <Tooltip overlay={<div>{value.intake.complaint}:<br/>{value.intake.nurse_description}</div>}>
                <span style={{overflowX: "hidden", textOverflow: "ellipsis"}}>{value.intake.complaint}</span>
            </Tooltip>&nbsp;
            <span>
                <ArrowLeftOutlined/>&nbsp;
                {value.treatment.destination || <span className={'error-text'}>(לא הוחלט)</span>}
            </span>
        </div>
        <PatientArrival/>
    </div>
}
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faWarning,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router-dom";
import {useMatomo} from '@datapunt/matomo-tracker-react'

export const PatientWarning = ({patient, warning, index, style}) => {
    const navigate = useNavigate();
    const {trackEvent} = useMatomo()
    return <div className={`severity-background severity-${warning.severity.value}`}
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
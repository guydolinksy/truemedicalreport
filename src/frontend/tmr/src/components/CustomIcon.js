import React from 'react';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faFlaskVial,
    faHeart,
    faHeartPulse,
    faPercentage,
    faTemperatureHalf,
    faUserDoctor,
    faUserNurse,
    faXRay,
    faFileMedical,
} from "@fortawesome/free-solid-svg-icons";

export const CustomIcon = ({status, icon}) => {
    const style = {'error': {color: '#d32029'}, 'processing': {color: '#1890ff'}, 'success': {color: '#49aa19'}}[status]
    if (icon === 'pulse')
        return <FontAwesomeIcon style={style} icon={faHeartPulse}/>
    if (icon === 'temperature')
        return <FontAwesomeIcon style={style} icon={faTemperatureHalf}/>
    if (icon === 'saturation')
        return <FontAwesomeIcon style={style} icon={faPercentage}/>
    if (icon === 'bloodPressure')
        return <FontAwesomeIcon style={style} icon={faHeart}/>
    if (icon === 'imaging')
        return <FontAwesomeIcon style={style} icon={faXRay}/>
    if (icon === 'laboratory')
        return <FontAwesomeIcon style={style} icon={faFlaskVial}/>
    if (icon === 'doctor')
        return <FontAwesomeIcon style={style} icon={faUserDoctor}/>
    if (icon === 'nurse')
        return <FontAwesomeIcon style={style} icon={faUserNurse}/>
    if (icon === 'referral')
        return <FontAwesomeIcon style={style} icon={faFileMedical}/>
    return <span>{icon}</span>
}
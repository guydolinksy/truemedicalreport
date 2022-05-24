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
    faXRay
} from "@fortawesome/free-solid-svg-icons";

export const CustomIcon = ({status, icon}) => {
    const style = {'error': {color: '#d32029'}, 'processing': {color: '#1890ff'}, 'success': {color: '#49aa19'}}[status]
    if (icon === 1)
        return <FontAwesomeIcon style={style} icon={faHeartPulse}/>
    if (icon === 2)
        return <FontAwesomeIcon style={style} icon={faTemperatureHalf}/>
    if (icon === 3)
        return <FontAwesomeIcon style={style} icon={faPercentage}/>
    if (icon === 4)
        return <FontAwesomeIcon style={style} icon={faHeart}/>
    if (icon === 5)
        return <FontAwesomeIcon style={style} icon={faXRay}/>
    if (icon === 6)
        return <FontAwesomeIcon style={style} icon={faFlaskVial}/>
    if (icon === 7)
        return <FontAwesomeIcon style={style} icon={faUserDoctor}/>
    if (icon === 8)
        return <FontAwesomeIcon style={style} icon={faUserNurse}/>
}
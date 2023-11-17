import React, {useContext} from 'react';
import {patientDataContext} from "../card/PatientBase";
import {loginContext} from "../LoginContext";

export const PatientInfo = ({config}) => {
    const {value} = useContext(patientDataContext.context);
    const {user} = useContext(loginContext);

    let gender = {
        male: 'בן ',
        female: 'בת ',
        [null]: '',
    }[value.info?.gender];

    return <h3 style={{
        textAlign: 'center',
        height: 'min-content',
        ...config.customStyle,
    }} className={`gender-${value.info?.gender}`}>
        {user.anonymous ? `${gender}(${value.info?.age || 'גיל לא ידוע'})` :
            `${value.info?.name}, ${gender}(${value.info?.age || 'גיל לא ידוע'})` +
            (value.info?.id_ ? `, ת.ז. ${value.info?.id_}` : '') +
            (value.info?.phone ? `, טלפון : ${value.info?.phone}` : '')}
    </h3>;
}
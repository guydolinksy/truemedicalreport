import React, {useContext} from "react";
import {patientDataContext} from "./PatientBase";
import {Tooltip} from "antd";
import Moment from 'react-moment';

export const PatientAge = ({patient}) => {
    const {value, loading} = useContext(patientDataContext.context);
    const genderedAge = {
        male: 'בן',
        female: 'בת',
    }
    return !patient || loading ? null : <span>
        {genderedAge[value.info.gender]}&nbsp;
        <Tooltip overlay={
            value.info.birthdate ? <Moment date={value.info.birthdate} format={"DD/MM/YYYY"}/> : "לא ידוע"
        }>
            {value.info.age || "(לא ידוע)"}
        </Tooltip>
    </span>
}
import React, {useCallback} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {Info} from "../components/panel/Info";
import {Spin} from 'antd';

import {patientDataContext} from "../components/card/PatientBase";

export const INFO_URL = '/views/:view/modes/:mode/info/:patient';

export const InfoView = (() => {
    const params = useParams();
    const navigate = useNavigate();
    const onError = useCallback(() => navigate('/'), [navigate])

    return <patientDataContext.Provider url={`/api/patients/${params.patient}/info`} defaultValue={{
        warnings: [], awaiting: {}, severity: {value: 0, at: null}, flagged: null,
        id_: null, name: null, age: null, gender: null, birthdate: null, arrival: null,
        treatment: {destination: null}, complaint: null, admission: {},
        intake: {nurse_description: null}, measures: {
            temperature: null,
            blood_pressure: null,
            saturation: null,
            pulse: null
        },
        full_measures: {
            temperature: [],
            blood_pressure: [],
            saturation: [],
            pulse: []
        }, visits: [], notifications: {}, labs: {}, imaging: {}, referrals: {}
    }} onError={onError}>
        {({loading}) => loading ? <Spin/> : <Info patient={params.patient}/>}
    </patientDataContext.Provider>
});
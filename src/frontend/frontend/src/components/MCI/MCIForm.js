import {UserTheme} from "../../themes/ThemeContext";
import {MCIFormSection} from "./MCIFormSection";
import React, {useContext, useEffect, useState} from 'react';
import {Collapse, Spin, Input} from 'antd'
import axios from 'axios';
import {patientDataContext} from "../PatientBase";
import {hashMatchContext} from "../HashMatch";
import {loginContext} from "../LoginContext";
import {Patient} from "../Patient";

const {Panel} = Collapse;
export const MCIFormInner = ({form, setHeader, onError}) => {
    const {value, loading, update} = useContext(patientDataContext.context);
    const {user} = useContext(loginContext);

    useEffect(() => {
        if (loading)
            setHeader({title: ''})
        else {
            let gender = {
                male: 'בן',
                female: 'בת',
            }[value.info.gender];
            setHeader({
                title: user.anonymous ? `${gender} (${value.info.age || 'גיל לא ידוע'})` :
                    `${value.info.name}, ${gender} (${value.info.age || 'גיל לא ידוע'})` +
                    (value.info.id_ ? `, ת.ז. ${value.info.id_}` : '') +
                    (value.info.phone ? `, טלפון : ${value.info.phone}` : ''),
                className: `gender-${value.info.gender}`
            });
        }
    }, [value, loading, setHeader]);

    return <>
        <Input value={value.comment} onChange={e => update(['comment'], e.target.value, false)} placeholder={'הערות:'}
               style={{width: '100%'}}/>
        <Collapse size={'small'} activeKey={form.map(section => section.key)}>
            {form.map(section => <Panel header={section.name} key={section.key}>
                <MCIFormSection name={section.name} options={section.options}/>
            </Panel>)}
        </Collapse>
    </>
}
export const MCIForm = ({setHeader, onError}) => {
    const [form, setForm] = useState([])
    const {matched, matching} = useContext(hashMatchContext);

    useEffect(() => {
        axios.get('/api/mci/form').then(response => {
            setForm(response.data)
        })
    }, []);


    return <UserTheme>
        {matched(['info']) &&
            <patientDataContext.Provider url={`/api/patients/${matching(['info'])[0]}/info`} defaultValue={{
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
                {({loading}) => loading ? <Spin/> :
                    <MCIFormInner form={form} patient={matching(['info'])[0]} setHeader={setHeader}/>}
            </patientDataContext.Provider>}
    </UserTheme>
}
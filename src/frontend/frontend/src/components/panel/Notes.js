import {Input} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';

export const Notes = (params) => {
    const {value, update} = useContext(patientDataContext.context);
    return <div {...params}>
        <Input value={value.comment} onChange={e => update(['comment'], e.target.value, false)} placeholder={'הערות:'}
               style={{width: '100%'}}/>
    </div>
}
import React, {useContext} from "react";
import {Checkbox, Collapse, TimePicker} from "antd";
import {patientDataContext} from "../PatientBase";
import moment from 'moment';

const {Panel} = Collapse;
export const MCIFormItem = ({option}) => {
    const {value, update} = useContext(patientDataContext.context);
    const data = (value.mci[option.key] || {})
    return <div style={{display: 'flex', flex: 1, justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{display: 'flex', flex: 1}}>
            {option.type === 'checkbox' &&
                <span><Checkbox checked={data.value} onChange={e => {
                    update(['mci', option.key], {
                        value: e.target.checked,
                        at: moment().toISOString()
                    }, 'MCIBooleanValue')
                }}/>&nbsp;{option.name}</span>}
            {option.type === 'collapse' &&
                <Collapse defaultActiveKey={['children']} style={{flex: 1}}>
                    <Panel key={'children'} header={option.name}>
                        <MCIFormSection options={option.children}/>
                    </Panel>
                </Collapse>}
        </div>
        {data.value && <TimePicker value={data.at ? moment(data.at) : null} format={"HH:mm"} onSelect={newTime => {
            update(['mci', option.key], {
                value: data.value,
                at: (moment().isBefore(newTime) ? newTime.subtract(1, 'days') : newTime).toISOString()
            }, 'MCIBooleanValue')
        }} allowClear={false} style={{width: 90}}/>}
    </div>
}

export const MCIFormSection = ({options}) => {

    return <div>
        {options.map((option, i) => <MCIFormItem key={i} option={option}/>)}
    </div>
}

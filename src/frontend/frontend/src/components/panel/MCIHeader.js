import {Input, Radio, Space} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';
import moment from "moment";

export const MCIHeader = ({sections, ...params}) => {
    const {value, update} = useContext(patientDataContext.context);

    return <Space className={'first-child-flex-1'} style={{
        display: 'flex',
        width: '100%',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        marginBottom: 8,
    }}>
        <Input value={value.comment} onChange={e => update(['comment'], e.target.value, false)}
               placeholder={'הערות:'}
               style={{flex: 1, minWidth: 250}}/>
        {sections.filter(section => section.type === 'radio').map(section =>
            <Radio.Group key={section.key} value={value.mci[section.key] && value.mci[section.key].value}
                         style={{width: '100%', textAlign: "center"}}
                         buttonStyle={"solid"} onChange={e => update(['mci', section.key], {
                value: e.target.value,
                at: moment().toISOString()
            }, 'MCIStringValue')}>
                {section.options.map(option => <Radio.Button key={option.key} value={option.key}>
                    {option.name}
                </Radio.Button>)}
            </Radio.Group>)}
    </Space>
}
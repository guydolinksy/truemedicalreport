import React, {useContext, useMemo} from "react";
import {Button, Card, TimePicker} from "antd";
import {patientDataContext} from "../card/PatientBase";
import moment from 'moment';
import {DeleteOutlined} from "@ant-design/icons";


export const MCI_DEPARTMENT = 'mci'
export const MCIFormItem = ({current, section, index, item}) => {
    const {value, update} = useContext(patientDataContext.context);
    return <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{display: 'flex', flex: 1}}>
            <span><Button type={'text'} danger icon={<DeleteOutlined/>} onClick={() => {
                update(['mci', section.key], current.filter(i => i.key !== item.key), 'MCIList')
            }}/>&nbsp;{item.value}</span>
        </div>
        {item.value &&
            <TimePicker inputReadOnly value={item.at ? moment(item.at) : null} format={"HH:mm"} onSelect={newTime => {
                update(['mci', section.key], [...current.slice(0, index), {
                        value: item.value,
                        at: (moment().isBefore(newTime) ? newTime.subtract(1, 'days') : newTime).toISOString()
                    }, ...current.slice(index + 1)], 'MCIList')
            }} allowClear={false} style={{width: 90}}/>}
    </div>
}

export const MCIFormSection = ({isDrawer, section}) => {
    const {value, update} = useContext(patientDataContext.context);

    const current = useMemo(() => {
        return value.mci[section.key] && value.mci[section.key].value ? value.mci[section.key].value : []
    }, [value, section.key])
    return <Card size={'small'} title={section.name} key={section.key}
                 style={{
                     width: '100%',
                     flex: isDrawer ? undefined : 1,
                     display: 'flex',
                     flexDirection: 'column',
                     maxHeight: 500
                 }}
                 bodyStyle={{
                     flex: isDrawer ? undefined : 1,
                     display: 'flex',
                     flexDirection: 'column',
                     overflowY: 'hidden'
                 }}
    >
        <div style={{display: 'flex', flexDirection: 'column', flex: 1, overflowY: 'scroll'}}>
            {current.map((item, i) =>
                <MCIFormItem key={item.key} index={i} section={section} current={current} item={item}/>
            )}
            <div style={{flex: 1}}/>
            <div style={{display: 'flex', flexWrap: 'wrap'}}>
                {section.options.map(option =>
                    <Button style={{flex: 1}} size={'small'} key={option.key} onClick={() => update(
                        ['mci', section.key], [...current, {
                                key: `${option.key}-${current.length}`,
                                value: option.name,
                                at: moment().toISOString(),
                                type: 'list_item'
                            }], 'MCIList')}>
                        {option.name}
                    </Button>)}
            </div>
        </div>
    </Card>
}

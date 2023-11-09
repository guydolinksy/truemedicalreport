import React, {useContext, useMemo} from "react";
import {Button, Card, TimePicker} from "antd";
import {patientDataContext} from "../card/PatientBase";
import moment from 'moment';
import {DeleteOutlined} from "@ant-design/icons";
import {useParams} from 'react-router-dom';

export const MCI_DEPARTMENT = 'mci'
export const MCIFormItem = ({current, sectionKey, index, item}) => {
    const {value, update} = useContext(patientDataContext.context);
    return <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center'}}>
        <div style={{display: 'flex', flex: 1}}>
            <span><Button type={'text'} danger icon={<DeleteOutlined/>} onClick={() => {
                update([MCI_DEPARTMENT, sectionKey], current.filter(i => i.key !== item.key), 'MCIList')
            }}/>&nbsp;{item.value}</span>
        </div>
        {item.value &&
            <TimePicker inputReadOnly value={item.at ? moment(item.at) : null} format={"HH:mm"} onSelect={newTime => {
                update([MCI_DEPARTMENT, sectionKey], [...current.slice(0, index), {
                    value: item.value,
                    at: (moment().isBefore(newTime) ? newTime.subtract(1, 'days') : newTime).toISOString().replace('Z', '+00:00')
                }, ...current.slice(index + 1)], 'MCIList')
            }} allowClear={false} style={{width: 90}}/>}
    </div>
}

export const MCISection = ({config}) => {
    const {patient} = useParams();
    const {value, update} = useContext(patientDataContext.context);

    console.log(config, value);
    const current = useMemo(() => {
        return value.mci[config.key] ?? [];
    }, [value, config.key])
    return <Card size={'small'} title={config.name} key={config.key}
                 style={{
                     width: '100%',
                     flex: patient ? undefined : 1,
                     display: 'flex',
                     flexDirection: 'column',
                     maxHeight: 500,
                     ...config.customStyle,
                 }}
                 bodyStyle={{
                     flex: patient ? undefined : 1,
                     display: 'flex',
                     flexDirection: 'column',
                     overflowY: 'hidden'
                 }}
    >
        <div style={{display: 'flex', flexDirection: 'column', flex: 1, overflowY: 'scroll'}}>
            {current.map((item, i) =>
                <MCIFormItem key={item.key} sectionKey={config.key} index={i} current={current} item={item}/>
            )}
            <div style={{flex: 1}}/>
            <div style={{display: 'flex', flexWrap: 'wrap'}}>
                {config.options.map(option =>
                    <Button style={{flex: 1}} size={'small'} key={option.key} onClick={() => update(
                        [MCI_DEPARTMENT, config.key], [...current, {
                            key: `${option.key}-${current.length}`,
                            value: option.name,
                            at: moment().toISOString().replace('Z', '+00:00'),
                            type: 'list_item'
                        }], 'MCIList')}>
                        {option.name}
                    </Button>)}
            </div>
        </div>
    </Card>
}

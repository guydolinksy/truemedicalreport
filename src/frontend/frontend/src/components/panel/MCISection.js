import React, {useCallback, useContext, useMemo, useState} from "react";
import {Button, Card, TimePicker} from "antd";
import {patientDataContext} from "../card/PatientBase";
import moment from 'moment';
import {DeleteOutlined} from "@ant-design/icons";
import {useParams} from 'react-router-dom';
import {Customizer} from './Customizer';

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

const INITIAL_MODAL_PROPS = { customizer: undefined, isOpen: false, onEnd: () => {}, onCancel: () => {} };

export const MCISection = ({config}) => {
    const [modalProps, setModalProps] = useState(INITIAL_MODAL_PROPS);
    const {patient} = useParams();
    const {value, update} = useContext(patientDataContext.context);

    const current = useMemo(() => {
        return value.mci[config.key] ?? [];
    }, [value, config.key]);
    const getOnDone = useCallback((option) => {
      const onCancel = () => {
        setModalProps(INITIAL_MODAL_PROPS);
      };
      const onDone = (value) => {
        setModalProps(INITIAL_MODAL_PROPS);
        return update(
          [MCI_DEPARTMENT, config.key], [...current, {
            key: `${option.key}-${current.length}`,
            value: `${option.name}${value ? ` - ${value}` : ''}`,
            at: moment().toISOString().replace('Z', '+00:00'),
            type: 'list_item'
          }], 'MCIList');
      };
      return () => {
        if (option.customizers?.length && option.customizers[0].type === 'location') {
          setModalProps({ customizer: option.customizers[0], isOpen: true, onEnd: onDone, onCancel })
          return;
        }
        return onDone();
      };
    }, [config.key, current, update]);
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
                  <Button style={{flex: 1}} size={'small'} key={option.key} onClick={getOnDone(option)}>
                    {option.name}
                  </Button>)}
            </div>
        </div>
        <Customizer {...modalProps} />
    </Card>
}

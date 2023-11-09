import {Card, Empty} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';
import {RelativeTime} from "../RelativeTime";

const EcgRecord = ({record}) => <div style={{display: "flex", justifyContent: "space-between"}} key={record.title}>
    <a style={{cursor: "pointer"}} href={record.link}>{record.title}</a>
    <RelativeTime style={{fontSize: 12}} date={record.date}/>
</div>


export const ECGs = (params) => {
    const {value} = useContext(patientDataContext.context);

    return <Card title={
        <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
            <span>בדיקות א.ק.ג</span>
        </div>
    }>
        {!!value?.ecg_records?.length
            ? value.ecg_records.map((record, index) => <EcgRecord record={record} key={index}/>)
            : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו בדיקות א.ק.ג'}/>
        }
    </Card>

}
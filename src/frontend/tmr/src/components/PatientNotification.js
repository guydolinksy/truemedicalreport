import React from 'react';
import {Badge} from "antd";

export const PatientNotification = ({notification}) => {
    return <span style={{display: "flex", justifyContent: "space-between"}}>
        <span style={{lineHeight: '16px'}}>{notification.patient.name}</span>
        <Badge  size={"default"} count={notification.notifications.length}/>
    </span>
}
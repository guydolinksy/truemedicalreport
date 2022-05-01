import React from 'react';

export const PatientNotification = ({notification}) => {
    return <div>
        <span
            style={{lineHeight: '16px'}}>{notification.patient.name}&ensp;-&ensp;{notification.notifications.length}</span>
    </div>
}
import React, {useContext} from "react";
import {Button, Tooltip, notification} from 'antd';
import {UserOutlined} from '@ant-design/icons';

import {PatientAge} from './PatientAge';
import {loginContext} from "./LoginContext";
import {patientDataContext} from "./PatientBase";


export const openNotification = (type, message) => {
    notification[type]({
        message: message,
        duration: 3, // Display duration in seconds
    });
}
const handleCopyToClipboard = (event, text) => {
    event.stopPropagation()
    try {
        navigator.clipboard.writeText(text);
        openNotification('success', 'תעודת הזהות הועתקה');
    } catch (err) {
        openNotification('error', 'קרתה תקלה בהעתקת תעודת הזהות');
    }
};
export const PatientHeader = ({patient, avatar}) => {
    const {value} = useContext(patientDataContext.context);
    const {user} = useContext(loginContext);
    if (!patient)
        return <Button shape={"circle"} type={"text"}>{avatar || <UserOutlined/>}</Button>
    return <span className={`gender-${value.info.gender}`}>
        {avatar || value.admission.bed || <UserOutlined/>}&nbsp;
        {!user.anonymous && <span>
            <Tooltip overlay={<div onClick={(event) => handleCopyToClipboard(event, value.info.id_)}>
                {`ת.ז. ${value.info.id_ || 'לא ידוע'}`}
            </div>}>
                {value.info.name}</Tooltip>,&nbsp;
        </span>}
        <PatientAge patient={patient}/>
    </span>
}
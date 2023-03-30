import React, {useEffect} from "react";
import {Link} from "react-router-dom";
import {Badge} from "antd";
import Moment from "react-moment";

export const Notification = ({patient, message, unread, markRead}) => {
    useEffect(() => {
        let task = setTimeout(markRead ||(() => {}), 6000);
        return () => clearTimeout(task);
    }, [patient, message, markRead]);
    return <>
        <Link to={`#info#${patient}#${message.type}#${message.static_id}`}>
            {unread && <Badge status={'processing'}/>}
            &nbsp;<span className={message.danger ? 'warn-text' : undefined}>{message.message}</span>
        </Link>
        <Moment style={{display: "block"}} date={message.at} format={'HH:mm'}/>
    </>
}
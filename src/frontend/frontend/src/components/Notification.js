import React, {useEffect} from "react";
import {Badge} from "antd";
import {useNavigate} from "react-router";
import {RelativeTime} from "./RelativeTime";

export const Notification = ({patient, message, unread, markRead, ...props}) => {
    const {navigate} = useNavigate();
    useEffect(() => {
        let task = setTimeout(markRead || (() => {
        }), 6000);
        return () => clearTimeout(task);
    }, [patient, message, markRead]);
    return <>
        <a href={`#info#${patient}#${message.type}#${message.static_id}`} onClick={(e) => {
            navigate(`#info#${patient}#${message.type}#${message.static_id}`);
            e.stopPropagation()
        }} {...props}>
            {unread && <span><Badge status={'processing'}/>&nbsp;</span>}
            <span className={message.danger ? 'warn-text' : undefined}>{message.message}</span>
        </a>
        <RelativeTime style={{fontSize: 12}} date={message.at}/>
    </>
}
import React, {useEffect} from "react";
import {Badge} from "antd";
import {useNavigate} from "react-router";
import {RelativeTime} from "./RelativeTime";
import useModal from "antd/es/modal/useModal";
import {modalButton} from "./iframeModal";
import {faPlus} from "@fortawesome/free-solid-svg-icons";

export const Notification = ({patient, message, unread, markRead, showExternalLink, ...props}) => {
    const {navigate} = useNavigate();
    const [modal, modalContext] = useModal();
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
        {showExternalLink && modalButton(modal, faPlus, "צפה.י במערכת חיצונית", message.link)}
        <RelativeTime style={{fontSize: 12}} date={message.at}/>
        {modalContext}
    </>
}

import React, {useState} from 'react';
import {Badge, Menu, Space} from "antd";

import {UserOutlined, FlagFilled, PushpinOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";

const {SubMenu, Item} = Menu;

export const PatientNotification = ({notification, onTitleClick, ...props}) => {
    const colors = {
        1: '#f5222d',
        2: '#fa541c',
        3: '#52c41a',
    }
    const title = <span className={"ant-menu-title-content"} style={{
        display: "flex",
        flexFlow: "row nowrap",
        justifyContent: "space-between",
    }}>
        <div style={{
            display: "flex",
            flexFlow: "column nowrap",
            alignItems: "flex-start",
            lineHeight: '20px',
            minWidth: "0px"
        }}>
            <div><UserOutlined/>{notification.patient.external_data.name}</div>
            <div style={{textOverflow: "ellipsis", fontSize: "10px"}}>{notification.preview}</div>
        </div>
        <div style={{
            display: "flex",
            flexFlow: "column nowrap",
            alignItems: "flex-end",
            lineHeight: '20px',
            minWidth: "0px"
        }}>
            <Moment style={{display: "block"}} date={notification.at || notification.patient.external_data.arrival} format={'hh:mm'}/>
            <Space>
                {notification.patient.internal_data.flagged && <PushpinOutlined style={{marginLeft: 0}}/>}
                {notification.notifications.length > 0 && <Badge style={{backgroundColor: colors[notification.level]}}
                                                                 count={notification.notifications.length}
                                                                 size={"small"}/>}
            </Space>
        </div>
    </span>

    return <SubMenu key={notification.patient.oid} icon={false} onTitleClick={onTitleClick}
                    title={title} {...props}>
        {notification.notifications.map((message, j) =>
            <Item key={`${notification.patient.oid}-${j}`} danger={message.danger}>
                <Link to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
                    {message.message}
                </Link>
            </Item>
        )}
    </SubMenu>
}
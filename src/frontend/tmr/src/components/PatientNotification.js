import React from 'react';
import {Badge, Collapse, List, Space} from "antd";

import {PushpinOutlined, UserOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";
import Moment from "react-moment";

const {Panel} = Collapse;

export const PatientNotification = ({notification}) => {
    const colors = {
        1: '#f5222d',
        2: '#fa541c',
        3: '#52c41a',
    }

    return <Panel key={notification.patient.oid} showArrow={false} header={<div style={{
        display: "flex",
        flexFlow: "column nowrap",
        alignItems: "flex-start",
    }}>
        <div><UserOutlined/>{notification.patient.name}</div>
        <div style={{textOverflow: "ellipsis", fontSize: "10px"}}>{notification.preview}</div>
    </div>} extra={<div style={{
        display: "flex",
        flexFlow: "column nowrap",
        alignItems: "flex-end",
    }}>
        <Moment style={{display: "block"}} date={notification.at || notification.patient.arrival} format={'hh:mm'}/>
        <Space>
            {notification.patient.flagged && <PushpinOutlined style={{marginLeft: 0}}/>}
            {notification.notifications.length > 0 &&
                <Badge style={{backgroundColor: colors[notification.level]}}
                       count={notification.notifications.length} size={"small"}/>}
        </Space>
    </div>
    }>
        <List>
            {notification.notifications.map((message, j) =>
                <Link key={`${notification.patient.oid}-${j}`}
                      to={`#info#${notification.patient.oid}#${message.type}#${message.static_id}`}>
                    <span style={message.danger ? {color: "red"} : {}}>{message.message}</span>
                </Link>
            )}
        </List>
    </Panel>
}
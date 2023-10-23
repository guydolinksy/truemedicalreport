import React, {useContext} from 'react';
import {RelativeTime} from "./RelativeTime";

import {Space, Tooltip} from "antd";
import {CheckCircleOutlined, RedoOutlined} from '@ant-design/icons';
import moment from "moment";
import {patientDataContext} from "./PatientBase";

export const PatientWatching = () => {
    const {value, update} = useContext(patientDataContext.context);
    return Object.values(value.watching).filter(w => w.triggered).length > 0 &&
        <div>
            <div style={{
                direction: "rtl",
                userSelect: "none",
                padding: "8px 12px",
                cursor: "pointer",
                height: 82,
                overflowY: "overlay"
            }}>
                {Object.entries(value.watching).filter(([key, watch]) => watch.triggered).map(([key, watch]) => {
                    return <div key={key} style={{
                        display: "flex",
                        flexFlow: "row nowrap",
                        justifyContent: "space-between",
                        alignItems: "baseline"
                    }}>
                        <div style={{
                            display: "flex",
                            flexFlow: "row nowrap",
                            whiteSpace: "nowrap",
                            overflowX: "hidden"
                        }}><Space>
                            <Tooltip overlay={'אישור צפייה'}>
                                <span onClick={e => {
                                    update(['watching', key], {
                                        watched: false,
                                        triggered: false,
                                        updated_at: moment().toISOString()
                                    }, 'WatchKey');
                                    e.stopPropagation();
                                }}><CheckCircleOutlined className={'ok-text'}/></span>
                            </Tooltip>
                            <Tooltip overlay={'המשך מעקב'}>
                                <span onClick={e => {
                                    update(['watching', key], {
                                        watched: true,
                                        triggered: false,
                                        updated_at: moment().toISOString()
                                    }, 'WatchKey')
                                    e.stopPropagation();
                                }}><RedoOutlined className={'error-text'}/></span>
                            </Tooltip>
                            {watch.message}</Space>
                        </div>
                        {<RelativeTime style={{fontSize: 12}} date={watch.updated_at}/>}
                    </div>
                })}
            </div>
        </div>
}
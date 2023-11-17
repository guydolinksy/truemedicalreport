import {Card} from 'antd';
import React from 'react';

export const PanelPlugin = ({config}) => {
    return <Card title={config.title} style={{flex: 1, maxWidth: 500, minWidth: 300, ...config.customStyle}}>
        <iframe style={{border: "none", width: "100%", height: "250px"}} title={config.title} src={config.url}/>
    </Card>

}
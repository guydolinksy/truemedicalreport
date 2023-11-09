import React, {useContext} from "react"
import {useNavigate} from "react-router-dom";
import {loginContext} from "./LoginContext";
import {Button, Layout, Space} from 'antd';
import {modeContext} from "../contexts/ModeContext";


const {Content} = Layout;

const Action = ({name, url}) => {
    const navigate = useNavigate();
    return <Button style={{
        height: 200,
        width: 200,
        whiteSpace: 'wrap',
        textAlign: 'center',
        fontSize: '2.5rem',
        display: 'flex',
        alignItems: 'center'
    }} onClick={() => navigate(url)}>
        {name}
    </Button>
}
export const Home = () => {
    const {userSettings} = useContext(loginContext);

    return <Content style={{
        padding: 'max(32px, min(8vw, 8vh))',
        overflowY: 'auto',
        textAlign: 'center',
    }}>
        <h1 style={{textAlign: 'center'}}>ברוך.ה הבא.ה לתמ"ר (תמונת מצב רפואית),<br/>מהיכן תרצה.י להתחיל?</h1>
        <Space style={{justifyContent: 'center'}} wrap>
            {(userSettings.actions || []).map(action => <Action {...action}/>)}
        </Space>
    </Content>
}


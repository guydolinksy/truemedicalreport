import React, {useContext} from "react"
import {useNavigate} from "react-router-dom";
import {loginContext} from "./LoginContext";
import {Button, Layout, Space} from 'antd';
import {modeContext} from "../contexts/ModeContext";


const {Content} = Layout;
const sortTypesOfDisplay = (displayData) => {
    const returnObject = {
        departments: [],
        views: [],
        favorites: []
    }
    displayData.forEach(obj => {
        switch (obj.type) {
            case ("Department"):
                returnObject.departments.push(obj)
                break
            case ("View"):
                returnObject.views.push(obj)
                break
            case ("Favorite"):
                returnObject.favorites.push(obj)
                break
        }
    })
    return returnObject
}
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
    const {isLandscape} = useContext(modeContext);

    return <Content>
        <div style={{display: "flex", flexDirection: "row", alignItems: "center", height: '100%'}}>
            <div style={{display: "flex", flexDirection: "column", alignItems: "center", flex: 1}}>
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    maxWidth: isLandscape ? 'min(80vw, 1200px)' : 'min(80vw, 1200px)',
                    maxHeight: isLandscape ? 'min(80vh, 1200px)' : 'min(80vh, 1200px)',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: 16,
                }}>
                    <h1 style={{textAlign: 'center'}}>ברוך.ה הבא.ה לתמ"ר (תמונת מצב רפואית),<br/> מהיכן תרצה.י להתחיל?
                    </h1>
                    <div style={{overflowY: 'auto'}}>
                        <Space style={{justifyContent: 'center'}} wrap>
                            {(userSettings.actions || []).map(action => <Action {...action}/>)}
                        </Space>
                    </div>
                </div>
            </div>
        </div>
    </Content>
}


import React, {useContext} from "react"
import {Card, Space, Layout} from 'antd'
import {CloseOutlined, HeartTwoTone} from '@ant-design/icons';
import {useNavigate} from "react-router-dom";
import {viewsDataContext} from "../contexts/ViewsDataContext";
import {loginContext} from "./LoginContext";
import {modeContext} from "../contexts/ModeContext";

const {Content} = Layout;

export const View = ({view}) => {
    const navigate = useNavigate()
    const {name, patients_count, key, type, modes} = view;
    return <Card
        extra={type === "Favorite"
            ? <CloseOutlined onClick={() => alert("Removed")}/>
            : <HeartTwoTone twoToneColor="#eb2f96" onClick={() => alert("Saved")}/>}
        className={'main-display-item'}
        size={'small'}
        title={name}
        key={key}
        style={{width: 200, display: 'flex', flexDirection: 'column'}}
        bodyStyle={{display: 'flex', flexDirection: 'column', overflowY: 'hidden'}}
        actions={modes.map(mode => <span
            onClick={() => navigate(`/views/${type}/${key}/modes/${mode.key}`)}>{mode.name}</span>)}
    >
        <div onClick={() => navigate(`/views/${type}/${key}`)}>
            <div>מספר מטופלים: {patients_count}</div>
        </div>
    </Card>
}
export const ViewsSelection = ({options}) => {
    return <Space style={{rowGap: 16}} wrap>
        {options.map(item => <View key={item.key} view={item}/>)}
    </Space>
}

export const Views = () => {
    const {value} = useContext(viewsDataContext.context);
    const {isLandscape} = useContext(modeContext);
    const {userSettings} = useContext(loginContext);
    const departments = value.getViews.views.filter(view => view.type === 'department');
    const views = value.getViews.views.filter(view => view.type === 'custom');
    const favorites = value.getViews.views.filter(view => (userSettings.favoriteViews || []).includes(view.key));
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
                    <h1 style={{textAlign: 'center'}}>בחר.י תצוגה מבין האפשרויות הבאות:</h1>
                    <div style={{overflowY: 'auto', textAlign: 'center'}}>
                        <Space direction={'vertical'}>
                            <ViewsSelection options={favorites}/>
                            <ViewsSelection options={departments}/>
                            <ViewsSelection options={views}/>
                        </Space>
                    </div>
                </div>
            </div>
        </div>
    </Content>
}


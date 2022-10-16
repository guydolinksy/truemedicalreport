import {Menu} from "antd";
import {SettingOutlined} from "@ant-design/icons";
import React, {useContext} from "react";
import {useLocation, useNavigate} from "react-router";
import {loginContext} from "./LoginContext";


export const MainMenu = () => {
    const {user} = useContext(loginContext);
    const navigate = useNavigate();
    const {pathname} = useLocation();
    return <div style={{display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
        <Menu theme={"dark"} mode={"horizontal"} selectedKeys={pathname.split('/').slice(1, 2)}
              items={[{key: '', label: 'תמ״ר'}]} onClick={() => navigate('/')} style={{flex: "1 0 0px"}}/>
        <Menu theme={"dark"} mode={"horizontal"} selectedKeys={pathname.split('/').slice(1, 2)}
              items={(user && user.admin) ? [{key: 'settings', label: <SettingOutlined/>}] : []}
              onClick={() => navigate('/settings')}/>
    </div>
}
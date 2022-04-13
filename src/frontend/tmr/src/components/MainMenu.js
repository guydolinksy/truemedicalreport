import {Menu} from "antd";
import {Link} from "react-router-dom";
import {SettingOutlined} from "@ant-design/icons";
import React, {useContext} from "react";
import {useLocation} from "react-router";
import {loginContext} from "./LoginContext";

const {Item} = Menu;

export const MainMenu = () => {
    const {user} = useContext(loginContext);
    const {pathname} = useLocation();
    return <div style={{display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
        <Menu mode={"horizontal"} selectedKeys={pathname.split('/').slice(1, 2)}>
            <Item key={''}><Link to={'/'}>תמ״ר</Link></Item>
        </Menu>
        <Menu mode={"horizontal"} selectedKeys={pathname.split('/').slice(1, 2)}>
            {user && user.admin && <Item key={'settings'}><Link to={'/settings'}><SettingOutlined/></Link></Item>}
        </Menu>
    </div>
}
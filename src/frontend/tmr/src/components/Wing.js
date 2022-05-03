import React, {useCallback, useContext, useEffect, useState} from 'react';
import {Avatar, Badge, Card, Col, Input, Layout, Menu, Row, Spin} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "./DataContext";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faBuilding, faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import debounce from 'lodash/debounce';
import {Highlighter} from './Highlighter'
import {Bed} from "./Bed";
import {PatientNotification} from "./PatientNotification";
import {SettingOutlined} from "@ant-design/icons";

const {Search} = Input;
const {Content, Sider} = Layout;
const {SubMenu, Item} = Menu;
const wingDataContext = createContext(null);
const notificationsDataContext = createContext(null);

const highlighter = new Highlighter('root');

const WingNotificationsInner = ({wingName}) => {
    const navigate = useNavigate();
    const [openKeys, setOpenKeys] = useState([]);
    const [search, setSearch] = useState('');
    const {value, lastMessage} = useContext(notificationsDataContext.context);

    useEffect(() => {
        highlighter.apply(search)
    }, [search]);

    useEffect(() => {
        if (!lastMessage)
            return;
        setOpenKeys(prevState => prevState.concat(...JSON.parse(lastMessage.data).openKeys || []));
    }, [lastMessage]);

    const toggleOpen = useCallback(notification => {
        if (openKeys.includes(notification.patient.oid))
            navigate(`#highlight#${notification.patient.oid}#close`)
        else
            navigate(`#highlight#${notification.patient.oid}#open`)
    }, [openKeys, navigate]);

    return <div style={{
        display: "flex",
        flexDirection: "column",
        height: '100vh',
        overflowY: "hidden",
        justifyContent: "space-between",
    }}>
        <div style={{
            display: "flex",
            flexDirection: "column",
            flex: 1,
            overflowY: "hidden",
        }}>
            <Menu selectable={false} theme={"dark"} mode={"inline"} style={{userSelect: "none", overflowY: "scroll"}}
                  expandIcon={null && <SettingOutlined/>}>
                <SubMenu key={'wing'} icon={<FontAwesomeIcon icon={faBuilding}/>} title={wingName}>
                </SubMenu>
            </Menu>
            <Menu selectable={false} theme={"dark"} mode={"inline"}
                  style={{userSelect: "none", overflowY: "scroll"}}
                  openKeys={openKeys} onOpenChange={setOpenKeys}>
                <Item key={'search'}>
                    <Search allowClear onChange={debounce(e => setSearch(e.target.value), 300)} placeholder={'חיפוש'}/>
                </Item>
                {value.map((notification) => <PatientNotification key={notification.patient.oid}
                                                                  notification={notification}
                                                                  onTitleClick={() => toggleOpen(notification)}/>)}
            </Menu>
        </div>
        <Menu selectable={false} theme={"dark"} mode={"inline"} style={{userSelect: "none"}}>
            <Item key={'exit'} icon={<FontAwesomeIcon icon={faRightFromBracket}/>}>
                <Link to={'/'}>חזרה למחלקה</Link>
            </Item>
        </Menu>
    </div>
};
const WingNotifications = ({department, wing, wingName, onError}) => {
    const notificationsURI = `/api/departments/${department}/wings/${wing}/notifications`;

    return <notificationsDataContext.Provider url={notificationsURI} defaultValue={[]} onError={onError}>
        {({loading}) => loading ? <Spin/> : <WingNotificationsInner wingName={wingName}/>}
    </notificationsDataContext.Provider>;
}
export const WingInner = ({department, wing, onError}) => {
    const navigate = useNavigate();
    const {value, flush} = useContext(wingDataContext.context);

    const onInfoError = useCallback(() => {
        flush()
        navigate('#')
    }, [navigate, flush]);

    const unassignedPatients = value.patients.filter(({oid, external_data}) => !external_data.admission.bed);

    return <Layout>
        <Sider breakpoint={"lg"} width={350}>
            <WingNotifications department={department} wing={wing} wingName={value.details.name} onError={onError}/>
        </Sider>
        <Content style={{backgroundColor: "#000d17", overflowY: "scroll"}}>
            <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                {(value.details.beds ? [<Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
                    {(value.details.rows || []).map((row, i) =>
                        <Row key={i} style={row} wrap={false}>
                            {(value.details.columns || []).map((column, j) =>
                                value.details.beds[i][j] === null ? <div key={`filler-${j}`} style={column}/> :
                                    <Bed key={`bed-${value.details.beds[i][j]}`} style={column} admission={{
                                        department: department,
                                        wing: wing,
                                        bed: value.details.beds[i][j]
                                    }} onError={flush}/>
                            )}
                        </Row>
                    )}
                </Card>] : []).concat(
                    <Card key={'overflow'} style={{width: '100%', flex: '1'}}>
                        <div style={{
                            display: "grid",
                            gridGap: 16,
                            gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))"
                        }}>
                            {unassignedPatients.map(patient =>
                                <Patient key={patient.oid} patient={patient.oid}
                                         style={{flex: '1', minWidth: 300}} onError={flush}/>)}
                            <Patient patient={null} avatar={null} style={{flex: '1', minWidth: 300}}/>
                        </div>
                    </Card>)}
            </Col>
        </Content>
        <PatientInfo onError={onInfoError}/>
    </Layout>
};

export const Wing = ({department, wing, onError}) => {
    const uri = `/api/departments/${department}/wings/${wing}`;

    return <wingDataContext.Provider url={uri} defaultValue={{patients: [], details: {}}} onError={onError}>
        {({loading}) => loading ? <Spin/> : <WingInner department={department} wing={wing} onError={onError}/>}
    </wingDataContext.Provider>
}

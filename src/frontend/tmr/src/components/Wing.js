import React, {useContext, useEffect, useState} from 'react';
import {Card, Col, Input, Layout, Menu, Row, Spin} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "./DataContext";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faBuilding, faRightFromBracket,} from "@fortawesome/free-solid-svg-icons";
import {UserOutlined} from "@ant-design/icons";
import {useNavigate} from "react-router";
import {PatientInfo} from "./PatientInfo";
import debounce from 'lodash/debounce';
import {Highlighter} from './Highlighter'
import {Bed} from "./Bed";

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
    const {getData, lastMessage} = useContext(notificationsDataContext.context);

    useEffect(() => {
        highlighter.apply(search)
    }, [search]);

    useEffect(() => {
        if (!lastMessage)
            return;
        setOpenKeys(prevState => prevState.concat(...JSON.parse(lastMessage.data).openKeys || []));
    }, [lastMessage]);

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
            <Menu selectable={false} theme={"dark"} mode={"inline"}
                  style={{userSelect: "none"}}>
                <Item key={'wing'} icon={<FontAwesomeIcon icon={faBuilding}/>}>
                    {wingName}
                </Item>
            </Menu>
            <Menu selectable={false} theme={"dark"} mode={"inline"}
                  style={{userSelect: "none", overflowY: "scroll"}}
                  openKeys={openKeys} onOpenChange={setOpenKeys}>
                <Item key={'search'}>
                    <Search allowClear onChange={debounce(e => setSearch(e.target.value), 300)} placeholder={'חיפוש'}/>
                </Item>
                {getData([]).map((notification, i) =>
                    <SubMenu key={notification.patient.oid} title={notification.patient.name}
                             icon={<UserOutlined/>}
                             style={notification.danger ? {color: '#ff4d4f'} : {}}
                             onTitleClick={() => {
                                 if (openKeys.includes(notification.patient.oid))
                                     navigate(`#highlight#${notification.patient.oid}#close`)
                                 else
                                     navigate(`#highlight#${notification.patient.oid}#open`)
                             }}>
                        {notification.messages.map((message, j) =>
                            <Item key={`${notification.patient.oid}-${j}`} danger={message.danger}>
                                <Link
                                    to={`#info#${notification.patient.oid}#${message.section || 'labs'}#lab-${message.id || j}`}>
                                    {message.content}
                                </Link>
                            </Item>
                        )}
                    </SubMenu>
                )}
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

    return <notificationsDataContext.Provider url={notificationsURI}
                                              updateURL={notificationsURI}
                                              socketURL={notificationsURI}
                                              defaultValue={[]}
                                              onError={onError}>
        {({loadingData}) => loadingData ? <Spin/> : <WingNotificationsInner wingName={wingName}/>}
    </notificationsDataContext.Provider>;
}

export const Wing = ({department, wing, onError}) => {
    const uri = `/api/departments/${department}/wings/${wing}`;

    return <wingDataContext.Provider url={uri} defaultValue={{patients: [], details: {}}} onError={onError}>
        {({loadingData, getData, flushData}) => {
            const assignedPatients = (getData(['patients']) || []).filter(({oid, admission}) => admission.bed)
            const title = <span>מטופלים במיטות: {assignedPatients.length}</span>
            const unassignedPatients = (getData(['patients']) || []).filter(({oid, admission}) => !admission.bed)
            const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>

            const details = (getData(['details']) || []);

            return <Layout>
                <Sider breakpoint={"lg"} width={230}>
                    <WingNotifications department={department} wing={wing} wingName={details.name} onError={onError}/>
                </Sider>
                <Content style={{backgroundColor: "#000d17", overflowY: "scroll"}}>
                    <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                        {loadingData ? <Spin/> :
                            (details.beds ? [<Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
                                {(details.rows || []).map((row, i) =>
                                    <Row key={i} style={row} wrap={false}>
                                        {(details.columns || []).map((column, j) =>
                                            details.beds[i][j] === null ? <div key={j} style={column}/> :
                                                <Bed key={j} style={column} admission={{
                                                    department: department,
                                                    wing: wing,
                                                    bed: details.beds[i][j]
                                                }} onError={() => flushData()}/>
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
                                                     style={{flex: '1', minWidth: 300}}/>)}
                                    </div>
                                </Card>)}
                    </Col>
                </Content>
                <PatientInfo/>
            </Layout>
        }}
    </wingDataContext.Provider>
}

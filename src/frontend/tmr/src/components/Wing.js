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
                <Item>
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
const WingNotifications = ({wing, wingName}) => {
    const notificationsURI = `/api/wings/${wing}/notifications`;

    return <notificationsDataContext.Provider url={notificationsURI}
                                              updateURL={notificationsURI}
                                              socketURL={notificationsURI}
                                              defaultValue={[]}>
        {({loadingData}) => loadingData ? <Spin/> : <WingNotificationsInner wingName={wingName}/>}
    </notificationsDataContext.Provider>;
}

export const Wing = ({id}) => {
    const uri = `/api/wings/${id}`;

    return <wingDataContext.Provider url={uri} updateURL={uri} socketURL={uri}
                                     defaultValue={{patients_beds: [], structure: {}}}>
        {({loadingData, getData}) => {
            const assignedPatients = (getData(['patients_beds']) || []).filter(({oid, bed}) => bed)
            const title = <span>מטופלים במיטות: {assignedPatients.length}</span>
            const unassignedPatients = (getData(['patients_beds']) || []).filter(({oid, bed}) => !bed)
            const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>

            const structure = (getData(['structure']) || []);

            return <Layout>
                <Sider breakpoint={"lg"} width={230}>
                    <WingNotifications wing={id} wingName={structure.name}/>
                </Sider>
                <Content style={{backgroundColor: "#000d17", overflowY: "scroll"}}>
                    <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                        {loadingData ? <Spin/> :
                            (structure.beds ? [<Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
                                {(structure.rows || []).map((row, i) =>
                                    <Row key={i} style={row} wrap={false}>
                                        {(structure.columns || []).map((column, j) =>
                                            structure.beds[i][j] === null ? <div key={j} style={column}/> :
                                                <Patient key={j} style={column} bed={structure.beds[i][j]}/>
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
                                            <Patient key={patient.oid} id={patient.oid}
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

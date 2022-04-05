import React, {useState} from 'react';
import {Card, Col, Menu, Row, Spin} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "./DataContext";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faBuilding,
    faRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";
import {Layout} from "antd";
import {UserOutlined} from "@ant-design/icons";
import {useNavigate} from "react-router";

const {Content, Sider} = Layout;
const {SubMenu, ItemGroup, Item} = Menu;
const wingDataContext = createContext(null);
const notificationsDataContext = createContext(null);

export const Wing = ({id}) => {
    const uri = `/api/wings/${id}`;
    const notificationsURI = `/api/wings/${id}/notifications`;
    const navigate = useNavigate();
    const [openKeys, setOpenKeys] = useState([]);

    return <wingDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount
                                     defaultValue={{patients_beds: [], structure: {}}}>
        {({loadingData, getData}) => {
            const assignedPatients = (getData(['patients_beds']) || []).filter(({oid, bed}) => bed)
            const title = <span>מטופלים במיטות: {assignedPatients.length}</span>
            const unassignedPatients = (getData(['patients_beds']) || []).filter(({oid, bed}) => !bed)
            const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>

            const structure = (getData(['structure']) || []);

            return loadingData ? <Spin/> : <Layout>
                <Sider breakpoint={"lg"} width={230}>
                    <notificationsDataContext.Provider url={notificationsURI}
                                                       updateURL={notificationsURI}
                                                       socketURL={notificationsURI} fetchOnMount
                                                       defaultValue={[]}>
                        {({loadingData, getData}) => loadingData ? <Spin/> :
                            <div style={{
                                display: "flex",
                                flexDirection: "column",
                                height: '100vh',
                                justifyContent: "space-between"
                            }}>
                                <Menu selectable={false} theme={"dark"} mode={"inline"} style={{userSelect: "none"}}
                                      openKeys={openKeys} onOpenChange={setOpenKeys}>
                                    <Item key={'wing'} icon={<FontAwesomeIcon icon={faBuilding}/>}>
                                        {structure.name}
                                    </Item>
                                    {getData([]).map((notification, i) =>
                                        <SubMenu key={notification.patient.oid} title={notification.patient.name}
                                                 icon={<UserOutlined/>}
                                                 style={notification.danger ? {color: '#ff4d4f'} : {}}
                                                 onTitleClick={() => {
                                                     if (openKeys.includes(notification.patient.oid))
                                                         navigate(`#!${notification.patient.oid}`)
                                                     else
                                                         navigate(`#${notification.patient.oid}`)
                                                 }}>
                                            {notification.messages.map((message, j) =>
                                                <Item key={j} danger={message.danger}>{message.content}</Item>
                                            )}
                                        </SubMenu>
                                    )}
                                </Menu>
                                <Menu selectable={false} theme={"dark"} mode={"inline"} style={{userSelect: "none"}}>
                                    <Item key={'exit'} icon={<FontAwesomeIcon icon={faRightFromBracket}/>}>
                                        <Link to={'/'}>חזרה למחלקה</Link>
                                    </Item>
                                </Menu>
                            </div>}
                    </notificationsDataContext.Provider>
                </Sider>
                <Content>
                    <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                        {structure.beds && <Card style={{width: '100%', marginBottom: 16}} bodyStyle={{rowGap: 16}}>
                            {(structure.rows || []).map((row, i) =>
                                <Row key={i} style={row} wrap={false}>
                                    {(structure.columns || []).map((column, j) =>
                                        structure.beds[i][j] === null ? <div key={j} style={column}/> :
                                            <Patient key={j} style={column} bed={structure.beds[i][j]}/>
                                    )}
                                </Row>
                            )}
                        </Card>}
                        <Card style={{width: '100%', flex: '1'}}>
                            <Row style={{rowGap: 16, columnGap: 16}}>
                                {unassignedPatients.map(patient =>
                                    <Patient key={patient.oid} id={patient.oid} style={{flex: '1', minWidth: 300}}/>)}
                            </Row>
                        </Card>
                    </Col>
                </Content></Layout>
        }}
    </wingDataContext.Provider>
}

import React from 'react';
import {Card, Col, Row, Spin} from 'antd';
import {Patient} from "./Patient";
import {createContext} from "./DataContext";
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";

const wingDataContext = createContext(null);
const notificationsDataContext = createContext(null);

export const Wing = ({id}) => {
    const uri = `/api/wings/${id}`;
    const notificationsURI = `/api/wings/${id}/notifications`;
    return <wingDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount
                                     defaultValue={{patients: [], structure: {blocks: []}}}>
        {({loadingData, getData}) => {
            const assignedPatients = (getData(['patients']) || []).filter(({id, bed}) => bed)
            const title = <span>מטופלים במיטות: {assignedPatients.length}</span>
            const unassignedPatients = (getData(['patients']) || []).filter(({id, bed}) => !bed)
            const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>

            const structure = (getData(['structure']) || []);
            return loadingData ? <Spin/> : <Col style={{padding: 16, height: '100%', display: 'flex', flexFlow: 'column nowrap'}}>
                <Row gutter={16} style={{marginBottom: 16}}>
                    <Col span={4}>
                        <Card title={structure.name} size={"small"} bordered={false}
                              style={{width: '100%', height: '100%'}}
                              extra={<Link to={'/'}><FontAwesomeIcon icon={faRightFromBracket}/></Link>}>
                            <notificationsDataContext.Provider url={notificationsURI} updateURL={notificationsURI}
                                                               socketURL={notificationsURI} fetchOnMount
                                                               defaultValue={[]}>
                                {({loadingData, getData}) => loadingData ? <Spin/> :
                                    getData([]).map((notification, i) =>
                                        <Card key={i} title={notification.title} size={"small"}>
                                            {notification.content}
                                        </Card>)}
                            </notificationsDataContext.Provider>
                        </Card>
                    </Col>
                    <Col span={20}>
                        <Card style={{width: '100%', height: '100%'}}>
                            {(structure.rows || []).map((row, i) =>
                                <Row key={i} style={row} wrap={false}>
                                    {(structure.columns || []).map((column, j) =>
                                        structure.beds[i][j] === 0 ? <div key={j} style={column}/> :
                                            <Patient key={j} style={column} bed={structure.beds[i][j]}/>
                                    )}
                                </Row>
                            )}
                        </Card>
                    </Col>
                </Row>
                <Card style={{width: '100%', flex: '1'}}>
                    <Row gutter={4}>
                        {unassignedPatients.map(patient =>
                                <Patient key={patient['_id']['$oid']} id={patient['_id']['$oid']} style={{flex: '1', minWidth: 300}}/>)}
                    </Row>
                </Card>
            </Col>
        }}
    </wingDataContext.Provider>
}

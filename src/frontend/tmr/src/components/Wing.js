import React, {useEffect, useState} from 'react';
import Axios from 'axios';
import {Row, Col, Card, Spin} from 'antd';
import {Patient} from "./Patient";
import {useNavigate} from 'react-router';
import {createContext} from "./DataContext";

const wingDataContext = createContext(null);

export const Wing = ({id}) => {
    const uri = `/api/wings/${id}`;
    return <wingDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount
                                     defaultValue={{patients: [], structure: {blocks: []}}}>
        {({loadingData, getData}) => {
            const assignedPatients = (getData(['patients_beds']) || []).filter(({id, bed}) => bed)
            const title = <span>{getData(['structure', 'name'])} מטופלים במיטות: {assignedPatients.length}</span>
            const unassignedPatients = (getData(['patients_beds']) || []).filter(({id, bed}) => !bed)
            const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>

            const blocks = (getData(['structure', 'blocks']) || []);
            return loadingData ? <Spin/> : <Col style={{padding: 16}}>
                {blocks.length > 0 &&
                    <Card bordered={false} bodyStyle={{backgroundColor: "#f6ffed"}} title={title}>
                        <Row gutter={16} style={{marginBottom: 16}}>{blocks.map((block, i) =>
                            <Col key={i} span={24 / blocks.length}>
                                <Card bordered={false}>
                                    <Row gutter={16}>{block.sides.map((side, j, a) =>
                                        <Col key={j} span={24 / a.length}>{side.beds.map((bed, k) =>
                                            <Patient key={k} bed={bed}/>)}
                                        </Col>)}
                                    </Row>
                                </Card>
                            </Col>)}
                        </Row>
                    </Card>}
                <Card bordered={false} bodyStyle={{backgroundColor: "#f9f0ff"}} title={overflowTitle}>
                    <Row gutter={16}>
                        {unassignedPatients.map((patient, i) =>
                            <Col key={patient['oid']} flex={"1 1 300"}>
                                <Patient id={patient['oid']}/>
                            </Col>)}
                    </Row>
                </Card>
            </Col>
        }}
    </wingDataContext.Provider>
}

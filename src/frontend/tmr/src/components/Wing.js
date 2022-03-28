import React, {useEffect, useState} from 'react';
import Axios from 'axios';
import {Row, Col, Card} from 'antd';
import {Patient} from "./Patient";
import {useNavigate} from 'react-router';

export const Wing = ({id}) => {
    const [wingData, setWingData] = useState({patients: [], structure: {blocks: []}});
    const navigate = useNavigate();

    useEffect(() => {
        Axios.get(`/api/wing/${id}`).then(response => {
            setWingData(response.data);
        }).catch(error => {
            navigate('/')
            console.error(error)
        })
    }, [id, navigate]);
    const title = <span>מטופלים במיטות: {wingData.patients.filter(({id, bed}) => bed).length}</span>
    const unassignedPatients = wingData.patients.filter(({id, bed}) => !bed)
    const overflowTitle = <span>מטופלים ללא מיטה: {unassignedPatients.length}</span>
    return <Col style={{padding: 16}}>
        {wingData.structure.blocks.length > 0 &&
            <Card bordered={false} bodyStyle={{backgroundColor: "#f6ffed"}} title={title}>
                <Row gutter={16} style={{marginBottom: 16}}>{wingData.structure.blocks.map((block, i) =>
                    <Col key={i} span={24 / wingData.structure.blocks.length}>
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
                    <Col key={patient['_id']['$oid']} style={{width: "20%"}}><Patient id={patient['_id']['$oid']}/></Col>)}
            </Row>
        </Card>

    </Col>
}
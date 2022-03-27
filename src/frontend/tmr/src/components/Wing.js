import React, {useEffect, useState} from 'react';
import Axios from 'axios';
import {Row, Col, Card} from 'antd';
import {Patient} from "./Patient";
import {useNavigate} from 'react-router';

export const Wing = ({id}) => {
    const [wingData, setWingData] = useState({patients: [], blocks: []});
    const navigate = useNavigate();

    useEffect(() => {
        Axios.get(`/api/wing/${id}`).then(response => {
            setWingData(response.data);
        }).catch(error => {
            navigate('/')
            console.error(error)
        })
    }, [id, navigate]);

    return <Col style={{padding: 16}}>
        <Row gutter={16} style={{marginBottom: 16}}>{wingData.blocks.map((block, i) =>
            <Col key={i} span={24 / wingData.blocks.length}>
                <Card bordered={false}>
                    <Row gutter={16}>{block.sides.map((side, j, a) =>
                        <Col key={j} span={24 / a.length}>{side.beds.map((bed, k) =>
                            <Patient key={k} bed={bed}/>)}
                        </Col>)}
                    </Row>
                </Card>
            </Col>)}
        </Row>
        <Card bordered={false} bodyStyle={{backgroundColor: "#f9f0ff"}} title={wingData.patients.length}>
            <Row gutter={16}>
                {wingData.patients.filter(({id, bed}) => !bed).map(({id}, i) =>
                    <Col key={id} span={4}><Patient id={id}/></Col>)}
            </Row>
        </Card>

    </Col>
}
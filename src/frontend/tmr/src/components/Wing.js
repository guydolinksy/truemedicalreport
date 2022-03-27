import React from 'react';
import Axios from 'axios';
import {Row, Col, Card} from 'antd';
import {Patient} from "./Patient";


export const Wing = ({id}) => {
    const blocks = [
        {
            name: 'מסדרון ימין',
            sides: [
                {name: 'צד ימין', beds: [1, 2, 3, 4]},
                {name: 'צד שמאל', beds: [5, 6, 7, 8]},
            ]
        }, {
            name: 'מסדרון שמאל',
            sides: [
                {name: 'צד ימין', beds: [9, 10, 11, 12]},
                {name: 'צד שמאל', beds: [13, 14, 15, 16]},
            ]
        }
    ];
    const unassignedPatients = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];

    let patientCount = "N/A";
    Axios.get(`/api/wing/${id}/patient_count`).then(response => {
        patientCount = response;
    }).catch(error => {
        console.error(error)
    })

    return <Col style={{padding: 16}}>
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
        <Card bordered={false} bodyStyle={{backgroundColor: "#f9f0ff"}} title={patientCount}>
            <Row gutter={16}>
                {unassignedPatients.map((patientId, i) =>
                    <Col key={i} span={4}><Patient id={patientId}/></Col>)}
            </Row>
        </Card>

    </Col>
}
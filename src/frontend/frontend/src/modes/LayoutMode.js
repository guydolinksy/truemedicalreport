import {Bed} from "../components/Bed";
import {MIN_WIDTH, Patient} from "../components/card/Patient";
import React, {useContext, useMemo} from "react";
import {Card, Empty, Row, Space, Spin} from 'antd';
import {useParams} from 'react-router-dom';
import {viewsContext} from "../contexts/ViewsContext";
import {wingDataContext} from '../contexts/WingContext';

export const LayoutMode = ({onError}) => {
    const {value: viewsValue} = useContext(viewsContext.context)
    const {view} = useParams();

    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);

    const unassignedPatients = useMemo(() => {
        return value.getPatients.patients.filter(patient => patient.admission.bed === null)
    }, [value]);
    return <wingDataContext.Provider url={`/api/departments/${curView.department_id}/wings/${curView.wing_id}`}
                                     defaultValue={{}} onError={onError}>
        {({loading, value}) => loading ? <Spin/> : <>
            <Card key={'grid'} style={{width: '100%', marginBottom: 16}}>
                {(value.getWings.wings[0].details.rows || []).map((row, i) => <Row key={i} style={row} wrap={false}>
                    {(value.getWings.wings[0].details.columns || []).map((column, j) =>
                        value.getWings.wings[0].details.beds[i][j] === null ?
                            <div key={`filler-${j}`} style={column}/> :
                            <Bed key={`bed-${value.getWings.wings[0].details.beds[i][j]}`} style={column} admission={{
                                department_id: curView.department_id,
                                wing_id: curView.wing_id,
                                bed: value.getWings.wings[0].details.beds[i][j]
                            }} onError={onError}/>
                    )}
                </Row>)}
            </Card>,
            <Card key={'overflow'} style={{width: '100%', flex: '1 0 300px', overflowY: 'auto'}}>
                <Space wrap style={{
                    justifyContent: 'center',
                    display: "grid",
                    gridGap: 16,
                    gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
                }}>
                    {unassignedPatients.length ? unassignedPatients.map(
                        ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}} onError={onError}/>
                    ) : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>}
                </Space>
            </Card>
        </>}
    </wingDataContext.Provider>
}
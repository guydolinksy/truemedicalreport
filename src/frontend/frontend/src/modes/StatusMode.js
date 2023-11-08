import {MIN_WIDTH, Patient} from "../components/card/Patient";
import React, {useContext, useMemo} from "react";
import {Card, Spin} from 'antd';
import {useParams} from 'react-router-dom'
import {wingDataContext} from '../contexts/WingContext';
import {viewsContext} from "../contexts/ViewsContext";

export const StatusModeInner = ({patients, mci}) => {
    const needAttention = patients.filter(
        (patient) => patient.watching.find(watchKey => watchKey.triggered)
    )
    const unassigned = patients.filter(
        patient => !needAttention.find(({oid}) => oid === patient.oid) && patient.status === 'unassigned'
    )
    const undecided = patients.filter(
        patient => !needAttention.find(({oid}) => oid === patient.oid) && patient.status === 'undecided'
    )
    const decided = patients.filter(
        patient => !needAttention.find(({oid}) => oid === patient.oid) && patient.status === 'decided'
    )
    return <>
        <Card size={'small'} key={'needAttention'} style={{width: '100%', marginBottom: 16}}
              title={`ממתינים עבורך (${needAttention.length})`}
              bodyStyle={{
                  display: !needAttention.length ? 'none' : "grid",
                  gridGap: 16,
                  gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
              }}>
            {needAttention.length > 0 && needAttention.map(
                ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}} showAttention/>
            )}
        </Card>
        <Card size={'small'} key={'unassigned'} style={{width: '100%', marginBottom: 16}}
              title={`ללא שיוך לרופא.ה (${unassigned.length})`}
              bodyStyle={{
                  display: !unassigned.length ? 'none' : "grid",
                  gridGap: 16,
                  gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
              }}>
            {unassigned.length > 0 && unassigned.map(
                ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}}/>
            )}
        </Card>
        <Card size={'small'} key={'undecided'} style={{width: '100%', marginBottom: 16}}
              title={`ללא החלטה על יעד (${undecided.length})`}
              bodyStyle={{
                  display: !undecided.length ? 'none' : "grid",
                  gridGap: 16,
                  gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
              }}>
            {undecided.length > 0 && undecided.map(
                ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}}/>
            )}
        </Card>
        <Card size={'small'} key={'decided'} style={{width: '100%', marginBottom: 16}}
              title={`ממתין לאשפוז/שחרור (${decided.length})`}
              bodyStyle={{
                  display: !decided.length ? 'none' : "grid",
                  gridGap: 16,
                  gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`
              }}>
            {decided.length > 0 && decided.map(
                ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}}/>
            )}
        </Card>
    </>
}
export const StatusMode = ({onError}) => {
    const {value} = useContext(viewsContext.context)
    const {view} = useParams();

    const curView = useMemo(() => {
        return value.getViews.views.find(v => v.key === view)
    }, [value, view])
    return <wingDataContext.Provider url={`/api/departments/${curView.department_id}/wings/${curView.wing_id}`}
                                     defaultValue={{}} onError={onError}>
        {({loading, value}) => loading ? <Spin/> : <StatusModeInner patients={value.getPatients.patients}/>}
    </wingDataContext.Provider>
}
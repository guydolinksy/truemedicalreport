import {Bed} from "../components/Bed";
import {MIN_WIDTH, Patient} from "../components/card/Patient";
import React, {useContext, useMemo} from "react";
import {Empty, Layout} from 'antd';
import {generatePath, Navigate, useParams} from 'react-router-dom';
import {viewsDataContext} from "../contexts/ViewsDataContext";
import {createDataContext} from "../contexts/DataContext";
import {Legend} from "../components/Legend";
import {WingNotifications} from "../components/WingNotifications";
import {filterContext, filtersDataContext, PatientsFilter} from "../components/PatientsFilter";
import {DEFAULT_MODE_URL} from "../pages/ModeView";
import {AdmitPatient} from "../components/AdmitPatient";
import {InfoDrawer} from "../components/panel/Info";

const {Content} = Layout;
export const layoutDataContext = createDataContext();
const LayoutModeInner = ({onError}) => {
    const {value: viewsValue} = useContext(viewsDataContext.context)
    const {viewType, view} = useParams();

    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);

    const {value: filtersValue} = useContext(filtersDataContext.context)

    const {value} = useContext(layoutDataContext.context)
    const {filteredPatients, isFiltered} = useContext(filterContext)

    const unassignedPatients = useMemo(() => {
        return filtersValue.getPatients.patients.filter(patient => patient.admission.bed === null)
    }, [filtersValue]);
    const listPatients = isFiltered ? filteredPatients : unassignedPatients;
    if (!value.getWings.wings[0].details.layout)
        return <Navigate to={generatePath(DEFAULT_MODE_URL, {viewType, view})}/>
    return <Content style={{
        padding: 'max(32px, min(8vw, 8vh))',
        overflowY: 'auto',
        display: "grid",
        gridTemplateColumns: value.getWings.wings[0].details.layout.columns,
        gridTemplateRows: `${value.getWings.wings[0].details.layout.rows}  repeat(auto-fill, 1fr)`,
        gap: 32,
    }}>
        {!isFiltered && value.getWings.wings[0].details.layout && value.getWings.wings[0].details.layout.beds.map((bed, i) => {
            if (bed === null)
                return <div key={i}/>
            return <Bed key={i} admission={{
                department_id: curView.department_id,
                wing_id: curView.wing_id,
                bed: bed
            }}/>
        })}
        {listPatients.length ? listPatients.map(
            ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}} onError={onError}/>
        ) : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>}
    </Content>
}

export const LayoutMode = ({onError}) => {
    const {value} = useContext(viewsDataContext.context)
    const {view} = useParams();

    const curView = useMemo(() => {
        return value.getViews.views.find(v => v.key === view)
    }, [value, view]);
    return <layoutDataContext.Provider url={`/api/departments/${curView.department_id}/wings/${curView.wing_id}/layout`}
                                       onError={onError}>
        {() => <>
            <PatientsFilter>
                <LayoutModeInner onError={onError}/>
                <WingNotifications/>
            </PatientsFilter>
            <Legend/>
            <InfoDrawer/>
            <AdmitPatient/>
        </>}
    </layoutDataContext.Provider>
}
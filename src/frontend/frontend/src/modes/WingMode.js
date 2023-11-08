import React, {useContext, useMemo} from "react";
import {Legend} from "../components/Legend";
import {viewsContext} from "../contexts/ViewsContext";
import {Spin, Drawer, Empty} from 'antd';
import {useParams} from 'react-router-dom';
import {FilterPatients} from "../components/FilterPatients";
import {wingDataContext} from '../contexts/WingContext';
import {useLocalStorage} from "../hooks/localStorageHook";
import moment from 'moment';
import {INFO_URL} from "../pages/InfoView";
import {InfoContext} from "../components/panel/Info";
import {MIN_WIDTH, Patient} from "../components/card/Patient";

export const WingModeInner = ({onError, style}) => {
    const {value} = useContext(wingDataContext.context)

    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
    const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);
    const [selectedTime, setSelectedTime] = useLocalStorage('selectedTime', []);


    const patients = useMemo(() => {
        return value.getPatients.patients.filter(({oid}) => !selectedAwaiting.filter(
            filter => value.getWings.wings[0].filters.mapping[filter] !== undefined
        ).length || selectedAwaiting.find(
            filter => (value.getWings.wings[0].filters.mapping[filter] || []).includes(oid)
        )).filter(({oid}) => !selectedTreatments.filter(
            filter => value.getWings.wings[0].filters.mapping[filter] !== undefined
        ).length || selectedTreatments.find(
            filter => (value.getWings.wings[0].filters.mapping[filter] || []).includes(oid)
        )).filter(({oid}) => !selectedDoctors.filter(
            filter => value.getWings.wings[0].filters.mapping[filter] !== undefined
        ).length || selectedDoctors.find(
            filter => (value.getWings.wings[0].filters.mapping[filter] || []).includes(oid)
        )).filter(({oid}) => !selectedTime.filter(
            filter => value.getWings.wings[0].filters.mapping[filter] !== undefined
        ).length || selectedTime.find(
            filter => (value.getWings.wings[0].filters.mapping[filter] || []).includes(oid)
        )).sort((i, j) =>
            moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1
        )
    }, [value, selectedAwaiting, selectedDoctors, selectedTreatments, selectedTime])
    return patients.length ? patients.map(
        ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}} onError={onError}/>
    ) : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>

}
export const WingMode = ({onError, style}) => {
    const {value: viewsValue} = useContext(viewsContext.context)
    const {view} = useParams();
    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);
    return <wingDataContext.Provider url={`/api/departments/${curView.department_id}/wings/${curView.wing_id}`}
                                     onError={onError}>
        {() => <>
            <WingModeInner/>
            <Legend/>
            <FilterPatients/>
            {/*<Drawer title={'foo'} placement={"left"} open={true}*/}
            {/*        onClose={() => {}} size={500}>*/}
            {/*    <InfoContext patient={''} setHeader={() => {}} onError={() => {}}/>*/}
            {/*</Drawer>*/}
        </>}
    </wingDataContext.Provider>
}
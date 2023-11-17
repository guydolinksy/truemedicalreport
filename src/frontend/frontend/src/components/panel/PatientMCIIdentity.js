import {patientDataContext} from "../card/PatientBase";
import React, {useContext, useMemo, useState, useEffect} from 'react';
import {DeleteOutlined, MergeCellsOutlined, SplitCellsOutlined} from "@ant-design/icons";
import {useParams, generatePath, useNavigate} from 'react-router-dom';
import {MODE_URL} from "../../pages/ModeView";
import Axios from 'axios';
import {Button, Select} from 'antd';
import {PatientLabel} from "../PatientLabel";
import {loginContext} from "../LoginContext";
import {viewsDataContext} from "../../contexts/ViewsDataContext";

const PatientMCIIdentityInner = () => {
    const {user} = useContext(loginContext);
    const {viewType, view, mode, patient} = useParams();
    const {value: viewsValue} = useContext(viewsDataContext.context);
    const {value} = useContext(patientDataContext.context);
    const [mergeTo, setMergeTo] = useState(null);
    const [unmergedPatients, setUnmergedPatients] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        Axios.get(`/api/mci/unmerged`).then((response) => {
            setUnmergedPatients(response.data.map(p => {
                const data = Object.assign({}, p, {
                    views: viewsValue.getViews.views.filter(v => v.patients.find(({oid}) => oid === p.oid)),
                });
                return {
                    value: data.oid,
                    label: <PatientLabel patient={data} user={user}/>
                }
            }))
        })
    }, []);
    const hasData = useMemo(() => {
        return !value.mci.diagnosis.length || !value.mci.pre_hospital_treatment.length ||
            !value.mci.hospital_treatment.length || !value.mci.imaging.length
    }, [value])
    const deletePatient = () => {
        Axios.post(`/api/mci/delete`, {anonymous_patient: patient}).then(() => {
            navigate(generatePath(MODE_URL, {
                viewType: viewType,
                view: view,
                mode: mode
            }))
        })
    }
    const mergePatient = () => {
        Axios.post(`/api/mci/merge`, {patient_id: mergeTo, anonymous_patient: patient}).then(() => {
            navigate(generatePath(MODE_URL, {
                viewType: viewType,
                view: view,
                mode: mode
            }))
        })
    }
    const unmergePatient = () => {
        Axios.post(`/api/mci/unmerge`, {patient_id: patient}).then(() => {
            navigate(generatePath(MODE_URL, {
                viewType: viewType,
                view: view,
                mode: mode
            }))
        })
    }

    if (value.source_identity === 'manually')
        return <div style={{display: 'flex', flex: 1, minWidth: 'fit-content'}}>
            <Button danger icon={<DeleteOutlined/>} type={'primary'} onClick={deletePatient} disabled={hasData}/>
            <Select value={mergeTo} onChange={setMergeTo} disabled={!hasData} options={unmergedPatients}
                    style={{flex: 1}} dropdownStyle={{minWidth: 300}} placement={'bottomLeft'}/>
            <Button icon={<MergeCellsOutlined/>} type={'primary'} onClick={mergePatient}
                    disabled={!hasData || !mergeTo}/>
        </div>
    return <div>
        <Button icon={<SplitCellsOutlined/>} type={'primary'} onClick={unmergePatient}/>
    </div>
}
export const PatientMCIIdentity = () => {
    const {patient} = useParams();
    const {value} = useContext(patientDataContext.context);
    return [undefined, null, 'merged'].includes(value.source_identity) || !patient ? null : <PatientMCIIdentityInner/>
}
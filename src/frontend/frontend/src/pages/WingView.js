import React, {useCallback} from 'react';
import {useNavigate, useParams} from 'react-router-dom';
import {Wing} from "../components/Wing";
import {createContext} from "../hooks/DataContext";
import {Spin} from 'antd';

export const WING_URL = '/departments/:department/wings/:wing';

export const wingDataContext = createContext(null);

export const WingView = (() => {
    const params = useParams();
    const navigate = useNavigate();
    const onError = useCallback(() => navigate('/'), [navigate])

    return <wingDataContext.Provider url={`/api/departments/${params.department}/wings/${params.wing}`} defaultValue={
        {patients: [], details: {}, filters: {mapping: {}, filters: []}}
    } onError={onError}>
        {({loading}) => loading ? <Spin/> : <Wing department={params.department} wing={params.wing} onError={onError}/>}
    </wingDataContext.Provider>
});
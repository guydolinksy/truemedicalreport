import {viewsDataContext} from "../contexts/ViewsDataContext";
import {Button} from 'antd';
import {UserAddOutlined} from "@ant-design/icons";
import React, {useMemo, useContext, useEffect} from 'react';
import {useParams, useNavigate, generatePath} from 'react-router-dom';
import {hashMatchContext} from "./HashMatch";
import axios from 'axios';
import moment from 'moment';
import {INFO_URL} from "../pages/InfoView";
import {MCI_DEPARTMENT} from "./panel/MCISection";

export const AdmitPatient = () => {
    const {viewType, view, mode} = useParams();
    const {value: viewsValue} = useContext(viewsDataContext.context)
    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);
    const {matched} = useContext(hashMatchContext);
    const navigate = useNavigate();
    useEffect(() => {
        if (!matched(['new']))
            return;
        axios.post('/api/mci/patient', {
                arrival: moment().toISOString().replace('Z', '+00:00'),
                wing: curView.wing_id
            }
        ).then(response => {
            navigate(generatePath(INFO_URL, {viewType, view, mode, patient: response.data}))
        })
    }, [matched]);
    return curView.department_id === MCI_DEPARTMENT &&
        <Button size={'large'} type={'primary'} shape={'circle'} icon={<UserAddOutlined/>}
                style={{position: 'absolute', left: 40, bottom: 40}} onClick={() => navigate('#new')}/>
}
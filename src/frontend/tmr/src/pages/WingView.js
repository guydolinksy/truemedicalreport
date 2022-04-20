import React, {useCallback} from 'react';
import {useParams, useNavigate} from 'react-router';
import {Wing} from "../components/Wing";
import {LoginRequired} from "../components/LoginContext";

export const WING_URL = '/departments/:department/wings/:wing';

export const WingView = (() => {
    const params = useParams();
    const navigate = useNavigate();
    const onError = useCallback(() => navigate('/'), [navigate])
    return <LoginRequired>
        <Wing department={params.department} wing={params.wing} onError={onError}/>
    </LoginRequired>
});
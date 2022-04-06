import {useParams, useNavigate} from 'react-router';
import {Wing} from "../components/Wing";
import {LoginRequired} from "../components/LoginContext";

export const WING_URL = '/wing/:wing';

export const WingView = (() => {


    const params = useParams()
    return <LoginRequired><Wing id={params.wing}/></LoginRequired>
});
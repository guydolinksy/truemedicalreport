import {useParams} from 'react-router';
import {Wing} from "../components/Wing";

export const WING_URL = '/wing/:wing'
export const WingView = () => {
    const params = useParams()
    return <Wing id={params.wing}/>
}
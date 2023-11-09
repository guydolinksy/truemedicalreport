import {useContext} from 'react';
import {loginContext} from "../LoginContext";
import {AuthenticationCard} from "./AuthenticationCard";
import {ChangePasswordCard} from "./ChangePasswordCard";
import {DisplayCard} from "./DisplayCard";

export const Settings = () => {
    const {user} = useContext(loginContext);
    return <>
        {user && user.canChangePassword && <ChangePasswordCard/>}
        {user && <DisplayCard/>}
        {user && user.is_admin && <AuthenticationCard/>}
    </>
}
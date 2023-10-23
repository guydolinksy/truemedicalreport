import React, {useContext} from 'react';
import {Department} from "../components/Department";
import {Layout, Spin, Modal} from 'antd';
import {Outlet, useParams, useLocation, useNavigate} from "react-router-dom";
import {createContext} from "../hooks/DataContext";
import {Legend} from "../components/Legend";
import {Settings} from "../components/settings/Settings";
import {DepartmentItemsCard} from "../components/settings/DepartmentItemsCard";
import {loginContext} from "../components/LoginContext";

const {Content} = Layout;


export const DEPARTMENT_URL = '/departments/:department'

export const departmentDataContext = createContext({value: {}});
export const DepartmentView = () => {
    const params = useParams()
    const {hash} = useLocation()
    const {user} = useContext(loginContext)
    const navigate = useNavigate();
    return <departmentDataContext.Provider url={`/api/departments/${params.department}`} defaultValue={{
        name: null, wings: []
    }}>
        {({loading}) => loading ? <Spin/> : params.wing ? <Outlet/> :
            <Content style={{flex: 1, display: "flex", flexDirection: "column", overflowY: 'hidden'}}>
                <Department department={params.department} style={{margin: "50px 250px", overflowY: 'auto'}}/>
                {user && <Modal open={hash === '#settings'} title={'הגדרות:'} footer={null}
                                onCancel={() => navigate('#')}>
                    <DepartmentItemsCard/>
                </Modal>}
            </Content>}
    </departmentDataContext.Provider>
}
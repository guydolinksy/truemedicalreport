import React, {Suspense, useState} from "react";
import {DarkTheme, LightTheme} from "../themes/ThemeContext";
import debounce from "lodash/debounce";
import {Button, Input} from "antd";
import {useNavigate} from "react-router";

const {Search} = Input;

export const PatientList = ({value, user, userSettings}) => {
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    return <div style={{display: "flex", flexDirection: "column", maxHeight: "30vh", overflowY: "scroll"}}
                className={userSettings.theme}>
        <Suspense fallback={<span/>}>
            {userSettings.theme === 'dark-theme' ? <DarkTheme/> : <LightTheme/>}
        </Suspense>
        <Search key={'search'} style={{marginBottom: "0.5rem"}} allowClear
                onChange={debounce(e => setSearch(e.target.value), 300)}
                placeholder={'חיפוש:'}/>
        {value.department_patients.sort((a, b) => a.info.name.localeCompare(b.info.name))
            .filter((patient) => patient.info.id_.includes(search) || patient.info.name.includes(search))
            .map((patient, i) =>
                <Button key={i} onClick={() => navigate(
                    `/departments/${patient.admission.department}/wings/${patient.admission.wing}#highlight#${patient.oid}#open`
                )} className={`gender-${patient?.info?.gender}`}>
                    {user.anonymous ? '---' : patient?.info?.name}
                </Button>)}
    </div>
}

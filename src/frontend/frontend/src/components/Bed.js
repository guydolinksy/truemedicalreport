import {Patient} from "./Patient";
import React from "react";
import {createContext} from "../hooks/DataContext";

const bedContext = createContext(null);

export const Bed = ({admission, style, onError}) => {
    const url = `/api/departments/${admission.department_id}/wings/${admission.wing_id}/beds/${admission.bed}`;

    return <bedContext.Provider url={url} defaultValue={{patient: null}} onError={onError}>
        {({loading, value, flush}) => {
            return <Patient loading={loading} patient={value.patient} avatar={admission.bed} style={style} onError={flush}/>
        }}
    </bedContext.Provider>
}

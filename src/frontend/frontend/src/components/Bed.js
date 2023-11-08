import {Patient} from "./card/Patient";
import React from "react";
import {createContext} from "../contexts/DataContext";

const bedContext = createContext();

export const Bed = ({admission, style, onError}) => {
    const url = `/api/departments/${admission.department_id}/wings/${admission.wing_id}/beds/${admission.bed}`;

    return <bedContext.Provider url={url} onError={onError}>
        {({value, flush}) => {
            return <Patient patient={value.getBed?.patient} avatar={admission.bed} style={style}
                            onError={flush}/>
        }}
    </bedContext.Provider>
}

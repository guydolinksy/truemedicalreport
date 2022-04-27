import {Patient} from "./Patient";
import React from "react";
import {createContext} from "./DataContext";
import {Spin} from "antd";

const bedContext = createContext(null);

export const Bed = ({admission, style, onError}) => {
    const url = `/api/departments/${admission.department}/wings/${admission.wing}/beds/${admission.bed}`;

    return <bedContext.Provider url={url} defaultValue={{}} onError={onError}>
        {({loadingData, getData, flushData}) => {
            if (loadingData)
                return <Spin/>
            return <Patient patient={getData(['patient'])} avatar={admission.bed} style={style} onError={flushData}/>
        }}
    </bedContext.Provider>
}

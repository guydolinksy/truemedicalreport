import React, {useContext} from 'react';
import {generatePath, Navigate, useParams} from 'react-router-dom';
import {viewsContext} from "../contexts/ViewsContext";
import {ListMode} from "../modes/ListMode";
import {LayoutMode} from "../modes/LayoutMode";
import {DepartmentMode} from "../modes/DepartmentMode";
import {StatusMode} from "../modes/StatusMode";
import {WingMode} from "../modes/WingMode";
import {TraumaMode} from "../modes/TraumaMode";

export const MODE_URL = '/views/:view/modes/:mode';
export const DEFAULT_MODE_URL = '/views/:view';


export const DefaultModeForView = () => {
    const {view} = useParams();
    const {value} = useContext(viewsContext.context);
    return <Navigate to={generatePath(MODE_URL, {
        view: view,
        mode: value.getViews.views.find(({key}) => key === view).default_mode.key
    })}/>
}

export const ModeView = (() => {
    const {mode} = useParams();

    if (mode === 'department')
        return <DepartmentMode/>
    if (mode === 'patients')
        return <ListMode/>
    if (mode === 'wing')
        return <WingMode/>
    if (mode === 'layout')
        return <LayoutMode/>
    if (mode === 'status')
        return <StatusMode/>
    if (mode === 'trauma')
        return <TraumaMode/>
    // if (mode === 'ors')
    //     return <ORMode/>
    // if (mode === 'imaging')
    //     return <ImagingMode/>
    return <div/>
});

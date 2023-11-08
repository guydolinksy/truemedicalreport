import React, {useContext, useEffect, useState} from 'react';
import {patientDataContext} from "../card/PatientBase";
import {useParams} from 'react-router-dom';
import axios from 'axios';
import {Spin} from 'antd';
import {Notes} from "./Notes";
import {FullMeasures} from "./FullMeasures";
import {BasicInfo} from "./BasicInfo";
import {loginContext} from "../LoginContext";
import {Notifications} from "./Notifications";
import {Imaging} from "./Imaging";
import {Labs} from "./Labs";
import {Referrals} from "./Referrals";
import {InfoPlugin} from "./InfoPlugin";
import {Visits} from "./Visits";
import {MedicalSummary} from "./MedicalSummary";
import {ECGs} from "./ECGs";
import {MCIFormSection} from "./MCIFormSection";
import {MCIHeader} from "./MCIHeader";
import {createContext} from "../../contexts/DataContext";

export const panelContext = createContext();

export const InfoPanel = ({setHeader}) => {
    const {user} = useContext(loginContext);
    const {view, mode} = useParams()
    const {value} = useContext(patientDataContext.context);

    useEffect(() => {
        let gender = {
            male: 'בן ',
            female: 'בת ',
            [null]: '',
        }[value.info?.gender];
        setHeader({
            title: user.anonymous ? `${gender}(${value.info?.age || 'גיל לא ידוע'})` :
                `${value.info?.name}, ${gender}(${value.info?.age || 'גיל לא ידוע'})` +
                (value.info?.id_ ? `, ת.ז. ${value.info?.id_}` : '') +
                (value.info?.phone ? `, טלפון : ${value.info?.phone}` : ''),
            className: `gender-${value.info?.gender}`
        });
    }, [value, setHeader]);

    return <panelContext.Provider url={`/api/settings/view/${view}/info/format`}>
        {({value}) => value.components.map(component => {
            if (component.type === 'Notes')
                return <Notes {...component.config}/>
            if (component.type === 'FullMeasures')
                return <FullMeasures {...component.config}/>
            if (component.type === 'BasicInfo')
                return <BasicInfo {...component.config}/>
            if (component.type === 'Notifications')
                return <Notifications {...component.config}/>
            if (component.type === 'Imaging')
                return <Imaging {...component.config}/>
            if (component.type === 'Labs')
                return <Labs {...component.config}/>
            if (component.type === 'Referrals')
                return <Referrals {...component.config}/>
            if (component.type === 'Visits')
                return <Visits {...component.config}/>
            if (component.type === 'MedicalSummary')
                return <MedicalSummary {...component.config}/>
            if (component.type === 'ECGs')
                return <ECGs {...component.config}/>
            if (component.type === 'MCIHeader')
                return <MCIHeader {...component.config}/>
            if (component.type === 'MCIInputSection')
                return <MCIFormSection {...component.config}/>
            if (component.type === 'InfoPlugin')
                return <InfoPlugin {...component.config}/>
            return <div>Unknown Component {component}</div>
        })}
    </panelContext.Provider>
}
export const Info = () => {
    const [header, setHeader] = useState(null)

    return <div style={{
        flex: 1,
        overflowY: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    }}>
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            margin: "4vh 4vw",
            overflowY: 'hidden',
            maxWidth: "80rem",
            width: '100%',
            flex: 1,
        }}>
            {header && <h1 style={{textAlign: 'center'}} className={header.className}>{header.title}</h1>}
            <InfoPanel setHeader={setHeader}/>
        </div>
    </div>
}

export const InfoContext = ({patient, onError, setHeader}) => {
    return <patientDataContext.Provider url={`/api/patients/${patient}/info`} onError={onError}>
        {() => <InfoPanel setHeader={setHeader}/>}
    </patientDataContext.Provider>
}

const Foo = () => {

}
const Bar = () => {
    return <Foo/>
}
const FooBar = () => {
    return Foo()
}
import React, {useCallback, useEffect, useRef, useState} from "react";
import {Button, Card, Carousel, Input, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faClock,
    faHeart,
    faHeartPulse,
    faTemperatureHalf,
    faUserNurse,
    faWarning,
} from "@fortawesome/free-solid-svg-icons";
import {CheckOutlined, UserOutlined, AlertOutlined, FlagOutlined} from '@ant-design/icons'
import Axios from 'axios';

const PatientDataContext = React.createContext();

const deepReplace = (path, data, value) => {
    if (!path.length) {
        return value
    }
    const key = path.pop()
    return Object.assign({}, data, {[key]: deepReplace(path, data[key], value)});
}
const withPatientData = Component => ({id, bed, data, ...props}) => {
    const [patientData, setPatientData] = useState({loading: true});

    useEffect(() => {
        if (data) {
            setPatientData(data);
            return;
        }
        Axios.get(bed ? `/api/patient/bed/${bed}` : `/api/patient/id/${id}`).then(response => {
            setPatientData(Object.assign({loading: false}, response.data));
        }).catch(error => {
            console.error(error)
        })

    }, [bed, id, data]);
    const updatePatientData = useCallback((path, value) => {
        setPatientData(prevState => deepReplace(path.slice().reverse(), prevState, value));
    }, []);
    return <PatientDataContext.Provider value={{patientData: patientData, updatePatientData: updatePatientData}}>
        <Component id={id} bed={bed} patientData={patientData} updatePatientData={updatePatientData} {...props}/>
    </PatientDataContext.Provider>
}
const PatientData = ({path, hover, icon, size, editable}) => {
    const [editing, setEditing] = useState(false)


    return <PatientDataContext.Consumer>
        {({patientData, updatePatientData}) => {
            const value = path.reduce((data, name) => data ? data[name] : undefined, patientData);
            const content = <span style={{userSelect: "none"}}><FontAwesomeIcon icon={icon}/>&nbsp;{value}</span>;
            return <Tooltip overlay={hover}>
                {!editable ? content : !editing ?
                    <Button type={"text"} onClick={() => setEditing(true)}>{content}</Button> :
                    <Input.Group compact>
                        <Input size={size} style={{width: 150}}
                               value={value}
                               onChange={e => updatePatientData(path, e.target.value)}
                               onPressEnter={() => setEditing(false)}
                        />
                        <Button type="primary" size={size} onClick={() => setEditing(false)} icon={<CheckOutlined/>}/>
                    </Input.Group>}
            </Tooltip>
        }}
    </PatientDataContext.Consumer>
}


const dataItems = [
    {path: ['measures', 'temperature'], icon: faTemperatureHalf, hover: 'מדידת חום אחרונה', showMinimized: true},
    {path: ['measures', 'bloodPressure'], icon: faHeart, hover: 'מדידת לחץ דם אחרונה', showMinimized: true},
    {path: ['measures', 'pulse'], icon: faHeartPulse, hover: 'מדידת דופק אחרונה', showMinimized: true},
    {path: ['esiScore'], icon: faUserNurse, hover: 'ערך ESI אחרון', showMinimized: true},
]

export const Patient = withPatientData(({bed, patientData, updatePatientData}) => {
    let avatar;
    if ((patientData.warnings || []).length)
        avatar = <Button shape={"circle"} type={"primary"} icon={<AlertOutlined/>} danger/>
    else if (patientData.flagged)
        avatar = <Button shape={"circle"} type={"primary"} icon={<FlagOutlined/>} danger
                         onClick={() => updatePatientData(['flagged'], false)}/>
    else if (bed)
        avatar = <Button shape={"circle"} type={"primary"}
                         onClick={() => updatePatientData(['flagged'], true)}>{bed}</Button>
    else
        avatar = <Button shape={"circle"} type={"primary"} icon={<UserOutlined/>}
                         onClick={() => updatePatientData(['flagged'], true)}/>;

    const title = <span>{avatar}&nbsp;{patientData.name}</span>
    const actions = dataItems.filter(({path, showMinimized}) => (bed || showMinimized)).map(
        ({path, icon, hover}) =>
            <PatientData editable={false} icon={icon} path={path} hover={hover}/>
    );
    const extra = <PatientData editable size={"small"} icon={faClock} hover={'ממתין.ה עבור'} path={["awaiting"]}/>


    const slider = useRef(null);

    return <Card type={"inner"} size={"small"} headStyle={{backgroundColor: "#e6fffb"}} bodyStyle={{padding: 0}}
                 style={{marginBottom: 16}}
                 title={title} actions={actions} extra={extra}>
        <Carousel ref={slider} autoplay dotPosition={"top"}>
            <div>
                <div style={{
                    userSelect: "none",
                    padding: 20,
                    backgroundColor: "#fff7e6",
                    textAlign: "center",
                    cursor: (patientData.warnings || []).length ? "pointer" : undefined
                }}
                     onClick={() => slider.current.next()}>
                    {patientData.complaint}
                </div>
            </div>
            {(patientData.warnings || []).map((warning, i) =>
                <div>
                    <div key={i}
                         style={{
                             userSelect: "none",
                             padding: 20,
                             backgroundColor: "#ffccc7",
                             textAlign: "center",
                             cursor: "pointer"
                         }}
                         onClick={() => slider.current.next()}>
                        {warning}&nbsp;<FontAwesomeIcon icon={faWarning}/>
                    </div>
                </div>)}
        </Carousel>
    </Card>
});
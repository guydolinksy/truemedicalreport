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
            setPatientData({
                name: 'ישראל ישראלי',
                complaint: 'קוצר נשימה',
                awaiting: 'פענוח סיטי',
                flagged: false,
                loading: false,
                pulse: 80,
                bloodPressure: "140/80",
                esiScore: 5,
                temperature: 38,
                warnings: bed === 7 || id === 8 ? ['מחכה לך', 'טרופונין 18 מ״ג/ליטר'] : [],
                notifications: [],
            })
            console.error(error)
        })

    }, [bed, id, data]);
    const updatePatientData = useCallback((name, value) => {
        setPatientData(prevState => Object.assign({}, prevState, {[name]: value}));
    }, [])
    return <PatientDataContext.Provider value={{patientData: patientData, updatePatientData: updatePatientData}}>
        <Component id={id} bed={bed} patientData={patientData} updatePatientData={updatePatientData} {...props}/>
    </PatientDataContext.Provider>
}
const PatientData = ({name, hover, icon, size, editable}) => {
    const [editing, setEditing] = useState(false)


    return <PatientDataContext.Consumer>
        {({patientData, updatePatientData}) => {
            const content = <span style={{userSelect: "none"}}>
                <FontAwesomeIcon icon={icon}/>&nbsp;{patientData[name]}
            </span>;
            return <Tooltip overlay={hover}>
                {!editable ? content : !editing ?
                    <Button type={"text"} onClick={() => setEditing(true)}>{content}</Button> :
                    <Input.Group compact>
                        <Input size={size} style={{width: 150}} value={patientData[name]}
                               onChange={e => updatePatientData(name, e.target.value)}
                               onPressEnter={() => setEditing(false)}
                        />
                        <Button type="primary" size={size} onClick={() => setEditing(false)} icon={<CheckOutlined/>}/>
                    </Input.Group>}
            </Tooltip>
        }}
    </PatientDataContext.Consumer>
}


const dataItems = [
    {name: 'temperature', icon: faTemperatureHalf, hover: 'מדידת חום אחרונה', showMinimized: true},
    {name: 'bloodPressure', icon: faHeart, hover: 'מדידת לחץ דם אחרונה', showMinimized: true},
    {name: 'pulse', icon: faHeartPulse, hover: 'מדידת דופק אחרונה', showMinimized: true},
    {name: 'esiScore', icon: faUserNurse, hover: 'ערך ESI אחרון', showMinimized: false},
]

export const Patient = withPatientData(({bed, patientData, updatePatientData}) => {

    let avatar = undefined;
    if ((patientData.warnings || []).length)
        avatar = <Button shape={"circle"} type={"primary"} icon={<AlertOutlined/>} danger/>
    else if (patientData.flagged)
        avatar = <Button shape={"circle"} type={"primary"} icon={<FlagOutlined/>} danger
                         onClick={() => updatePatientData('flagged', false)}/>
    else if (bed)
        avatar =
            <Button shape={"circle"} type={"primary"} onClick={() => updatePatientData('flagged', true)}>{bed}</Button>
    else
        avatar = <Button shape={"circle"} type={"primary"} icon={<UserOutlined/>}
                         onClick={() => updatePatientData('flagged', true)}/>;

    const title = <span>{avatar}&nbsp;{patientData.name}</span>
    const actions = dataItems.filter(
        ({name, showMinimized}) => (bed || showMinimized) && patientData[name] !== undefined
    ).map(
        ({name, icon, hover}) =>
            <PatientData editable={false} icon={icon} name={name} hover={hover}/>
    );
    const extra = <PatientData editable size={"small"} icon={faClock} hover={'ממתין.ה עבור'} name={"awaiting"}/>


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
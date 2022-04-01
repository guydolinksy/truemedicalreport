import React, {useCallback, useEffect, useRef, useState} from "react";
import {Button, Card, Carousel, Input, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faClock,
    faHeart,
    faHeartPulse,
    faTemperatureHalf,
    faUserNurse,
    faWarning,
} from "@fortawesome/free-solid-svg-icons";
import {AlertOutlined, CheckOutlined, FlagOutlined, UserOutlined} from '@ant-design/icons';
import {createContext} from "./DataContext";

const patientDataContext = createContext(null);
const PatientData = patientDataContext.withData(
    ({path, hover, icon, size, editable, loadingData, getData, updateData}) => {
        const [editing, setEditing] = useState(false)

        const [value, setValue] = useState(getData(path))
        useEffect(() => {
            setValue(getData(path));
            setEditing(false)
        }, [path, getData])

        const onSave = useCallback(() => {
            updateData(path, value);
            setEditing(false)
        }, [path, value, updateData])

        const content = <span style={{userSelect: "none"}}><FontAwesomeIcon icon={icon}/>&nbsp;{value}</span>;
        return loadingData ? <Spin/> : <Tooltip overlay={hover}>
            {!editable ? content : !editing ?
                <Button style={{padding: 0}} type={"text"} onClick={() => setEditing(true)}>{content}</Button> :
                <Input.Group compact>
                    <Input size={size} style={{width: 150}} value={value}
                           onChange={e => setValue(e.target.value)} onPressEnter={onSave}/>
                    <Button type="primary" size={size} onClick={onSave} icon={<CheckOutlined/>}/>
                </Input.Group>}
        </Tooltip>
    }
);

const Measure = patientDataContext.withData(
    ({path, loadingData, getData, updateData, ...props}) => {
        return <PatientData path={path.concat('value')} {...props}/>
    }
);

const dataItems = [
    {path: ['measures', 'temperature',], icon: faTemperatureHalf, hover: 'מדידת חום אחרונה', showMinimized: true},
    {path: ['measures', 'bloodPressure'], icon: faHeart, hover: 'מדידת לחץ דם אחרונה', showMinimized: true},
    {path: ['measures', 'pulse'], icon: faHeartPulse, hover: 'מדידת דופק אחרונה', showMinimized: true},
    {path: ['esi_score'], icon: faUserNurse, hover: 'ערך ESI אחרון', showMinimized: true},
]

const {Meta} = Card;

export const Patient = ({bed, id, style}) => {
    const slider = useRef(null);
    const uri = bed ? `/api/patients/bed/${bed}` : `/api/patients/id/${id}`
    return <patientDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount defaultValue={{}}>
        {({loadingData, getData, updateData}) => {
            if (loadingData)
                return <Spin/>

            let avatar, props = {shape: 'circle'};
            if ((getData(['warnings']) || []).length)
                avatar = <Button {...props} icon={<AlertOutlined/>} danger/>
            else if (getData(['flagged']))
                avatar =
                    <Button {...props} icon={<FlagOutlined/>} danger onClick={() => updateData(['flagged'], false)}/>
            else if (bed)
                avatar = <Button {...props} onClick={() => updateData(['flagged'], true)}>{bed}</Button>
            else
                avatar = <Button  {...props} icon={<UserOutlined/>} onClick={() => updateData(['flagged'], true)}/>;

            const title = <span>{avatar}&nbsp;{getData(['name'])}</span>
            const actions = dataItems.filter(({path, showMinimized}) => (bed || showMinimized)).map(
                ({path, icon, hover}) =>
                    <Measure editable={false} icon={icon} path={path} hover={hover}/>
            );
            const extra = <PatientData editable size={"small"} icon={faClock} hover={'ממתין.ה עבור'}
                                       path={["awaiting"]}/>

            return <Card type={"inner"} size={"small"} headStyle={{backgroundColor: "#e6fffb"}}
                         bodyStyle={{padding: 0}}
                         style={{border: "1px solid black", margin: 8, maxWidth: '400px', ...style}}
                         title={title} actions={actions} extra={extra}>
                <Carousel ref={slider} autoplay dotPosition={"top"}>
                    <div>
                        <div style={{
                            userSelect: "none",
                            padding: 20,
                            backgroundColor: "#fff7e6",
                            textAlign: "center",
                            cursor: (getData(['warnings']) || []).length ? "pointer" : undefined
                        }}
                             onClick={() => slider.current.next()}>
                            {getData(['complaint'])}
                        </div>
                    </div>
                    {(getData(['warnings']) || []).slice(0, 0).map((warning, i) =>
                        <div key={i}>
                            <div
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
        }}
    </patientDataContext.Provider>
};
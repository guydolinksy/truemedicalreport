import React, {useCallback, useEffect, useRef, useState} from "react";
import {Badge, Button, Card, Carousel, Input, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faClock,
    faHeart,
    faHeartPulse,
    faTemperatureHalf,
    faUserNurse,
    faWarning,
} from "@fortawesome/free-solid-svg-icons";
import {AlertOutlined, CheckOutlined, FlagFilled, UserOutlined} from '@ant-design/icons';
import {createContext} from "./DataContext";
import {useLocation, useParams} from "react-router";

const patientDataContext = createContext(null);
const PatientData = patientDataContext.withData(
    ({path, hover, icon, size, editable, danger, loadingData, getData, updateData}) => {
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

        const content = <span style={{userSelect: "none", color: danger ? 'red' : undefined}}>
            <FontAwesomeIcon icon={icon}/>&nbsp;{value}
        </span>;
        return loadingData ? <Spin/> : <Tooltip overlay={hover}>
            {!editable ? content :
                !editing ? <Button style={{padding: 0}} type={"text"} onClick={() => setEditing(true)}
                                   danger={danger}>{content}</Button> :
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
        return <PatientData path={path.concat('value')} {...props} danger={!getData(path.concat('is_valid'))}/>
    }
);

const dataItems = [
    {path: ['measures', 'temperature',], icon: faTemperatureHalf, hover: 'מדידת חום אחרונה', showMinimized: true},
    {path: ['measures', 'blood_pressure'], icon: faHeart, hover: 'מדידת לחץ דם אחרונה', showMinimized: true},
    {path: ['measures', 'pulse'], icon: faHeartPulse, hover: 'מדידת דופק אחרונה', showMinimized: true},
    {path: ['esi_score'], icon: faUserNurse, hover: 'ערך ESI אחרון', showMinimized: true},
]

const {Meta} = Card;

export const Patient = ({bed, id, style}) => {
    const slider = useRef(null);
    const {hash} = useLocation();
    const uri = bed ? `/api/patients/bed/${bed}` : `/api/patients/id/${id}`
    return <patientDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount defaultValue={{}}>
        {({loadingData, getData, updateData}) => {
            if (loadingData)
                return <Spin/>
            const oid = getData(['oid']);
            const flagged = getData(['flagged']), warnings = getData(['warnings']) || []
            const avatar = <Button shape={"circle"} onClick={() => updateData(['flagged'], !flagged)}
                                   icon={bed || <UserOutlined/>}/>;
            const title = <span>{avatar}&nbsp;{getData(['name'])}</span>
            const actions = dataItems.filter(({path, showMinimized}) => (bed || showMinimized)).map(
                ({path, icon, hover}) =>
                    <Measure editable={false} icon={icon} path={path} hover={hover}/>
            );
            const extra = <PatientData editable size={"small"} icon={faClock} hover={'ממתין.ה עבור'}
                                       path={["awaiting"]}/>
            const carousel = <Carousel ref={slider} autoplay dotPosition={"top"}>
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
                {(getData(['warnings']) || []).map((warning, i) =>
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
            let content = carousel;
            if (warnings.length)
                content = <div style={style}>
                    <Badge.Ribbon text={warnings.length} color={"red"}>{carousel}</Badge.Ribbon>
                </div>
            else if (flagged)
                content = <div style={style}><Badge.Ribbon text={<FlagFilled/>}>{carousel}</Badge.Ribbon></div>

            let animation = undefined;
            if (hash === `#${oid}`)
                animation = 'highlight-open 1s ease-out'
            else if (hash === `#!${oid}`)
                animation = 'highlight-close 1s';
            return <Card type={"inner"} size={"small"}
                         headStyle={{backgroundColor: "#e6fffb", animation: animation}}
                         bodyStyle={{padding: 0}} style={{margin: 0, maxWidth: '400px', ...style}}
                         title={title} actions={actions} extra={extra}>{content}</Card>
        }}
    </patientDataContext.Provider>
};
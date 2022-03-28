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
import {AlertOutlined, CheckOutlined, FlagOutlined, UserOutlined} from '@ant-design/icons'
import Axios from 'axios';
import useWebSocket from "react-use-websocket";

const Data = React.createContext(null);

const DataContext = ({url, updateURL, socketURL, defaultValue, fetchOnMount, ...props}) => {
    const [{loadingData, value}, setValue] = useState({loading: false, value: defaultValue});
    const {lastMessage} = useWebSocket(`wss://${window.location.host}/api/ws`, {queryParams: {url: socketURL}});

    useEffect(() => {
        if (!fetchOnMount) return;
        Axios.get(url).then(response => {
            setValue({loading: false, value: response.data});
        }).catch(error => {
            console.error(error)
        })
    }, [url, fetchOnMount, lastMessage]);

    const getData = useCallback((path) =>
            path.reduce((data, name) => data ? data[name] : undefined, value),
        [value]);

    const updateData = useCallback((path, newValue) => {
        const deepReplace = (path, data, value) => {
            if (!path.length) {
                return value
            }
            const key = path.pop()
            return Object.assign({}, data, {[key]: deepReplace(path, data[key], value)});
        }
        setValue(prevState => {
            const newData = deepReplace(path.slice().reverse(), prevState.value, newValue)
            Axios.post(updateURL, {data: newData, path: path, value: newValue}).catch(error => {
                console.error(error)
            });
            return {loading: prevState.loading, value: newData}
        });
    }, [updateURL]);

    return <Data.Provider value={{getData: getData, updateData: updateData, loadingData: loadingData}}>
        {props.children({getData: getData, updateData: updateData, loadingData: loadingData, ...props})}
    </Data.Provider>
}
const withData = Component => ({...props}) => {
    return <Data.Consumer>{({getData, updateData, loadingData}) =>
        <Component loadingData={loadingData} getData={getData} updateData={updateData} {...props}/>
    }</Data.Consumer>
};

const PatientData = withData(({path, hover, icon, size, editable, loadingData, getData, updateData}) => {
    const [editing, setEditing] = useState(false)

    const content = <span style={{userSelect: "none"}}><FontAwesomeIcon icon={icon}/>&nbsp;{getData(path)}</span>;
    return <Tooltip overlay={hover}>
        {!editable ? content : !editing ?
            <Button type={"text"} onClick={() => setEditing(true)}>{content}</Button> :
            <Input.Group compact>
                <Input size={size} style={{width: 150}}
                       value={getData(path)}
                       onChange={e => updateData(path, e.target.value)}
                       onPressEnter={() => setEditing(false)}
                />
                <Button type="primary" size={size} onClick={() => setEditing(false)} icon={<CheckOutlined/>}/>
            </Input.Group>}
    </Tooltip>
});


const dataItems = [
    {path: ['measures', 'temperature'], icon: faTemperatureHalf, hover: 'מדידת חום אחרונה', showMinimized: true},
    {path: ['measures', 'bloodPressure'], icon: faHeart, hover: 'מדידת לחץ דם אחרונה', showMinimized: true},
    {path: ['measures', 'pulse'], icon: faHeartPulse, hover: 'מדידת דופק אחרונה', showMinimized: true},
    {path: ['esiScore'], icon: faUserNurse, hover: 'ערך ESI אחרון', showMinimized: true},
]

export const Patient = ({bed, id, defaultData}) => {
    const slider = useRef(null);
    const uri = bed ? `/api/patient/bed/${bed}` : `/api/patient/id/${id}`
    return <DataContext url={uri} updateURL={uri} socketURL={uri} fetchOnMount defaultValue={defaultData}>
        {({loadingData, getData, updateData}) => {
            let avatar;
            if ((getData(['warnings']) || []).length)
                avatar = <Button shape={"circle"} type={"primary"} icon={<AlertOutlined/>} danger/>
            else if (getData(['flagged']))
                avatar = <Button shape={"circle"} type={"primary"} icon={<FlagOutlined/>} danger
                                 onClick={() => updateData(['flagged'], false)}/>
            else if (bed)
                avatar = <Button shape={"circle"} type={"primary"}
                                 onClick={() => updateData(['flagged'], true)}>{bed}</Button>
            else
                avatar = <Button shape={"circle"} type={"primary"} icon={<UserOutlined/>}
                                 onClick={() => updateData(['flagged'], true)}/>;

            const title = <span>{avatar}&nbsp;{getData(['name'])}</span>
            const actions = dataItems.filter(({path, showMinimized}) => (bed || showMinimized)).map(
                ({path, icon, hover}) =>
                    <PatientData editable={false} icon={icon} path={path} hover={hover}/>
            );
            const extra = <PatientData editable size={"small"} icon={faClock} hover={'ממתין.ה עבור'}
                                       path={["awaiting"]}/>

            return <Card type={"inner"} size={"small"} headStyle={{backgroundColor: "#e6fffb"}}
                         bodyStyle={{padding: 0}}
                         style={{marginBottom: 16}}
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
            </Card>
        }}
    </DataContext>
};
import React, {useContext} from "react";
import {Card, Col, Progress, Row, Tooltip} from "antd";
import {generatePath} from "react-router-dom";
import {WING_URL} from "../pages/WingView";
import {useNavigate} from "react-router";
import {CustomIcon} from "./CustomIcon";
import Moment from "react-moment";
import {CloseCircleOutlined} from "@ant-design/icons";
import {loginContext} from "./LoginContext";
import Axios from "axios";
import {departmentDataContext} from "../pages/DepartmentView";

const hideSetting = (e, setting) => {
    if (e.stopPropagation) e.stopPropagation();
    console.log(setting)
    Axios.post('/api/settings/statistics', {values: setting}).then(() => {
        console.log("success")
        document.location.reload();
    }).catch(error => {
        if (Axios.isCancel(error))
            return;
        console.log("failed")
    });

}

export const Department = ({department, wingId, onOk, style}) => {
    const mci = department === 'mci';
    const navigate = useNavigate();
    const {userSettings} = useContext(loginContext);
    const {value: departmentValue} = useContext(departmentDataContext.context);

    return <Row gutter={16} style={style}>
        {departmentValue.wings.map((wing, i) => {
            const toActions = filter => [({
                key: filter.key,
                icon: filter.icon,
                count: filter.count,
                title: filter.title,
                duration: filter.duration,
                valid: filter.valid,
            })].concat(...(filter.children || []).map(toActions))
            const actions = [].concat(
                ...wing.filters.doctors.map(toActions),
                ...wing.filters.awaiting.map(toActions),
                ...wing.filters.treatments.map(toActions),
                ...wing.filters.time_since_arrival.map(toActions),
            ).filter(({key}) => {
                const filters = [].concat(userSettings.statistics[wing.oid] || [], userSettings.statistics.default || []);
                if (filters.some(([regex, result]) => result && key.match(regex)))
                    return true
                return !filters.some(([regex, result]) => !result && key.match(regex));
            }).map(
                ({count, title, icon, duration, valid, key}) => <div key={key}
                                                                     style={{
                                                                         display: "flex",
                                                                         flexDirection: "column",
                                                                         alignItems: "center",
                                                                         padding: 5,
                                                                         border: "1px solid $f0f0f0"
                                                                     }}>
                    <div className="departmentActionItem" onClick={(e) => {
                        hideSetting(e, key)
                    }} style={{alignSelf: "start"}}>{<CloseCircleOutlined/>}</div>
                    <div style={{fontSize: 12}}>{title}{icon &&
                        <span>&nbsp;<CustomIcon status={'processing'} icon={icon}/></span>}</div>
                    {![null, undefined].includes(duration) && <div style={{userSelect: "none", fontSize: 14}}>
                        <Tooltip overlay={'זמן המתנה ממוצע'}>
                            <Moment interval={1000} durationFromNow format={'H[h]mm[m]'} date={duration}/>
                        </Tooltip>
                    </div>}
                    <div className={valid || !count ? undefined : 'error-text'}
                         style={{userSelect: "none", fontSize: 14}}>{count}</div>
                </div>
            );
            const untreated = (wing.filters.mapping['treatment.ללא'] || []).length,
                discharged = (wing.filters.mapping['treatment.שחרור'] || []).length,
                count = Object.keys(wing.patients).length,
                hospitalized = count - untreated - discharged;
            return <Col key={i} span={12}>
                <Card title={<div style={{display: 'flex', flexDirection: 'row', width: '100%'}}>
                    {wing.details.name}&nbsp;-&nbsp;<b>{count}</b>&nbsp;מטופלים.ות&nbsp;
                    <Tooltip title={`${untreated} ללא החלטה / ${hospitalized} אשפוז / ${discharged} שחרור`}>
                        <Progress percent={100 * (discharged + hospitalized) / count}
                                  success={{percent: 100 * discharged / count}} showInfo={false}/>
                    </Tooltip>
                </div>} style={{
                    maxHeight: 180,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    marginBottom: 16,
                }} hoverable onClick={() => {
                    navigate(wingId === wing.details.key && onOk ? () => onOk() :
                        generatePath(WING_URL, {department: department, wing: wing.details.key}))
                }} bodyStyle={{
                    overflowY: 'auto',
                    flex: 1,
                }} headStyle={{
                    backgroundColor: wingId === wing.details.key ? '#5f9ea0' : undefined
                }}>
                    <div style={{
                        display: "flex",
                        flexWrap: "wrap",
                        justifyContent: "center",
                        gap: "1rem",
                    }}>
                        {actions}
                    </div>
                </Card>
            </Col>
        })}
    </Row>
}
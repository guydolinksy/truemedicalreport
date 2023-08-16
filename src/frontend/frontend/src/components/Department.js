import React, {useContext} from "react";
import {Card, Col, Row, Spin, Tooltip} from "antd";
import {generatePath} from "react-router-dom";

import {createContext} from "../hooks/DataContext";
import {WING_URL} from "../pages/WingView";
import {useNavigate} from "react-router";
import {CustomIcon} from "./CustomIcon";
import Moment from "react-moment";
import {loginContext} from "./LoginContext";

const SHOW_ACTIONS = ['not-awaiting', 'doctor.exam', 'nurse.exam', 'imaging', 'laboratory', 'treatment.ללא'];

const departmentDataContext = createContext(null);
export const Department = ({department}) => {
    const uri = `/api/departments/${department}`;
    const navigate = useNavigate();
    const {userSettings} = useContext(loginContext);

    return <departmentDataContext.Provider url={uri} defaultValue={{wings: []}}>
        {({loading, value}) => <Row gutter={16}>
            {loading ? <Spin/> : value.wings.map((wing, i) => {
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
                    ({count, title, icon, duration, valid}) => <div
                        style={{display:"flex",flexDirection:"column", alignItems:"center", padding:5,border:"1px solid $f0f0f0"}}>
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
                return <Col key={i} span={12}>
                    <Card title={<span>{wing.details.name} - <b>{wing.count}</b> מטופלים.ות</span>}
                          style={{marginBottom: 16}} hoverable onClick={() =>
                        navigate(generatePath(WING_URL, {department: department, wing: wing.details.key}))
                    }>
                        <div style={{display:"flex",flexWrap:"wrap",justifyContent:"center",gap:"1rem"}}>
                            {actions}
                        </div>
                    </Card>
                </Col>
            })}
        </Row>}
    </departmentDataContext.Provider>
}
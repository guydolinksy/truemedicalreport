import React from "react";
import {Card, Col, Row, Spin} from "antd";
import {generatePath} from "react-router-dom";

import {createContext} from "../hooks/DataContext";
import {WING_URL} from "../pages/WingView";
import {useNavigate} from "react-router";
import {CustomIcon} from "./CustomIcon";

const SHOW_ACTIONS = ['not-awaiting', 'doctor.exam', 'nurse.exam', 'imaging', 'laboratory', 'referrals'];

const departmentDataContext = createContext(null);
export const Department = ({department}) => {
    const uri = `/api/departments/${department}`;
    const navigate = useNavigate();

    return <departmentDataContext.Provider url={uri} defaultValue={{wings: []}}>
        {({loading, value}) => <Row gutter={16}>
            {loading ? <Spin/> : value.wings.map((wing, i) => {
                const toActions = filter => [({
                    key: filter.key,
                    icon: filter.icon,
                    count: filter.count,
                    title: filter.title,
                    valid: filter.valid,
                })].concat(...(filter.children || []).map(toActions))
                const actions = [].concat(...wing.filters.awaiting.map(toActions)).filter(({key}) => SHOW_ACTIONS.includes(key)).map(
                    ({count, title, icon, valid}) => <div>
                        <div style={{fontSize: 12}}>{title}{icon &&
                            <span>&nbsp;<CustomIcon status={'processing'} icon={icon}/></span>}</div>
                        <div className={valid || !count ? undefined : 'error-text'}
                             style={{userSelect: "none", fontSize: 14}}>{count}</div>
                    </div>
                );
                return <Col key={i} span={12}>
                    <Card title={wing.details.name} actions={actions} style={{marginBottom: 16}} hoverable
                          onClick={() =>
                              navigate(generatePath(WING_URL, {department: department, wing: wing.details.key}))
                          }/>
                </Col>
            })}
        </Row>}
    </departmentDataContext.Provider>
}
import React from "react";
import {Card, Col, Row, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUser, faUserDoctor} from "@fortawesome/free-solid-svg-icons";
import {generatePath} from "react-router-dom";

import {createContext} from "./DataContext";
import {WING_URL} from "../pages/WingView";
import {useNavigate} from "react-router";

const departmentDataContext = createContext(null);
export const Department = ({department}) => {
    const uri = `/api/departments/${department}`;
    const navigate = useNavigate();

    return <departmentDataContext.Provider url={uri} defaultValue={[]}>
        {({loading, value}) => <Row gutter={16}>
            {loading ? <Spin/> : value.map((wing, i) => {
                const actions = [
                    <Tooltip overlay={"מטופלים המשוייכים לאגף"}><span style={{userSelect: "none"}}>
                    <FontAwesomeIcon icon={faUser}/>&nbsp;{wing.patient_count}
                </span></Tooltip>,
                    <Tooltip overlay={"מטופלים הממתינים לרופא.ה"}><span style={{userSelect: "none", color: "red"}}>
                    <FontAwesomeIcon icon={faUserDoctor}/>&nbsp;{wing.waiting_patient}
                </span></Tooltip>];
                return <Col key={i} span={12}>
                    <Card title={wing.name} actions={actions} style={{marginBottom: 16}} hoverable onClick={() =>
                        navigate(generatePath(WING_URL, {department: department, wing: wing.key}))
                    }/>
                </Col>
            })}
        </Row>}
    </departmentDataContext.Provider>
}
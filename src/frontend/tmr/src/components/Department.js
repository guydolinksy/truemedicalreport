import React from "react";
import {Card, Col, Row, Spin, Tooltip} from "antd";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUser, faUserDoctor} from "@fortawesome/free-solid-svg-icons";
import {FullscreenOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";

import {createContext} from "./DataContext";

const departmentDataContext = createContext(null);
export const Department = () => {
    const uri = `/api/departments/`;
    return <departmentDataContext.Provider url={uri} updateURL={uri} socketURL={uri} fetchOnMount defaultValue={[]}>
        {({loadingData, getData}) => <Row gutter={16}>
            {loadingData ? <Spin/> : (getData([]) || []).map((wing, i) => {
                const actions = [
                    <Tooltip overlay={"מטופלים המשוייכים לאגף"}><span style={{userSelect: "none"}}>
                    <FontAwesomeIcon icon={faUser}/>&nbsp;{wing.patient_count.patient_count}
                </span></Tooltip>,
                    <Tooltip overlay={"מטופלים הממתינים לרופא.ה"}><span style={{userSelect: "none", color: "red"}}>
                    <FontAwesomeIcon icon={faUserDoctor}/>&nbsp;{wing.waiting_patient.patient_count}
                </span></Tooltip>];
                const extra = <Link to={`/wing/${wing.oid}`}><FullscreenOutlined/></Link>
                return <Col key={i} span={12}>
                    <Card title={wing.name} actions={actions} extra={extra} style={{marginBottom: 16}}>

                    </Card>
                </Col>
            })}
        </Row>}
    </departmentDataContext.Provider>
}
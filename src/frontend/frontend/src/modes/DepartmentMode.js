import React, {useContext, useMemo} from "react";
import {Card, Col, Progress, Space, Layout, Tooltip} from "antd";
import {generatePath, useParams} from "react-router-dom";
import {useNavigate} from "react-router";
import {CustomIcon} from "../components/CustomIcon";
import Moment from "react-moment";
import {CloseCircleOutlined} from "@ant-design/icons";
import {loginContext} from "../components/LoginContext";
import Axios from "axios";
import {DepartmentItemsCard} from "../components/settings/DepartmentItemsCard";
import {viewsContext} from "../contexts/ViewsContext";
import {createContext} from "../contexts/DataContext";
import {MODE_URL} from "../pages/ModeView";

const {Content} = Layout;
export const departmentDataContext = createContext();
const hideSetting = (e, wing, userSettings, setting) => {
    if (e.stopPropagation) e.stopPropagation();
    console.log(setting)
    Axios.post('/api/settings/statistics', {
        statistics: Object.assign({},
            ...Object.entries(userSettings.statistics).filter(
                ([k, v]) => k !== wing.key
            ).map(
                ([k, v]) => ({[k]: v})
            ),
            {[wing.key]: (userSettings.statistics[wing.key] || []).concat([[setting, false]])}
        )
    }).then(() => {
        console.log("success")
        document.location.reload();
    }).catch(error => {
        if (Axios.isCancel(error))
            return;
        console.log("failed")
    });

}

const toActions = filter => [({
    key: filter.key,
    icon: filter.icon,
    count: filter.count,
    title: filter.title,
    duration: filter.duration,
    valid: filter.valid,
})].concat(...(filter.children || []).map(toActions))

export const DepartmentMode = ({onOk}) => {
    const navigate = useNavigate();
    const {userSettings} = useContext(loginContext);
    const {value: viewsValue} = useContext(viewsContext.context);

    const {view} = useParams();

    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);

    return <departmentDataContext.Provider url={`/api/departments/${curView.department_id}`}>
        {({value}) => <Content>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", height: '100%'}}>
                <div style={{display: "flex", flexDirection: "column", alignItems: "center", flex: 1}}>
                    <div style={{
                        display: "flex",
                        flexDirection: "column",
                        maxWidth: '80vw',
                        maxHeight: '80vh',
                        justifyContent: 'center',
                        alignItems: 'center',
                        gap: 16,
                    }}>
                        <div style={{overflowY: 'auto'}}>
                            <Space style={{justifyContent: 'center'}} wrap>
                                {value.getWings.wings.filter(wing => wing.patients_count > 0).map(wing => {
                                    const actions = [].concat(
                                        ...wing.filters.doctors.map(toActions),
                                        ...wing.filters.awaiting.map(toActions),
                                        ...wing.filters.treatments.map(toActions),
                                        ...wing.filters.time_since_arrival.map(toActions),
                                    ).filter(({key}) => {
                                        const filters = [].concat(
                                            userSettings.statistics[wing.key] || [],
                                            userSettings.statistics.default || []
                                        );
                                        if (filters.some(([regex, result]) => result && key.match(regex)))
                                            return true
                                        return !filters.some(([regex, result]) => !result && key.match(regex));
                                    }).map(({count, title, icon, duration, valid, key}) => <Space key={key} style={{
                                            alignItems: "center",
                                            padding: 5,
                                            border: "1px solid #f0f0f0"
                                        }}>
                                            <CloseCircleOutlined className="departmentActionItem" onClick={(e) => {
                                                hideSetting(e, wing, userSettings, key)
                                            }} style={{alignSelf: "start"}}/>
                                            <div className={valid || !count ? undefined : 'error-text'}
                                                 style={{userSelect: "none", fontSize: 14}}>{count}</div>
                                            <div style={{fontSize: 12}}>
                                                {icon && <span>&nbsp;<CustomIcon status={'processing'} icon={icon}/></span>}
                                            </div>
                                            <div style={{fontSize: 12}}>
                                                {title}
                                            </div>
                                            {![null, undefined].includes(duration) &&
                                                <div style={{userSelect: "none", fontSize: 14}}>
                                                    <Tooltip overlay={'זמן המתנה ממוצע'}>
                                                        <Moment interval={1000} durationFromNow format={'H[h]mm[m]'}
                                                                date={duration}/>
                                                    </Tooltip>
                                                </div>}
                                        </Space>
                                    );
                                    const untreated = ((wing.filters.mapping.find(
                                            m => m.key === 'treatment.ללא'
                                        ) || {}).values || []).length,
                                        discharged = ((wing.filters.mapping.find(
                                            m => m.key === 'treatment.שחרור'
                                        ) || {}).values || []).length,
                                        count = wing.patients_count,
                                        hospitalized = count - untreated - discharged;
                                    return <Col key={wing.key} span={12}>
                                        <Card
                                            title={<div style={{display: 'flex', flexDirection: 'row', width: '100%'}}>
                                                {wing.name}&nbsp;-&nbsp;<b>{count}</b>&nbsp;מטופלים.ות&nbsp;
                                                <Tooltip
                                                    title={`${untreated} ללא החלטה / ${hospitalized} אשפוז / ${discharged} שחרור`}>
                                                    <Progress percent={100 * (discharged + hospitalized) / count}
                                                              success={{percent: 100 * discharged / count}}
                                                              showInfo={false}/>
                                                </Tooltip>
                                            </div>} style={{
                                            maxHeight: 180,
                                            height: '100%',
                                            width: 'min(600px, 30vw)',
                                            minWidth: 350,
                                            display: 'flex',
                                            flexDirection: 'column',
                                            marginBottom: 16,
                                        }} hoverable onClick={() => {
                                            if (curView.wing_id === wing.key && onOk)
                                                onOk()
                                            else
                                                navigate(generatePath(MODE_URL, {
                                                    view: viewsValue.getViews.views.find(v =>
                                                        v.department_id === curView.department_id && v.wing_id === wing.key
                                                    ).key,
                                                    mode: 'wing',
                                                }))
                                        }} bodyStyle={{
                                            overflowY: 'auto',
                                            flex: 1,
                                        }} headStyle={{
                                            backgroundColor: curView.wing_id === wing.key ? '#5f9ea0' : undefined
                                        }}>
                                            <div style={{
                                                display: "flex",
                                                flexWrap: "wrap",
                                                flexDirection: "row",
                                                justifyContent: "center",
                                                gap: "1rem",
                                            }}>
                                                {actions}
                                            </div>
                                        </Card>
                                    </Col>
                                })}
                            </Space>
                        </div>
                        <DepartmentItemsCard/>
                    </div>
                </div>
            </div>
        </Content>}
    </departmentDataContext.Provider>
}
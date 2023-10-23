import {Badge, Button, Input, Select, Space} from "antd";
import {BellOutlined, ManOutlined, ReadOutlined, SettingOutlined, WomanOutlined} from "@ant-design/icons";
import React, {useContext, useEffect, useState} from "react";
import {Link, useLocation, useNavigate, useParams} from "react-router-dom";
import {loginContext} from "./LoginContext";
import {menuContext} from "../pages/MainView";


const {Search} = Input;
export const MainMenu = () => {
    const {user, userSettings} = useContext(loginContext);
    const {wing, department} = useParams();
    const [patients, setPatients] = useState([]);

    const {value, loading} = useContext(menuContext.context);
    useEffect(() => {
        setPatients(Object.entries((value.find(d => d.key === department) || {patients: {}}).patients).sort(
            ([o1, a], [o2, b]) => a.info.name.localeCompare(b.info.name)
        ).map(([oid, patient]) => {
            const department = value.find(d => d.key === patient.admission.department_id),
                wing = department.wings.find(w => w.details.key === patient.admission.wing_id)
            return {
                oid: oid,
                id: patient.info?.id_,
                name: patient.info?.name,
                comment: patient.comment,
                department_id: patient.admission.department_id,
                wing_id: patient.admission.wing_id,
                wing: {
                    name: wing.details.name,
                    color: wing.details.color,
                },
                gender: patient.info?.gender,
            }
        }))
    }, [value, department]);


    const [notifications, setNotifications] = useState(1);

    const navigate = useNavigate();
    const {hash} = useLocation();


    const wings = (value.find(d => d.key === department) || {}).wings || [];

    return <div style={{display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
        <Link to={'/'} style={{marginLeft: 14, color: 'white'}}><img src={'/tmr.png'} height={40}/> תמ״ר</Link>
        {!loading && <Space>
            <Select style={{width: 300}} value={department} placeholder={'בחר.י מחלקה'}
                    options={value.map(d => ({
                        value: d.key.toString(),
                        label: d.name,
                    }))} onSelect={value => navigate(`/departments/${value}`)}/>
            <Select allowClear style={{width: 300}} value={wing} placeholder={'בחר.י אגף'} disabled={!department}
                    options={wings.map(w => ({
                        value: w.details.key,
                        label: <span>{w.details.name} - <b>{Object.keys(w.patients).length}</b> מטופלים.ות</span>,
                    }))} onChange={value => navigate(`/departments/${department}` + (value ? `/wings/${value}` : ''))}/>
        </Space>}
        <div style={{flex: "1 0 0px"}}/>
        <Space>
            {patients.length > 0 && <Select style={{width: 300}} showSearch placeholder={'חיפוש מטופל.ת:'} onChange={
                (value, option) => {
                    console.log(value, option)
                    navigate(
                        `/departments/${option.department_id}/wings/${option.wing_id}#locate#${value}#open`
                    )
                }
            } filterOption={
                (search, option) => option.id.includes(search) || option.name.includes(search) || (option.comment || '').includes(search)
            } options={patients.map(patient => ({
                value: patient.oid,
                id: patient.id,
                name: patient.name,
                comment: patient.comment,
                department_id: patient.department_id,
                wing_id: patient.wing_id,
                label: <div style={{width: '100%', justifyContent: 'space-between', display: 'flex'}}>
                    <span><span className={`gender-${patient.gender}`}>
                        {patient.gender === 'male' && <ManOutlined/>}
                        {patient.gender === 'female' && <WomanOutlined/>}
                    </span>&nbsp;{user.anonymous ? '---' : patient.name}{patient.comment ? ` (${patient.comment})` : ''}</span>
                    <span style={{color: patient.wing.color}}>{patient.wing.name}</span>
                </div>
            }))} value={null}
            />}
            {wing && <Button type={'text'} onClick={() => navigate('#help')}>
                <ReadOutlined style={{fontSize: 16, color: 'white'}}/>
            </Button>}
            {wing && <Button type={'text'} onClick={() => navigate('#notifications')} style={{color: 'white'}}>
                <Badge size={'small'} count={notifications}>
                    <BellOutlined style={{fontSize: 16, color: 'white'}}/>
                </Badge>
            </Button>}
            {user && !wing && <Button type={'text'} onClick={() => navigate('#settings')}>
                <SettingOutlined style={{fontSize: 16, color: 'white'}}/>
            </Button>}
        </Space>
    </div>
}

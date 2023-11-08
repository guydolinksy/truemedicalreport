import React, {useCallback, useContext, useEffect, useRef, useState} from "react";
import Axios from "axios";
import {Alert, Button, Card, Checkbox, Form, Modal, Dropdown, Space, Input} from "antd";
import {loginContext} from "../LoginContext";
import {hashMatchContext} from "../HashMatch";
import {useNavigate} from 'react-router-dom';
import {viewsContext} from "../../pages/ViewsView";
import {useField} from "../../hooks/fieldHook";
import {PlusCircleOutlined, DownOutlined, LeftOutlined} from '@ant-design/icons'

const viewTypes = [{key: "department", name: 'מחלקה'}, {key: "wing", name: 'אגף'}, {key: "wing", name: 'פילטר'}]
const modeTypes = [{key: "wing", name: 'מטופלים'}, {key: "layout", name: 'מיקום'}, {key: "status", name: 'סטטוס'}]

const renderDropdown = (types, setter) => {
    return types.map((type, idx) => {
        return {
            key: "" + idx,
            label: (
                <div onClick={() => setter(type)}>{type.name}</div>
            )
        }
    })
}

export const DepartmentItemsCard = () => {
    const {value: viewsValue} = useContext(viewsContext.context)
    const {user, userSettings} = useContext(loginContext);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [canSubmit, setCanSubmit] = useState(false);
    const [initialValue, setInitialValue] = useState(userSettings.statistics);
    const [formattedData, setFormattedData] = useState({components: []});
    const [selectedView, setSelectedView] = useState({key: "department", name: 'מחלקה'});
    const [selectedMode, setSelectedMode] = useState({key: 'status', name: 'סטטוס'});
    const [values,setValues] = useState({})
    const form = useRef();

    useEffect(() => {
        setInitialValue(userSettings.statistics)
    }, [userSettings.statistics]);

    const onFinish = useCallback((values) => {
        Axios.post('/api/settings/statistics', values).then(() => {
            setSuccess(true);
            document.location.reload();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });

    }, []);

    useEffect(() => {
        fetchFormattedData(selectedView.key, selectedMode.key)
    }, [selectedView, selectedMode])

    const renderValue = (departmentItem) => <Checkbox.Item>
        {departmentItem}
    </Checkbox.Item>

    const fetchFormattedData = (view, mode) => {
        Axios.get(`/api/settings/view/${view}/mode/${mode}/info/format`).then(response => {
            console.log(response.data)
            setFormattedData(response.data)
        }).catch(err => console.log(err))
    }

    const onChange = useCallback((changedValues, allValues) => {
        setError(false);
        setCanSubmit(true);
    }, [setError, setCanSubmit]);

    const navigate = useNavigate();

    const getValues = (path,value) => {
        console.log(path,value)
        if(path.length > 0 ) {
            const last = path.pop()
            return getValues(path, {[last]: value})
        } else {
            console.log(path,value)
            // setValues()
        }
    }

    useEffect(() => { console.log(values)},[values])

    const {matched} = useContext(hashMatchContext);
    return <Modal open={user && matched(['settings'])} title={'הגדרות:'} footer={null}
                  onCancel={() => navigate('#')} width={1200}>
        <Card title={'הגדרות הצגת פרטי מחלקה'}>
            {success ? <Alert message={'הגדרות התצוגה נשמרו בהצלחה'} type={"success"} closable
                              afterClose={() => setSuccess(false)}/> :
                <Form ref={form} name={"display"} title={'הגדרות הצגת פרטי מחלקה'} onFinish={onFinish}
                      onValuesChange={onChange}
                      initialValues={initialValue}>
                    <Form.Item name={"views"} label={"תצוגה:"} rules={[(() => ({
                        validator(_, value) {
                            if (!value || !error)
                                return Promise.resolve();
                            return Promise.reject(new Error('שגיאת נתונים , יש לנסות שנית!'));
                        }
                    }))]}>
                        {/*<Checkbox.Group>*/}
                        {/*    {!!initialValue?.length && initialValue.map(value => renderValue(value))}*/}
                        {/*</Checkbox.Group>*/}
                    </Form.Item>
                    <Form.Item name={"views"} label={"תצוגה:"}>
                        <Dropdown menu={{items: renderDropdown(viewTypes, setSelectedView)}}>
                            <a onClick={(e) => e.preventDefault()}>
                                <Space>
                                    {selectedView.name}
                                </Space>
                            </a>
                        </Dropdown>
                    </Form.Item>
                    <Form.Item name={"modes"} label={"מצבים:"}>
                        <Dropdown menu={{items: renderDropdown(modeTypes, setSelectedMode)}}>
                            <a onClick={(e) => e.preventDefault()}>
                                <Space>
                                    {selectedMode.name}
                                </Space>
                            </a>
                        </Dropdown>
                    </Form.Item>
                    <Form.Item name={"config"} label={"תצורה:"}>
                        <RenderObject name={'components'} content={formattedData.components} path={['components']}
                                    setValue={getValues}  customRenderers={{style: RenderJSON}}/>
                    </Form.Item>
                    <Form.Item>
                        <Button disabled={!canSubmit} type={"primary"} htmlType={"submit"}>מחיקה</Button>
                    </Form.Item>
                </Form>}
        </Card>
    </Modal>
}

const RenderJSON = ({value, setValue, path}) => {
    return <Input value={JSON.stringify(value)} onChange={e => setValue(path, JSON.parse(e.target.value))}/>
}

const RenderObject = ({name, content, setValue, path, customRenderers = {}}) => {
    const [open, setOpen] = useState(path.length < 2)
    if (content === undefined)
        return <div>Undefined</div>
    if (typeof content === 'string') {
        return <span>
            <Input addonBefore={convertToHebrew(name)} style={{width: 'fit-content'}} value={content}
                   onChange={e => setValue(path,e.target.value)}/>
        </span>
    }
    if (content.length)
        return <Card style={{width: 'fit-content'}} title={<span>
            {open ? <DownOutlined/> : <LeftOutlined/>} {convertToHebrew(name)}
        </span>} size={'small'} extra={<PlusCircleOutlined/>}
                     onClick={e => {
                         setOpen(!open);
                         e.stopPropagation()
                     }} bodyStyle={{display: open ? undefined : 'none'}}>
            {open && content.map((item, i) => <RenderObject key={i} content={item} setValue={setValue}
                                                            path={path.concat(i)}
                                                            customRenderers={customRenderers}/>)}
        </Card>
    if (typeof content === 'object')
        return <Card style={{width: 'fit-content'}} title={<span>
            {open ? <DownOutlined/> : <LeftOutlined/>} {convertToHebrew(name)|| content.name}
        </span>} size={'small'}
                     onClick={e => {
                         setOpen(!open);
                         e.stopPropagation()
                     }} bodyStyle={{display: open ? undefined : 'none'}}>
            {open && Object.entries(content).map(([k, v]) => {
                const Renderer = customRenderers[k] || RenderObject
                if (k === 'style') {
                    return;
                }

                if (k === 'options') {
                    console.log(k, v)
                }

                return <div key={k} style={{whiteSpace: 'nowrap'}}>
                    <Renderer name={k} content={v} setValue={setValue} path={path.concat(k)}
                              customRenderers={customRenderers}/>
                </div>
            })}
        </Card>
    return <div>Unknown</div>
}

const convertToHebrew = (value) => {
    switch (value) {
        case "type":
            return "סוג"
        case "config":
            return "תצורה"
        case "components":
            return "רכיבים"
        case "key":
            return "מפתח"
        case "name":
            return "שם"
        case "short_name":
            return "ראשי תיבות"
        case "department_id":
            return "מס מחלקה"
        case "wing_id":
            return "סוג אגף"
        case "color":
            return "צבע"
        case "patients_count":
            return "מספר מטופלים"
        case "patients":
            return "מטופלים"
        case "modes":
            return "מצבים"
        case "default_mode":
            return "מצב ברירת מחדל"
        case "gender":
            return "מין"
        case "id":
            return "ת.ז."
        case "info":
            return "מידע"
        case "oid":
            return "מזהה מטופל"
        case "comment":
            return "תגובה"
        case "options":
            return "אפשרויות"
        case "customizers":
            return "התאמות"
        default:
            break;
    }
}
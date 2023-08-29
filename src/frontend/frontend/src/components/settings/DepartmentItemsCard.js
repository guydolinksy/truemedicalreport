import React, {useCallback, useEffect, useRef, useState} from "react";
import Axios from "axios";
import {Alert, Button, Card, Checkbox, Form} from "antd";

//TODO: add a dictionary so the label will be in hebrew
const settingToOption = (setting) => {return {label:setting, value:setting}}

export const DepartmentItemsCard = () => {
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(false);
    const [hiddenSettings, setHiddenSettings] = useState({});
    const [selectedSettings,setSelectedSettings] = useState({})

    const form = useRef();
     const handleCheckboxChange = (wing, checkedValues) => {
        setSelectedSettings((prevSelectedSettings) => ({
          ...prevSelectedSettings,
          [wing]: checkedValues,
        }));
      };
     useEffect(() => {
         setError(!(!!Object.keys(selectedSettings).length &&
             Object.keys(selectedSettings).some(setting=> !!selectedSettings[setting].length)))
     },[selectedSettings])

    useEffect(() => {
        const s = Axios.CancelToken.source();
        Axios.get('/api/settings/display', {cancelToken: s.token}).then(response => {
            setHiddenSettings(response.data?.statistics);
            form.current.resetFields();
        }).catch(error => {
            if (Axios.isCancel(error))
                return;
            setError(true);
        });
        return () => s.cancel();
    }, []);

    const onFinish = async () => {
        const settingsToKeep = {}
        Object.keys(hiddenSettings).forEach(wing => {
            if (!!selectedSettings[wing]) settingsToKeep[wing] = hiddenSettings[wing]
                .filter(setting => !selectedSettings[wing].some(selectedSetting => setting[0] === selectedSetting))
        })
        Axios.post('/api/settings/display', {statistics: settingsToKeep}).then(() => {
            document.location.reload();
        }).catch(error => {
            // if (Axios.isCancel(error))

        });
    }

  const HiddenSettingsComponent = () =>
    !!hiddenSettings ? (
      <div>
        {Object.keys(hiddenSettings).map((wing, index) => (
            <>
                {!!hiddenSettings[wing].length && <div key={wing}>
                <div>{wing}</div>
                <Checkbox.Group
                  value={selectedSettings[wing]} // Set checked values using the state
                  options={hiddenSettings[wing].map((setting) => settingToOption(setting[0]))}
                  onChange={(checkedValue) => handleCheckboxChange(wing, checkedValue)}
                />
              </div>}
            </>
        ))}
      </div>
    ) : (
      <div>אין הגדרות מוסתרות</div>
    );


    return <Card title={'הגדרות הצגת פרטי מחלקה'}>
        {success ? <Alert message={'הגדרות התצוגה נשמרו בהצלחה'} type={"success"} closable
                          afterClose={() => setSuccess(false)}/> :
            <Form ref={form} name={"display"} title={'הגדרות הצגת פרטי מחלקה'}
                  onFinish={onFinish}
                  initialValues={hiddenSettings}>
                <Form.Item name={"items"} label={"לא להציג:"} rules={[(() => ({
                    validator(_, value) {
                        if (!value || !error)
                            return Promise.resolve();
                        return Promise.reject(new Error('שגיאת נתונים , יש לנסות שנית!'));
                    }
                }))]}>
                        <HiddenSettingsComponent />
                </Form.Item>
                <Form.Item>
                    <Button disabled={error} type={"primary"} htmlType={"submit"}>עדכן</Button>
                </Form.Item>
            </Form>}
    </Card>
}
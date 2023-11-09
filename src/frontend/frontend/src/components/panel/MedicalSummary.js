import {Card, Modal, Space} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';
import {iframeModal} from "../modals";
import {faWindowRestore} from "@fortawesome/free-solid-svg-icons";

export const MedicalSummary = (params) => {
    const {value} = useContext(patientDataContext.context);
    const [modal, modalContext] = Modal.useModal();

    return <Card title={
        <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
            <span>סיכום רפואי</span>
            <Space align="center">
                {iframeModal(modal, faWindowRestore, "צפה.י בקמיליון", value.medical_summary_link)}
            </Space>
        </div>
    }>
        {modalContext}
    </Card>

}
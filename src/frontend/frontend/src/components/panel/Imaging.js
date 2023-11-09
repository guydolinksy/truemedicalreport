import {Badge, Card, Empty, Modal} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext} from 'react';
import {htmlModal, iframeModal} from "../modals";
import {faFileLines, faXRay} from "@fortawesome/free-solid-svg-icons";
import {hashMatchContext} from "../HashMatch";
import {loginContext} from "../LoginContext";

export const Imaging = (params) => {
    const {value} = useContext(patientDataContext.context);
    const [modal, modalContext] = Modal.useModal();
    const {matched} = useContext(hashMatchContext);
    const {patient} = useContext(loginContext);

    return <Card title={
        <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
            <span>הדמיות</span>
            <div><Badge style={{backgroundColor: '#1890ff'}} count={Object.keys(value.imaging).length}
                        size={"small"}/></div>
        </div>
    }>
        {modalContext}
        {Object.keys(value.imaging).length ? Object.values(value.imaging).map((image, i) =>
            <p key={i} style={{
                animation: matched(['info', patient, 'imaging', `${image.external_id}`]) ? 'highlight 2s ease-out' : undefined
            }}>
                {image.title} - {image.status_text}
                {iframeModal(modal, faXRay, "דימות", image.link)}
                {htmlModal(modal, faFileLines, "פענוח", image.interpretation)}
            </p>
        ) : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו הדמיות'}/>}
    </Card>
}
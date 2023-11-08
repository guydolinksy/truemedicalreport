import {Badge, Button, Card, Empty, Modal, Space} from 'antd';
import {patientDataContext} from "../card/PatientBase";
import React, {useContext, useState} from 'react';
import {iframeModal} from "../modals";
import moment from "moment";
import {faWindowRestore} from "@fortawesome/free-solid-svg-icons";
import {RelativeTime} from "../RelativeTime";
import {hashMatchContext} from "../HashMatch";
import {loginContext} from "../LoginContext";

const labStatuses = {
    1: ' - הוזמן',
    2: ' - שויכו דגימות',
    3: ' - בעבודה',
    4: ' - תוצאות',
}


const RANGE_CODE_TO_DESCRIPTION = {
    "H": "High",
    "L": "Low",
    "VH": "Very High",
    "VL": "Very Low",
    "HH": "Panic High",
    "LL": "Panic Low",
    "JESUS": "Call the nearby priest"
}

const displayLab = (lab, displayAllResults, matched, patient) => {

    const rangeToResults = {};
    Object.values(lab.results).forEach(result => {
        if (!rangeToResults.hasOwnProperty(result.range)) {
            rangeToResults[result.range] = []
        }

        rangeToResults[result.range].push(result);
    })

    const ranges = Object.keys(rangeToResults);

    let badgeColor = "#000000";
    if (ranges.some(range => ["HH", "LL"].includes(range)))
        badgeColor = "#FF0000";
    else if (ranges.some(range => ["VH", "VL"].includes(range)))
        badgeColor = "#FF00FF";
    else if (ranges.some(range => ["H", "L", "X"].includes(range)))
        badgeColor = "#FFA500";
    else if (lab.status === 4 && ranges.every(range => range === "N"))
        badgeColor = "#00FF00";

    const rangesToConsiderAsBad = ["HH", "LL", "VH", "VL"].concat(displayAllResults ? ["H", "L"] : []).map(
        status => rangeToResults[status] || []
    )

    let badgeText = '-';
    if (lab.status === 4) {
        const badResultsCount = rangesToConsiderAsBad.map(results => results.length).reduce((a, b) => a + b)
        if (badResultsCount)
            badgeText = badResultsCount.toString()
        else if (ranges.every(range => range === "N"))
            badgeText = "✓";
        else
            badgeText = "X";
    }

    return <p key={`${lab.category}-${lab.ordered_at}`} style={{
        animation: matched(['info', patient, 'labs', encodeURIComponent(lab.category), lab.ordered_at.replace(/:/g, '-').replace(/\+/g, '-')]) ? 'highlight 2s ease-out' : undefined,
        direction: "rtl"
    }}>
        <p>
            <span><Badge style={{backgroundColor: badgeColor}} count={badgeText}/>&nbsp;
                {lab.category_display_name} {labStatuses[lab.status]} {ranges.some(range => range === "X") && ' - פסול'}
                <RelativeTime style={{fontSize: 12, float: "left"}} date={lab.ordered_at}/>
            </span>
        </p>
        <p style={{marginRight: "2rem"}}>
            {rangesToConsiderAsBad.flat().map((result, i) => <p key={i}>
                <span>{RANGE_CODE_TO_DESCRIPTION[result.range]} {result.test_type_name}: {result.result} {result.units}</span>
            </p>)}
            {displayAllResults && (rangeToResults[null] || []).length > 0 && <p>
                הוזמנו: {rangeToResults[null].map(result => result.test_type_name).join(', ')}
            </p>}
        </p>
    </p>
}

export const Labs = (params) => {
    const [displayAllResults, setDisplayAllResults] = useState(false)
    const [modal, modalContext] = Modal.useModal();
    const {value} = useContext(patientDataContext.context);
    const {matched} = useContext(hashMatchContext);
    const {patient} = useContext(loginContext);

    return <Card header={
        <div style={{width: '100%', display: "flex", flexFlow: "row nowrap", justifyContent: "space-between"}}>
            <span>מעבדה</span>
            <Space align="center">
                <Badge style={{backgroundColor: '#1890ff'}} count={Object.keys(value.labs).length}
                       size={"small"}/>
                {iframeModal(modal, faWindowRestore, "צפה.י בקמיליון", value.lab_link)}
            </Space>
        </div>
    }>

            {modalContext}
        {Object.keys(value.labs).length ? <>
            {Object.values(value.labs).sort(
                (a, b) => moment(a.ordered_at).isSame(b.ordered_at) ? 0 :
                    moment(a.ordered_at).isBefore(b.ordered_at) ? 1 : -1
            ).map(
                lab => displayLab(lab, displayAllResults, matched, patient)
            )}
            <Button onClick={() => setDisplayAllResults(!displayAllResults)}>
                <span>{displayAllResults ? "הסתר בדיקות" : "הצג בדיקות"}</span>
            </Button>
        </> : <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו בדיקות מעבדה'}/>}
    </Card>

}
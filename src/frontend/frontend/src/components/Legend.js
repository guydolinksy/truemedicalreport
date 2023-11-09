import React, {Suspense, useContext} from "react";
import {DarkTheme, LightTheme} from "../themes/ThemeContext";
import {Badge, Drawer} from "antd";
import {CustomIcon} from "./CustomIcon";
import {hashMatchContext} from "./HashMatch";
import {loginContext} from "./LoginContext";
import {useNavigate} from 'react-router-dom';

export const Legend = ({}) => {
    const {userSettings} = useContext(loginContext)
    const navigate = useNavigate();
    const {matched} = useContext(hashMatchContext);
    return <Drawer title={'מקרא'} placement={"left"} open={matched(['help'])} onClose={() => navigate('#')}>
        <div style={{display: "flex", flexDirection: "column", rowGap: 5}} className={userSettings.theme}>
            <Suspense fallback={<span/>}>
                {userSettings.theme === 'dark-theme' ? <DarkTheme/> : <LightTheme/>}
            </Suspense>
            <div><Badge className={'gender-male'}>ישראל ישראלי</Badge> - זכר</div>
            <div><Badge className={'gender-female'}>ישראלה ישראלית</Badge> - נקבה</div>
            <div><Badge className={'border-solid severity-border severity-1'}>דחיפות 1</Badge></div>
            <div><Badge className={'border-solid severity-border severity-2'}>דחיפות 2</Badge></div>
            <div><Badge className={'border-solid severity-border severity-3'}>דחיפות 3</Badge></div>
            <div><Badge className={'border-solid severity-border severity-4'}>דחיפות 4</Badge></div>
            <div><Badge className={'border-solid severity-border severity-5'}>דחיפות 5</Badge></div>
            <div><Badge className={'status-bar status-unassigned'}>&nbsp;לא שויך.ה רופא.ה</Badge></div>
            <div><Badge className={'status-bar status-undecided'}>&nbsp;שויך.ה רופא.ה אך אין החלטה על יעד</Badge></div>
            <div><Badge className={'status-bar status-decided'}>&nbsp;שויך.ה רופא.ה והוחלט יעד אשפוז/שחרור</Badge></div>
            <div><CustomIcon status={"error"} icon={"referral"}/>&nbsp;הפנייה מתעכבת</div>
            <div><CustomIcon status={"processing"} icon={"laboratory"}/>&nbsp;מעבדה בעיבוד</div>
            <div><CustomIcon status={"success"} icon={"imaging"}/>&nbsp;הדמייה הושלמה או פוענחה</div>
        </div>
    </Drawer>
}
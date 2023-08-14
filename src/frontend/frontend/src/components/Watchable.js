import {Button, Tooltip} from "antd";
import {BellOutlined, BellFilled} from "@ant-design/icons";
import {patientDataContext} from "./Patient";
import {useContext, useState} from "react";

export const Watchable = ({watchKey, updateAt, children}) => {
    const {value, update} = useContext(patientDataContext);
    const [hover, setHover] = useState(false);
    const watched = value.watching[watchKey] !== undefined;
    return <span onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}>
        {(hover || watched) && <Tooltip overlay={watched ? 'לחץ.י לביטול המתנה לנתון' : 'לחץ.י להמתנה לנתון זה'}>
            <Button className={`status-color status-${watched ?'processing': 'neutral'}`} icon={watched ? <BellFilled/> : <BellOutlined/>}
                    onClick={() => update(['watching', watchKey], watched ? null : {
                        update_at: updateAt,
                    })}/>
        </Tooltip>}
        {children}
    </span>
}
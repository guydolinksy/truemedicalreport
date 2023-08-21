import {Button} from "antd";
import {BellFilled, BellOutlined} from "@ant-design/icons";
import {patientDataContext} from "./Patient";
import {useContext, useState} from "react";

export const Watchable = ({watchKey, updateAt, children}) => {
    const {value, update} = useContext(patientDataContext.context);
    const [hover, setHover] = useState(false);
    const watched = value.watching[watchKey] !== undefined && value.watching[watchKey].watched;
    return <span onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}>
        {(hover || watched) &&
            <Button type={"text"} className={`status-color status-${watched ? 'processing' : 'neutral'}`}
                    icon={watched ? <BellFilled/> : <BellOutlined/>} onClick={(e) => {
                update(['watching', watchKey], {
                    update_at: updateAt,
                    watched: !watched,
                })
                e.stopPropagation();
            }}/>}
        {children}
    </span>
}
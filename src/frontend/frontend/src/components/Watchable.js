import {BellFilled, BellOutlined} from "@ant-design/icons";
import {patientDataContext} from "./card/PatientBase";
import {useContext, useState} from "react";

export const Watchable = ({ forceOpen, watchKey, updateAt, children}) => {
    const {value, update} = useContext(patientDataContext.context);
    const [hover, setHover] = useState(false);

    const watched = value && value.watching[watchKey] !== undefined && value.watching[watchKey].watched;
    const props = {
        className: `status-color status-${watched ? 'processing' : 'neutral'}`,
        onClick: (e) => {
            update(['watching', watchKey], {
                update_at: updateAt,
                watched: !watched,
            }, 'WatchKey')
            e.stopPropagation();
        }
    }
    return <span onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
                 style={{flexWrap: "nowrap", display: 'flex'}}>
        {(forceOpen || hover || watched) && (watched ? <BellFilled {...props}/> : <BellOutlined {...props}/>)}&nbsp;{children}
    </span>
}
import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Tooltip} from "antd";

export const modalButton = (modal, faIconName, tooltip, link) => {
    return link && <Tooltip overlay={tooltip}>
        <FontAwesomeIcon icon={faIconName} onClick={e => {
            modal.info({
                icon: null,
                width: "95%",
                okText: "סגור",
                centered: true,
                bodyStyle: {
                    padding: "10px"
                },
                content: <iframe
                    style={{
                        border: 0,
                        width: "100%",
                        height: 0.75 * window.document.documentElement.clientHeight
                    }}
                    src={link}
                />
            })
            e.stopPropagation();
        }}/>
    </Tooltip>
}

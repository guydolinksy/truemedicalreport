import React, {useContext, useMemo} from "react";
import {Legend} from "../components/Legend";
import {viewsContext} from "../contexts/ViewsContext";
import {useParams} from 'react-router-dom';
import {Empty, Layout, Space} from 'antd';
import {MIN_WIDTH, Patient} from "../components/card/Patient";

const {Content} = Layout
export const ListMode = ({onError, style, showAttention}) => {
    const {value: viewsValue} = useContext(viewsContext.context)
    const {view} = useParams();

    const curView = useMemo(() => {
        return viewsValue.getViews.views.find(v => v.key === view)
    }, [viewsValue, view]);
    return <Content>
        <div style={{display: "flex", flexDirection: "row", alignItems: "center", height: '100%'}}>
            <div style={{display: "flex", flexDirection: "column", alignItems: "center", flex: 1}}>
                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    maxWidth: '80vw',
                    maxHeight: '80vh',
                    justifyContent: 'center',
                    alignItems: 'center',
                    gap: 16,
                }}>
                    <div style={{overflowY: 'auto'}}>
                        <Space style={{justifyContent: 'center', ...style}} wrap>
                            {curView.patients.length ? curView.patients.map(
                                ({oid}) => <Patient key={oid} patient={oid} style={{minWidth: MIN_WIDTH}}
                                                    onError={onError}
                                                    showAttention={showAttention}/>
                            ) : <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE}/>}
                        </Space>
                    </div>
                    <Legend/>
                </div>
            </div>
        </div>
    </Content>
}
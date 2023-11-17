import {ManOutlined, WomanOutlined} from "@ant-design/icons";

export const PatientLabel = ({patient, user}) => {
    return <div style={{width: '100%', justifyContent: 'space-between', display: 'flex'}}>
                    <span><span className={`gender-${patient.info.gender}`}>
                        {patient.info.gender === 'male' && <ManOutlined/>}
                        {patient.info.gender === 'female' && <WomanOutlined/>}
                    </span>&nbsp;{user.anonymous ? '---' : patient.info.name}{patient.comment ? ` (${patient.comment})` : ''}</span>
        <span style={{minWidth: 20}}/>
        {patient.views.slice(0, 1).map(v =>
            <span key={0} style={{color: v.color}}>{v.name}</span>
        )}
    </div>
}
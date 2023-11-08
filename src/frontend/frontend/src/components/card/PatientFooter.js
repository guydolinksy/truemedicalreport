import React, {useContext} from "react";
import {patientDataContext} from "./PatientBase";
import {FileAddOutlined} from '@ant-design/icons';
import {NoteTooltip} from "../NoteTooltip";
import moment from "moment";


export const PatientFooter = () => {
    const {value} = useContext(patientDataContext.context);
    const notes = value.discussion.notes || {};
    const descNotes = Object.keys(notes).sort((a, b) =>
        moment(notes[a].at).isSame(notes[b].at) ? 0 : moment(notes[a].at).isAfter(notes[b].at) ? -1 : 1
    );
    const doctorNotes = Object.assign({}, ...value.treatment.doctors.map(doctor => ({
        [doctor]: notes[descNotes.find(note => notes[note].by === doctor && !notes[note].subject)] || undefined
    })));
    const subjectNotes = Object.assign({}, ...Object.entries(value.referrals).map(([id, ref]) => ({
        [ref.to]: notes[descNotes.find(note => notes[note].subject === ref.to.trim())] || undefined
    })));
    const unpairedNotes = descNotes.filter(note =>
        notes[note].subject ? !Object.keys(subjectNotes).includes(notes[note].subject) :
            !value.treatment.doctors.includes(notes[note].by)
    );
    return (
        <div style={{display: "flex", flexDirection: "column", backgroundColor: '#f5f5f5'}}>
            {(value.treatment.doctors.length > 0 || Object.keys(value.referrals).length > 0 || unpairedNotes.length > 0) &&
                <div style={{
                    display: "flex",
                    justifyContent: "space-between",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    padding: "0px 12px 8px 12px"
                }}>
                    {value.treatment.doctors.length > 0 && <div style={{
                        display: "flex",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap"
                    }}>
                        {value.treatment.doctors.map((doctor, index) =>
                            <NoteTooltip key={index} placeholder={doctor} note={doctorNotes[doctor]}>
                                <div style={{
                                    overflow: "hidden",
                                    textOverflow: "ellipsis",
                                    whiteSpace: "nowrap",
                                    fontWeight: 'bold'
                                }}>
                                    {index !== 0 ? ',' : ''}{doctor}
                                </div>
                            </NoteTooltip>)}
                    </div>}
                    {Object.keys(value.referrals).length > 0 && <div style={{
                        display: "flex",
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap"
                    }}>
                        {Object.values(value.referrals).filter(ref => !ref.completed).map((ref, index) =>
                            <NoteTooltip key={index} placeholder={ref.to} note={subjectNotes[ref.to]}>
                                <div style={{
                                    overflow: "hidden",
                                    textOverflow: "ellipsis",
                                    whiteSpace: "nowrap",
                                    fontWeight: 'bold'
                                }}>
                                    {index !== 0 ? ',' : ''}{ref.to}
                                </div>
                            </NoteTooltip>)}
                    </div>}
                    {unpairedNotes.length > 0 && <NoteTooltip notes={unpairedNotes.map(note => notes[note])}>
                        <div>
                            <FileAddOutlined/>
                        </div>
                    </NoteTooltip>}
                </div>}
        </div>)
}
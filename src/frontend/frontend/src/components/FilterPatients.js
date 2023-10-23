import {Divider, Tag, Tree} from "antd";
import React from "react";
import {useLocalStorage} from "../hooks/localStorageHook";

const {CheckableTag} = Tag;

export const FilterPatients = ({value}) => {
    const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
    const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
    const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);
    const [selectedTime, setSelectedTime] = useLocalStorage('selectedTime', []);

    const toTree = filter => ({
        key: filter.key,
        title: `(${filter.count}) ${filter.title}`,
        children: (filter.children || []).map(toTree)
    })

    const handleDoctorFilterChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedDoctors, tag] : selectedDoctors.filter((t) => t !== tag);
        setSelectedDoctors(nextSelectedTags);
    };

    const handleDecisionStatusFilterChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTreatments, tag] : selectedTreatments.filter((t) => t !== tag);
        setSelectedTreatments(nextSelectedTags);
    };

    const handleTimeFilterChange = (tag, checked) => {
        const nextSelectedTags = checked ? [...selectedTime, tag] : selectedTime.filter((t) => t !== tag);
        setSelectedTime(nextSelectedTags);
    };

    const filterTagsContainerStyle = {
        display: 'flex',
        flexWrap: "wrap",
        gap: '5px 0',
        justifyContent: "space-between",
    }

    return <div>
        <div style={filterTagsContainerStyle}>
            <b style={{whiteSpace: "nowrap"}}>רופא.ה:</b>
            {value.filters.doctors.map(filter => <CheckableTag
                key={filter.key}
                checked={selectedDoctors.indexOf(filter.key) > -1}
                onChange={(checked) => handleDoctorFilterChange(filter.key, checked)}
            >
                {filter.title}
            </CheckableTag>)}
        </div>
        <Divider style={{marginTop: 10, marginBottom: 10}}/>
        <div style={filterTagsContainerStyle}>
            <b style={{whiteSpace: "nowrap"}}>יעד:</b>
            {value.filters.treatments.map(filter => <CheckableTag
                key={filter.key}
                checked={selectedTreatments.indexOf(filter.key) > -1}
                onChange={(checked) => handleDecisionStatusFilterChange(filter.key, checked)}
            >
                {filter.title}
            </CheckableTag>)}
        </div>
        <Divider style={{marginTop: 10, marginBottom: 10}}/>
        <div style={filterTagsContainerStyle}>
            <b style={{whiteSpace: "nowrap"}}>זמן במיון:</b>
            {value.filters.time_since_arrival.map(filter => <CheckableTag
                key={filter.key}
                checked={selectedTime.indexOf(filter.key) > -1}
                onChange={(checked) => handleTimeFilterChange(filter.key, checked)}
            >
                {filter.title}
            </CheckableTag>)}
        </div>
        <Divider style={{marginTop: 10, marginBottom: 10}}/>
        <Tree treeData={value.filters.awaiting.map(toTree)} style={{width: '100%'}} checkable multiple
              defaultExpandedKeys={value.filters.awaiting.map(x => x.key)}
              placeholder="סינון לפי המתנה עבור:" onCheck={setSelectedAwaiting}
              checkedKeys={selectedAwaiting}/>
    </div>
}
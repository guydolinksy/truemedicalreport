import { Button, Divider, Popover, Tag, Tree } from 'antd';
import React, { useContext } from 'react';
import { useLocalStorage } from '../hooks/localStorageHook';
import { loginContext } from './LoginContext';
import { FilterOutlined } from '@ant-design/icons';
import { wingDataContext } from '../contexts/WingContext';

const { CheckableTag } = Tag;

export const FilterPatients = ({}) => {
  const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
  const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
  const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);
  const [selectedTime, setSelectedTime] = useLocalStorage('selectedTime', []);

  const toTree = (filter) => ({
    key: filter.key,
    title: `(${filter.count}) ${filter.title}`,
    children: (filter.children || []).map(toTree),
  });

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
    flexWrap: 'wrap',
    gap: '5px 0',
    justifyContent: 'space-between',
  };
  const { user, userSettings } = useContext(loginContext);
  const { value } = useContext(wingDataContext.context);
  return (
    <Popover
      placement={'leftTop'}
      content={
        <div>
          <div style={filterTagsContainerStyle}>
            <b style={{ whiteSpace: 'nowrap' }}>רופא.ה:</b>
            {value.getWings.wings[0].filters.doctors.map((filter) => (
              <CheckableTag
                key={filter.key}
                checked={selectedDoctors.indexOf(filter.key) > -1}
                onChange={(checked) => handleDoctorFilterChange(filter.key, checked)}
              >
                {filter.title}
              </CheckableTag>
            ))}
          </div>
          <Divider style={{ marginTop: 10, marginBottom: 10 }} />
          <div style={filterTagsContainerStyle}>
            <b style={{ whiteSpace: 'nowrap' }}>יעד:</b>
            {value.getWings.wings[0].filters.treatments.map((filter) => (
              <CheckableTag
                key={filter.key}
                checked={selectedTreatments.indexOf(filter.key) > -1}
                onChange={(checked) => handleDecisionStatusFilterChange(filter.key, checked)}
              >
                {filter.title}
              </CheckableTag>
            ))}
          </div>
          <Divider style={{ marginTop: 10, marginBottom: 10 }} />
          <div style={filterTagsContainerStyle}>
            <b style={{ whiteSpace: 'nowrap' }}>זמן במיון:</b>
            {value.getWings.wings[0].filters.time_since_arrival.map((filter) => (
              <CheckableTag
                key={filter.key}
                checked={selectedTime.indexOf(filter.key) > -1}
                onChange={(checked) => handleTimeFilterChange(filter.key, checked)}
              >
                {filter.title}
              </CheckableTag>
            ))}
          </div>
          <Divider style={{ marginTop: 10, marginBottom: 10 }} />
          <Tree
            treeData={value.getWings.wings[0].filters.awaiting.map(toTree)}
            style={{ width: '100%' }}
            checkable
            multiple
            defaultExpandedKeys={value.getWings.wings[0].filters.awaiting.map((x) => x.key)}
            placeholder="סינון לפי המתנה עבור:"
            onCheck={setSelectedAwaiting}
            checkedKeys={selectedAwaiting}
          />
        </div>
      }
      title={'סינון תצוגת אגף'}
    >
      <Button
        type={'primary'}
        style={{ position: 'absolute', top: 80, left: 0, width: 40, zIndex: 1000 }}
        icon={<FilterOutlined />}
      />
    </Popover>
  );
};

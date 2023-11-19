import { Button, Divider, Popover, Tag, Tree } from 'antd';
import React, { useContext, useMemo, createContext } from 'react';
import { useLocalStorage } from '../hooks/localStorageHook';
import { FilterOutlined } from '@ant-design/icons';
import { viewsDataContext } from '../contexts/ViewsDataContext';
import { useParams } from 'react-router-dom';
import moment from 'moment';
import { createDataContext } from '../contexts/DataContext';

const { CheckableTag } = Tag;

export const filterContext = createContext();
export const filtersDataContext = createDataContext();

const PatientsFilterInner = ({ children }) => {
  const { value } = useContext(filtersDataContext.context);

  const [selectedAwaiting, setSelectedAwaiting] = useLocalStorage('selectedAwaiting', []);
  const [selectedDoctors, setSelectedDoctors] = useLocalStorage('selectedDoctors', []);
  const [selectedTreatments, setSelectedTreatments] = useLocalStorage('selectedTreatments', []);
  const [selectedTime, setSelectedTime] = useLocalStorage('selectedTime', []);

  const { filteredPatients, isFiltered } = useMemo(() => {
    const relevantAwaiting = selectedAwaiting.filter(
      (filter) => value.getViewFilters.filters[0].mapping[filter] !== undefined,
    );
    const relevantDoctors = selectedDoctors.filter(
      (filter) => value.getViewFilters.filters[0].mapping[filter] !== undefined,
    );
    const relevantTreatments = selectedTreatments.filter(
      (filter) => value.getViewFilters.filters[0].mapping[filter] !== undefined,
    );
    const relevantTime = selectedTime.filter((filter) => value.getViewFilters.filters[0].mapping[filter] !== undefined);
    return {
      filteredPatients: value.getPatients.patients
        .filter(
          ({ oid }) =>
            !relevantAwaiting.length ||
            relevantAwaiting.find((filter) => (value.getViewFilters.filters[0].mapping[filter] || []).includes(oid)),
        )
        .filter(
          ({ oid }) =>
            !relevantTreatments.length ||
            relevantTreatments.find((filter) => (value.getViewFilters.filters[0].mapping[filter] || []).includes(oid)),
        )
        .filter(
          ({ oid }) =>
            !relevantDoctors.length ||
            relevantDoctors.find((filter) => (value.getViewFilters.filters[0].mapping[filter] || []).includes(oid)),
        )
        .filter(
          ({ oid }) =>
            !relevantTime.length ||
            relevantTime.find((filter) => (value.getViewFilters.filters[0].mapping[filter] || []).includes(oid)),
        )
        .sort((i, j) => (moment(i.admission.arrival).isAfter(j.admission.arrival) ? 1 : -1)),
      isFiltered: relevantAwaiting.length || relevantDoctors.length || relevantTime.length || relevantTime.length,
    };
  }, [value.getPatients.patients, value, selectedAwaiting, selectedDoctors, selectedTreatments, selectedTime]);

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
  return (
    <filterContext.Provider value={{ filteredPatients, isFiltered }}>
      {children}
      <Popover
        placement={'leftTop'}
        title={'סינון תצוגת אגף'}
        content={
          <div>
            <div style={filterTagsContainerStyle}>
              <b style={{ whiteSpace: 'nowrap' }}>רופא.ה:</b>
              {value.getViewFilters.filters[0].doctors.map((filter) => (
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
              {value.getViewFilters.filters[0].treatments.map((filter) => (
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
              {value.getViewFilters.filters[0].time_since_arrival.map((filter) => (
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
              treeData={value.getViewFilters.filters[0].awaiting.map(toTree)}
              style={{ width: '100%' }}
              checkable
              multiple
              defaultExpandedKeys={value.getViewFilters.filters[0].awaiting.map((x) => x.key)}
              placeholder="סינון לפי המתנה עבור:"
              onCheck={setSelectedAwaiting}
              checkedKeys={selectedAwaiting}
            />
          </div>
        }
      >
        <Button
          type={'primary'}
          style={{ position: 'absolute', top: 80, left: 0, width: 40, zIndex: 1000 }}
          icon={<FilterOutlined />}
        />
      </Popover>
    </filterContext.Provider>
  );
};

export const PatientsFilter = ({ children, onError }) => {
  const { viewType, view } = useParams();

  return (
    <filtersDataContext.Provider url={`/api/views/${viewType}/${view}/filters`} onError={onError}>
      {() => <PatientsFilterInner>{children}</PatientsFilterInner>}
    </filtersDataContext.Provider>
  );
};

import { MIN_WIDTH, Patient } from '../components/card/Patient';
import React, { useContext } from 'react';
import { Card, Layout } from 'antd';
import { filterContext, PatientsFilter } from '../components/PatientsFilter';
import { Legend } from '../components/Legend';
import { WingNotifications } from '../components/WingNotifications';
import { AdmitPatient } from '../components/AdmitPatient';
import { InfoDrawer } from '../components/panel/Info';

const { Content } = Layout;
const StatusModeInner = () => {
  const { filteredPatients } = useContext(filterContext);
  console.log(filteredPatients);
  const needAttention = filteredPatients.filter((patient) => patient.watching.find((watchKey) => watchKey.triggered));
  const unassigned = filteredPatients.filter(
    (patient) => !needAttention.find(({ oid }) => oid === patient.oid) && patient.status === 'unassigned',
  );
  const undecided = filteredPatients.filter(
    (patient) => !needAttention.find(({ oid }) => oid === patient.oid) && patient.status === 'undecided',
  );
  const decided = filteredPatients.filter(
    (patient) => !needAttention.find(({ oid }) => oid === patient.oid) && patient.status === 'decided',
  );
  return (
    <Content
      style={{
        padding: 'max(32px, min(8vw, 8vh))',
        overflowY: 'auto',
        display: 'grid',
        gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`,
        // gridAutoRows: '1fr',
        gap: 32,
      }}
    >
      <Card
        size={'small'}
        style={{ gridColumn: '1 / -1' }}
        bodyStyle={{ display: 'none' }}
        title={`ממתינים עבורך (${needAttention.length})`}
      />
      {needAttention.map(({ oid }) => (
        <Patient key={oid} patient={oid} style={{ minWidth: MIN_WIDTH }} />
      ))}
      <Card
        size={'small'}
        style={{ gridColumn: '1 / -1' }}
        bodyStyle={{ display: 'none' }}
        title={`ללא שיוך לרופא.ה (${unassigned.length})`}
      />
      {unassigned.map(({ oid }) => (
        <Patient key={oid} patient={oid} style={{ minWidth: MIN_WIDTH }} />
      ))}
      <Card
        size={'small'}
        style={{ gridColumn: '1 / -1' }}
        bodyStyle={{ display: 'none' }}
        title={`ללא החלטה על יעד (${undecided.length})`}
      />
      {undecided.map(({ oid }) => (
        <Patient key={oid} patient={oid} style={{ minWidth: MIN_WIDTH }} />
      ))}
      <Card
        size={'small'}
        style={{ gridColumn: '1 / -1' }}
        bodyStyle={{ display: 'none' }}
        title={`ממתין לאשפוז/שחרור (${decided.length})`}
      />
      {decided.map(({ oid }) => (
        <Patient key={oid} patient={oid} style={{ minWidth: MIN_WIDTH }} />
      ))}
    </Content>
  );
};
export const StatusMode = ({ onError }) => {
  return (
    <>
      <PatientsFilter>
        <StatusModeInner />
        <WingNotifications />
      </PatientsFilter>
      <Legend />
      <InfoDrawer />
      <AdmitPatient />
    </>
  );
};

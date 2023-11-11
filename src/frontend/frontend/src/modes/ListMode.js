import React, { useContext } from 'react';
import { Legend } from '../components/Legend';
import { Empty, Layout } from 'antd';
import { MIN_WIDTH, Patient } from '../components/card/Patient';
import { filterContext, PatientsFilter } from '../components/PatientsFilter';
import { WingNotifications } from '../components/WingNotifications';
import { AdmitPatient } from '../components/AdmitPatient';
import { InfoDrawer } from '../components/panel/Info';

const { Content } = Layout;
const ListModeInner = ({ onError }) => {
  const { filteredPatients } = useContext(filterContext);
  return filteredPatients.length ? (
    filteredPatients.map(({ oid }) => (
      <Patient key={oid} patient={oid} style={{ minWidth: MIN_WIDTH }} onError={onError} />
    ))
  ) : (
    <Empty description={false} image={Empty.PRESENTED_IMAGE_SIMPLE} />
  );
};

export const ListMode = ({ onError }) => {
  return (
    <Content
      style={{
        padding: 'max(32px, min(8vw, 8vh))',
        overflowY: 'auto',
        display: 'grid',
        gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`,
        gridAutoRows: '1fr',
        gap: 32,
      }}
    >
      <PatientsFilter>
        <ListModeInner onError={onError} />
        <WingNotifications />
      </PatientsFilter>
      <Legend />
      <InfoDrawer />
      <AdmitPatient />
    </Content>
  );
};

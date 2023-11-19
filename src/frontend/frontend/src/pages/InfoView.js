import React, { useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Layout } from 'antd';
import { Info } from '../components/panel/Info';
import { patientDataContext } from '../components/card/PatientBase';

const { Content } = Layout;

const MIN_WIDTH = 300;

export const INFO_URL = '/views/:viewType/:view/modes/:mode/info/:patient';

export const InfoView = () => {
  const { patient } = useParams();
  const navigate = useNavigate();
  const onError = useCallback(() => navigate('/'), [navigate]);

  return (
    <patientDataContext.Provider url={`/api/patients/${patient}/info`} onError={onError}>
      {() => (
        <Content
          style={{
            padding: 'max(32px, min(8vw, 8vh))',
            overflowY: 'auto',
            textAlign: 'center',
            display: 'grid',
            gridTemplateColumns: `repeat(auto-fill, minmax(${MIN_WIDTH}px, 1fr))`,
            gridAutoRows: `1fr`,
          }}
        >
          <Info patient={patient} />
        </Content>
      )}
    </patientDataContext.Provider>
  );
};

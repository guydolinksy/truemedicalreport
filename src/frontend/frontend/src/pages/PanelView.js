import React, { useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Layout } from 'antd';
import { PatientPanel } from '../components/panel/Info';
import { patientDataContext } from '../components/card/PatientBase';
import { Settings } from '../components/settings/Settings';
import { PanelFormatCard } from '../components/settings/PanelFormatCard';

const { Content } = Layout;

const MIN_WIDTH = 300;

export const PANEL_URL = '/views/:viewType/:view/modes/:mode/panel/:patient';

export const PanelView = () => {
  const { patient } = useParams();
  const navigate = useNavigate();
  const onError = useCallback(() => navigate('/'), [navigate]);

  return (
    <patientDataContext.Provider url={`/api/patients/${patient}/panel`} onError={onError}>
      {() => (
        <Content
          style={{
            padding: 'max(32px, min(8vw, 8vh))',
            overflowY: 'auto',
            textAlign: 'center',
            display: 'flex',
            flexWrap: 'wrap',
            columnGap: 8,
            rowGap: 8,
          }}
        >
          <PatientPanel />
          <Settings>
            <PanelFormatCard />
          </Settings>
        </Content>
      )}
    </patientDataContext.Provider>
  );
};

import React, { useContext, useEffect, useState } from 'react';
import { patientDataContext } from '../card/PatientBase';
import { generatePath, useNavigate, useParams } from 'react-router-dom';
import { Notes } from './Notes';
import { FullMeasures } from './FullMeasures';
import { BasicInfo } from './BasicInfo';
import { loginContext } from '../LoginContext';
import { Notifications } from './Notifications';
import { Imaging } from './Imaging';
import { Labs } from './Labs';
import { Referrals } from './Referrals';
import { InfoPlugin } from './InfoPlugin';
import { Visits } from './Visits';
import { MedicalSummary } from './MedicalSummary';
import { ECGs } from './ECGs';
import { MCISection } from './MCISection';
import { MCIHeader } from './MCIHeader';
import { MCI } from './MCI';
import { createDataContext } from '../../contexts/DataContext';
import { INFO_URL } from '../../pages/InfoView';
import { hashMatchContext } from '../HashMatch';
import { modeContext } from '../../contexts/ModeContext';
import { Drawer, Button } from 'antd';
import { ArrowsAltOutlined } from '@ant-design/icons';

const COMPONENT_TYPE_TO_COMPONENT = {
  Notes,
  FullMeasures,
  BasicInfo,
  Notifications,
  Imaging,
  Labs,
  Referrals,
  Visits,
  MedicalSummary,
  ECGs,
  MCIHeader,
  MCISection,
  InfoPlugin,
  MCI,
};

export const panelContext = createDataContext();

export const InfoPanel = ({ setHeader }) => {
  const { user } = useContext(loginContext);
  const { viewType, view, mode } = useParams();
  const { value } = useContext(patientDataContext.context);
  const navigate = useNavigate();
  const { matched, matching } = useContext(hashMatchContext);
  const { isTablet } = useContext(modeContext);

  useEffect(() => {
    if (isTablet && matched(['info'])) {
      navigate(
        generatePath(INFO_URL, {
          viewType,
          view,
          mode,
          patient: matching(['info'])[0],
        }),
      );
    }
  }, [isTablet, matched, matching, navigate, viewType, view, mode]);

  useEffect(() => {
    let gender = {
      male: 'בן ',
      female: 'בת ',
      [null]: '',
    }[value.info?.gender];
    setHeader({
      title: user.anonymous
        ? `${gender}(${value.info?.age || 'גיל לא ידוע'})`
        : `${value.info?.name}, ${gender}(${value.info?.age || 'גיל לא ידוע'})` +
          (value.info?.id_ ? `, ת.ז. ${value.info?.id_}` : '') +
          (value.info?.phone ? `, טלפון : ${value.info?.phone}` : ''),
      className: `gender-${value.info?.gender}`,
    });
  }, [value, setHeader]);

  return (
    <panelContext.Provider url={`/api/settings/views/${viewType}/${view}/modes/${mode}/info/format`}>
      {({ value }) =>
        value.components.map((component) => {
          const Component = COMPONENT_TYPE_TO_COMPONENT[component.type];
          if (!Component) return <div key={component.key}>Unknown Component {component.type}</div>;
          return <Component key={component.key} config={component.config} />;
        })
      }
    </panelContext.Provider>
  );
};
export const Info = () => {
  const [header, setHeader] = useState(null);

  return (
    <>
      {header && (
        <h1
          style={{
            textAlign: 'center',
            gridColumn: '1 / -1',
          }}
          className={header.className}
        >
          {header.title}
        </h1>
      )}
      <InfoPanel setHeader={setHeader} />
    </>
  );
};
export const InfoDrawer = () => {
  const [header, setHeader] = useState({ title: '', className: '' });
  const { viewType, view, mode } = useParams();
  const navigate = useNavigate();
  const { matched, matching } = useContext(hashMatchContext);
  return (
    <Drawer
      title={header.title}
      placement={'left'}
      open={matched(['info'])}
      extra={
        <Button
          type={'text'}
          icon={<ArrowsAltOutlined />}
          onClick={() => {
            navigate(generatePath(INFO_URL, { viewType, view, mode, patient: matching(['info'])[0] }));
          }}
        />
      }
      onClose={() => navigate('#')}
      className={header.className}
      size={500}
    >
      <InfoContext setHeader={setHeader} />
    </Drawer>
  );
};
export const InfoContext = ({ onError, setHeader }) => {
  const { matching } = useContext(hashMatchContext);
  return (
    <patientDataContext.Provider url={`/api/patients/${matching(['info'])[0]}/info`} onError={onError}>
      {() => <InfoPanel setHeader={setHeader} />}
    </patientDataContext.Provider>
  );
};

import React, { useContext, useRef } from 'react';
import { Badge, Button, Card, Carousel, Select, Tooltip } from 'antd';
import { FlagFilled, SendOutlined, UserOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { useMatomo } from '@datapunt/matomo-tracker-react';
import moment from 'moment';
import { hashMatchContext } from '../HashMatch';
import { patientDataContext } from './PatientBase';
import { PatientHeader } from './PatientHeader';
import { PatientMeasures } from './PatientMeasures';
import { PatientStatus } from './PatientStatus';
import { PatientFooter } from './PatientFooter';
import { PatientWatching } from './PatientWatching';
import { PatientWarning } from './PatientWarning';

import './Patient.css';
import { PatientContent } from './PatientContent';
import { PatientExtra } from './PatientExtra';
import { MCI_DEPARTMENT } from '../panel/MCISection';

export const MIN_WIDTH = 350,
  MAX_WIDTH = 500,
  MAX_HEIGHT = 250;

const getNextDestination = (wing_id, mci) => {
  if (!mci) return null;
  if (mci.next_destination) return mci.next_destination.value;
  if (
    (mci.chest_xray && mci.chest_xray.value) ||
    (mci.fast && mci.fast.value) ||
    (mci.ct && mci.ct.value) ||
    (mci.angiogram && mci.angiogram.value)
  ) {
    return wing_id === '17' ? 'er_imaging' : 'general_imaging';
  } else if (mci.mri && mci.mri.value) {
    return 'er_imaging';
  }
};
const MCIPatientBody = () => {
  const { value, update } = useContext(patientDataContext.context);
  const destinations = DESTINATIONS[value.admission.wing_id] || DESTINATIONS[undefined];
  const next_destination = getNextDestination(value.admission.wing_id, value.mci);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, padding: '8px 12px' }}>
      {/*<MCIFormItem item={{key: 'ct', name: 'ct', type: 'checkbox'}}/>*/}
      {/*<MCIFormItem item={{key: 'blood_type', name: 'דם לסוג והצלבה', type: 'checkbox'}}/>*/}
      <div>יעד:&nbsp;{value.treatment.destination || '-'}</div>
      <div>הערות:&nbsp;{value.comment}</div>
      <div style={{ flex: 1 }} />
      <div
        style={{
          width: '100%',
          overflowX: 'hidden',
          textOverflow: 'ellipsis',
          display: 'flex',
          flexWrap: 'wrap',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {destinations.slice(0, 2).map((destination) => (
          <Button
            key={destination.key}
            onClick={(e) => {
              update(
                [MCI_DEPARTMENT, 'next_destination'],
                {
                  value: destination.key,
                  at: moment().toISOString().replace('Z', '+00:00'),
                },
                'MCIStringValue',
              );
              e.stopPropagation();
            }}
            style={{ flex: 1 }}
          >
            {destination.name}
          </Button>
        ))}
      </div>
      <div
        style={{
          width: '100%',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <Select
          style={{ minWidth: 100, flex: 1 }}
          value={next_destination}
          placeholder={'יעד הבא'}
          options={destinations.map((d) => ({ value: d.key, label: d.name }))}
          onSelect={(value) =>
            update(
              [MCI_DEPARTMENT, 'next_destination'],
              {
                value: value,
                at: moment().toISOString().replace('Z', '+00:00'),
              },
              'MCIStringValue',
            )
          }
        />
        <Button
          disabled={!next_destination}
          danger
          onClick={(e) => {
            update(
              ['admission'],
              {
                arrival: value.admission.arrival,
                department_id: value.admission.department_id,
                wing_id: next_destination,
              },
              'Admission',
            );
            update([MCI_DEPARTMENT, 'next_destination'], null, false);
            e.stopPropagation();
          }}
          icon={<SendOutlined style={{ transform: 'scaleX(-1)' }} />}
        />
      </div>
    </div>
  );
};
const DESTINATIONS = {
  intake_red: [
    { key: 'operating_room', name: 'חדר ניתוח' },
    { key: 'er_imaging', name: 'דימות מלר"ד' },
    { key: 'intake_yellow', name: 'צהוב - אגף 3' },
    { key: 'intake_green', name: 'ירוק - אגף 4' },
    { key: 'general_imaging', name: 'אתר דימות' },
    { key: 'intensive_care', name: 'טיפול נמרץ כללי' },
    { key: 'cardiac_intensive_care', name: 'טיפול נמרץ לב' },
    { key: 'trauma_unit', name: 'יחידת הטראומה' },
    { key: 'surgical_b', name: 'כירוגיה ב' },
    { key: 'surgical_c', name: 'כירוגיה ג' },
    { key: 'neurosurgical', name: 'נוירוכירוגיה' },
    { key: 'orthopedics_a', name: 'אורתופדיה א' },
    { key: 'orthopedics_b', name: 'אורתופדיה ב' },
    { key: 'hand_palm', name: 'כף יד' },
    { key: 'mouth_and_jaw', name: 'פה ולסת' },
    { key: 'ent,name', name: 'אף אוזן גרון' },
    { key: 'urology,name', name: 'אורולוגיה' },
    { key: 'cardiovascular', name: 'חזה וכלי דם' },
    { key: 'pediatric', name: 'ילדים' },
    { key: 'pediatric_icu', name: 'טיפול נמרץ ילדים' },
    { key: 'internal_medicine_a', name: 'פנימית א' },
    { key: 'internal_medicine_b', name: 'פנימית ב' },
    { key: 'internal_medicine_c', name: 'פנימית ג' },
    { key: 'internal_medicine_d', name: 'פנימית ד' },
    { key: 'internal_medicine_e', name: 'פנימית ה' },
    { key: 'internal_medicine_f', name: 'פנימית ו' },
    { key: 'internal_medicine_i', name: 'פנימית ט' },
  ],
  intake_yellow: [
    { key: 'general_imaging', name: 'אתר דימות' },
    { key: 'imaging_department', name: 'אגף דימות' },
    { key: 'intake_red', name: 'אדום - חדר הלם' },
    { key: 'intake_green', name: 'ירוק - אגף 4' },
    { key: 'er_imaging', name: 'הדמייה במלר"ד' },
    { key: 'intensive_care', name: 'טיפול נמרץ כללי' },
    { key: 'cardiac_intensive_care', name: 'טיפול נמרץ לב' },
    { key: 'trauma_unit', name: 'יחידת הטראומה' },
    { key: 'surgical_b', name: 'כירוגיה ב' },
    { key: 'surgical_c', name: 'כירוגיה ג' },
    { key: 'neurosurgical', name: 'נוירוכירוגיה' },
    { key: 'orthopedics_a', name: 'אורתופדיה א' },
    { key: 'orthopedics_b', name: 'אורתופדיה ב' },
    { key: 'hand_palm', name: 'כף יד' },
    { key: 'mouth_and_jaw', name: 'פה ולסת' },
    { key: 'ent,name', name: 'אף אוזן גרון' },
    { key: 'urology,name', name: 'אורולוגיה' },
    { key: 'cardiovascular', name: 'חזה וכלי דם' },
    { key: 'pediatric', name: 'ילדים' },
    { key: 'pediatric_icu', name: 'טיפול נמרץ ילדים' },
    { key: 'internal_medicine_a', name: 'פנימית א' },
    { key: 'internal_medicine_b', name: 'פנימית ב' },
    { key: 'internal_medicine_c', name: 'פנימית ג' },
    { key: 'internal_medicine_d', name: 'פנימית ד' },
    { key: 'internal_medicine_e', name: 'פנימית ה' },
    { key: 'internal_medicine_f', name: 'פנימית ו' },
    { key: 'internal_medicine_i', name: 'פנימית ט' },
  ],
  intake_green: [
    { key: 'general_imaging', name: 'אתר דימות' },
    { key: 'intake_red', name: 'אדום - חדר הלם' },
    { key: 'intake_yellow', name: 'צהוב - אגף 3' },
    { key: 'operating_room', name: 'חדר ניתוח' },
    { key: 'er_imaging', name: 'הדמייה במלר"ד' },
    { key: 'intensive_care', name: 'טיפול נמרץ כללי' },
    { key: 'cardiac_intensive_care', name: 'טיפול נמרץ לב' },
    { key: 'trauma_unit', name: 'יחידת הטראומה' },
    { key: 'surgical_b', name: 'כירוגיה ב' },
    { key: 'surgical_c', name: 'כירוגיה ג' },
    { key: 'neurosurgical', name: 'נוירוכירוגיה' },
    { key: 'orthopedics_a', name: 'אורתופדיה א' },
    { key: 'orthopedics_b', name: 'אורתופדיה ב' },
    { key: 'hand_palm', name: 'כף יד' },
    { key: 'mouth_and_jaw', name: 'פה ולסת' },
    { key: 'ent,name', name: 'אף אוזן גרון' },
    { key: 'urology,name', name: 'אורולוגיה' },
    { key: 'cardiovascular', name: 'חזה וכלי דם' },
    { key: 'pediatric', name: 'ילדים' },
    { key: 'pediatric_icu', name: 'טיפול נמרץ ילדים' },
    { key: 'internal_medicine_a', name: 'פנימית א' },
    { key: 'internal_medicine_b', name: 'פנימית ב' },
    { key: 'internal_medicine_c', name: 'פנימית ג' },
    { key: 'internal_medicine_d', name: 'פנימית ד' },
    { key: 'internal_medicine_e', name: 'פנימית ה' },
    { key: 'internal_medicine_f', name: 'פנימית ו' },
    { key: 'internal_medicine_i', name: 'פנימית ט' },
  ],
  [undefined]: [
    { key: 'intake_red', name: 'אדום - חדר הלם' },
    { key: 'intake_yellow', name: 'צהוב - אגף 3' },
    { key: 'intake_green', name: 'ירוק - אגף 4' },
    { key: 'operating_room', name: 'חדר ניתוח' },
    { key: 'er_imaging', name: 'הדמייה במלר"ד' },
    { key: 'general_imaging', name: 'אתר דימות' },
    { key: 'intensive_care', name: 'טיפול נמרץ כללי' },
    { key: 'cardiac_intensive_care', name: 'טיפול נמרץ לב' },
    { key: 'trauma_unit', name: 'יחידת הטראומה' },
    { key: 'surgical_b', name: 'כירוגיה ב' },
    { key: 'surgical_c', name: 'כירוגיה ג' },
    { key: 'neurosurgical', name: 'נוירוכירוגיה' },
    { key: 'orthopedics_a', name: 'אורתופדיה א' },
    { key: 'orthopedics_b', name: 'אורתופדיה ב' },
    { key: 'hand_palm', name: 'כף יד' },
    { key: 'mouth_and_jaw', name: 'פה ולסת' },
    { key: 'ent,name', name: 'אף אוזן גרון' },
    { key: 'urology,name', name: 'אורולוגיה' },
    { key: 'cardiovascular', name: 'חזה וכלי דם' },
    { key: 'pediatric', name: 'ילדים' },
    { key: 'pediatric_icu', name: 'טיפול נמרץ ילדים' },
    { key: 'internal_medicine_a', name: 'פנימית א' },
    { key: 'internal_medicine_b', name: 'פנימית ב' },
    { key: 'internal_medicine_c', name: 'פנימית ג' },
    { key: 'internal_medicine_d', name: 'פנימית ד' },
    { key: 'internal_medicine_e', name: 'פנימית ה' },
    { key: 'internal_medicine_f', name: 'פנימית ו' },
    { key: 'internal_medicine_i', name: 'פנימית ט' },
  ],
};

const PatientBody = ({ mci, patient }) => {
  const { value } = useContext(patientDataContext.context);
  return mci ? (
    <MCIPatientBody />
  ) : (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        flex: 1,
        minWidth: '0%',
        backgroundColor: '#f5f5f5',
      }}
    >
      <PatientStatus patient={patient} style={{ padding: '8px 12px', gap: 20 }} />
      <Carousel autoplay swipeToSlide draggable dotPosition={'botto'}>
        {Object.values(value.watching).filter((w) => w.triggered).length > 0 && <PatientWatching />}
        <PatientContent patient={patient} />
        {Object.entries(value.warnings)
          .filter(([key, { acknowledge }], i) => !acknowledge)
          .map(([key, warning], i) => (
            <PatientWarning
              key={i}
              patient={patient}
              warning={warning}
              index={i}
              contentStyle={{
                direction: 'rtl',
                userSelect: 'none',
                cursor: 'pointer',
                padding: '8px 12px',
                overflowY: 'auto',
                height: '100%',
              }}
            />
          ))}
      </Carousel>
      <PatientFooter />
    </div>
  );
};

const PatientInner = ({ patient, avatar, style, showAttention }) => {
  const ref = useRef(null);
  const { hash } = useLocation();
  const { value, update } = useContext(patientDataContext.context);
  const { matched, matching } = useContext(hashMatchContext);
  const { trackEvent } = useMatomo();

  let text = Object.keys(value.warnings).length || (
    <Tooltip overlay={'סימון דגל'}>
      {
        <FlagFilled
          onClick={(e) => {
            update(['flagged'], !value.flagged);
            trackEvent({ category: 'patient-flagged', action: 'click-event' });
            e.stopPropagation();
          }}
        />
      }
    </Tooltip>
  );
  if (hash.split('#').length > 2 && hash.split('#')[2] === patient && ref.current)
    ref.current.scrollIntoViewIfNeeded(true);

  let content = (
    <Card
      ref={ref}
      type={'inner'}
      size={'small'}
      style={{
        margin: 0,
        borderStyle: patient ? 'solid' : 'dotted',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        overflowX: 'hidden',
      }}
      headStyle={{
        paddingRight: -4,
        paddingLeft: -4,
        animation: matched(['notifications', patient])
          ? `highlight-${matching([null, patient])[0]} 2s ease-out`
          : undefined,
      }}
      bodyStyle={{
        padding: 0,
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
      }}
      title={<PatientHeader patient={patient} avatar={avatar} />}
      hoverable
      className={`severity-border severity-${value.severity ? value.severity.value : 0}`}
      extra={<PatientExtra />}
    >
      <div style={{ display: 'flex', flexDirection: 'row', height: '100%' }}>
        <PatientMeasures patient={patient} />
        <PatientBody showAttention={showAttention} patient={patient} />
      </div>
    </Card>
  );
  return (
    <div
      className={`status-bar status-${value.status || 'unassigned'}`}
      style={{
        maxWidth: MAX_WIDTH,
        minWidth: MIN_WIDTH,
        maxHeight: MAX_HEIGHT,
        display: 'flex',
        flexDirection: 'column',
        ...style,
      }}
    >
      <Badge.Ribbon text={text} color={Object.keys(value.warnings).length ? 'red' : value.flagged ? 'blue' : 'grey'}>
        {content}
      </Badge.Ribbon>
    </div>
  );
};
export const Patient = ({ patient, avatar, style, onError, showAttention }) => {
  const placeholder = (content) => (
    <Card
      size={'small'}
      bodyStyle={{ padding: 0 }}
      headStyle={{
        paddingRight: -4,
        paddingLeft: -4,
      }}
      title={
        <Button shape={'circle'} type={'text'}>
          {avatar || <UserOutlined />}
        </Button>
      }
      style={{
        margin: 0,
        height: '100%',
        maxWidth: MAX_WIDTH,
        minWidth: MIN_WIDTH,
        maxHeight: MAX_HEIGHT,
        borderStyle: patient ? 'solid' : 'dotted',
        borderColor: '#d9d9d9',
        ...style,
      }}
    >
      <div style={style}>
        <div
          style={{
            userSelect: 'none',
            padding: 20,
            textAlign: 'center',
            ...style,
          }}
          className={'severity-0 severity-background'}
        >
          {content}
        </div>
      </div>
    </Card>
  );
  return patient ? (
    <patientDataContext.Provider
      url={`/api/patients/${patient}`}
      defaultValue={{
        warnings: [],
        awaiting: [],
        severity: { value: 0, at: null },
        flagged: null,
        id_: null,
        name: null,
        age: null,
        gender: null,
        birthdate: null,
        arrival: null,
        protocol: { title: null, attributes: {} },
        treatment: { destination: null },
        complaint: null,
        admission: { bed: null },
        measures: {},
      }}
      onError={onError}
    >
      {() => <PatientInner patient={patient} avatar={avatar} style={style} showAttention={showAttention} />}
    </patientDataContext.Provider>
  ) : (
    placeholder(
      <>
        <div>מיטה</div>
        <div>פנוייה</div>
      </>,
    )
  );
};

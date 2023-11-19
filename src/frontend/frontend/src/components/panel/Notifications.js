import { Badge, Card, Empty } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import { useParams } from 'react-router-dom';
import { Notification } from '../Notification';
import { hashMatchContext } from '../HashMatch';

export const Notifications = (params) => {
  const { value, update } = useContext(patientDataContext.context);
  const { patient } = useParams();
  const { matched, matching } = useContext(hashMatchContext);
  return (
    <Card
      title={
        <div style={{ width: '100%', display: 'flex', flexFlow: 'row nowrap', justifyContent: 'space-between' }}>
          <span>עדכונים</span>
          <div>
            <Badge
              style={{ backgroundColor: '#1890ff' }}
              count={Object.keys(value.notifications).length}
              size={'small'}
            />
          </div>
        </div>
      }
      style={{
        animation: matched(['info', patient, 'notifications']) ? 'highlight 2s ease-out' : undefined,
      }}
    >
      {Object.keys(value.notifications).length > 0 ? (
        Object.values(value.notifications).map((notification, i) => (
          <div style={{ display: 'flex', flexFlow: 'row nowrap', justifyContent: 'space-between' }}>
            <Notification key={i} patient={patient} message={notification} showExternalLink={true} />
          </div>
        ))
      ) : (
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'אין עדכונים זמינים'} />
      )}
    </Card>
  );
};

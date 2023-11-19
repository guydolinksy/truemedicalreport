import { Badge, Card, Empty } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import { RelativeTime } from '../RelativeTime';

export const Medications = ({ config }) => {
  const { value } = useContext(patientDataContext.context);

  return (
    <Card
      title={
        <div style={{ width: '100%', display: 'flex', flexFlow: 'row nowrap', justifyContent: 'space-between' }}>
          <span>תרופות</span>
          <div>
            <Badge
              style={{ backgroundColor: '#1890ff' }}
              count={Object.keys(value.treatment.medications).length}
              size={'small'}
            />
          </div>
        </div>
      }
      style={{ flex: 1, maxWidth: 500, minWidth: 300, ...config.customStyle }}
    >
      {Object.keys(value.treatment.medications).length ? (
        Object.values(value.treatment.medications).map((medication, i) => (
          <p key={i}>
            {medication.label} - {medication.instructions} - {medication.given ? 'בוצע' : 'הוראה פתוחה'} -{' '}
            <RelativeTime style={{ fontSize: 12 }} date={medication.given || medication.since} />
          </p>
        ))
      ) : (
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא נרשמו תרופות'} />
      )}
    </Card>
  );
};

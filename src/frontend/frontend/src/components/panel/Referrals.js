import { Badge, Card, Empty } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import { RelativeTime } from '../RelativeTime';

export const Referrals = (params) => {
  const { value } = useContext(patientDataContext.context);

  return (
    <Card
      title={
        <div style={{ width: '100%', display: 'flex', flexFlow: 'row nowrap', justifyContent: 'space-between' }}>
          <span>ייעוץ</span>
          <div>
            <Badge style={{ backgroundColor: '#1890ff' }} count={Object.keys(value.referrals).length} size={'small'} />
          </div>
        </div>
      }
    >
      {Object.keys(value.referrals).length ? (
        Object.values(value.referrals).map((referral, i) => (
          <p key={i}>
            {referral.to} - {referral.completed_at ? 'הושלם' : 'בהמתנה'} -{' '}
            <RelativeTime style={{ fontSize: 12 }} date={referral.at} />
          </p>
        ))
      ) : (
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא נרשמו הפניות'} />
      )}
    </Card>
  );
};

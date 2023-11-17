import React, { useContext, useEffect, useState } from 'react';
import { patientDataContext } from './PatientBase';
import { RelativeTime } from '../RelativeTime';
import { CustomIcon } from '../CustomIcon';
import moment from 'moment';
import { useTime } from 'react-timer-hook';

import { Space, Spin, Tooltip } from 'antd';

export const PatientAwaiting = () => {
  const AWAITING = ['laboratory', 'imaging', 'referral', 'nurse', 'doctor'];
  const { value } = useContext(patientDataContext.context);

  return (
    <Space style={{ paddingLeft: 20 }}>
      {AWAITING.filter((k) => value.awaiting[k]).map((k, i) => {
        return <PatientAwaitingIcon awaitings={value.awaiting[k]} type={k} key={k} />;
      })}
    </Space>
  );
};
const PatientAwaitingIcon = ({ awaitings, type }) => {
  const [status, setStatus] = useState();
  const { seconds } = useTime({});
  useEffect(() => {
    if (
      Object.values(awaitings).some(
        ({ since, limit, completed_at }) => !completed_at && moment().subtract(limit, 'seconds').isAfter(since),
      )
    )
      setStatus('error');
    else if (!Object.values(awaitings).some(({ completed_at }) => !completed_at)) setStatus('success');
    else setStatus('processing');
  }, [awaitings, seconds]);

  let completed = Object.values(awaitings).filter(({ completed_at }) => completed_at),
    pending = Object.values(awaitings).filter(({ completed_at }) => !completed_at);
  const AWAITING_TITLE = {
    laboratory: 'בדיקות מעבדה',
    imaging: 'בדיקות הדמיה',
    referral: 'הפניות וייעוצים',
    nurse: 'צוות סיעודי',
    doctor: 'צוות רפואי',
  };
  return (
    <Tooltip
      key={type}
      overlay={
        <div>
          <div>
            <b style={{ textDecoration: 'underline' }}>{AWAITING_TITLE[type]}</b>
          </div>
          {pending.length > 0 && (
            <div>
              <b>ממתין.ה עבור (דקות):</b>
            </div>
          )}
          {pending
            .sort((a, b) => (a.since > b.since ? 1 : -1))
            .map(({ name, status, since }, i) => (
              <div key={i}>
                {name} - {status} - <RelativeTime date={since} />
              </div>
            ))}
          {pending.length > 0 && completed.length > 0 && (
            <div>
              <br />
            </div>
          )}
          {completed.length > 0 && (
            <div>
              <b>הושלמו:</b>
            </div>
          )}
          {completed
            .sort((a, b) => (a.since > b.since ? 1 : -1))
            .map(({ name, status, since }, i) => (
              <div key={i}>
                {name} - {status}
              </div>
            ))}
        </div>
      }
    >
      <span>
        <CustomIcon status={status} icon={type} />
      </span>
    </Tooltip>
  );
};

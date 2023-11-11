import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import Moment from 'react-moment';

export const Visits = (params) => {
  const { value } = useContext(patientDataContext.context);
  return (
    <div {...params}>
      {value.visits.length > 0 &&
        value.visits.map((visit, i) => (
          <p key={i}>
            {visit.title} ב
            <a href={'/'}>
              <Moment date={visit.at} />
            </a>
          </p>
        ))}
    </div>
  );
};

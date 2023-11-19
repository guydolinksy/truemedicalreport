import { Badge, Card, Empty } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import moment from 'moment';
import { RelativeTime } from '../RelativeTime';
import { hashMatchContext } from '../HashMatch';
import { loginContext } from '../LoginContext';

const cultureStatuses = {
  1: ' - הוזמן',
  2: ' - שויכו דגימות',
  3: ' - בעבודה',
  4: ' - תוצאות',
};

const RANGE_CODE_TO_DESCRIPTION = {
  H: 'High',
  L: 'Low',
  VH: 'Very High',
  VL: 'Very Low',
  HH: 'Panic High',
  LL: 'Panic Low',
  JESUS: 'Call the nearby priest',
};

const displayCulture = (culture, matched, patient) => {
  const rangeToResults = {};
  Object.values(culture.results).forEach((result) => {
    if (!rangeToResults.hasOwnProperty(result.range)) {
      rangeToResults[result.range] = [];
    }

    rangeToResults[result.range].push(result);
  });

  const ranges = Object.keys(rangeToResults);

  let badgeColor = '#000000';
  if (ranges.some((range) => ['HH', 'LL'].includes(range))) badgeColor = '#FF0000';
  else if (ranges.some((range) => ['VH', 'VL'].includes(range))) badgeColor = '#FF00FF';
  else if (ranges.some((range) => ['H', 'L', 'X'].includes(range))) badgeColor = '#FFA500';
  else if (culture.status === 4 && ranges.every((range) => range === 'N')) badgeColor = '#00FF00';

  const rangesToConsiderAsBad = ['HH', 'LL', 'VH', 'VL', 'H', 'L'].map((status) => rangeToResults[status] || []);

  let badgeText = '-';
  if (culture.status === 4) {
    const badResultsCount = rangesToConsiderAsBad.map((results) => results.length).reduce((a, b) => a + b);
    if (badResultsCount) badgeText = badResultsCount.toString();
    else if (ranges.every((range) => range === 'N')) badgeText = '✓';
    else badgeText = 'X';
  }

  return (
    <p
      key={`${culture.category}-${culture.ordered_at}`}
      style={{
        animation: matched([
          'panel',
          patient,
          'cultures',
          encodeURIComponent(culture.category),
          culture.ordered_at.replace(/:/g, '-').replace(/\+/g, '-'),
        ])
          ? 'highlight 2s ease-out'
          : undefined,
        direction: 'rtl',
      }}
    >
      <p>
        <span>
          <Badge style={{ backgroundColor: badgeColor }} count={badgeText} />
          &nbsp;
          {culture.category_display_name} {cultureStatuses[culture.status]}{' '}
          {ranges.some((range) => range === 'X') && ' - פסול'}
          <RelativeTime style={{ fontSize: 12, float: 'left' }} date={culture.ordered_at} />
        </span>
      </p>
      <p style={{ marginRight: '2rem' }}>
        {rangesToConsiderAsBad.flat().map((result, i) => (
          <p key={i}>
            <span>
              {RANGE_CODE_TO_DESCRIPTION[result.range]} {result.test_type_name}: {result.result} {result.units}
            </span>
          </p>
        ))}
        {(rangeToResults[null] || []).length > 0 && (
          <p>הוזמנו: {rangeToResults[null].map((result) => result.test_type_name).join(', ')}</p>
        )}
      </p>
    </p>
  );
};

export const Cultures = ({ config }) => {
  const { value } = useContext(patientDataContext.context);
  const { matched } = useContext(hashMatchContext);
  const { patient } = useContext(loginContext);

  return (
    <Card
      title={
        <div style={{ width: '100%', display: 'flex', flexFlow: 'row nowrap', justifyContent: 'space-between' }}>
          <span>תרביות</span>
          <Badge style={{ backgroundColor: '#1890ff' }} count={Object.keys(value.cultures).length} size={'small'} />
        </div>
      }
      style={{ flex: 1, maxWidth: 500, minWidth: 300, ...config.customStyle }}
    >
      {Object.keys(value.cultures).length ? (
        <>
          {Object.values(value.cultures)
            .sort((a, b) =>
              moment(a.ordered_at).isSame(b.ordered_at) ? 0 : moment(a.ordered_at).isBefore(b.ordered_at) ? 1 : -1,
            )
            .map((culture) => displayCulture(culture, matched, patient))}
        </>
      ) : (
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={'לא הוזמנו תרביות'} />
      )}
    </Card>
  );
};

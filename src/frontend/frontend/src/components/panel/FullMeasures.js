import { List } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import { useParams } from 'react-router-dom';
import { hashMatchContext } from '../HashMatch';
import { loginContext } from '../LoginContext';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import highchartsMore from 'highcharts/highcharts-more';
import lightTheme from 'highcharts/themes/grid-light';
import darkTheme from 'highcharts/themes/dark-unica';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { faHeart, faHeartPulse, faPercent, faTemperatureHalf } from '@fortawesome/free-solid-svg-icons';

highchartsMore(Highcharts);
const fontFamily =
  "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif";

const themes = { 'dark-theme': darkTheme, 'light-theme': lightTheme };
const MeasureGraph = ({ data, title, graphProps }) => {
  const { userSettings } = useContext(loginContext);
  (themes[userSettings.theme] || ((x) => x))(Highcharts);
  return (
    <HighchartsReact
      highcharts={Highcharts}
      options={{
        title: null,
        xAxis: { type: 'datetime', useHTML: true },
        yAxis: { opposite: true, title: { enabled: false } },
        chart: { height: 80, width: 200, spacingBottom: 5, style: { fontFamily: fontFamily } },
        legend: { enabled: false },
        credits: { enabled: false },
        tooltip: { outside: true },
        plotOptions: { series: { marker: { radius: 3 }, lineWidth: 1 } },
        series: [{ data: data, name: title, ...graphProps }],
      }}
    />
  );
};
const FullMeasure = ({ patient, measure, icon, latest, data, title, graphProps }) => {
  const { matched } = useContext(hashMatchContext);
  return (
    <List.Item
      style={{
        padding: 5,
        display: 'flex',
        animation: matched(['info', patient, 'measures', measure]) ? 'highlight 2s ease-out' : undefined,
      }}
    >
      <div style={{ textAlign: 'center', flex: 1 }}>
        <div style={{ fontSize: 12 }}>
          <FontAwesomeIcon icon={icon} /> {title}
        </div>
        <div
          className={latest && !latest.is_valid ? 'error-text' : undefined}
          style={{
            userSelect: 'none',
            fontSize: 14,
          }}
        >
          {(latest && latest.value) || '-'}
        </div>
      </div>
      <MeasureGraph data={data} title={title} graphProps={graphProps} />
    </List.Item>
  );
};
export const FullMeasures = (params) => {
  const { patient } = useParams();
  const { value } = useContext(patientDataContext.context);
  return (
    <div {...params}>
      <FullMeasure
        key={'temperature'}
        patient={patient}
        measure={'temperature'}
        icon={faTemperatureHalf}
        latest={value.measures.temperature}
        title={'חום'}
        graphProps={{ type: 'line' }}
        data={value.full_measures.temperature}
      />
      <FullMeasure
        key={'blood_pressure'}
        patient={patient}
        measure={'blood_pressure'}
        icon={faHeart}
        latest={value.measures.blood_pressure}
        title={'לחץ דם'}
        graphProps={{
          type: 'arearange',
          tooltip: {
            pointFormat:
              '<span style="color:{series.color}">●' + '</span> {series.name}: <b>{point.low}/{point.high}</b><br/>',
          },
        }}
        data={value.full_measures.blood_pressure}
      />
      <FullMeasure
        key={'pulse'}
        patient={patient}
        measure={'pulse'}
        icon={faHeartPulse}
        latest={value.measures.pulse}
        title={'דופק'}
        graphProps={{ type: 'line' }}
        data={value.full_measures.pulse}
      />
      <FullMeasure
        key={'saturation'}
        patient={patient}
        measure={'saturation'}
        icon={faPercent}
        latest={value.measures.saturation}
        title={'סטורציה'}
        graphProps={{ type: 'line' }}
        data={value.full_measures.saturation}
      />
    </div>
  );
};

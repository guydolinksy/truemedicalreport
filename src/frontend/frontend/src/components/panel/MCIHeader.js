import { Input, Radio, Space } from 'antd';
import { patientDataContext } from '../card/PatientBase';
import React, { useContext } from 'react';
import moment from 'moment';
import './MCIForm.css';

export const MCIHeader = ({ config, ...params }) => {
  const { value, update } = useContext(patientDataContext.context);

  return (
    <Space
      className={'first-child-flex-1'}
      style={{
        display: 'flex',
        width: '100%',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        marginBottom: 8,
        ...config.customStyle,
      }}
    >
      <Input
        value={value.comment}
        onChange={(e) => update(['comment'], e.target.value, false)}
        placeholder={'הערות:'}
        style={{ flex: 1, minWidth: 250 }}
      />
      {config.sections.map((section) => (
        <Radio.Group
          key={section.key}
          value={value.mci[section.key] && value.mci[section.key].value}
          style={{ width: '100%', textAlign: 'center' }}
          buttonStyle={'solid'}
          onChange={(e) =>
            update(
              ['mci', section.key],
              {
                value: e.target.value,
                at: moment().toISOString().replace('Z', '+00:00'),
              },
              'MCIStringValue',
            )
          }
        >
          {section.options.map((option) => (
            <Radio.Button key={option.key} value={option.key}>
              {option.name}
            </Radio.Button>
          ))}
        </Radio.Group>
      ))}
    </Space>
  );
};

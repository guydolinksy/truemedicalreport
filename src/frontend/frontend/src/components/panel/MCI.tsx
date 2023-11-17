import { Button, Card, Divider as AntdDivider, InputNumber, Menu, Radio, Table } from 'antd';
import type { FC } from 'react';
import React, { useCallback, useState } from 'react';
import Moment from 'react-moment';
import 'moment';

import { Drugs, Flip, Person, Procedures, Other, Vitals } from '../icons';
import { MCITag } from './MCITag';

const Divider: FC = () => <AntdDivider type="vertical" orientation={'center'} style={{ backgroundColor: '#A4AFB7' }} />;

const Identification: FC<{ title: string }> = ({ title }) => (
  <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between' }}>
    <span style={{ font: 'normal normal normal 20px/27px Segoe UI', color: '#605F86' }}>{title}</span>
    <InputNumber controls={false} size={'small'} style={{ width: '164px' }} />
  </div>
);

const columns = [
  { title: 'שעה', dataIndex: 'at' },
  { title: 'פרוצדורה', dataIndex: 'procedure' },
  { title: 'בוצע ע״י', dataIndex: 'performer' },
  { title: 'הערות', dataIndex: 'notes' },
];

interface IMCIProps {
  config: {
    john_doe_name: string;
    identification: { key: string; value: string }[];
    age_groups: { values: { key: string; value: string }[]; default_value: string };
    tags: { key: string; value: string }[];
    table: { empty_text: string };
    vitals: { empty_text: string; values: { key: string; value: string; title: string; empty_text: string }[] };
  };
}

export const MCI: FC<IMCIProps> = ({ config }) => {
  const [tags, setTags] = useState<Record<string, boolean>>({});
  const onTagChange = useCallback(
    (value: string) => (checked: boolean) => setTags((v) => ({ ...v, [value]: checked })),
    [],
  );
  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex', margin: '-8vh' }}>
      <div
        style={{
          width: '600px',
          height: '1200px',
          background: '#F0F0F7 0% 0% no-repeat padding-box',
          display: 'flex',
          flexDirection: 'column',
          paddingRight: '56px',
          paddingTop: '56px',
        }}
      >
        <div style={{ width: '100%', display: 'inline-flex' }}>
          <span
            style={{
              font: 'normal normal 600 28px/37px Segoe UI',
              color: '#605F86',
            }}
          >
            {config.john_doe_name}
          </span>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row' }}>
          <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', width: '250px' }}>
            {config.identification.map(({ key, value }) => (
              <Identification key={key} title={value} />
            ))}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <Radio.Group defaultValue={config.age_groups.default_value} style={{ marginRight: '62px' }}>
              {config.age_groups.values.map(({ key, value }) => (
                <Radio key={key} value={key}>
                  {value}
                </Radio>
              ))}
            </Radio.Group>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                marginTop: '10px',
              }}
            >
              <Button type={'primary'}>הבא נתונים</Button>
            </div>
          </div>
        </div>
        <div
          style={{ width: '100%', display: 'inline-flex', alignItems: 'center', marginTop: '20px', flexWrap: 'wrap' }}
        >
          {config.tags.map(({ key, value }) => (
            <MCITag key={key} tag={value} checked={tags[key]} onChange={onTagChange(key)} />
          ))}
        </div>
        <div>
          <Menu
            style={{ backgroundColor: 'unset', marginRight: '-20px', marginTop: '20px' }}
            defaultActiveFirst
            mode={'horizontal'}
            items={[
              { label: 'פרוצדורות ותרופות', key: 'procedures' },
              { label: 'הערות', key: 'notes' },
            ]}
          />
          <div
            style={{
              marginTop: '15px',
              marginRight: '-20px',
              font: 'normal normal 600 22px/30px Segoe UI',
              color: '#6462A3',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <Button type={'text'} icon={<Procedures />} style={{ display: 'flex', alignItems: 'center' }}>
              פרוצדורות
            </Button>
            <Divider />
            <Button type={'text'} icon={<Drugs />} style={{ display: 'flex', alignItems: 'center' }}>
              תרופות
            </Button>
            <Divider />
            <Button type={'text'} icon={<Vitals />} style={{ display: 'flex', alignItems: 'center' }}>
              מדדים
            </Button>
            <Divider />
            <Button type={'text'} icon={<Other />} style={{ display: 'flex', alignItems: 'center' }}>
              אחר
            </Button>
          </div>
        </div>
        <div style={{ width: '100%', marginTop: '30px' }}>
          <Table columns={columns} locale={{ emptyText: config.table.empty_text }} size={'small'} />
        </div>
      </div>
      <div style={{ display: 'grid', flex: 1, height: '1200px', background: 'white' }}>
        <div style={{ marginLeft: '10px', marginTop: '10px', justifySelf: 'end' }}>
          <span>
            <Moment format={'hh:mm'} style={{ marginRight: '5px' }} />
            <Moment format={'A'} />
          </span>
          <Button type={'primary'} style={{ marginRight: '10px' }}>
            המשך טיפול
          </Button>
        </div>
        <div
          style={{
            marginLeft: '10px',
            position: 'relative',
            top: '50%',
            left: 0,
            display: 'flex',
            justifySelf: 'end',
            flexDirection: 'column',
          }}
        >
          {config.vitals.empty_text}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', direction: 'ltr' }}>
            {config.vitals.values.map(({ key, value, title, empty_text }) => (
              <Card key={key} style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
                <div>{empty_text}</div>
                <div>{value}</div>
                <div>{title}</div>
              </Card>
            ))}
          </div>
        </div>
        <div>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              marginTop: '-550px',
            }}
          >
            <div style={{ marginBottom: '10px' }}>
              <Flip />
            </div>
            <div style={{ display: 'flex', justifyContent: 'start' }}>
              <span style={{ marginTop: '25px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
                L
              </span>
              <Person />
              <span style={{ marginTop: '25px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
                R
              </span>
            </div>
            <div style={{ marginTop: '20px' }}>
              <Radio.Group defaultValue={'injuries'}>
                <Radio value="injuries" style={{ marginLeft: '50px' }}>
                  פציעות
                </Radio>
                <Radio value="burns">כוויות</Radio>
              </Radio.Group>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

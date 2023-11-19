import { PlusOutlined, MinusOutlined } from '@ant-design/icons';
import { Button, Card, Checkbox, Divider as AntdDivider, Input, InputNumber, Menu, Radio, Slider, Table } from 'antd';
import type { FC } from 'react';
import React, { useCallback, useMemo, useState } from 'react';
import Moment from 'react-moment';
import 'moment';
import moment from 'moment';

import { Drugs, Flip, Person, Procedures, Other, Vitals, Ambulance, Helicopter } from '../icons';
import { MCIHeaderNew } from './MCIHeaderNew';
import { MCIRadio } from './MCIRadio';
import { MCISectionNew } from './MCISectionNew';
import { MCITag } from './MCITag';

const Divider: FC<{ full?: boolean }> = ({ full }) => (
  <AntdDivider
    type="vertical"
    orientation={'center'}
    style={{ backgroundColor: '#A4AFB7', height: full ? '100%' : undefined }}
  />
);

const FullDivider: FC = () => (
  <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
    <Divider full />
  </div>
);

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

const toggleIcons = {
  ambulance: <Ambulance />,
  helicopter: <Helicopter />,
};

interface IMCIProps {
  config: {
    john_doe_name: string;
    identification: { key: string; value: string }[];
    age_groups: { values: { key: string; value: string }[]; default_value: string };
    tags: { key: string; value: string }[];
    table: { empty_text: string };
    vitals: { empty_text: string; values: { key: string; value: string; title: string; empty_text: string }[] };
    field_intake: {
      identification: { key: string; value: string }[];
      toggles: {
        key: string;
        value: string;
        values: { key: string; value?: string; icon?: keyof typeof toggleIcons }[];
        default_value: string;
      }[];
      injury_mechanisms: { title: string; values: { key: string; value: string }[] };
      additional_information: { title: string; values: { key: string; value: string }[] };
      procedures: { title: string; values: { key: string; value: string }[] };
      arteries: { title: string; values: { key: string; value: string }[] };
      blood_and_fluids: { title: string; values: { key: string; value: string }[] };
      medications: {
        title: string;
        values: { key: string; value: string; subtitle: string; step: number; unit: string }[];
        other: string;
      };
      vitals: {
        title: string;
        values: {
          min?: number;
          max: number;
          key: string;
          value: string;
          min_label?: string;
          max_label?: string;
          step?: number;
        }[];
      };
    };
  };
}

// TODO - remove khosem orakim - choose from existing
// TODO - other in main tab - blood products, looks like drugs modal, without suggested column
// TODO - procedures -> treatments, allow notes like in injuries modal
// TODO - fields drugs should have time selector

export const MCI: FC<IMCIProps> = ({ config }) => {
  const { max, marks, formatter } = useMemo(() => {
    const now = moment();
    const start = moment(now).add(-4, 'h');

    const max = moment(now).diff(start, 'm');
    const offset = moment(now).diff(moment(now).startOf('h'), 'm');
    const marks = {
      0: now.format('HH:mm'),
      ...(offset > 30
        ? {
            [max - 240 + offset]: moment(start)
              .add(240 - offset, 'm')
              .format('HH:mm'),
          }
        : {}),
      [max - 180 + offset]: moment(start)
        .add(180 - offset, 'm')
        .format('HH:mm'),
      [max - 120 + offset]: moment(start)
        .add(120 - offset, 'm')
        .format('HH:mm'),
      [max - 60 + offset]: moment(start)
        .add(60 - offset, 'm')
        .format('HH:mm'),
    };
    const formatter = (value?: number) =>
      moment(now)
        .add(-(value ?? 0), 'm')
        .format('HH:mm');

    return { max, marks, formatter };
  }, []);
  const [filled, setFilled] = useState(false);
  const [tags, setTags] = useState<Record<string, boolean>>({});
  const onTagChange = useCallback(
    (value: string) => (checked: boolean) => setTags((v) => ({ ...v, [value]: checked })),
    [],
  );
  if (filled) {
    return (
      <div style={{ width: '100vw', height: '100vh', display: 'flex', margin: '-8vh', overflow: 'hidden' }}>
        <div
          style={{
            width: '600px',
            height: '1200px',
            background: '#F0F0F7 0% 0% no-repeat padding-box',
            display: 'flex',
            flexDirection: 'column',
            paddingRight: '30px',
            paddingTop: '30px',
          }}
        >
          <div style={{ width: '100%', display: 'inline-flex', marginBottom: '20px' }}>
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
                  <MCIRadio key={key} value={key} name={value} />
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
                <span style={{ marginRight: '10px' }}>פרוצדורות</span>
              </Button>
              <Divider />
              <Button type={'text'} icon={<Drugs />} style={{ display: 'flex', alignItems: 'center' }}>
                <span style={{ marginRight: '10px' }}>תרופות</span>
              </Button>
              <Divider />
              <Button type={'text'} icon={<Vitals />} style={{ display: 'flex', alignItems: 'center' }}>
                <span style={{ marginRight: '10px' }}>מדדים</span>
              </Button>
              <Divider />
              <Button type={'text'} icon={<Other />} style={{ display: 'flex', alignItems: 'center' }}>
                <span style={{ marginRight: '10px' }}>אחר</span>
              </Button>
            </div>
          </div>
          <div style={{ width: '100%', marginTop: '30px' }}>
            <Table columns={columns} locale={{ emptyText: config.table.empty_text }} size={'small'} />
          </div>
        </div>
        <div style={{ flex: 1, background: 'white', height: '100%', paddingRight: '100px', paddingTop: '50px' }}>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <span style={{ marginTop: '60px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
              L
            </span>
            <div style={{ width: '200px' }}>
              <div style={{ marginBottom: '10px' }}>
                <Flip />
              </div>
              <Person />
              <div style={{ marginTop: '20px' }}>
                <Radio.Group defaultValue={'injuries'}>
                  <MCIRadio value={'injuries'} name={'פציעות'} style={{ marginLeft: '50px' }} />
                  {/* TODO - change to imaging, title of modal should be body part, full body should be a button next to figure */}
                  <MCIRadio value={'imaging'} name={'הדמיות'} />
                </Radio.Group>
              </div>
            </div>
            <span style={{ marginTop: '60px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
              R
            </span>
          </div>
        </div>
        <div style={{ display: 'flex', height: '100%', background: 'white', flexDirection: 'column' }}>
          <div
            style={{
              marginLeft: '10px',
              marginTop: '10px',
              display: 'flex',
              justifyContent: 'end',
              alignItems: 'center',
            }}
          >
            <span>
              <Moment format={'hh:mm'} style={{ marginRight: '5px' }} />
              <Moment format={'A'} />
            </span>
            {/* TODO - העבר */}
            <Button type={'primary'} style={{ marginRight: '10px' }} onClick={() => setFilled(false)}>
              המשך טיפול
            </Button>
          </div>
          <div
            style={{
              marginLeft: '10px',
              marginTop: '50px',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            {/* TODO - remove burns */}
            {config.vitals.empty_text}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', direction: 'ltr' }}>
              {config.vitals.values.map(({ key, value, title, empty_text }) => (
                <Card key={key} style={{ margin: '6px', display: 'flex', flexDirection: 'column' }} size={'small'}>
                  <div>{empty_text}</div>
                  <div>{value}</div>
                  <div>{title}</div>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div
      style={{
        width: '100vw',
        height: '100vh',
        display: 'flex',
        margin: '-8vh',
        overflow: 'hidden',
        background: 'white',
        flexDirection: 'column',
      }}
    >
      <MCIHeaderNew onClick={() => setFilled(true)} buttonText={'סיום טיפול בשטח'} />
      <div style={{ width: '100%', display: 'flex', flexDirection: 'row' }}>
        <div
          style={{
            flex: 1,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            paddingRight: '30px',
            paddingTop: '30px',
          }}
        >
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', width: '275px' }}>
              {config.field_intake.identification.map(({ key, value }) => (
                <Identification key={key} title={value} />
              ))}
            </div>
          </div>
          <div
            style={{
              width: '100%',
              display: 'flex',
              alignItems: 'flex-start',
              marginTop: '20px',
              flexDirection: 'column',
            }}
          >
            {config.field_intake.toggles.map(({ key, value, default_value, values }) => (
              <div key={key} style={{ display: 'flex', margin: '15px', alignItems: 'center' }}>
                <div style={{ display: 'flex', width: '50px', alignItems: 'start' }}>{value}:</div>
                <Radio.Group defaultValue={default_value}>
                  {values.map(({ key: innerKey, value: innerValue, icon }) => (
                    <MCIRadio
                      key={innerKey}
                      value={innerKey}
                      name={icon ? toggleIcons[icon] : innerValue}
                      style={{ minWidth: '75px', alignItems: 'center' }}
                    />
                  ))}
                </Radio.Group>
              </div>
            ))}
          </div>
          {/* TODO - merge with below, only leave smoke, abc, unconscious  */}
          <MCISectionNew title={config.field_intake.injury_mechanisms.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'center',
                marginTop: '10px',
                flexWrap: 'wrap',
              }}
            >
              {config.field_intake.injury_mechanisms.values.map(({ key, value }) => (
                <MCITag key={key} tag={value} checked={tags[key]} onChange={onTagChange(key)} />
              ))}
            </div>
          </MCISectionNew>
          <MCISectionNew title={config.field_intake.additional_information.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'center',
                marginTop: '10px',
                flexWrap: 'wrap',
              }}
            >
              {config.field_intake.additional_information.values.map(({ key, value }) => (
                <MCITag key={key} tag={value} checked={tags[key]} onChange={onTagChange(key)} />
              ))}
            </div>
          </MCISectionNew>
        </div>
        <FullDivider />
        <div
          style={{
            flex: 1,
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            padding: '15px',
          }}
        >
          <MCISectionNew title={config.field_intake.procedures.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'center',
                marginTop: '10px',
                flexWrap: 'wrap',
                justifyContent: 'space-between',
              }}
            >
              {config.field_intake.procedures.values.map(({ key, value }) => (
                <MCITag key={key} tag={value} checked={tags[key]} onChange={onTagChange(key)} block />
              ))}
            </div>
          </MCISectionNew>
          <MCISectionNew title={config.field_intake.arteries.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'center',
                marginTop: '10px',
                flexWrap: 'wrap',
                justifyContent: 'space-between',
              }}
            >
              {config.field_intake.arteries.values.map(({ key, value }) => (
                <Checkbox key={key}>{value}</Checkbox>
              ))}
            </div>
            <div style={{ display: 'flex', width: '100%', justifyContent: 'center' }}>
              <Slider
                style={{ width: '90%', marginTop: '60px' }}
                included={false}
                max={max}
                marks={marks}
                tooltip={{ formatter, open: true }}
                reverse
              />
            </div>
          </MCISectionNew>
          <MCISectionNew title={config.field_intake.blood_and_fluids.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'start',
                marginTop: '10px',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              {config.field_intake.blood_and_fluids.values.map(({ key, value }) => (
                <div
                  key={key}
                  style={{
                    display: 'flex',
                    width: '70%',
                    justifyContent: 'space-between',
                    margin: '6px',
                    alignItems: 'center',
                  }}
                >
                  <Checkbox>{value}</Checkbox>
                  <div>
                    <InputNumber
                      addonBefore={<PlusOutlined />}
                      addonAfter={<MinusOutlined />}
                      defaultValue={0}
                      style={{ width: '120px' }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </MCISectionNew>
        </div>
        <FullDivider />
        <div style={{ flex: 1, height: '100%', flexDirection: 'column' }}>
          <MCISectionNew title={config.field_intake.medications.title}>
            <div
              style={{
                width: '100%',
                display: 'inline-flex',
                alignItems: 'start',
                marginTop: '10px',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              {config.field_intake.medications.values.map(({ key, value, subtitle }) => (
                <div
                  key={key}
                  style={{
                    display: 'flex',
                    width: '70%',
                    justifyContent: 'space-between',
                    margin: '6px',
                    alignItems: 'center',
                  }}
                >
                  <Checkbox style={{ alignItems: 'center' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'start' }}>
                      <span>{value}</span>
                      <span>{subtitle}</span>
                    </div>
                  </Checkbox>
                  <div>
                    <InputNumber
                      addonBefore={<PlusOutlined />}
                      addonAfter={<MinusOutlined />}
                      defaultValue={0}
                      style={{ width: '120px' }}
                    />
                  </div>
                </div>
              ))}
              {/* TODO - if other is used - add another below it, remove checkboxes here and in fluids */}
              {config.field_intake.medications.other && (
                <div
                  style={{
                    display: 'flex',
                    width: '70%',
                    justifyContent: 'space-between',
                    margin: '6px',
                    alignItems: 'center',
                  }}
                >
                  <Checkbox style={{ alignItems: 'center' }}>
                    <Input placeholder={'אחר'} />
                  </Checkbox>
                  <div>
                    <InputNumber
                      addonBefore={<PlusOutlined />}
                      addonAfter={<MinusOutlined />}
                      defaultValue={0}
                      style={{ width: '120px' }}
                    />
                  </div>
                </div>
              )}
            </div>
          </MCISectionNew>
          <MCISectionNew title={config.field_intake.vitals.title}>
            {config.field_intake.vitals.values.map(
              ({ key, value, min = 0, max: vitalMax = 250, min_label, max_label, step }) => (
                <div key={key} style={{ display: 'flex', width: '100%', justifyContent: 'space-around' }}>
                  <div style={{ display: 'flex', width: '90px', justifyContent: 'start' }}>{value}</div>
                  <Slider
                    style={{ width: '60%' }}
                    included={false}
                    min={min}
                    max={vitalMax}
                    marks={{ [min]: min_label ?? '0', [vitalMax]: max_label ?? `${vitalMax}` }}
                    step={step}
                    tooltip={{ open: false }}
                    defaultValue={(min + vitalMax) / 2}
                    reverse
                  />
                  <div style={{ display: 'flex', width: '90px', justifyContent: 'start', marginRight: '30px' }}>
                    {value}
                  </div>
                </div>
              ),
            )}
          </MCISectionNew>
        </div>
      </div>
    </div>
  );
};

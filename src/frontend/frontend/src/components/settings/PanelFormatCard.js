import React, { useCallback, useContext, useEffect, useRef, useState } from 'react';
import { Alert, Button, Card, Checkbox, Form, Input } from 'antd';
import { loginContext } from '../LoginContext';
import { useNavigate, useParams } from 'react-router-dom';
import { viewsDataContext } from '../../contexts/ViewsDataContext';
import { CopyOutlined, DownOutlined, LeftOutlined } from '@ant-design/icons';
import { panelDataContext } from '../panel/Info';

const renderDropdown = (types, setter) => {
  return types.map((type, idx) => {
    return {
      key: '' + idx,
      label: <div onClick={() => setter(type)}>{type.name}</div>,
    };
  });
};

const PanelFormatCardInner = () => {
  const { user } = useContext(loginContext);
  const { value } = useContext(panelDataContext.context);

  return (
    user.is_admin && (
      <Card title={'הגדרות הצגת פרטי מחלקה'}>
        <RenderObject
          name={'components'}
          content={value.components}
          path={['components']}
          customRenderers={{ customStyle: RenderJSON }}
        />
      </Card>
    )
  );
};

export const PanelFormatCard = () => {
  const { viewType, view, mode } = useParams();
  return (
    <panelDataContext.Provider url={`/api/settings/views/${viewType}/${view}/modes/${mode}/panel/format`}>
      {() => <PanelFormatCardInner />}
    </panelDataContext.Provider>
  );
};

const RenderJSON = ({ value, setValue, path }) => {
  return <Input value={JSON.stringify(value)} onChange={(e) => setValue(path, JSON.parse(e.target.value))} />;
};

const RenderObject = ({ name, content, path, customRenderers = {} }) => {
  const [open, setOpen] = useState(path.length < 2);

  const { value, update } = useContext(panelDataContext.context);

  if (content === undefined) return <div>Undefined</div>;
  if (typeof content === 'string') {
    return (
      <span>
        <Input
          addonBefore={convertToHebrew(name)}
          style={{ width: 'fit-content' }}
          value={content}
          onChange={(e) => update(path, e.target.value)}
        />
      </span>
    );
  }
  if (content.length !== undefined)
    return (
      <Card
        style={{ width: 'fit-content' }}
        title={
          <span
            onClick={(e) => {
              setOpen(!open);
              e.stopPropagation();
            }}
          >
            {open ? <DownOutlined /> : <LeftOutlined />} {convertToHebrew(name)}
          </span>
        }
        size={'small'}
        extra={
          <CopyOutlined
            onClick={() => {
              if (!open) return setOpen(true);
              // duplicateValue(path, content)
            }}
          />
        }
        bodyStyle={{ display: open ? undefined : 'none' }}
      >
        {open &&
          content.map((item, i) => (
            <RenderObject key={i} content={item} path={path.concat(item.key)} customRenderers={customRenderers} />
          ))}
      </Card>
    );
  if (typeof content === 'object')
    return (
      <Card
        style={{ width: 'fit-content' }}
        title={
          <span
            onClick={(e) => {
              setOpen(!open);
              e.stopPropagation();
            }}
          >
            {open ? <DownOutlined /> : <LeftOutlined />} {convertToHebrew(name) || content.name}
          </span>
        }
        size={'small'}
        bodyStyle={{ display: open ? undefined : 'none' }}
      >
        {open &&
          Object.entries(content).map(([k, v]) => {
            const Renderer = customRenderers[k] || RenderObject;

            return (
              <div key={k} style={{ whiteSpace: 'nowrap' }}>
                <Renderer name={k} content={v} path={path.concat(k)} customRenderers={customRenderers} />
              </div>
            );
          })}
      </Card>
    );
  return <div>Unknown</div>;
};

const convertToHebrew = (value) => {
  switch (value) {
    case 'type':
      return 'סוג';
    case 'customStyle':
      return 'עיצוב רכיב';
    case 'config':
      return 'תצורה';
    case 'components':
      return 'רכיבים';
    case 'key':
      return 'מפתח';
    case 'name':
      return 'שם';
    case 'short_name':
      return 'ראשי תיבות';
    case 'department_id':
      return 'מס מחלקה';
    case 'wing_id':
      return 'סוג אגף';
    case 'color':
      return 'צבע';
    case 'patients_count':
      return 'מספר מטופלים';
    case 'patients':
      return 'מטופלים';
    case 'modes':
      return 'מצבים';
    case 'default_mode':
      return 'מצב ברירת מחדל';
    case 'gender':
      return 'מין';
    case 'id':
      return 'ת.ז.';
    case 'info':
      return 'מידע';
    case 'oid':
      return 'מזהה מטופל';
    case 'comment':
      return 'תגובה';
    case 'options':
      return 'אפשרויות';
    case 'customizers':
      return 'התאמות';
    default:
      break;
  }
};

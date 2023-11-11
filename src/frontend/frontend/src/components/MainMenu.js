import { Badge, Button, Modal, Select, Space } from 'antd';
import { BellOutlined, ManOutlined, ReadOutlined, SettingOutlined, WomanOutlined } from '@ant-design/icons';
import React, { useContext, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { loginContext } from './LoginContext';
import { modeContext } from '../contexts/ModeContext';
import { viewsDataContext } from '../contexts/ViewsDataContext';
import { ViewsSelection } from './Views';
import './MainMenu.css';
import { notificationsContext } from '../contexts/NotificationContext';
import { MCI_DEPARTMENT } from './panel/MCISection';

export const MainMenu = () => {
  const { user } = useContext(loginContext);
  const { viewType, view, patient, mode } = useParams();

  const { value } = useContext(viewsDataContext.context);

  const curView = useMemo(() => {
    return value.getViews.views.find((v) => v.type === viewType && v.key === view);
  }, [value, viewType, view]);
  const departmentView = useMemo(
    () =>
      curView &&
      curView.type === 'wing' &&
      value.getViews.views.find((v) => v.type === 'department' && v.department_id === curView.department_id),
    [curView, value],
  );

  const patients = useMemo(() => {
    return value.getPatients.patients
      .filter((p) => !curView || curView.patients.find(({ oid }) => oid === p.oid))
      .sort((a, b) => a.info.name.localeCompare(b.info.name))
      .map((p) => {
        return {
          oid: p.oid,
          id: p.info?.id_,
          name: p.info?.name,
          comment: p.comment,
          views: value.getViews.views.filter((v) => v.patients.find(({ oid }) => oid === p.oid)),
          gender: p.info?.gender,
        };
      });
  }, [value, curView]);

  const { notifications } = useContext(notificationsContext);

  const navigate = useNavigate();
  const { isSmall, isTiny, isMedium } = useContext(modeContext);
  const [modal, modalContext] = Modal.useModal();

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      {modalContext}
      <Space style={{ flex: 1, columnGap: isSmall ? 16 : 24 }}>
        <Link to={'/'} style={{ color: 'white', display: 'flex', alignItems: 'center' }}>
          <img src={'/tmr.png'} height={40} />
          &nbsp;תמ״ר
        </Link>
        <Select
          allowClear
          value={curView && (departmentView ? departmentView.key : curView.key)}
          placeholder={'בחר.י תצוגה'}
          dropdownStyle={{ width: '15rem', minWidth: '15rem' }}
          options={value.getViews.views
            .filter((v) => ['department', 'custom'].includes(v.type))
            .map((v) => ({
              value: v.key,
              key: v.key,
              type: v.type,
              label: isSmall ? v.short_name : v.name,
            }))}
          onSelect={(v, o) => navigate(`/views/${o.type}/${o.key}`)}
          onClear={() => navigate(`/views`)}
        />
        {curView && ['department', 'wing'].includes(curView.type) && (
          <Select
            allowClear
            dropdownStyle={{ width: '15rem', minWidth: '15rem' }}
            value={curView && curView.wing_id}
            placeholder={'בחר.י אגף'}
            disabled={!curView || !curView.department_id}
            options={value.getViews.views
              .filter((v) => v.type === 'wing' && curView && v.department_id === curView.department_id)
              .sort((va, vb) => vb.patients_count - va.patients_count)
              .map((v) => ({
                value: v.wing_id,
                key: v.key,
                type: v.type,
                label: (
                  <span>
                    {v.name} - <b>{v.patients_count}</b>
                    {!isMedium && <span> מטופלים.ות</span>}
                  </span>
                ),
              }))}
            onSelect={(v, o) => navigate(`/views/${o.type}/${o.key}`)}
            onClear={() => {
              const { key } = value.getViews.views.find(
                (v) => v.type === 'department' && v.department_id === curView.department_id,
              );
              navigate(`/views/department/${key}`);
            }}
          />
        )}
        <div className={'spacer'} />
        {curView && curView.modes.length > 1 && (
          <Select
            placement={'bottomLeft'}
            value={mode}
            dropdownStyle={{ width: '10rem', minWidth: '10rem' }}
            options={
              !curView
                ? []
                : curView.modes.map((m) => ({
                    value: m.key,
                    key: m.key,
                    label: isMedium ? m.short_name : m.name,
                  }))
            }
            onSelect={(m) => navigate(`/views/${viewType}/${view}/modes/${m}`)}
          />
        )}
        {patients.length > 0 && (
          <Select
            placement={'bottomLeft'}
            dropdownStyle={{ width: '15rem', minWidth: '15rem' }}
            className={'patient-search'}
            style={isSmall ? {} : { width: 'fit-content' }}
            showSearch
            placeholder={'חיפוש מטופל.ת:'}
            onChange={(value, option) => {
              if (option.views.length === 1)
                navigate(`/views/${option.views[0].type}/${option.views[0].key}#locate#${value}#open`);
              else
                modal.info({
                  icon: null,
                  okText: 'ביטול',
                  centered: true,
                  closeable: true,
                  maskClosable: true,
                  content: <ViewsSelection options={option.views} title={'מעבר אל:'} />,
                });
            }}
            filterOption={(search, option) =>
              option.id.includes(search) || option.name.includes(search) || (option.comment || '').includes(search)
            }
            options={patients.map((p) => ({
              value: p.oid,
              id: p.id,
              name: p.name,
              comment: p.comment,
              views: p.views,
              label: (
                <div
                  className={'patient-search'}
                  style={{ width: '100%', justifyContent: 'space-between', display: 'flex' }}
                >
                  <span>
                    <span className={`gender-${p.gender}`}>
                      {p.gender === 'male' && <ManOutlined />}
                      {p.gender === 'female' && <WomanOutlined />}
                    </span>
                    &nbsp;{user.anonymous ? '---' : p.name}
                    {p.comment ? ` (${p.comment})` : ''}
                  </span>
                  {p.views.slice(0, 1).map((v) => (
                    <span key={0} style={{ color: v.color }}>
                      {v.name}
                    </span>
                  ))}
                </div>
              ),
            }))}
            value={null}
          />
        )}
        {curView && curView.department_id !== MCI_DEPARTMENT && !patient && (
          <ReadOutlined onClick={() => navigate('#help')} style={{ fontSize: 16, color: 'white' }} />
        )}
        {curView && !patient && (
          <Badge size={'small'} count={notifications}>
            <BellOutlined onClick={() => navigate('#notifications')} style={{ fontSize: 16, color: 'white' }} />
          </Badge>
        )}
        {user && curView && !curView.wing_id && !patient && (
          <SettingOutlined onClick={() => navigate('#settings')} style={{ fontSize: 16, color: 'white' }} />
        )}
      </Space>
    </div>
  );
};

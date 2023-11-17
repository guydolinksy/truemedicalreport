import React, { useContext } from 'react';
import { generatePath, Navigate, useParams, Outlet } from 'react-router-dom';
import { viewsDataContext } from '../contexts/ViewsDataContext';
import { ListMode } from '../modes/ListMode';
import { LayoutMode } from '../modes/LayoutMode';
import { DepartmentMode } from '../modes/DepartmentMode';
import { StatusMode } from '../modes/StatusMode';
import { TraumaMode } from '../modes/TraumaMode';
import { Empty } from 'antd';

export const MODE_URL = '/views/:viewType/:view/modes/:mode';
export const DEFAULT_MODE_URL = '/views/:viewType/:view';

export const DefaultModeForView = () => {
  const { viewType, view } = useParams();
  const { value } = useContext(viewsDataContext.context);
  return (
    <Navigate
      to={generatePath(MODE_URL, {
        viewType: viewType,
        view: view,
        mode: value.getViews.views.find(({ key }) => key === view).default_mode.key,
      })}
    />
  );
};

export const ModeView = () => {
  const { mode, patient } = useParams();

  const Viewer = patient
    ? Outlet
    : {
        department: DepartmentMode,
        patients: ListMode,
        layout: LayoutMode,
        status: StatusMode,
        trauma: TraumaMode,
        // ors: ORMode,
        // imaging: ImagingMode,
      }[mode] || Empty;
  return <Viewer />;
};

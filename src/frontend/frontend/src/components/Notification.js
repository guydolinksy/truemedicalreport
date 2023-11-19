import React, { useEffect } from 'react';
import { Badge } from 'antd';
import { useNavigate } from 'react-router-dom';
import { RelativeTime } from './RelativeTime';
import useModal from 'antd/es/modal/useModal';
import { iframeModal } from './modals';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { Watchable } from './Watchable';

export const Notification = ({ patient, message, unread, markRead, showExternalLink, ...props }) => {
  const navigate = useNavigate();
  const [modal, modalContext] = useModal();
  useEffect(() => {
    let task = setTimeout(markRead || (() => {}), 6000);
    return () => clearTimeout(task);
  }, [patient, message, markRead]);
  return (
    <>
      <a
        href={`#info#${patient}#${message.type_}#${message.static_id}`}
        onClick={(e) => {
          navigate(`#info#${patient}#${message.type_}#${message.static_id}`);
          e.stopPropagation();
        }}
        {...props}
      >
        {unread && (
          <span>
            <Badge status={'processing'} />
            &nbsp;
          </span>
        )}
        <Watchable watchKey={`${message.type_}#${message.static_id}`} updateAt={message.at}>
          <span className={message.danger ? 'warn-text' : undefined}>{message.message}</span>
        </Watchable>
      </a>
      {showExternalLink && iframeModal(modal, faPlus, 'צפה.י במערכת חיצונית', message.link)}
      <RelativeTime style={{ fontSize: 12 }} date={message.at} />
      {modalContext}
    </>
  );
};
